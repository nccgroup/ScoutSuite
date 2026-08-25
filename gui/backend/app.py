import asyncio
import json
import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .config import BASE_DIR, REPORTS_DIR, FRONTEND_DIST_DIR
from .db import init_db, get_db_connection
from .auth import (
    UserLogin, TokenResponse, authenticate_user,
    create_access_token, get_current_user
)
from .credentials_manager import (
    CredentialCreate, save_credential, list_credentials,
    get_credential, delete_credential
)
from .scout_runner import (
    run_scan_task, cancel_scan, register_websocket,
    unregister_websocket, active_processes
)

app = FastAPI(title="ScoutSuite GUI Server", version="1.0.0")

# Enable CORS for React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


# ---------------- Auth Endpoints ----------------

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user["username"], "id": user["id"]})
    return TokenResponse(access_token=access_token, username=user["username"])


@app.get("/api/auth/me")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user


# ---------------- Credentials Endpoints ----------------

@app.get("/api/credentials")
async def get_credentials_list(provider: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    return list_credentials(provider)


@app.post("/api/credentials")
async def create_new_credential(cred: CredentialCreate, current_user: dict = Depends(get_current_user)):
    cred_id = save_credential(cred)
    return {"id": cred_id, "message": "Credential saved successfully"}


@app.delete("/api/credentials/{cred_id}")
async def remove_credential(cred_id: str, current_user: dict = Depends(get_current_user)):
    deleted = delete_credential(cred_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Credential not found")
    return {"message": "Credential removed successfully"}


# ---------------- Scan Management Endpoints ----------------

class ScanCreateRequest(BaseModel):
    provider: str
    auth_type: Optional[str] = None
    credential_id: Optional[str] = None
    inline_credentials: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None


@app.get("/api/scans")
async def list_scans(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans ORDER BY start_time DESC")
    rows = cursor.fetchall()
    conn.close()

    scans = []
    for r in rows:
        summary = json.loads(r["summary_json"]) if r["summary_json"] else None
        params = json.loads(r["params_json"]) if r["params_json"] else {}
        scans.append({
            "id": r["id"],
            "provider": r["provider"],
            "credential_id": r["credential_id"],
            "status": r["status"],
            "start_time": r["start_time"],
            "end_time": r["end_time"],
            "report_path": r["report_path"],
            "summary": summary,
            "error_message": r["error_message"],
            "is_running": r["id"] in active_processes
        })
    return scans


@app.post("/api/scans")
async def start_scan(request: ScanCreateRequest, current_user: dict = Depends(get_current_user)):
    scan_id = str(uuid.uuid4())
    start_time = datetime.utcnow().isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (id, provider, credential_id, status, start_time, params_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        scan_id,
        request.provider.lower(),
        request.credential_id,
        "queued",
        start_time,
        json.dumps(request.dict())
    ))
    conn.commit()
    conn.close()

    # Launch background scan worker
    asyncio.create_task(run_scan_task(scan_id, request.dict()))
    return {"scan_id": scan_id, "status": "queued", "message": "Scan started"}


@app.get("/api/scans/{scan_id}")
async def get_scan_details(scan_id: str, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Scan not found")

    return {
        "id": row["id"],
        "provider": row["provider"],
        "credential_id": row["credential_id"],
        "status": row["status"],
        "start_time": row["start_time"],
        "end_time": row["end_time"],
        "report_path": row["report_path"],
        "params": json.loads(row["params_json"]) if row["params_json"] else {},
        "summary": json.loads(row["summary_json"]) if row["summary_json"] else None,
        "error_message": row["error_message"],
        "is_running": row["id"] in active_processes
    }


@app.get("/api/scans/{scan_id}/logs")
async def get_scan_logs(scan_id: str, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, log_level, message FROM scan_logs WHERE scan_id = ? ORDER BY id ASC", (scan_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"timestamp": r["timestamp"], "level": r["log_level"], "message": r["message"]} for r in rows]


@app.post("/api/scans/{scan_id}/cancel")
async def stop_scan(scan_id: str, current_user: dict = Depends(get_current_user)):
    cancelled = await cancel_scan(scan_id)
    if not cancelled:
        raise HTTPException(status_code=400, detail="Scan could not be cancelled or is not running")
    return {"message": "Scan cancelled successfully"}


@app.delete("/api/scans/{scan_id}")
async def delete_scan(scan_id: str, current_user: dict = Depends(get_current_user)):
    if scan_id in active_processes:
        await cancel_scan(scan_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT provider FROM scans WHERE id = ?", (scan_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Scan not found")

    provider = row["provider"]
    cursor.execute("DELETE FROM scan_logs WHERE scan_id = ?", (scan_id,))
    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    conn.commit()
    conn.close()

    # Delete reports directory if exists
    report_folder = REPORTS_DIR / f"{provider}_{scan_id}"
    if report_folder.exists():
        try:
            shutil.rmtree(report_folder)
        except Exception:
            pass

    return {"message": "Scan and reports deleted"}


# ---------------- Dashboard & Analytics ----------------

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM scans")
    total_scans = cursor.fetchone()["total"]

    cursor.execute("SELECT status, COUNT(*) as count FROM scans GROUP BY status")
    status_counts = {r["status"]: r["count"] for r in cursor.fetchall()}

    cursor.execute("SELECT provider, COUNT(*) as count FROM scans GROUP BY provider")
    provider_counts = {r["provider"]: r["count"] for r in cursor.fetchall()}

    cursor.execute("SELECT * FROM scans ORDER BY start_time DESC LIMIT 5")
    recent = []
    for r in cursor.fetchall():
        recent.append({
            "id": r["id"],
            "provider": r["provider"],
            "status": r["status"],
            "start_time": r["start_time"],
            "report_path": r["report_path"]
        })
    conn.close()

    return {
        "total_scans": total_scans,
        "status_counts": status_counts,
        "provider_counts": provider_counts,
        "recent_scans": recent
    }


# ---------------- WebSocket for Live Logs ----------------

@app.websocket("/ws/scans/{scan_id}/logs")
async def scan_logs_websocket(websocket: WebSocket, scan_id: str):
    await websocket.accept()
    register_websocket(scan_id, websocket)
    try:
        while True:
            # Keep-alive receive loop
            await websocket.receive_text()
    except WebSocketDisconnect:
        unregister_websocket(scan_id, websocket)
    except Exception:
        unregister_websocket(scan_id, websocket)


# ---------------- Static Files & Report Serving ----------------

# Mount reports directory
if REPORTS_DIR.exists():
    app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR), html=True), name="reports")

# Mount frontend if built
if FRONTEND_DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIST_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gui.backend.app:app", host="0.0.0.0", port=8000, reload=True)

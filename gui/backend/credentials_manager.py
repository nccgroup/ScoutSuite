import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from .config import CREDENTIALS_DIR
from .db import get_db_connection


class CredentialCreate(BaseModel):
    name: str
    provider: str  # 'aws', 'azure', 'gcp', 'aliyun', 'kubernetes', 'do', 'oci'
    auth_type: str  # 'keys', 'profile', 'service_account', 'service_principal', etc.
    data: Dict[str, Any]
    raw_file_content: Optional[str] = None
    file_name: Optional[str] = None


class CredentialResponse(BaseModel):
    id: str
    name: str
    provider: str
    auth_type: str
    created_at: str
    updated_at: str
    data_summary: Dict[str, Any]


def mask_sensitive(data: Dict[str, Any]) -> Dict[str, Any]:
    """Mask secrets and tokens for safe display in UI"""
    masked = {}
    sensitive_keys = {
        "aws_secret_access_key", "aws_session_token", "client_secret",
        "password", "access_key_secret", "token", "access_secret", "private_key"
    }
    for k, v in data.items():
        if k in sensitive_keys and isinstance(v, str) and v:
            masked[k] = v[:4] + "********" + v[-4:] if len(v) > 8 else "********"
        elif k in ["aws_access_key_id", "access_key_id", "client_id"] and isinstance(v, str) and v:
            masked[k] = v[:4] + "...." + v[-4:] if len(v) > 8 else v
        else:
            masked[k] = v
    return masked


def save_credential(cred: CredentialCreate) -> str:
    cred_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    file_path = None

    # Handle file storage if file content was provided
    if cred.raw_file_content:
        file_ext = os.path.splitext(cred.file_name or "credential")[1] or ".json"
        safe_filename = f"{cred.provider}_{cred_id}{file_ext}"
        target_path = CREDENTIALS_DIR / safe_filename
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(cred.raw_file_content)
        file_path = str(target_path)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO credentials (id, name, provider, auth_type, data, file_path, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cred_id,
        cred.name,
        cred.provider.lower(),
        cred.auth_type,
        json.dumps(cred.data),
        file_path,
        now,
        now
    ))
    conn.commit()
    conn.close()
    return cred_id


def list_credentials(provider: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if provider:
        cursor.execute("SELECT * FROM credentials WHERE provider = ? ORDER BY created_at DESC", (provider.lower(),))
    else:
        cursor.execute("SELECT * FROM credentials ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        raw_data = json.loads(r["data"]) if r["data"] else {}
        result.append({
            "id": r["id"],
            "name": r["name"],
            "provider": r["provider"],
            "auth_type": r["auth_type"],
            "has_file": bool(r["file_path"]),
            "data_summary": mask_sensitive(raw_data),
            "created_at": r["created_at"],
            "updated_at": r["updated_at"]
        })
    return result


def get_credential(cred_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (cred_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "name": row["name"],
        "provider": row["provider"],
        "auth_type": row["auth_type"],
        "data": json.loads(row["data"]) if row["data"] else {},
        "file_path": row["file_path"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }


def delete_credential(cred_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM credentials WHERE id = ?", (cred_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    if row["file_path"] and os.path.exists(row["file_path"]):
        try:
            os.remove(row["file_path"])
        except Exception:
            pass

    cursor.execute("DELETE FROM credentials WHERE id = ?", (cred_id,))
    conn.commit()
    conn.close()
    return True

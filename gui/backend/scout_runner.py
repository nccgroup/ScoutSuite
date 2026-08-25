import asyncio
import json
import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import shutil

from .config import BASE_DIR, REPORTS_DIR
from .db import get_db_connection
from .credentials_manager import get_credential

logger = logging.getLogger("scoutsuite_gui.runner")

# In-memory dictionary for active scan processes
active_processes: Dict[str, asyncio.subprocess.Process] = {}
# Active WebSocket connections per scan_id: {scan_id: set([websocket, ...])}
active_websockets: Dict[str, set] = {}


def register_websocket(scan_id: str, ws):
    if scan_id not in active_websockets:
        active_websockets[scan_id] = set()
    active_websockets[scan_id].add(ws)


def unregister_websocket(scan_id: str, ws):
    if scan_id in active_websockets and ws in active_websockets[scan_id]:
        active_websockets[scan_id].remove(ws)
        if not active_websockets[scan_id]:
            del active_websockets[scan_id]


async def broadcast_log(scan_id: str, log_entry: Dict[str, Any]):
    if scan_id in active_websockets:
        dead_ws = set()
        for ws in active_websockets[scan_id]:
            try:
                await ws.send_json(log_entry)
            except Exception:
                dead_ws.add(ws)
        for ws in dead_ws:
            active_websockets[scan_id].discard(ws)


def save_log_to_db(scan_id: str, message: str, log_level: str = "INFO"):
    timestamp = datetime.utcnow().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scan_logs (scan_id, timestamp, log_level, message)
        VALUES (?, ?, ?, ?)
    """, (scan_id, timestamp, log_level, message))
    conn.commit()
    conn.close()


def update_scan_status(
    scan_id: str,
    status: str,
    end_time: Optional[str] = None,
    report_path: Optional[str] = None,
    summary_json: Optional[str] = None,
    error_message: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE scans
        SET status = ?, end_time = COALESCE(?, end_time),
            report_path = COALESCE(?, report_path),
            summary_json = COALESCE(?, summary_json),
            error_message = COALESCE(?, error_message)
        WHERE id = ?
    """, (status, end_time, report_path, summary_json, error_message, scan_id))
    conn.commit()
    conn.close()


def build_scout_command(scan_id: str, scan_config: Dict[str, Any]) -> tuple[List[str], Dict[str, str], str]:
    """
    Build CLI argument list and environment variables for ScoutSuite.
    Returns (cmd_args, env_vars, report_dir_path).
    """
    provider = scan_config.get("provider", "aws").lower()
    report_dir = str(REPORTS_DIR / f"{provider}_{scan_id}")
    os.makedirs(report_dir, exist_ok=True)

    cmd = [
        sys.executable,
        "-u",
        str(BASE_DIR / "scout.py"),
        provider,
        "--report-dir", report_dir,
        "--report-name", f"scoutsuite-{provider}-{scan_id[:8]}",
        "--no-browser",
        "--force"
    ]

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # Resolve credential data if provided
    cred_id = scan_config.get("credential_id")
    cred_data = {}
    cred_file = None
    auth_type = scan_config.get("auth_type")

    if cred_id:
        cred = get_credential(cred_id)
        if cred:
            cred_data = cred.get("data", {})
            cred_file = cred.get("file_path")
            if not auth_type:
                auth_type = cred.get("auth_type")

    # If direct credentials passed in scan_config, override
    if "inline_credentials" in scan_config and scan_config["inline_credentials"]:
        inline = scan_config["inline_credentials"]
        cred_data.update(inline)
        if not auth_type and "auth_type" in inline:
            auth_type = inline["auth_type"]

    # Handle inline file upload content if present
    file_content = cred_data.get("raw_file_content") or cred_data.get("service_account_content") or cred_data.get("file_content")
    if file_content and not cred_file:
        ext = ".json"
        if provider == "kubernetes":
            ext = ".yaml"
        temp_file_path = str(REPORTS_DIR / f"temp_{provider}_{scan_id[:8]}_{uuid.uuid4().hex[:6]}{ext}")
        with open(temp_file_path, "w", encoding="utf-8") as tf:
            tf.write(file_content)
        cred_file = temp_file_path

    # Provider specific flags
    if provider == "aws":
        if auth_type == "profile" or cred_data.get("profile"):
            cmd.extend(["--profile", cred_data.get("profile", "default")])
        elif cred_data.get("aws_access_key_id") and cred_data.get("aws_secret_access_key"):
            cmd.append("--access-keys")
            cmd.extend(["--access-key-id", str(cred_data["aws_access_key_id"])])
            cmd.extend(["--secret-access-key", str(cred_data["aws_secret_access_key"])])
            if cred_data.get("aws_session_token"):
                cmd.extend(["--session-token", str(cred_data["aws_session_token"])])
        elif auth_type == "keys":
            cmd.append("--access-keys")
            if cred_data.get("aws_access_key_id"):
                cmd.extend(["--access-key-id", str(cred_data["aws_access_key_id"])])
            if cred_data.get("aws_secret_access_key"):
                cmd.extend(["--secret-access-key", str(cred_data["aws_secret_access_key"])])

    elif provider == "azure":
        # Determine Azure auth mode
        if auth_type == "cli":
            cmd.append("--cli")
        elif auth_type == "msi":
            cmd.append("--msi")
        elif auth_type in ["file_auth", "file"] or (cred_file and auth_type not in ["cli", "service_principal", "user_account", "user_account_browser"]):
            if cred_file:
                cmd.extend(["--file-auth", cred_file])
            else:
                cmd.append("--cli")
        elif auth_type in ["user_account", "user"]:
            cmd.append("--user-account")
            if cred_data.get("tenant_id"):
                cmd.extend(["--tenant", str(cred_data["tenant_id"])])
            if cred_data.get("username"):
                cmd.extend(["--username", str(cred_data["username"])])
            if cred_data.get("password"):
                cmd.extend(["--password", str(cred_data["password"])])
        elif auth_type in ["user_account_browser", "browser"]:
            cmd.append("--user-account-browser")
            if cred_data.get("tenant_id"):
                cmd.extend(["--tenant", str(cred_data["tenant_id"])])
        elif auth_type in ["service_principal", "sp"] or cred_data.get("client_id") or cred_data.get("client_secret"):
            cmd.append("--service-principal")
            if cred_data.get("tenant_id"):
                cmd.extend(["--tenant", str(cred_data["tenant_id"])])
            if cred_data.get("client_id"):
                cmd.extend(["--client-id", str(cred_data["client_id"])])
            if cred_data.get("client_secret"):
                cmd.extend(["--client-secret", str(cred_data["client_secret"])])
        else:
            # If no auth flag matched, check fallback: if tenant + client info present use SP, else CLI
            if cred_data.get("tenant_id") and cred_data.get("client_id"):
                cmd.append("--service-principal")
                cmd.extend(["--tenant", str(cred_data["tenant_id"])])
                cmd.extend(["--client-id", str(cred_data["client_id"])])
                if cred_data.get("client_secret"):
                    cmd.extend(["--client-secret", str(cred_data["client_secret"])])
            elif cred_file:
                cmd.extend(["--file-auth", cred_file])
            else:
                # Default to CLI
                cmd.append("--cli")

        # Subscriptions scope
        if cred_data.get("all_subscriptions"):
            cmd.append("--all-subscriptions")
        elif cred_data.get("subscription_ids"):
            subs = cred_data["subscription_ids"]
            if isinstance(subs, str):
                subs = [s.strip() for s in subs.split(",") if s.strip()]
            if subs:
                cmd.extend(["--subscriptions"] + subs)

    elif provider == "gcp":
        if auth_type == "user_account":
            cmd.append("--user-account")
        elif cred_file:
            cmd.extend(["--service-account", cred_file])
        elif cred_data.get("service_account_file"):
            cmd.extend(["--service-account", str(cred_data["service_account_file"])])
        else:
            # Fallback to user-account if no service account file
            cmd.append("--user-account")

        if cred_data.get("all_projects"):
            cmd.append("--all-projects")
        elif cred_data.get("project_id"):
            cmd.extend(["--project-id", str(cred_data["project_id"])])
        if cred_data.get("folder_id"):
            cmd.extend(["--folder-id", str(cred_data["folder_id"])])
        if cred_data.get("organization_id"):
            cmd.extend(["--organization-id", str(cred_data["organization_id"])])

    elif provider == "aliyun":
        cmd.append("--access-keys")
        if cred_data.get("access_key_id"):
            cmd.extend(["--access-key-id", str(cred_data["access_key_id"])])
        if cred_data.get("access_key_secret"):
            cmd.extend(["--access-key-secret", str(cred_data["access_key_secret"])])

    elif provider == "kubernetes":
        if cred_file:
            cmd.extend(["--config-file", cred_file])
        context = cred_data.get("kubernetes_context") or cred_data.get("context")
        if context:
            cmd.extend(["--context", str(context)])
        cluster_provider = cred_data.get("kubernetes_cluster_provider") or cred_data.get("cluster_provider")
        if cluster_provider and cluster_provider in ["aks", "eks", "gke"]:
            cmd.extend(["--cluster-provider", str(cluster_provider)])
            sub_id = cred_data.get("kubernetes_azure_subscription_id") or cred_data.get("subscription_id")
            if cluster_provider == "aks" and sub_id:
                cmd.extend(["--subscription-id", str(sub_id)])

    elif provider == "do":
        if cred_data.get("token"):
            cmd.extend(["--token", str(cred_data["token"])])
        if cred_data.get("access_key") and cred_data.get("access_secret"):
            cmd.extend(["--access_key", str(cred_data["access_key"])])
            cmd.extend(["--access_secret", str(cred_data["access_secret"])])

    elif provider == "oci":
        oci_profile = cred_data.get("profile") or "DEFAULT"
        if cred_data.get("profile"):
            cmd.extend(["--profile", str(cred_data["profile"])])

        # If a custom OCI config file is attached
        if cred_file and os.path.exists(cred_file):
            env["OCI_CONFIG_FILE"] = str(cred_file)
        elif cred_data.get("config_file") and os.path.exists(str(cred_data.get("config_file"))):
            env["OCI_CONFIG_FILE"] = str(cred_data["config_file"])
        # If direct OCI parameters were provided (user, tenancy, fingerprint, region, key)
        elif cred_data.get("user") and cred_data.get("tenancy") and cred_data.get("fingerprint"):
            oci_dir = os.path.join(report_dir, "oci_auth")
            os.makedirs(oci_dir, exist_ok=True)
            
            # Write private key if provided
            key_file_path = cred_data.get("key_file")
            if cred_data.get("private_key_content"):
                key_file_path = os.path.join(oci_dir, "oci_api_key.pem")
                with open(key_file_path, "w", encoding="utf-8") as kf:
                    kf.write(cred_data["private_key_content"])
                os.chmod(key_file_path, 0o600)
            
            # Generate temporary OCI config
            generated_config = os.path.join(oci_dir, "config")
            with open(generated_config, "w", encoding="utf-8") as cf:
                cf.write(f"[{oci_profile}]\n")
                cf.write(f"user={cred_data.get('user')}\n")
                cf.write(f"fingerprint={cred_data.get('fingerprint')}\n")
                cf.write(f"tenancy={cred_data.get('tenancy')}\n")
                cf.write(f"region={cred_data.get('region', 'us-ashburn-1')}\n")
                if key_file_path:
                    cf.write(f"key_file={key_file_path}\n")
            
            env["OCI_CONFIG_FILE"] = generated_config


    # General Scan options
    options = scan_config.get("options", {})
    if options.get("services"):
        cmd.append("--services")
        cmd.extend(options["services"])
    if options.get("skipped_services"):
        cmd.append("--skip")
        cmd.extend(options["skipped_services"])
    if options.get("regions"):
        cmd.append("--regions")
        cmd.extend(options["regions"])
    if options.get("excluded_regions"):
        cmd.append("--exclude-regions")
        cmd.extend(options["excluded_regions"])
    if options.get("max_workers"):
        cmd.extend(["--max-workers", str(options["max_workers"])])
    if options.get("ruleset"):
        cmd.extend(["--ruleset", str(options["ruleset"])])
    if options.get("fetch_local"):
        cmd.append("--local")
    return cmd, env, report_dir


async def run_scan_task(scan_id: str, scan_config: Dict[str, Any]):
    cmd, env, report_dir = build_scout_command(scan_id, scan_config)
    
    update_scan_status(scan_id, "running")
    start_msg = f"Starting ScoutSuite audit: {' '.join(cmd)}"
    save_log_to_db(scan_id, start_msg, "INFO")
    await broadcast_log(scan_id, {"type": "log", "timestamp": datetime.utcnow().isoformat(), "message": start_msg, "level": "INFO"})

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=env,
            cwd=str(BASE_DIR)
        )
        active_processes[scan_id] = process

        # Read stdout asynchronously line-by-line
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            text = line.decode("utf-8", errors="replace").rstrip()
            if text:
                level = "ERROR" if "Exception" in text or "error" in text.lower() else "INFO"
                save_log_to_db(scan_id, text, level)
                await broadcast_log(scan_id, {
                    "type": "log",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": text,
                    "level": level
                })

        return_code = await process.wait()
        end_time = datetime.utcnow().isoformat()

        # Find generated HTML report
        html_files = [f for f in os.listdir(report_dir) if f.endswith(".html")] if os.path.exists(report_dir) else []
        relative_report_path = f"/reports/{os.path.basename(report_dir)}/{html_files[0]}" if html_files else None

        # Parse summary if json available
        summary_data = {}
        js_results_dir = os.path.join(report_dir, "scoutsuite-results")
        if os.path.exists(js_results_dir):
            for file in os.listdir(js_results_dir):
                if file.startswith("scoutsuite_results_") and file.endswith(".js"):
                    try:
                        # ScoutSuite writes: scoutsuite_results = { ... }
                        with open(os.path.join(js_results_dir, file), "r", encoding="utf-8") as rf:
                            content = rf.read()
                            json_str = content[content.find("{"):content.rfind("}")+1]
                            parsed = json.loads(json_str)
                            summary_data = {
                                "account_id": parsed.get("account_id"),
                                "services_count": len(parsed.get("service_list", [])),
                                "findings_count": parsed.get("last_run", {}).get("rules_count", 0),
                                "run_summary": parsed.get("last_run", {}).get("summary", {})
                            }
                    except Exception as e:
                        logger.warning(f"Could not parse js results: {e}")

        if return_code == 0 or return_code == 200: # 200 means completed with findings
            status = "completed"
            end_msg = f"Audit completed successfully. Return code: {return_code}"
        else:
            status = "failed"
            end_msg = f"Audit failed with exit code: {return_code}"

        update_scan_status(
            scan_id,
            status=status,
            end_time=end_time,
            report_path=relative_report_path,
            summary_json=json.dumps(summary_data) if summary_data else None,
            error_message=end_msg if status == "failed" else None
        )
        save_log_to_db(scan_id, end_msg, "INFO" if status == "completed" else "ERROR")
        await broadcast_log(scan_id, {
            "type": "status",
            "status": status,
            "report_path": relative_report_path,
            "end_time": end_time,
            "summary": summary_data
        })

    except asyncio.CancelledError:
        end_time = datetime.utcnow().isoformat()
        update_scan_status(scan_id, "cancelled", end_time=end_time, error_message="Scan was cancelled by user")
        save_log_to_db(scan_id, "Scan cancelled by user.", "WARNING")
        await broadcast_log(scan_id, {"type": "status", "status": "cancelled"})

    except Exception as e:
        end_time = datetime.utcnow().isoformat()
        err_str = f"Internal runner error: {str(e)}"
        update_scan_status(scan_id, "failed", end_time=end_time, error_message=err_str)
        save_log_to_db(scan_id, err_str, "ERROR")
        await broadcast_log(scan_id, {"type": "status", "status": "failed", "error": err_str})

    finally:
        active_processes.pop(scan_id, None)


async def cancel_scan(scan_id: str) -> bool:
    if scan_id in active_processes:
        proc = active_processes[scan_id]
        try:
            proc.terminate()
            await asyncio.sleep(1)
            if proc.returncode is None:
                proc.kill()
            update_scan_status(scan_id, "cancelled", end_time=datetime.utcnow().isoformat())
            return True
        except Exception as e:
            logger.error(f"Failed to cancel process {scan_id}: {e}")
            return False
    return False

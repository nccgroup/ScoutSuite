import os
import shutil
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
GUI_DIR = BASE_DIR / "gui"
BACKEND_DIR = GUI_DIR / "backend"

# All User-related files (DB, Credentials, Reports) consolidated in ScoutSuite/User/
USER_DIR = BASE_DIR / "User"
CREDENTIALS_DIR = USER_DIR / "credentials"
REPORTS_DIR = USER_DIR / "reports"
DB_PATH = USER_DIR / "scoutsuite_gui.db"
FRONTEND_DIST_DIR = GUI_DIR / "frontend" / "dist"

# Ensure User runtime directories exist
USER_DIR.mkdir(parents=True, exist_ok=True)
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Migration helper: Move existing legacy files to User/ if found
old_db = BACKEND_DIR / "scoutsuite_gui.db"
if old_db.exists() and not DB_PATH.exists():
    try:
        shutil.move(str(old_db), str(DB_PATH))
    except Exception:
        pass

old_creds = BACKEND_DIR / "credentials"
if old_creds.exists() and old_creds.is_dir() and old_creds != CREDENTIALS_DIR:
    for item in old_creds.iterdir():
        target = CREDENTIALS_DIR / item.name
        if not target.exists():
            try:
                shutil.move(str(item), str(target))
            except Exception:
                pass

old_reports = BASE_DIR / "reports"
if old_reports.exists() and old_reports.is_dir() and old_reports != REPORTS_DIR:
    for item in old_reports.iterdir():
        target = REPORTS_DIR / item.name
        if not target.exists():
            try:
                shutil.move(str(item), str(target))
            except Exception:
                pass

# Security & JWT
JWT_SECRET_KEY = os.environ.get("SCOUT_GUI_SECRET", "scoutsuite-gui-insecure-secret-key-change-in-prod")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Default Admin User
DEFAULT_ADMIN_USERNAME = os.environ.get("SCOUT_ADMIN_USER", "admin")
DEFAULT_ADMIN_PASSWORD = os.environ.get("SCOUT_ADMIN_PASS", "admin123")

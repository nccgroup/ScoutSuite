import sqlite3
import json
import logging
import bcrypt
from datetime import datetime
from typing import Optional, List, Dict, Any
from .config import DB_PATH, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

logger = logging.getLogger("scoutsuite_gui.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # Credentials Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        provider TEXT NOT NULL,
        auth_type TEXT NOT NULL,
        data TEXT NOT NULL,
        file_path TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # Scans Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id TEXT PRIMARY KEY,
        provider TEXT NOT NULL,
        credential_id TEXT,
        status TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        report_name TEXT,
        report_path TEXT,
        params_json TEXT,
        summary_json TEXT,
        error_message TEXT
    );
    """)

    # Scan Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        log_level TEXT,
        message TEXT NOT NULL,
        FOREIGN KEY(scan_id) REFERENCES scans(id) ON DELETE CASCADE
    );
    """)

    # Default admin user if none exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (DEFAULT_ADMIN_USERNAME,))
    if not cursor.fetchone():
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(DEFAULT_ADMIN_PASSWORD.encode("utf-8"), salt).decode("utf-8")
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (DEFAULT_ADMIN_USERNAME, hashed, datetime.utcnow().isoformat())
        )
        logger.info(f"Initialized default user '{DEFAULT_ADMIN_USERNAME}'")

    conn.commit()
    conn.close()

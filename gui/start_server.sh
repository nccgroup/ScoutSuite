#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$ROOT_DIR"

VENV_PATH="$ROOT_DIR/.venv-scout"

# If virtual environment is missing or incomplete, run setup automatically
if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "[!] Virtual environment not found or incomplete. Running setup script first..."
    bash "$SCRIPT_DIR/setup_wsl.sh"
fi

# Activate virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
fi

echo "=========================================================="
echo "          Starting ScoutSuite GUI Server inside WSL       "
echo "=========================================================="
echo "Backend & UI URL: http://localhost:8000"
echo "Press Ctrl+C to terminate the server."
echo "=========================================================="

export PYTHONPATH="$ROOT_DIR:$PYTHONPATH"

# If frontend dist folder doesn't exist, try building it
if [ ! -d "$ROOT_DIR/gui/frontend/dist" ]; then
    if command -v npm &> /dev/null; then
        echo "[*] Building React frontend..."
        cd "$ROOT_DIR/gui/frontend" && npm install && npm run build && cd "$ROOT_DIR"
    fi
fi

# Run Uvicorn serving FastAPI + Static SPA
python3 -m uvicorn gui.backend.app:app --host 0.0.0.0 --port 8000 --reload

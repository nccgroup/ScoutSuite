#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "=========================================================="
echo "    ScoutSuite GUI - WSL Setup & Dependency Installer     "
echo "=========================================================="

cd "$ROOT_DIR"

# 1. Detect Python Version
if ! command -v python3 &> /dev/null; then
    echo "[*] Installing Python 3, pip, and venv..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv python3-full
fi

PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "3")
echo "[*] Detected Python version: $PY_VER"

# Ensure python3-venv / specific version venv package is installed
echo "[*] Ensuring Python venv packages are installed in system..."
sudo apt update
sudo apt install -y "python${PY_VER}-venv" python3-venv python3-pip python3-full python3-setuptools || true

# 2. Check Node.js and npm
if ! command -v npm &> /dev/null; then
    echo "[*] Installing Node.js & npm..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# 3. Setup Python Virtual Environment
VENV_PATH="$ROOT_DIR/.venv-scout"

# If venv directory exists but is broken (no bin/activate), remove it
if [ -d "$VENV_PATH" ] && [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "[!] Cleaning up broken previous virtual environment..."
    rm -rf "$VENV_PATH"
fi

if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "[*] Creating Python virtual environment at .venv-scout..."
    if ! python3 -m venv "$VENV_PATH"; then
        echo "[!] Standard venv creation failed. Attempting with virtualenv / without-pip fallback..."
        sudo apt install -y python3-virtualenv || true
        if command -v virtualenv &> /dev/null; then
            virtualenv "$VENV_PATH"
        else
            python3 -m venv --without-pip "$VENV_PATH"
            source "$VENV_PATH/bin/activate"
            curl -sS https://bootstrap.pypa.io/get-pip.py | python3
        fi
    fi
fi

echo "[*] Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo "[*] Installing ScoutSuite and GUI backend requirements..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r gui/backend/requirements-gui.txt

# 4. Install frontend dependencies and build
echo "[*] Installing React frontend dependencies..."
cd "$ROOT_DIR/gui/frontend"
npm install

echo "[*] Building React frontend for production distribution..."
npm run build

echo "=========================================================="
echo "   Setup Complete! You can now start the GUI with:       "
echo "   bash gui/start_server.sh                              "
echo "=========================================================="

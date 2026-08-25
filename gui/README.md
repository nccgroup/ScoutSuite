# ScoutSuite GUI Console

A graphical web dashboard and orchestration interface for [ScoutSuite](https://github.com/nccgroup/ScoutSuite) running seamlessly inside **WSL (Windows Subsystem for Linux)** and accessed via Windows web browsers.

---

## 🌟 Key Features

1. **Authentication & Session Security**:
   - Protected Web GUI login screen (Default: `admin` / `admin123`).
   - JWT-based authentication session management.

2. **Credentials & Profile Vault (`User/credentials/`)**:
   - Securely save and manage AWS Access Keys, Named Profiles (`~/.aws/credentials`), GCP Service Account JSON keys, Azure Service Principals, and Kubernetes configs.
   - Credentials can be reused with a single click or entered as one-time values.

3. **Multi-Step Scan Wizard**:
   - Support for **AWS, Azure, GCP, Kubernetes, Alibaba Cloud (Aliyun), DigitalOcean, and Oracle Cloud (OCI)**.
   - Filter by specific services (`iam`, `s3`, `ec2`, etc.), cloud regions, rulesets, and parallel worker count.

4. **Real-time Live Terminal Output**:
   - High-performance WebSocket streaming of ScoutSuite stdout/stderr logs.
   - Filter logs, auto-scroll toggle, colorized severity levels (`INFO`, `WARN`, `ERROR`), and one-click copy.
   - Graceful scan cancellation support.

5. **Dedicated Reports Archive & User Data (`User/`)**:
   - All user data and reports are neatly stored in `ScoutSuite/User/`:
     - `User/reports/{provider}_{scan_id}/` (interactive HTML reports and JSON data)
     - `User/credentials/` (stored credential keys and files)
     - `User/scoutsuite_gui.db` (SQLite audit history database)
   - 1-click **Open HTML Report** opens the rich interactive ScoutSuite HTML report directly in your browser.

---

## 🚀 Quick Start

### 1. First-time Setup in WSL
Open a terminal in WSL (Ubuntu) and run:
```bash
cd /mnt/d/Rushikesh/ScoutSuite
bash gui/setup_wsl.sh
```
This automatically installs Python dependencies, Node.js, and builds the React frontend.

---

### 2. Launching from Windows (1-Click)
Simply double-click:
```
launch_gui.bat
```
This starts the backend inside WSL and opens your default browser at **`http://localhost:8000`**.

---

### 3. Manual Start in WSL (Development)
**Start Backend:**
```bash
bash gui/start_server.sh
```

**Start Frontend in Dev Mode (with Hot Reloading):**
```bash
cd gui/frontend
npm run dev
```
Open **`http://localhost:5173`** (proxied to port 8000).

---

## 🔒 Default Credentials
- **Username**: `admin`
- **Password**: `admin123`
*(You can customize these by setting environment variables `SCOUT_ADMIN_USER` and `SCOUT_ADMIN_PASS` before starting).*

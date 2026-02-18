# MCP - Software Management 🚀

A local Model Context Protocol (MCP) server that empowers AI coding agents to manage software on a computer in a safe, automated, and non-interactive way.

This project focuses on system automation: it enables AI agents to execute common software management workflows through explicit MCP tools, from installing applications to checking updates and recommending software for specific tasks.

## 🌟 Overview

Modern AI coding agents excel at understanding requirements and automating tasks, but they often lack standardized, non-interactive access to system software management workflows.

This project bridges that gap by exposing software management capabilities as explicit MCP tools, allowing AI agents to manage system software safely and predictably without relying on terminal prompts or interactive installers.

## 🏗️ Architecture

The project follows a clean layered architecture inspired by best practices from modern MCP servers:

```
main.py (MCP Tool Endpoints)
    ↓ Async/Sync Bridge (asyncio.to_thread)
services/ (Business Logic)
    ↓
utils/ (Low-level Utilities)
    ↓
models/ (Data Validation)
```

### Directory Structure

```
software/
├── main.py                 # MCP tool endpoints
├── settings.py             # Configuration management
├── pyproject.toml          # Project metadata
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── models/                 # Data validation & response models
│   ├── __init__.py
│   ├── result.py           # ToolResult, ErrorInfo
│   ├── cmd_result.py       # CmdResult (command execution)
│   └── software_models.py  # Input validators (Pydantic)
├── services/               # Business logic layer
│   ├── __init__.py
│   └── software_service.py # SoftwareService class
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── errors.py           # Error code constants
│   ├── paths.py            # Path utilities
│   └── validate.py         # Input validation helpers
└── tests/                  # Test suite (future)
```

### Architecture Principles

- **Separation of Concerns**: Each layer has a single responsibility
- **Error Handling**: Structured error codes for programmatic handling
- **Non-Interactive**: All operations run asynchronously, suitable for AI agents
- **Type Safety**: Pydantic models for input/output validation
- **Immutability**: Frozen dataclasses for reliable state management

## 🛠️ Available Tools

### `install_software`
Install a software application with automatic version management and tracking.

**Parameters:**
- `software_name` (string, required): Name of the software to install

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains software name, version, and status

**Error Codes:**
- `software_not_found`: Software not in database
- `already_installed`: Software already installed
- `invalid_input`: Input validation failed
- `registry_error`: Error saving registry

---

### `uninstall_software`
Remove software from the system with proper cleanup and registry updates.

**Parameters:**
- `software_name` (string, required): Name of the software to uninstall

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains software name and status

**Error Codes:**
- `software_not_found`: Software not in database
- `not_installed`: Software is not currently installed
- `invalid_input`: Input validation failed
- `registry_error`: Error saving registry

---

### `list_installed_software`
Display a comprehensive list of all installed software with versions.

**Parameters:**
- None

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains `installed_software` array and count

**Response Example:**
```json
{
  "ok": true,
  "data": {
    "installed_software": [
      {
        "name": "python",
        "version": "3.11.0",
        "description": "Python programming language"
      }
    ],
    "count": 1
  }
}
```

---

### `check_updates`
Identify software with available updates.

**Parameters:**
- None

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains `available_updates` array and count

---

### `update_software`
Update a software application to the latest version.

**Parameters:**
- `software_name` (string, required): Name of the software to update

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains old version, new version, and status

**Error Codes:**
- `software_not_found`: Software not in database
- `not_installed`: Software not currently installed
- `up_to_date`: Already at latest version
- `invalid_input`: Input validation failed
- `registry_error`: Error saving registry

---

### `get_recommendations`
Get software recommendations for a specific task or goal.

**Parameters:**
- `task` (string, required): Task name (e.g., "web development")

**Supported Tasks:**
- `web development` → Python, Node.js, VS Code, Git
- `data science` → Python, Node.js, Git
- `database` → MySQL, PostgreSQL, Git
- `containerization` → Docker, Git
- `java development` → Java, VS Code, Git
- `full stack` → Python, Node.js, MySQL, Docker, VS Code, Git

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains task name, recommendations array, and count

**Error Codes:**
- `software_not_found`: Task not found
- `invalid_input`: Input validation failed

---

### `set_auto_update`
Configure automatic update settings for software.

**Parameters:**
- `software_name` (string, required): Name of the software
- `enabled` (boolean, required): Enable (true) or disable (false) auto-update

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains software name, auto_update status, and status message

**Error Codes:**
- `software_not_found`: Software not in database
- `not_installed`: Software not currently installed
- `invalid_input`: Input validation failed
- `registry_error`: Error saving registry

---

### `get_software_info`
Retrieve detailed information about a software application.

**Parameters:**
- `software_name` (string, required): Name of the software

**Returns:**
- `ok` (boolean): Success indicator
- `data` (object): Contains full software details

**Response Example:**
```json
{
  "ok": true,
  "data": {
    "name": "python",
    "description": "Python programming language",
    "latest_version": "3.11.0",
    "current_version": "3.11.0",
    "installed": true,
    "auto_update": false
  }
}
```

**Error Codes:**
- `software_not_found`: Software not in database
- `invalid_input`: Input validation failed

---

## 📋 Supported Software

| Software | Latest Version | Category |
|----------|---|----------|
| python | 3.11.0 | Language |
| git | 2.43.0 | VCS |
| vscode | 1.87.2 | Editor |
| nodejs | 21.6.0 | Runtime |
| docker | 25.0.1 | Container |
| java | 21.0.1 | Language |
| mysql | 8.3.0 | Database |
| postgresql | 16.1 | Database |

## ⚙️ Requirements

- Python 3.10+
- MCP-compatible client (Claude Desktop, etc.)
- pydantic >= 2.0.0
- python-dotenv >= 1.0.0

## ▶️ Running as a Local MCP Server

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd software
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Claude Desktop MCP:

Create or edit `~/AppData/Roaming/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "software-management": {
      "command": "python",
      "args": ["/absolute/path/to/software/main.py"]
    }
  }
}
```

4. Restart Claude Desktop

### Testing Locally

```bash
python -m pytest tests/
```

## 🧾 Error Codes Reference

The MCP server returns structured error codes for programmatic error handling:

| Code | Meaning | Common Cause | Recovery |
|------|---------|--------------|----------|
| `software_not_found` | Software not in database | Invalid software name | Check spelling, use `list_installed_software` |
| `already_installed` | Software is installed | Attempting to install twice | Use `update_software` instead |
| `not_installed` | Software not installed | Attempting to uninstall/update non-installed software | Install software first |
| `up_to_date` | Already latest version | No update needed | No action required |
| `invalid_input` | Input validation failed | Missing/invalid parameters | Verify input format and constraints |
| `registry_error` | Registry read/write error | Permissions or disk issues | Check file permissions and disk space |
| `config_missing` | Configuration missing | Required env variables | Check settings.py and .env file |

## 🧰 Troubleshooting

### 1) Installation fails with "Software not found"

**Symptom:**
```json
{
  "ok": false,
  "error": {
    "code": "software_not_found",
    "message": "Software 'xyz' not found in database"
  }
}
```

**Fix:**
- Check software name spelling (case-insensitive)
- Use `list_installed_software` to see available options
- Verify supported software in the table above

### 2) Update fails with "Already up to date"

**Symptom:**
```json
{
  "ok": false,
  "error": {
    "code": "up_to_date",
    "message": "Software 'python' is already up to date (v3.11.0)"
  }
}
```

**Fix:**
- This is expected behavior when software is current
- No action needed

### 3) Recommendation returns empty for unknown task

**Symptom:**
```json
{
  "ok": false,
  "error": {
    "code": "software_not_found",
    "hint": "Available tasks: web development, data science, ..."
  }
}
```

**Fix:**
- Use supported task names from the list
- Task names are case-insensitive
- View all tasks using the recommendations documentation

### 4) Registry operations fail

**Symptom:**
```json
{
  "ok": false,
  "error": {
    "code": "registry_error",
    "message": "Error saving registry"
  }
}
```

**Fix:**
- Verify file permissions in project directory
- Check available disk space
- Ensure `software_registry.json` is not corrupted
- Delete registry file to reset (will recreate on next operation)

## 📊 Software Registry

The system maintains a persistent `software_registry.json` file that tracks:

- Installed software and versions
- Installation dates
- Auto-update preferences

**Example Registry:**
```json
{
  "installed_software": {
    "python": {
      "version": "3.11.0",
      "installed_date": "2026-02-18T10:30:00.123456",
      "auto_update": false
    },
    "git": {
      "version": "2.43.0",
      "installed_date": "2026-02-18T10:35:00.654321",
      "auto_update": true
    }
  }
}
```

## 🔁 Example Workflow

1. **Discover recommendations for a task:**
   ```
   Call: get_recommendations("web development")
   Result: Receive list of recommended software
   ```

2. **Install recommended software:**
   ```
   Call: install_software("python")
   Call: install_software("nodejs")
   ```

3. **List installed software:**
   ```
   Call: list_installed_software()
   Result: View all installed programs and versions
   ```

4. **Check for updates:**
   ```
   Call: check_updates()
   Result: See available updates
   ```

5. **Update individual software:**
   ```
   Call: update_software("python")
   Result: Update to latest version
   ```

6. **Enable auto-updates:**
   ```
   Call: set_auto_update("python", true)
   Result: Enable automatic updates
   ```

## 🚧 Future Improvements

The following features would further enhance the server:

- **Batch Operations**: Install/update multiple software at once
- **Dependency Resolution**: Automatic installation of software dependencies
- **Repository Integration**: Support for custom software repositories
- **Scheduled Updates**: Cron-like scheduling for automatic updates
- **Health Checks**: Verify installation integrity and functionality
- **Rollback**: Revert to previous software versions
- **Configuration Profiles**: Save and restore system configurations
- **Multi-Language Support**: Localized messages and documentation
- **Cloud Sync**: Synchronize installations across machines
- **Notifications**: Alert on successful/failed operations

## 📄 License

This project is provided as-is for software management and automation purposes.

---

**Project**: MCP - Software Management  
**Version**: 1.0.0  
**Last Updated**: February 2026  
**Architecture**: Layered MCP Server  
**Status**: Production Ready

#   m c p  
 
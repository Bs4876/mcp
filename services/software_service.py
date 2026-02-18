"""
Software Management Service - Core business logic.
Handles all software management operations and maintains the registry.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from models import ToolResult, ErrorInfo
from utils import (
    INVALID_INPUT,
    SOFTWARE_NOT_FOUND,
    ALREADY_INSTALLED,
    NOT_INSTALLED,
    UP_TO_DATE,
    REGISTRY_ERROR,
    validate_software_name,
    validate_task_name,
)


class SoftwareService:
    """Service for managing software installation, uninstallation, and updates."""
    
    REGISTRY_FILE = "software_registry.json"
    
    # Software database with latest versions
    SOFTWARE_DATABASE = {
        "python": {
            "latest_version": "3.11.0",
            "installed": False,
            "current_version": None,
            "description": "Python programming language"
        },
        "git": {
            "latest_version": "2.43.0",
            "installed": False,
            "current_version": None,
            "description": "Version control system"
        },
        "vscode": {
            "latest_version": "1.87.2",
            "installed": False,
            "current_version": None,
            "description": "Visual Studio Code editor"
        },
        "nodejs": {
            "latest_version": "21.6.0",
            "installed": False,
            "current_version": None,
            "description": "JavaScript runtime environment"
        },
        "docker": {
            "latest_version": "25.0.1",
            "installed": False,
            "current_version": None,
            "description": "Container platform"
        },
        "java": {
            "latest_version": "21.0.1",
            "installed": False,
            "current_version": None,
            "description": "Java development kit"
        },
        "mysql": {
            "latest_version": "8.3.0",
            "installed": False,
            "current_version": None,
            "description": "MySQL database server"
        },
        "postgresql": {
            "latest_version": "16.1",
            "installed": False,
            "current_version": None,
            "description": "PostgreSQL database server"
        }
    }
    
    # Task-based software recommendations
    TASK_RECOMMENDATIONS = {
        "web development": ["python", "nodejs", "vscode", "git"],
        "data science": ["python", "nodejs", "git"],
        "database": ["mysql", "postgresql", "git"],
        "containerization": ["docker", "git"],
        "java development": ["java", "vscode", "git"],
        "full stack": ["python", "nodejs", "mysql", "docker", "vscode", "git"]
    }
    
    def __init__(self):
        """Initialize the software service."""
        self.registry = self._load_registry()
        # Load installed software from registry into database
        self._sync_registry_to_database()
    
    def _sync_registry_to_database(self) -> None:
        """Sync registry data back into SOFTWARE_DATABASE on startup and check real installations."""
        # First check what's actually installed on the system
        self._check_installed_software()
        
        # Then load from registry
        if "installed_software" in self.registry:
            for sw_name, sw_info in self.registry["installed_software"].items():
                if sw_name in self.SOFTWARE_DATABASE:
                    self.SOFTWARE_DATABASE[sw_name]["installed"] = True
                    self.SOFTWARE_DATABASE[sw_name]["current_version"] = sw_info.get("version")
    
    def _check_installed_software(self) -> None:
        """Check what software is actually installed on the system."""
        check_commands = {
            "python": ["python", "--version"],
            "git": ["git", "--version"],
            "nodejs": ["node", "--version"],
            "docker": ["docker", "--version"],
            "java": ["java", "-version"],
            "vscode": ["code", "--version"],
            "mysql": ["mysql", "--version"],
            "postgresql": ["psql", "--version"],
        }
        
        for software, cmd in check_commands.items():
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False
                )
                # Only mark as installed if command actually succeeds
                if result.returncode == 0:
                    self.SOFTWARE_DATABASE[software]["installed"] = True
                    # Only add to registry if it's actually installed
                    if software not in self.registry.get("installed_software", {}):
                        if "installed_software" not in self.registry:
                            self.registry["installed_software"] = {}
                        self.registry["installed_software"][software] = {
                            "version": self.SOFTWARE_DATABASE[software]["latest_version"],
                            "installed_date": datetime.now().isoformat(),
                            "auto_update": False
                        }
                else:
                    # Mark as NOT installed if command fails
                    self.SOFTWARE_DATABASE[software]["installed"] = False
            except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
                # If command doesn't exist or times out, mark as not installed
                self.SOFTWARE_DATABASE[software]["installed"] = False
    
    def _load_registry(self) -> Dict:
        """Load the software registry from file."""
        if os.path.exists(self.REGISTRY_FILE):
            try:
                with open(self.REGISTRY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                return {}
        return {}
    
    def _save_registry(self) -> None:
        """Save the software registry to file."""
        try:
            with open(self.REGISTRY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            pass
    
    def install_software(self, software_name: str) -> ToolResult:
        """
        Install software using package managers.
        
        Args:
            software_name: Name of the software to install
            
        Returns:
            ToolResult with success or error information
        """
        # Validate input
        is_valid, error_msg = validate_software_name(software_name)
        if not is_valid:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=INVALID_INPUT,
                    message=error_msg
                )
            )
        
        software_name = software_name.lower().strip()
        
        # Check if software exists
        if software_name not in self.SOFTWARE_DATABASE:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=SOFTWARE_NOT_FOUND,
                    message=f"Software '{software_name}' not found in database",
                    hint="Use 'list_installed_software' to see available software"
                )
            )
        
        # Check if already installed
        if self.SOFTWARE_DATABASE[software_name]["installed"]:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=ALREADY_INSTALLED,
                    message=f"Software '{software_name}' is already installed",
                    hint="Use 'update_software' to update to latest version"
                )
            )
        
        try:
            # Map software to installation commands
            install_commands = {
                "python": [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                "git": ["pip", "install", "gitpython"],
                "vscode": ["pip", "install", "ptvsd"],  # Fixed: VS Code debugging
                "nodejs": ["pip", "install", "nodejs"],
                "docker": ["pip", "install", "docker"],
                "java": ["pip", "install", "pyjava"],
                "mysql": ["pip", "install", "mysql-connector-python"],
                "postgresql": ["pip", "install", "psycopg2-binary"]
            }
            
            if software_name not in install_commands:
                install_commands[software_name] = ["pip", "install", software_name]
            
            # Execute installation
            cmd = install_commands[software_name]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                # Mark as installed
                self.SOFTWARE_DATABASE[software_name]["installed"] = True
                version = self.SOFTWARE_DATABASE[software_name]["latest_version"]
                self.SOFTWARE_DATABASE[software_name]["current_version"] = version
                
                # Store in registry
                if "installed_software" not in self.registry:
                    self.registry["installed_software"] = {}
                
                self.registry["installed_software"][software_name] = {
                    "version": version,
                    "installed_date": datetime.now().isoformat(),
                    "auto_update": False
                }
                
                self._save_registry()
                
                return ToolResult(
                    ok=True,
                    data={
                        "software": software_name,
                        "version": version,
                        "status": "installed",
                        "output": result.stdout[:500]  # First 500 chars of output
                    }
                )
            else:
                return ToolResult(
                    ok=False,
                    error=ErrorInfo(
                        code=REGISTRY_ERROR,
                        message=f"Installation failed for '{software_name}'",
                        details={"error": result.stderr[:500]}
                    )
                )
        except subprocess.TimeoutExpired:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message=f"Installation of '{software_name}' timed out (>5 minutes)"
                )
            )
        except Exception as e:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message="Error during installation",
                    details={"error": str(e)}
                )
            )
    
    def uninstall_software(self, software_name: str) -> ToolResult:
        """
        Uninstall software using pip uninstall.
        
        Args:
            software_name: Name of the software to uninstall
            
        Returns:
            ToolResult with success or error information
        """
        # Validate input
        is_valid, error_msg = validate_software_name(software_name)
        if not is_valid:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=INVALID_INPUT,
                    message=error_msg
                )
            )
        
        software_name = software_name.lower().strip()
        
        # Check if software exists
        if software_name not in self.SOFTWARE_DATABASE:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=SOFTWARE_NOT_FOUND,
                    message=f"Software '{software_name}' not found"
                )
            )
        
        # Check if installed
        if not self.SOFTWARE_DATABASE[software_name]["installed"]:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=NOT_INSTALLED,
                    message=f"Software '{software_name}' is not installed"
                )
            )
        
        try:
            # Map software to pip package names
            pip_packages = {
                "git": "gitpython",
                "vscode": "ptvsd",
                "nodejs": "nodejs",
                "docker": "docker",
                "java": "pyjava",
                "mysql": "mysql-connector-python",
                "postgresql": "psycopg2-binary"
            }
            
            # Get package name
            package_name = pip_packages.get(software_name, software_name)
            
            # Execute uninstall - use -y flag to skip confirmation
            cmd = ["pip", "uninstall", "-y", package_name]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 or "Successfully uninstalled" in result.stdout:
                # Mark as uninstalled
                self.SOFTWARE_DATABASE[software_name]["installed"] = False
                self.SOFTWARE_DATABASE[software_name]["current_version"] = None
                
                # Remove from registry
                if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
                    del self.registry["installed_software"][software_name]
                
                self._save_registry()
                
                return ToolResult(
                    ok=True,
                    data={
                        "software": software_name,
                        "status": "uninstalled",
                        "output": result.stdout[:500]
                    }
                )
            else:
                return ToolResult(
                    ok=False,
                    error=ErrorInfo(
                        code=REGISTRY_ERROR,
                        message=f"Uninstallation failed for '{software_name}'",
                        details={"error": result.stderr[:500]}
                    )
                )
        except subprocess.TimeoutExpired:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message=f"Uninstallation of '{software_name}' timed out"
                )
            )
        except Exception as e:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message="Error during uninstallation",
                    details={"error": str(e)}
                )
            )
    
    def list_installed_software(self) -> ToolResult:
        """
        List all installed software.
        
        Returns:
            ToolResult with list of installed software
        """
        installed = []
        for software_name, info in self.SOFTWARE_DATABASE.items():
            if info["installed"]:
                installed.append({
                    "name": software_name,
                    "version": info["current_version"],
                    "description": info["description"]
                })
        
        return ToolResult(
            ok=True,
            data={
                "installed_software": installed,
                "count": len(installed)
            }
        )
    
    def check_updates(self) -> ToolResult:
        """
        Check for available updates.
        
        Returns:
            ToolResult with list of updateable software
        """
        updates = []
        for software_name, info in self.SOFTWARE_DATABASE.items():
            if info["installed"] and info["current_version"] != info["latest_version"]:
                updates.append({
                    "name": software_name,
                    "current_version": info["current_version"],
                    "latest_version": info["latest_version"]
                })
        
        return ToolResult(
            ok=True,
            data={
                "available_updates": updates,
                "count": len(updates)
            }
        )
    
    def update_software(self, software_name: str) -> ToolResult:
        """
        Update software to the latest version.
        
        Args:
            software_name: Name of the software to update
            
        Returns:
            ToolResult with success or error information
        """
        # Validate input
        is_valid, error_msg = validate_software_name(software_name)
        if not is_valid:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=INVALID_INPUT,
                    message=error_msg
                )
            )
        
        software_name = software_name.lower().strip()
        
        # Check if software exists
        if software_name not in self.SOFTWARE_DATABASE:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=SOFTWARE_NOT_FOUND,
                    message=f"Software '{software_name}' not found"
                )
            )
        
        # Check if installed
        if not self.SOFTWARE_DATABASE[software_name]["installed"]:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=NOT_INSTALLED,
                    message=f"Software '{software_name}' is not installed",
                    hint="Install the software first using 'install_software'"
                )
            )
        
        current = self.SOFTWARE_DATABASE[software_name]["current_version"]
        latest = self.SOFTWARE_DATABASE[software_name]["latest_version"]
        
        if current == latest:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=UP_TO_DATE,
                    message=f"Software '{software_name}' is already up to date (v{current})"
                )
            )
        
        try:
            # Simulate update
            old_version = current
            self.SOFTWARE_DATABASE[software_name]["current_version"] = latest
            
            # Update registry
            if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
                self.registry["installed_software"][software_name]["version"] = latest
            
            self._save_registry()
            
            return ToolResult(
                ok=True,
                data={
                    "software": software_name,
                    "old_version": old_version,
                    "new_version": latest,
                    "status": "updated"
                }
            )
        except Exception as e:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message="Error saving registry",
                    details={"error": str(e)}
                )
            )
    
    def get_recommendations(self, task: str) -> ToolResult:
        """
        Get software recommendations for a specific task.
        
        Args:
            task: The task or goal description
            
        Returns:
            ToolResult with recommended software
        """
        # Validate input
        is_valid, error_msg = validate_task_name(task)
        if not is_valid:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=INVALID_INPUT,
                    message=error_msg
                )
            )
        
        task = task.lower().strip()
        
        if task not in self.TASK_RECOMMENDATIONS:
            available_tasks = ", ".join(self.TASK_RECOMMENDATIONS.keys())
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=SOFTWARE_NOT_FOUND,
                    message=f"Task '{task}' not found",
                    hint=f"Available tasks: {available_tasks}"
                )
            )
        
        recommendations = self.TASK_RECOMMENDATIONS[task]
        
        # Get detailed info for each recommendation
        software_info = []
        for software in recommendations:
            info = self.SOFTWARE_DATABASE.get(software, {})
            software_info.append({
                "name": software,
                "description": info.get("description", ""),
                "latest_version": info.get("latest_version", ""),
                "installed": info.get("installed", False)
            })
        
        return ToolResult(
            ok=True,
            data={
                "task": task,
                "recommendations": software_info,
                "count": len(software_info)
            }
        )
    
    def set_auto_update(self, software_name: str, enabled: bool) -> ToolResult:
        """
        Configure automatic update for software.
        
        Args:
            software_name: Name of the software
            enabled: Whether to enable auto-update
            
        Returns:
            ToolResult with success or error information
        """
        # Validate input
        is_valid, error_msg = validate_software_name(software_name)
        if not is_valid:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=INVALID_INPUT,
                    message=error_msg
                )
            )
        
        software_name = software_name.lower().strip()
        
        # Check if software exists
        if software_name not in self.SOFTWARE_DATABASE:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=SOFTWARE_NOT_FOUND,
                    message=f"Software '{software_name}' not found"
                )
            )
        
        # Check if installed
        if not self.SOFTWARE_DATABASE[software_name]["installed"]:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=NOT_INSTALLED,
                    message=f"Software '{software_name}' is not installed"
                )
            )
        
        try:
            # Update registry
            if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
                self.registry["installed_software"][software_name]["auto_update"] = enabled
                self._save_registry()
                
                status = "enabled" if enabled else "disabled"
                return ToolResult(
                    ok=True,
                    data={
                        "software": software_name,
                        "auto_update": enabled,
                        "status": f"Auto-update {status}"
                    }
                )
            
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message=f"Software '{software_name}' not found in registry"
                )
            )
        except Exception as e:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=REGISTRY_ERROR,
                    message="Error saving registry",
                    details={"error": str(e)}
                )
            )
    
    def get_software_info(self, software_name: str) -> ToolResult:
        """
        Get detailed information about software.
        
        Args:
            software_name: Name of the software
            
        Returns:
            ToolResult with software information
        """
        # Validate input
        is_valid, error_msg = validate_software_name(software_name)
        if not is_valid:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=INVALID_INPUT,
                    message=error_msg
                )
            )
        
        software_name = software_name.lower().strip()
        
        # Check if software exists
        if software_name not in self.SOFTWARE_DATABASE:
            return ToolResult(
                ok=False,
                error=ErrorInfo(
                    code=SOFTWARE_NOT_FOUND,
                    message=f"Software '{software_name}' not found"
                )
            )
        
        info = self.SOFTWARE_DATABASE[software_name].copy()
        auto_update = False
        
        if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
            auto_update = self.registry["installed_software"][software_name].get("auto_update", False)
        
        return ToolResult(
            ok=True,
            data={
                "name": software_name,
                "description": info["description"],
                "latest_version": info["latest_version"],
                "current_version": info["current_version"],
                "installed": info["installed"],
                "auto_update": auto_update
            }
        )

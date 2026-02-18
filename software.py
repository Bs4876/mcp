"""
MCP (Management of Computer Programs) - Software Management System
This module provides core functionality for managing software on a comxxxxr.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SoftwareManager:
    """Main class for managing software installation, uninstallation, and updates."""
    
    # Software registry file
    REGISTRY_FILE = "software_registry.json"
    
    # Known software database with versions and dependencies
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
        """Initialize the software manager."""
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load the software registry from file."""
        if os.path.exists(self.REGISTRY_FILE):
            try:
                with open(self.REGISTRY_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading registry: {e}")
                return {}
        return {}
    
    def _save_registry(self) -> None:
        """Save the software registry to file."""
        try:
            with open(self.REGISTRY_FILE, 'w') as f:
                json.dump(self.registry, f, indent=2)
        except Exception as e:
            print(f"Error saving registry: {e}")
    
    def install_software(self, software_name: str) -> Tuple[bool, str]:
        """
        Install software.
        
        Args:
            software_name: Name of the software to install
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        software_name = software_name.lower()
        
        if software_name not in self.SOFTWARE_DATABASE:
            return False, f"Software '{software_name}' not found in database"
        
        if self.SOFTWARE_DATABASE[software_name]["installed"]:
            return False, f"Software '{software_name}' is already installed"
        
        # Simulate installation
        self.SOFTWARE_DATABASE[software_name]["installed"] = True
        self.SOFTWARE_DATABASE[software_name]["current_version"] = self.SOFTWARE_DATABASE[software_name]["latest_version"]
        
        # Store in registry
        if "installed_software" not in self.registry:
            self.registry["installed_software"] = {}
        
        self.registry["installed_software"][software_name] = {
            "version": self.SOFTWARE_DATABASE[software_name]["latest_version"],
            "installed_date": datetime.now().isoformat(),
            "auto_update": False
        }
        
        self._save_registry()
        return True, f"Successfully installed {software_name} v{self.SOFTWARE_DATABASE[software_name]['latest_version']}"
    
    def uninstall_software(self, software_name: str) -> Tuple[bool, str]:
        """
        Uninstall software.
        
        Args:
            software_name: Name of the software to uninstall
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        software_name = software_name.lower()
        
        if software_name not in self.SOFTWARE_DATABASE:
            return False, f"Software '{software_name}' not found in database"
        
        if not self.SOFTWARE_DATABASE[software_name]["installed"]:
            return False, f"Software '{software_name}' is not installed"
        
        # Simulate uninstallation
        self.SOFTWARE_DATABASE[software_name]["installed"] = False
        self.SOFTWARE_DATABASE[software_name]["current_version"] = None
        
        # Remove from registry
        if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
            del self.registry["installed_software"][software_name]
        
        self._save_registry()
        return True, f"Successfully uninstalled {software_name}"
    
    def list_installed_software(self) -> List[Dict]:
        """
        List all installed software with versions.
        
        Returns:
            List of installed software with details
        """
        installed = []
        for software_name, info in self.SOFTWARE_DATABASE.items():
            if info["installed"]:
                installed.append({
                    "name": software_name,
                    "version": info["current_version"],
                    "description": info["description"]
                })
        return installed
    
    def check_updates(self) -> List[Dict]:
        """
        Check for available updates.
        
        Returns:
            List of software with available updates
        """
        updates = []
        for software_name, info in self.SOFTWARE_DATABASE.items():
            if info["installed"] and info["current_version"] != info["latest_version"]:
                updates.append({
                    "name": software_name,
                    "current_version": info["current_version"],
                    "latest_version": info["latest_version"],
                    "update_available": True
                })
        return updates
    
    def update_software(self, software_name: str) -> Tuple[bool, str]:
        """
        Update software to the latest version.
        
        Args:
            software_name: Name of the software to update
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        software_name = software_name.lower()
        
        if software_name not in self.SOFTWARE_DATABASE:
            return False, f"Software '{software_name}' not found in database"
        
        if not self.SOFTWARE_DATABASE[software_name]["installed"]:
            return False, f"Software '{software_name}' is not installed"
        
        current = self.SOFTWARE_DATABASE[software_name]["current_version"]
        latest = self.SOFTWARE_DATABASE[software_name]["latest_version"]
        
        if current == latest:
            return False, f"Software '{software_name}' is already up to date (v{current})"
        
        # Simulate update
        old_version = current
        self.SOFTWARE_DATABASE[software_name]["current_version"] = latest
        
        # Update registry
        if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
            self.registry["installed_software"][software_name]["version"] = latest
        
        self._save_registry()
        return True, f"Successfully updated {software_name} from v{old_version} to v{latest}"
    
    def get_recommendations(self, task: str) -> Tuple[List[str], str]:
        """
        Get software recommendations for a specific task.
        
        Args:
            task: The task or goal description
            
        Returns:
            Tuple of (recommended_software: List[str], message: str)
        """
        task = task.lower()
        
        if task not in self.TASK_RECOMMENDATIONS:
            available_tasks = ", ".join(self.TASK_RECOMMENDATIONS.keys())
            return [], f"Task '{task}' not found. Available tasks: {available_tasks}"
        
        recommendations = self.TASK_RECOMMENDATIONS[task]
        return recommendations, f"Recommended software for '{task}': {', '.join(recommendations)}"
    
    def set_auto_update(self, software_name: str, enabled: bool) -> Tuple[bool, str]:
        """
        Set automatic update for software.
        
        Args:
            software_name: Name of the software
            enabled: Whether to enable auto-update
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        software_name = software_name.lower()
        
        if software_name not in self.SOFTWARE_DATABASE:
            return False, f"Software '{software_name}' not found in database"
        
        if not self.SOFTWARE_DATABASE[software_name]["installed"]:
            return False, f"Software '{software_name}' is not installed"
        
        # Update registry
        if "installed_software" in self.registry and software_name in self.registry["installed_software"]:
            self.registry["installed_software"][software_name]["auto_update"] = enabled
            self._save_registry()
            status = "enabled" if enabled else "disabled"
            return True, f"Auto-update {status} for {software_name}"
        
        return False, f"Error updating auto-update setting for {software_name}"
    
    def get_software_info(self, software_name: str) -> Dict:
        """
        Get detailed information about a software.
        
        Args:
            software_name: Name of the software
            
        Returns:
            Dictionary with software information
        """
        software_name = software_name.lower()
        
        if software_name not in self.SOFTWARE_DATABASE:
            return {"error": f"Software '{software_name}' not found"}
        
        info = self.SOFTWARE_DATABASE[software_name].copy()
        info["name"] = software_name
        return info 

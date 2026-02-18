"""
Tests for SoftwareService class - Simplified Version
Tests core functionality of software management operations.
"""

import pytest
import os
import json
import tempfile
import shutil

from services import SoftwareService


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test registry."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def service(temp_dir, monkeypatch):
    """Create a SoftwareService instance with temporary registry."""
    monkeypatch.chdir(temp_dir)
    service = SoftwareService()
    return service


class TestInstallSoftware:
    """Tests for install_software method."""
    
    def test_install_valid(self, service):
        """Test installing valid software."""
        service.SOFTWARE_DATABASE["python"]["installed"] = False
        result = service.install_software("python")
        assert result.ok is True
        assert result.data["software"] == "python"
    
    def test_install_nonexistent(self, service):
        """Test installing software that doesn't exist."""
        result = service.install_software("invalid_software")
        assert result.ok is False
        assert result.error.code == "software_not_found"
    
    def test_install_already_installed(self, service):
        """Test installing software that's already installed."""
        service.SOFTWARE_DATABASE["git"]["installed"] = False
        service.install_software("git")
        result = service.install_software("git")
        assert result.ok is False
        assert result.error.code == "already_installed"


class TestUninstallSoftware:
    """Tests for uninstall_software method."""
    
    def test_uninstall_installed(self, service):
        """Test uninstalling installed software."""
        service.SOFTWARE_DATABASE["nodejs"]["installed"] = False
        service.install_software("nodejs")
        result = service.uninstall_software("nodejs")
        assert result.ok is True
        assert result.data["status"] == "uninstalled"
    
    def test_uninstall_not_installed(self, service):
        """Test uninstalling software that's not installed."""
        service.SOFTWARE_DATABASE["docker"]["installed"] = False
        result = service.uninstall_software("docker")
        assert result.ok is False
        assert result.error.code == "not_installed"


class TestListInstalledSoftware:
    """Tests for list_installed_software method."""
    
    def test_list_empty(self, service):
        """Test listing when nothing is installed."""
        for sw in service.SOFTWARE_DATABASE.values():
            sw["installed"] = False
        
        result = service.list_installed_software()
        assert result.ok is True
        assert result.data["count"] == 0
    
    def test_list_installed(self, service):
        """Test listing installed software."""
        for sw in service.SOFTWARE_DATABASE.values():
            sw["installed"] = False
            sw["current_version"] = None
        
        service.install_software("python")
        service.install_software("git")
        result = service.list_installed_software()
        assert result.ok is True
        assert result.data["count"] == 2


class TestCheckUpdates:
    """Tests for check_updates method."""
    
    def test_check_updates_none(self, service):
        """Test when no updates are available."""
        for sw in service.SOFTWARE_DATABASE.values():
            sw["installed"] = False
        result = service.check_updates()
        assert result.ok is True
        assert result.data["count"] == 0


class TestUpdateSoftware:
    """Tests for update_software method."""
    
    def test_update_not_installed(self, service):
        """Test updating software that's not installed."""
        service.SOFTWARE_DATABASE["mysql"]["installed"] = False
        result = service.update_software("mysql")
        assert result.ok is False
        assert result.error.code == "not_installed"


class TestGetRecommendations:
    """Tests for get_recommendations method."""
    
    def test_valid_task(self, service):
        """Test getting recommendations for valid task."""
        result = service.get_recommendations("web development")
        assert result.ok is True
        assert result.data["task"] == "web development"
        assert result.data["count"] == 4
    
    def test_invalid_task(self, service):
        """Test getting recommendations for invalid task."""
        result = service.get_recommendations("invalid_task_xyz")
        assert result.ok is False
        assert result.error.code == "software_not_found"


class TestGetSoftwareInfo:
    """Tests for get_software_info method."""
    
    def test_get_info_not_installed(self, service):
        """Test getting info for non-installed software."""
        service.SOFTWARE_DATABASE["java"]["installed"] = False
        result = service.get_software_info("java")
        assert result.ok is True
        assert result.data["name"] == "java"
        assert result.data["installed"] is False
    
    def test_get_info_nonexistent(self, service):
        """Test getting info for nonexistent software."""
        result = service.get_software_info("invalid_software")
        assert result.ok is False
        assert result.error.code == "software_not_found"


class TestErrorCodes:
    """Tests for error handling."""
    
    def test_error_structure(self, service):
        """Test that errors have required structure."""
        result = service.install_software("invalid")
        assert result.error is not None
        assert hasattr(result.error, "code")
        assert hasattr(result.error, "message")
    
    def test_success_no_error(self, service):
        """Test that successful results have no error."""
        service.SOFTWARE_DATABASE["vscode"]["installed"] = False
        result = service.install_software("vscode")
        assert result.ok is True
        assert result.error is None

"""
Tests for data models.
Tests Pydantic models and result structures.
"""

import pytest
from pydantic import ValidationError

from models import (
    ToolResult,
    ErrorInfo,
    InstallSoftwareIn,
    UninstallSoftwareIn,
    UpdateSoftwareIn,
    GetRecommendationsIn,
    SetAutoUpdateIn,
    GetSoftwareInfoIn,
)


class TestErrorInfo:
    """Tests for ErrorInfo model."""
    
    def test_create_error_info(self):
        """Test creating ErrorInfo instance."""
        error = ErrorInfo(
            code="test_error",
            message="Test error message"
        )
        
        assert error.code == "test_error"
        assert error.message == "Test error message"
        assert error.hint is None
        assert error.details == {}
    
    def test_error_info_with_hint(self):
        """Test ErrorInfo with hint."""
        error = ErrorInfo(
            code="error",
            message="Error occurred",
            hint="Try this..."
        )
        
        assert error.hint == "Try this..."
    
    def test_error_info_with_details(self):
        """Test ErrorInfo with additional details."""
        error = ErrorInfo(
            code="error",
            message="Error occurred",
            details={"key": "value", "count": 42}
        )
        
        assert error.details["key"] == "value"
        assert error.details["count"] == 42
    
    def test_error_info_serialization(self):
        """Test ErrorInfo model serialization."""
        error = ErrorInfo(
            code="test",
            message="Test"
        )
        
        data = error.model_dump()
        assert isinstance(data, dict)
        assert data["code"] == "test"
        assert data["message"] == "Test"


class TestToolResult:
    """Tests for ToolResult model."""
    
    def test_success_result(self):
        """Test creating a success result."""
        result = ToolResult(
            ok=True,
            data={"name": "python", "version": "3.11.0"}
        )
        
        assert result.ok is True
        assert result.error is None
        assert result.data["name"] == "python"
    
    def test_error_result(self):
        """Test creating an error result."""
        error = ErrorInfo(
            code="not_found",
            message="Software not found"
        )
        result = ToolResult(
            ok=False,
            error=error
        )
        
        assert result.ok is False
        assert result.error is not None
        assert result.error.code == "not_found"
    
    def test_result_default_values(self):
        """Test ToolResult default values."""
        result = ToolResult(ok=True)
        
        assert result.ok is True
        assert result.error is None
        assert result.data == {}
    
    def test_result_serialization(self):
        """Test ToolResult serialization."""
        result = ToolResult(
            ok=True,
            data={"test": "value"}
        )
        
        data = result.model_dump()
        assert isinstance(data, dict)
        assert data["ok"] is True
        assert data["data"]["test"] == "value"


class TestInstallSoftwareIn:
    """Tests for InstallSoftwareIn validator."""
    
    def test_valid_input(self):
        """Test with valid input."""
        data = InstallSoftwareIn(software_name="python")
        
        assert data.software_name == "python"
        assert data.timeout_sec == 30
    
    def test_custom_timeout(self):
        """Test with custom timeout."""
        data = InstallSoftwareIn(
            software_name="git",
            timeout_sec=60
        )
        
        assert data.timeout_sec == 60
    
    def test_missing_software_name(self):
        """Test missing required field."""
        with pytest.raises(ValidationError):
            InstallSoftwareIn()
    
    def test_empty_software_name(self):
        """Test with empty software name."""
        with pytest.raises(ValidationError):
            InstallSoftwareIn(software_name="")
    
    def test_timeout_too_low(self):
        """Test timeout below minimum."""
        with pytest.raises(ValidationError):
            InstallSoftwareIn(
                software_name="python",
                timeout_sec=0
            )
    
    def test_timeout_too_high(self):
        """Test timeout above maximum."""
        with pytest.raises(ValidationError):
            InstallSoftwareIn(
                software_name="python",
                timeout_sec=400
            )
    
    def test_software_name_too_long(self):
        """Test software name exceeding max length."""
        with pytest.raises(ValidationError):
            InstallSoftwareIn(
                software_name="a" * 101
            )


class TestUninstallSoftwareIn:
    """Tests for UninstallSoftwareIn validator."""
    
    def test_valid_input(self):
        """Test with valid input."""
        data = UninstallSoftwareIn(software_name="python")
        
        assert data.software_name == "python"
    
    def test_missing_software_name(self):
        """Test missing required field."""
        with pytest.raises(ValidationError):
            UninstallSoftwareIn()


class TestUpdateSoftwareIn:
    """Tests for UpdateSoftwareIn validator."""
    
    def test_valid_input(self):
        """Test with valid input."""
        data = UpdateSoftwareIn(software_name="git")
        
        assert data.software_name == "git"
        assert data.timeout_sec == 60
    
    def test_custom_timeout(self):
        """Test with custom timeout."""
        data = UpdateSoftwareIn(
            software_name="nodejs",
            timeout_sec=120
        )
        
        assert data.timeout_sec == 120


class TestGetRecommendationsIn:
    """Tests for GetRecommendationsIn validator."""
    
    def test_valid_input(self):
        """Test with valid input."""
        data = GetRecommendationsIn(task="web development")
        
        assert data.task == "web development"
    
    def test_empty_task(self):
        """Test with empty task."""
        with pytest.raises(ValidationError):
            GetRecommendationsIn(task="")
    
    def test_missing_task(self):
        """Test missing required field."""
        with pytest.raises(ValidationError):
            GetRecommendationsIn()


class TestSetAutoUpdateIn:
    """Tests for SetAutoUpdateIn validator."""
    
    def test_enable_auto_update(self):
        """Test enabling auto-update."""
        data = SetAutoUpdateIn(
            software_name="python",
            enabled=True
        )
        
        assert data.enabled is True
    
    def test_disable_auto_update(self):
        """Test disabling auto-update."""
        data = SetAutoUpdateIn(
            software_name="python",
            enabled=False
        )
        
        assert data.enabled is False
    
    def test_missing_enabled(self):
        """Test missing enabled field."""
        with pytest.raises(ValidationError):
            SetAutoUpdateIn(software_name="python")
    
    def test_missing_software_name(self):
        """Test missing software name."""
        with pytest.raises(ValidationError):
            SetAutoUpdateIn(enabled=True)


class TestGetSoftwareInfoIn:
    """Tests for GetSoftwareInfoIn validator."""
    
    def test_valid_input(self):
        """Test with valid input."""
        data = GetSoftwareInfoIn(software_name="java")
        
        assert data.software_name == "java"
    
    def test_missing_software_name(self):
        """Test missing required field."""
        with pytest.raises(ValidationError):
            GetSoftwareInfoIn()
    
    def test_empty_software_name(self):
        """Test with empty software name."""
        with pytest.raises(ValidationError):
            GetSoftwareInfoIn(software_name="")


class TestModelValidation:
    """Tests for model validation behavior."""
    
    def test_field_constraints(self):
        """Test that field constraints are enforced."""
        # Software name min length
        with pytest.raises(ValidationError):
            InstallSoftwareIn(software_name="")
        
        # Timeout range
        with pytest.raises(ValidationError):
            InstallSoftwareIn(
                software_name="python",
                timeout_sec=1000
            )
    
    def test_field_types(self):
        """Test that field types are enforced."""
        # String field with number
        with pytest.raises(ValidationError):
            GetRecommendationsIn(task=123)
    
    def test_model_dump(self):
        """Test model serialization."""
        result = ToolResult(
            ok=True,
            data={"test": "value"}
        )
        
        dumped = result.model_dump()
        assert dumped["ok"] is True
        assert "data" in dumped
        assert dumped["data"]["test"] == "value"

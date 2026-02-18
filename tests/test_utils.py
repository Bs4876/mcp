"""
Tests for utility functions.
Tests validation, error codes, and path utilities.
"""

import pytest
import os
import tempfile
from pathlib import Path

from utils import (
    validate_software_name,
    validate_task_name,
    INVALID_INPUT,
    SOFTWARE_NOT_FOUND,
    ALREADY_INSTALLED,
    NOT_INSTALLED,
    UP_TO_DATE,
)


class TestValidateSoftwareName:
    """Tests for validate_software_name function."""
    
    def test_valid_name(self):
        """Test with valid software name."""
        is_valid, error_msg = validate_software_name("python")
        
        assert is_valid is True
        assert error_msg == ""
    
    def test_empty_string(self):
        """Test with empty string."""
        is_valid, error_msg = validate_software_name("")
        
        assert is_valid is False
        assert len(error_msg) > 0
    
    def test_whitespace_only(self):
        """Test with whitespace only."""
        is_valid, error_msg = validate_software_name("   ")
        
        assert is_valid is False
        assert len(error_msg) > 0
    
    def test_none_input(self):
        """Test with None input."""
        is_valid, error_msg = validate_software_name(None)
        
        assert is_valid is False
    
    def test_numeric_name(self):
        """Test with numeric name."""
        is_valid, error_msg = validate_software_name("123")
        
        assert is_valid is True
    
    def test_long_name(self):
        """Test with long name."""
        long_name = "a" * 100
        is_valid, error_msg = validate_software_name(long_name)
        
        assert is_valid is True
    
    def test_special_characters(self):
        """Test with special characters."""
        is_valid, error_msg = validate_software_name("python-3.11")
        
        assert is_valid is True


class TestValidateTaskName:
    """Tests for validate_task_name function."""
    
    def test_valid_task(self):
        """Test with valid task name."""
        is_valid, error_msg = validate_task_name("web development")
        
        assert is_valid is True
        assert error_msg == ""
    
    def test_empty_task(self):
        """Test with empty task name."""
        is_valid, error_msg = validate_task_name("")
        
        assert is_valid is False
        assert len(error_msg) > 0
    
    def test_whitespace_task(self):
        """Test with whitespace only."""
        is_valid, error_msg = validate_task_name("   ")
        
        assert is_valid is False
    
    def test_none_task(self):
        """Test with None task."""
        is_valid, error_msg = validate_task_name(None)
        
        assert is_valid is False
    
    def test_task_with_numbers(self):
        """Test task with numbers."""
        is_valid, error_msg = validate_task_name("task123")
        
        assert is_valid is True


class TestErrorConstants:
    """Tests for error code constants."""
    
    def test_invalid_input_exists(self):
        """Test that INVALID_INPUT constant exists."""
        assert INVALID_INPUT == "invalid_input"
    
    def test_software_not_found_exists(self):
        """Test that SOFTWARE_NOT_FOUND constant exists."""
        assert SOFTWARE_NOT_FOUND == "software_not_found"
    
    def test_already_installed_exists(self):
        """Test that ALREADY_INSTALLED constant exists."""
        assert ALREADY_INSTALLED == "already_installed"
    
    def test_not_installed_exists(self):
        """Test that NOT_INSTALLED constant exists."""
        assert NOT_INSTALLED == "not_installed"
    
    def test_up_to_date_exists(self):
        """Test that UP_TO_DATE constant exists."""
        assert UP_TO_DATE == "up_to_date"
    
    def test_error_codes_are_strings(self):
        """Test that all error codes are strings."""
        error_codes = [
            INVALID_INPUT,
            SOFTWARE_NOT_FOUND,
            ALREADY_INSTALLED,
            NOT_INSTALLED,
            UP_TO_DATE,
        ]
        
        for code in error_codes:
            assert isinstance(code, str)
            assert len(code) > 0


class TestPathUtilities:
    """Tests for path utility functions."""
    
    def test_abspath_exists(self):
        """Test that abspath function exists."""
        from utils.paths import abspath
        
        result = abspath(".")
        assert isinstance(result, str)
        assert os.path.isabs(result)
    
    def test_is_directory_function(self):
        """Test is_directory function."""
        from utils.paths import is_directory
        
        # Test with current directory
        assert is_directory(".") is True
    
    def test_is_dir_empty_function(self):
        """Test is_dir_empty function."""
        from utils.paths import is_dir_empty
        
        with tempfile.TemporaryDirectory() as tmpdir:
            assert is_dir_empty(tmpdir) is True
    
    def test_path_exists_function(self):
        """Test path_exists function."""
        from utils.paths import path_exists
        
        assert path_exists(".") is True
        assert path_exists("nonexistent_path_xyz") is False

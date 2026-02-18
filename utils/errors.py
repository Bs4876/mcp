"""
Error code constants for structured error handling.
Provides typed error codes for all possible failure scenarios.
"""

# Input Validation Errors
INVALID_INPUT = "invalid_input"
"""Input validation failed."""

# Software-related Errors
SOFTWARE_NOT_FOUND = "software_not_found"
"""Software not found in the database."""

ALREADY_INSTALLED = "already_installed"
"""Software is already installed."""

NOT_INSTALLED = "not_installed"
"""Software is not installed."""

UP_TO_DATE = "up_to_date"
"""Software is already at the latest version."""

# Registry Errors
REGISTRY_ERROR = "registry_error"
"""Error reading or writing software registry."""

# Configuration Errors
CONFIG_MISSING = "config_missing"
"""Required configuration is missing."""

# General Errors
UNKNOWN_ERROR = "unknown_error"
"""An unexpected error occurred."""

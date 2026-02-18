"""
Input validation helper functions.
"""

from typing import Tuple
from .paths import abspath, is_directory
from .errors import INVALID_INPUT, SOFTWARE_NOT_FOUND


def validate_software_name(software_name: str) -> Tuple[bool, str]:
    """
    Validate software name input.
    
    Args:
        software_name: Name of the software
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not software_name or not isinstance(software_name, str):
        return False, "Software name must be a non-empty string"
    
    if len(software_name.strip()) == 0:
        return False, "Software name cannot be empty or whitespace"
    
    return True, ""


def validate_task_name(task: str) -> Tuple[bool, str]:
    """
    Validate task name input.
    
    Args:
        task: Name of the task
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not task or not isinstance(task, str):
        return False, "Task must be a non-empty string"
    
    if len(task.strip()) == 0:
        return False, "Task cannot be empty or whitespace"
    
    return True, ""

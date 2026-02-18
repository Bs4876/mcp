"""
Path utilities for safe path manipulation and validation.
"""

import os
from pathlib import Path
from typing import Optional


def abspath(p: str) -> str:
    """
    Convert a path to absolute path with expansion.
    
    Args:
        p: Path string (may include ~ or be relative)
        
    Returns:
        Absolute path as string
    """
    # Expand ~ and environment variables
    expanded = os.path.expanduser(os.path.expandvars(p))
    # Remove quotes if present
    if expanded.startswith('"') and expanded.endswith('"'):
        expanded = expanded[1:-1]
    # Remove trailing slashes (except for root)
    if expanded.endswith(os.sep) and len(expanded) > 1:
        expanded = expanded.rstrip(os.sep)
    return os.path.abspath(expanded)


def is_directory(path: str) -> bool:
    """
    Check if path is a directory and is readable.
    
    Args:
        path: Path to check
        
    Returns:
        True if path exists and is a directory
    """
    try:
        return os.path.isdir(path) and os.access(path, os.R_OK)
    except (OSError, PermissionError):
        return False


def is_dir_empty(path: str) -> bool:
    """
    Check if a directory is empty.
    
    Args:
        path: Directory path
        
    Returns:
        True if directory is empty or doesn't exist
    """
    try:
        return len(os.listdir(path)) == 0
    except (OSError, FileNotFoundError):
        return True


def is_git_repo(repo_dir_abs: str) -> bool:
    """
    Check if a directory is a git repository.
    
    Args:
        repo_dir_abs: Absolute repository directory path
        
    Returns:
        True if .git directory exists
    """
    git_dir = os.path.join(repo_dir_abs, ".git")
    return os.path.isdir(git_dir)


def path_exists(path: str) -> bool:
    """
    Check if a path exists.
    
    Args:
        path: Path to check
        
    Returns:
        True if path exists
    """
    return os.path.exists(path)

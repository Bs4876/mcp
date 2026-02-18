"""
Command execution result model for subprocess operations.
Encapsulates the outcome of running system commands.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CmdResult:
    """Result of a command execution via subprocess."""
    
    ok: bool
    """Whether the command executed successfully (exit code 0)."""
    
    cmd: str
    """The command that was executed."""
    
    cwd: Optional[str]
    """The working directory where the command ran."""
    
    code: Optional[int]
    """Exit code from the command (None if timed out)."""
    
    elapsed_sec: float
    """Elapsed time in seconds for command execution."""
    
    stdout: str
    """Standard output (may be truncated)."""
    
    stderr: str
    """Standard error output (may be truncated)."""
    
    stdout_truncated: bool
    """Flag indicating if stdout was truncated."""
    
    stderr_truncated: bool
    """Flag indicating if stderr was truncated."""
    
    error: Optional[str] = None
    """Error message if command failed (e.g., timeout error)."""

"""
Result and Error models for MCP tool responses.
Provides structured response format for all MCP tools.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class ErrorInfo(BaseModel):
    """Structured error information for tool failures."""
    
    code: str
    """Error identifier (e.g., 'software_not_found', 'invalid_input')."""
    
    message: str
    """Human-readable error message."""
    
    hint: Optional[str] = None
    """Recovery guidance or suggestion to fix the error."""
    
    details: Dict[str, Any] = {}
    """Additional technical details about the error."""


class ToolResult(BaseModel):
    """Unified response format for all MCP tools."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ok": True,
                "data": {"software": "python", "version": "3.11.0"},
                "error": None
            }
        }
    )
    
    ok: bool
    """Success indicator - True if operation succeeded, False if failed."""
    
    data: Dict[str, Any] = {}
    """Result payload on success. Contains operation-specific data."""
    
    error: Optional[ErrorInfo] = None
    """Error information on failure. None if operation succeeded."""

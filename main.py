#!/usr/bin/env python3
"""
MCP (Management of Computer Programs) - Software Management Server
A Model Context Protocol server for AI agents to manage software on a computer.
"""

import asyncio
from typing import Any

from mcp.server.fastmcp import FastMCP

from models import (
    ToolResult,
    InstallSoftwareIn,
    UninstallSoftwareIn,
    UpdateSoftwareIn,
    GetRecommendationsIn,
    SetAutoUpdateIn,
    GetSoftwareInfoIn,
)
from services import SoftwareService

# Initialize MCP server
mcp = FastMCP("software-management-mcp")

# Initialize service
software_service = SoftwareService()


@mcp.tool()
async def install_software(software_name: str) -> dict[str, Any]:
    """
    Install a software application.
    
    Args:
        software_name: Name of the software to install
        
    Returns:
        Installation result with status and version information
        
    Error Codes:
        - software_not_found: Software not found in database
        - already_installed: Software is already installed
        - invalid_input: Input validation failed
        - registry_error: Error saving software registry
    """
    # Validate input
    try:
        data = InstallSoftwareIn(software_name=software_name)
    except ValueError as e:
        return ToolResult(
            ok=False,
            error={"code": "invalid_input", "message": str(e)}
        ).model_dump()
    
    # Execute in sync context
    result = await asyncio.to_thread(
        software_service.install_software,
        data.software_name
    )
    
    return result.model_dump()


@mcp.tool()
async def uninstall_software(software_name: str) -> dict[str, Any]:
    """
    Uninstall a software application.
    
    Args:
        software_name: Name of the software to uninstall
        
    Returns:
        Uninstallation result with status
        
    Error Codes:
        - software_not_found: Software not found in database
        - not_installed: Software is not installed
        - invalid_input: Input validation failed
        - registry_error: Error saving software registry
    """
    # Validate input
    try:
        data = UninstallSoftwareIn(software_name=software_name)
    except ValueError as e:
        return ToolResult(
            ok=False,
            error={"code": "invalid_input", "message": str(e)}
        ).model_dump()
    
    # Execute in sync context
    result = await asyncio.to_thread(
        software_service.uninstall_software,
        data.software_name
    )
    
    return result.model_dump()


@mcp.tool()
async def list_installed_software() -> dict[str, Any]:
    """
    List all installed software with versions.
    
    Returns:
        List of installed software and count
        
    Response contains:
        - installed_software: Array of {name, version, description}
        - count: Total number of installed software
    """
    result = await asyncio.to_thread(software_service.list_installed_software)
    return result.model_dump()


@mcp.tool()
async def check_updates() -> dict[str, Any]:
    """
    Check for available updates to installed software.
    
    Returns:
        List of software with available updates
        
    Response contains:
        - available_updates: Array of {name, current_version, latest_version}
        - count: Total number of updateable software
    """
    result = await asyncio.to_thread(software_service.check_updates)
    return result.model_dump()


@mcp.tool()
async def update_software(software_name: str) -> dict[str, Any]:
    """
    Update a software application to the latest version.
    
    Args:
        software_name: Name of the software to update
        
    Returns:
        Update result with old and new versions
        
    Error Codes:
        - software_not_found: Software not found in database
        - not_installed: Software is not installed
        - up_to_date: Software is already at latest version
        - invalid_input: Input validation failed
        - registry_error: Error saving software registry
    """
    # Validate input
    try:
        data = UpdateSoftwareIn(software_name=software_name)
    except ValueError as e:
        return ToolResult(
            ok=False,
            error={"code": "invalid_input", "message": str(e)}
        ).model_dump()
    
    # Execute in sync context
    result = await asyncio.to_thread(
        software_service.update_software,
        data.software_name
    )
    
    return result.model_dump()


@mcp.tool()
async def get_recommendations(task: str) -> dict[str, Any]:
    """
    Get software recommendations for a specific task.
    
    Args:
        task: Task or goal name (e.g., 'web development', 'data science', 'database')
        
    Returns:
        Recommended software for the task with details
        
    Supported Tasks:
        - web development: Python, Node.js, VS Code, Git
        - data science: Python, Node.js, Git
        - database: MySQL, PostgreSQL, Git
        - containerization: Docker, Git
        - java development: Java, VS Code, Git
        - full stack: Python, Node.js, MySQL, Docker, VS Code, Git
        
    Error Codes:
        - software_not_found: Task not found in recommendations database
        - invalid_input: Input validation failed
    """
    # Validate input
    try:
        data = GetRecommendationsIn(task=task)
    except ValueError as e:
        return ToolResult(
            ok=False,
            error={"code": "invalid_input", "message": str(e)}
        ).model_dump()
    
    # Execute in sync context
    result = await asyncio.to_thread(
        software_service.get_recommendations,
        data.task
    )
    
    return result.model_dump()


@mcp.tool()
async def set_auto_update(software_name: str, enabled: bool) -> dict[str, Any]:
    """
    Configure automatic updates for a software application.
    
    Args:
        software_name: Name of the software
        enabled: Whether to enable (true) or disable (false) auto-update
        
    Returns:
        Configuration result with new auto-update status
        
    Error Codes:
        - software_not_found: Software not found in database
        - not_installed: Software is not installed
        - invalid_input: Input validation failed
        - registry_error: Error saving software registry
    """
    # Validate input
    try:
        data = SetAutoUpdateIn(software_name=software_name, enabled=enabled)
    except ValueError as e:
        return ToolResult(
            ok=False,
            error={"code": "invalid_input", "message": str(e)}
        ).model_dump()
    
    # Execute in sync context
    result = await asyncio.to_thread(
        software_service.set_auto_update,
        data.software_name,
        data.enabled
    )
    
    return result.model_dump()


@mcp.tool()
async def get_software_info(software_name: str) -> dict[str, Any]:
    """
    Get detailed information about a software application.
    
    Args:
        software_name: Name of the software
        
    Returns:
        Detailed software information including versions and status
        
    Response contains:
        - name: Software name
        - description: Software description
        - latest_version: Latest available version
        - current_version: Currently installed version (null if not installed)
        - installed: Whether software is installed
        - auto_update: Whether auto-update is enabled
        
    Error Codes:
        - software_not_found: Software not found in database
        - invalid_input: Input validation failed
    """
    # Validate input
    try:
        data = GetSoftwareInfoIn(software_name=software_name)
    except ValueError as e:
        return ToolResult(
            ok=False,
            error={"code": "invalid_input", "message": str(e)}
        ).model_dump()
    
    # Execute in sync context
    result = await asyncio.to_thread(
        software_service.get_software_info,
        data.software_name
    )
    
    return result.model_dump()


if __name__ == "__main__":
    # Run the MCP server with HTTP support
    import uvicorn
    
    # Create a web app from the MCP server
    app = mcp.streamable_http_app()
    
    # Run the HTTP server on port 7777
    uvicorn.run(app, host="127.0.0.1", port=7777)

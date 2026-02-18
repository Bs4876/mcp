"""
Input validation models for software management operations.
Uses Pydantic for comprehensive input validation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class InstallSoftwareIn(BaseModel):
    """Input model for software installation."""
    
    software_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the software to install"
    )
    
    timeout_sec: Optional[int] = Field(
        default=30,
        ge=1,
        le=300,
        description="Command timeout in seconds (1-300)"
    )


class UninstallSoftwareIn(BaseModel):
    """Input model for software uninstallation."""
    
    software_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the software to uninstall"
    )
    
    timeout_sec: Optional[int] = Field(
        default=30,
        ge=1,
        le=300,
        description="Command timeout in seconds (1-300)"
    )


class UpdateSoftwareIn(BaseModel):
    """Input model for software update."""
    
    software_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the software to update"
    )
    
    timeout_sec: Optional[int] = Field(
        default=60,
        ge=1,
        le=300,
        description="Command timeout in seconds (1-300)"
    )


class GetRecommendationsIn(BaseModel):
    """Input model for getting software recommendations."""
    
    task: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Task or goal name (e.g., 'web development', 'data science')"
    )


class SetAutoUpdateIn(BaseModel):
    """Input model for configuring automatic updates."""
    
    software_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the software"
    )
    
    enabled: bool = Field(
        ...,
        description="Enable or disable auto-update"
    )


class GetSoftwareInfoIn(BaseModel):
    """Input model for getting software information."""
    
    software_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the software"
    )

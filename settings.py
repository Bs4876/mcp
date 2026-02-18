"""
Configuration settings for the software management MCP server.
Loads settings from environment variables and .env file.
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


def get_default_env_path() -> str:
    """Get the default path for .env file."""
    current_dir = Path(__file__).parent
    return str(current_dir / ".env")


def _get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Safely get environment variable with default."""
    return os.getenv(key, default)


def load_settings() -> None:
    """Load environment variables from .env file if it exists."""
    env_path = get_default_env_path()
    if os.path.exists(env_path):
        load_dotenv(env_path)


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""
    
    # API settings
    API_HOST: str = "localhost"
    API_PORT: int = 5000
    
    # Debug mode
    DEBUG: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    def __post_init__(self):
        """Validate settings after initialization."""
        pass


def build_settings() -> Settings:
    """Build settings from environment variables."""
    load_settings()
    
    return Settings(
        API_HOST=_get_env("API_HOST", "localhost"),
        API_PORT=int(_get_env("API_PORT", "5000")),
        DEBUG=_get_env("DEBUG", "false").lower() == "true",
        LOG_LEVEL=_get_env("LOG_LEVEL", "INFO"),
    )


# Global settings instance
settings = build_settings()

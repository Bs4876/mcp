"""Models package - Data validation and result structures."""

from .result import ToolResult, ErrorInfo
from .cmd_result import CmdResult
from .software_models import (
    InstallSoftwareIn,
    UninstallSoftwareIn,
    UpdateSoftwareIn,
    GetRecommendationsIn,
    SetAutoUpdateIn,
    GetSoftwareInfoIn,
)

__all__ = [
    "ToolResult",
    "ErrorInfo",
    "CmdResult",
    "InstallSoftwareIn",
    "UninstallSoftwareIn",
    "UpdateSoftwareIn",
    "GetRecommendationsIn",
    "SetAutoUpdateIn",
    "GetSoftwareInfoIn",
]

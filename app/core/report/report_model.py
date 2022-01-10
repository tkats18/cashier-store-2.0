from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class ReportType(Enum):
    Y_REPORT = ("Y_REPORT",)
    X_REPORT = ("X_REPORT",)


@dataclass
class ReportResponse:
    response: Dict[str, Any]

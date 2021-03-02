from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ProfanityReport:

    error_id: str
    line_number: int
    message: str
    file_path: Optional[Path] = field(default=None)

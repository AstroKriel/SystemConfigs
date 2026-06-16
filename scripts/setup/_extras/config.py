## { MODULE

from dataclasses import dataclass
from pathlib import Path

from local_helpers import project_dirs

SYSTEM_DIR = project_dirs.SOURCES.system
WORKAROUNDS_DIR = project_dirs.SOURCES.workarounds


@dataclass
class ExtraConfig:
    name: str
    source_path: Path
    target_path: Path
    required_platforms: tuple[str, ...] = ()
    requires_sudo: bool = False


## } MODULE

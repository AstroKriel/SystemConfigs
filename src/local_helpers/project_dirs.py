## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass
from pathlib import Path

##
## === PROJECT ROOT
##

## src/local_helpers/project_dirs.py -> parent.parent.parent is the repo root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

##
## === DIRS
##


@dataclass(frozen=True)
class ProjectDirs:
    """Well-known directories within the dotfiles project."""

    root: Path
    configs: Path
    editors: Path
    tools: Path
    extras: Path
    shell: Path
    rules: Path
    config_profiles: Path


DIRS = ProjectDirs(
    root=_PROJECT_ROOT,
    configs=_PROJECT_ROOT / "configs",
    editors=_PROJECT_ROOT / "configs" / "editors",
    tools=_PROJECT_ROOT / "configs" / "tools",
    extras=_PROJECT_ROOT / "configs" / "extras",
    shell=_PROJECT_ROOT / "configs" / "shell",
    rules=_PROJECT_ROOT / "configs" / "rules",
    config_profiles=_PROJECT_ROOT / "config-profiles",
)

## } MODULE

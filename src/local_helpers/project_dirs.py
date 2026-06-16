## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass
from pathlib import Path

##
## === PATH ANCHORS
##

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_HOME = Path.home()

##
## === RECORD KEEPING
##

LOG_FILE = _PROJECT_ROOT / "history.log"
SSH_RECORDS = _PROJECT_ROOT / "ssh_keys"

##
## === DIRECTORIES
##


@dataclass(frozen=True)
class SourceDirs:
    """Well-known directories within the dotfiles project."""

    root: Path
    shell: Path
    system: Path
    workarounds: Path
    editors: Path
    tools: Path
    rules: Path


SOURCES = SourceDirs(
    root=_PROJECT_ROOT,
    shell=_PROJECT_ROOT / "configs" / "shell",
    system=_PROJECT_ROOT / "configs" / "system",
    workarounds=_PROJECT_ROOT / "configs" / "workarounds",
    editors=_PROJECT_ROOT / "configs" / "editors",
    tools=_PROJECT_ROOT / "configs" / "tools",
    rules=_PROJECT_ROOT / "configs" / "rules",
)


@dataclass(frozen=True)
class TargetDirs:
    """Well-known user-side directories referenced by the dotfiles project."""

    home: Path
    config: Path
    rules: Path
    ssh: Path


TARGETS = TargetDirs(
    home=_HOME,
    config=_HOME / ".config",
    rules=_HOME / ".rules",
    ssh=_HOME / ".ssh",
)

## } MODULE

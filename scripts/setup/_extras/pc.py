## { MODULE

from pathlib import Path
from scripts.setup._extras.config import ExtraConfig, SYSTEM_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "pc/path-aliases.sh":
    ExtraConfig(
        name="pc path aliases",
        source_path=SYSTEM_DIR / "pc" / "path-aliases.sh",
        target_path=Path.home() / ".path_aliases",
    ),
    "pc/ssh-agent.sh":
    ExtraConfig(
        name="pc ssh agent",
        source_path=SYSTEM_DIR / "pc" / "ssh-agent.sh",
        target_path=Path.home() / ".shell_ssh_agent",
    ),
}

## } MODULE

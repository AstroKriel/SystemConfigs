## { MODULE

from pathlib import Path
from scripts.setup._extras.config import ExtraConfig, SYSTEM_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "pc/macos/disable-navigation-keys.dict":
    ExtraConfig(
        name="macOS disabled navigation keys",
        source_path=SYSTEM_DIR / "pc" / "macos" / "disable-navigation-keys.dict",
        target_path=Path.home() / "Library" / "KeyBindings" / "DefaultKeyBinding.dict",
        required_platforms=("macos", ),
    ),
}

## } MODULE

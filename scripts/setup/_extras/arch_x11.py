## { MODULE

from pathlib import Path
from scripts.setup._extras.config import ExtraConfig, SYSTEM_DIR, WORKAROUNDS_DIR

EXTRAS: dict[str, ExtraConfig] = {
    "pc/arch-x11/lightdm-locale.xprofile":
    ExtraConfig(
        name="LightDM xprofile locale",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "lightdm-locale.xprofile",
        target_path=Path.home() / ".xprofile",
        required_platforms=("linux", "x11", "lightdm"),
    ),
    "pc/arch-x11/mouse-workspace-buttons.xbindkeysrc":
    ExtraConfig(
        name="xbindkeys mouse buttons",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "mouse-workspace-buttons.xbindkeysrc",
        target_path=Path.home() / ".xbindkeysrc",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/touchpad-workspace-gestures.conf":
    ExtraConfig(
        name="libinput-gestures workspaces",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "touchpad-workspace-gestures.conf",
        target_path=Path.home() / ".config" / "libinput-gestures.conf",
        required_platforms=("linux", "x11", "xfce"),
    ),
    "pc/arch-x11/xfce-theme-toggle":
    ExtraConfig(
        name="XFCE theme toggle",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "xfce-theme-toggle",
        target_path=Path.home() / ".local" / "bin" / "xfce-theme-toggle",
        required_platforms=("linux", "x11", "xfce"),
    ),
    "pc/arch-x11/conky/conky.conf":
    ExtraConfig(
        name="conky config",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "conky" / "conky.conf",
        target_path=Path.home() / ".config" / "conky" / "conky.conf",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/conky/conky.desktop":
    ExtraConfig(
        name="conky autostart",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "conky" / "conky.desktop",
        target_path=Path.home() / ".config" / "autostart" / "conky.desktop",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/conky/conky-battery":
    ExtraConfig(
        name="conky battery script",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "conky" / "conky-battery",
        target_path=Path.home() / ".local" / "bin" / "conky-battery",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/conky/conky-gpu":
    ExtraConfig(
        name="conky GPU script",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "conky" / "conky-gpu",
        target_path=Path.home() / ".local" / "bin" / "conky-gpu",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/conky/conky-cpu-temp":
    ExtraConfig(
        name="conky CPU temp script",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "conky" / "conky-cpu-temp",
        target_path=Path.home() / ".local" / "bin" / "conky-cpu-temp",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/conky/conky-gpu-temp":
    ExtraConfig(
        name="conky GPU temp script",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "conky" / "conky-gpu-temp",
        target_path=Path.home() / ".local" / "bin" / "conky-gpu-temp",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/window-management/center-window":
    ExtraConfig(
        name="center-window script",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "window-management" / "center-window",
        target_path=Path.home() / ".local" / "bin" / "center-window",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/window-management/tile-window":
    ExtraConfig(
        name="tile-window script",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "window-management" / "tile-window",
        target_path=Path.home() / ".local" / "bin" / "tile-window",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/autorandr/postswitch":
    ExtraConfig(
        name="autorandr postswitch hook",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "autorandr" / "postswitch",
        target_path=Path.home() / ".config" / "autorandr" / "postswitch",
        required_platforms=("linux", "x11"),
    ),
    "pc/arch-x11/zathura/zathurarc":
    ExtraConfig(
        name="zathura config",
        source_path=SYSTEM_DIR / "pc" / "arch-x11" / "zathura" / "zathurarc",
        target_path=Path.home() / ".config" / "zathura" / "zathurarc",
        required_platforms=("linux", "x11"),
    ),
    "workarounds/arch-x11/no-ucm.conf":
    ExtraConfig(
        name="WirePlumber no-UCM workaround",
        source_path=WORKAROUNDS_DIR / "arch-x11" / "no-ucm.conf",
        target_path=Path("/etc") / "wireplumber" / "wireplumber.conf.d" / "no-ucm.conf",
        required_platforms=("linux", "x11"),
        requires_sudo=True,
    ),
    "workarounds/arch-x11/xfce-session.service":
    ExtraConfig(
        name="XFCE graphical-session target activation",
        source_path=WORKAROUNDS_DIR / "arch-x11" / "xfce-session.service",
        target_path=Path.home() / ".config" / "systemd" / "user" / "xfce-session.service",
        required_platforms=("linux", "x11", "xfce"),
    ),
}

## } MODULE

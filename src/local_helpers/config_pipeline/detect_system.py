## { MODULE

##
## === DEPENDENCIES
##

## stdlib
import os
import platform
import shutil
from collections.abc import Callable
from pathlib import Path

## local
from local_helpers.config_pipeline import capability_map
from local_helpers.config_pipeline import system_descriptor

##
## === DETECT
##


def detect_system(
    *,
    os_release_path: Path | None = None,
) -> system_descriptor.SystemDescriptor:
    """
    Probe the real host for its platform tag and present managers.

    The one impure pipeline stage (`overview.md` "Pipeline architecture",
    stage 2): every other stage is pure and takes a `SystemDescriptor` by
    injection instead. The actual OS-fact gathering (`platform.system()`,
    `/etc/os-release`, `$XDG_SESSION_TYPE`, `shutil.which`) is kept to this
    function and its direct calls; the decision logic each delegates to
    (`_detect_platform_tags`, `_detect_present_managers`) is pure and
    injectable, so it is unit-testable without a matching host.
    """
    platform_tags = _detect_platform_tags(
        system_name=platform.system(),
        os_release=_read_os_release(
            os_release_path=os_release_path if os_release_path is not None else Path("/etc/os-release"),
        ),
        session_type=os.environ.get("XDG_SESSION_TYPE"),
    )
    present_managers = _detect_present_managers(
        candidates=capability_map.candidate_managers(
            platform_tags=platform_tags,
        ),
        which_fn=shutil.which,
    )
    return system_descriptor.SystemDescriptor(
        platform_tags=platform_tags,
        present_managers=present_managers,
    )


def _detect_platform_tags(
    *,
    system_name: str,
    os_release: dict[str, str] | None,
    session_type: str | None,
) -> tuple[str, ...]:
    """
    Pure given the raw facts a real probe collects; unit-testable without a
    matching host.

    Only the two platforms this repo's `capability_map` currently has an
    opinion on (`"arch-x11"`, `"macos"`) are recognised; an unrecognised
    combination yields no tags, which resolves like any other unrecognised
    platform (`AVN-4`/`AVN-5` hard-stop on anything gated by `when.platform`).
    """
    if system_name == "Darwin":
        return ("macos",)
    if system_name == "Linux" and os_release is not None:
        if os_release.get("ID") == "arch" and session_type == "x11":
            return ("arch-x11",)
    return ()


def _detect_present_managers(
    *,
    candidates: tuple[str, ...],
    which_fn: Callable[[str], str | None],
) -> tuple[str, ...]:
    """A candidate manager is present iff its `capability_map.MANAGER_CHECK_COMMAND` resolves on `$PATH`."""
    return tuple(
        manager
        for manager in candidates
        if which_fn(capability_map.MANAGER_CHECK_COMMAND.get(manager, manager)) is not None
    )


def _read_os_release(
    *,
    os_release_path: Path,
) -> dict[str, str] | None:
    """A minimal `KEY=value` parser for `/etc/os-release`; `None` when the file is absent (non-Linux hosts)."""
    if not os_release_path.is_file():
        return None
    fields: dict[str, str] = {}
    for line in os_release_path.read_text().splitlines():
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        fields[key.strip()] = value.strip().strip('"')
    return fields


## } MODULE

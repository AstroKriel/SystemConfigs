## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from dataclasses import dataclass

##
## === TYPES
##


@dataclass(frozen=True)
class SystemDescriptor:
    """
    The detected fact a host presents to `resolve_config`: platform tags and
    present package managers (`ov#13`).

    `platform_tags` carries compound platform keys (`"arch-x11"`, `"macos"`,
    `"fedora"`), matched against `ConfigSpec` `when.platform` and looked up in
    `capability_map.PLATFORM_CANDIDATE_MANAGERS`; not the legacy profile's
    generic tag list (`"linux"`, `"x11"`, ...).

    Always hand-constructed in tests, never probed (`config_plan.md`
    "Isolation"). The impure host probe that builds one for real belongs to
    `detect_system.py`, not yet written.
    """

    platform_tags: tuple[str, ...]
    present_managers: tuple[str, ...]


## } MODULE

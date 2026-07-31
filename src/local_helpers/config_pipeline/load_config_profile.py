## { MODULE

##
## === DEPENDENCIES
##

## stdlib
import tomllib
from pathlib import Path
from typing import cast

## local
from local_helpers.config_pipeline import config_profile
from local_helpers.config_pipeline import errors

##
## === CONSTANTS
##

PROFILE_FIELDS = ("tools", "editors", "extras", "shell", "managers", "prefer_managers", "exclude_managers")

##
## === LOAD
##


def load_config_profile(
    *,
    profile_path: Path,
) -> config_profile.ConfigProfile:
    """
    Parse the pipeline-native profile shape (`ConfigProfile`): a flat TOML of
    string-array subscription and policy fields.

    Distinct from `local_helpers.load_profiles.load_profile`, which reads the
    legacy `SystemProfile` shape (`this-system.toml`: scalar `shell`, extras
    as file paths, no `managers`/`prefer_managers`/`exclude_managers`).
    `overview.md`'s closing note defers migrating the tracked
    `config-profiles/*.toml` files to this shape; this loader is for the new
    format wherever it lands until then.
    """
    try:
        raw_text = profile_path.read_text()
    except OSError as error:
        raise errors.ConfigProfileError(
            profile_path=profile_path,
            reason="file could not be read",
        ) from error
    try:
        raw_profile = tomllib.loads(raw_text)
    except tomllib.TOMLDecodeError as error:
        raise errors.ConfigProfileError(
            profile_path=profile_path,
            reason="file is not valid TOML",
        ) from error
    fields: dict[str, tuple[str, ...]] = {}
    for field in PROFILE_FIELDS:
        value = raw_profile.get(field, [])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in cast(list[object], value)):
            raise errors.ConfigProfileError(
                profile_path=profile_path,
                reason=f"`{field}` must be a list of strings",
            )
        fields[field] = tuple(cast(list[str], value))
    return config_profile.ConfigProfile(**fields)


## } MODULE

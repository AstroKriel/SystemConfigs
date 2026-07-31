## { MODULE

##
## === DEPENDENCIES
##

## stdlib
from typing import TypeAlias

##
## === TYPE ALIASES
##

ManagerKey: TypeAlias = str
PlatformKey: TypeAlias = str

##
## === CAPABILITY MAP
##

## `platform -> [managers]` candidate list (`ov#5` "Resolver precedence");
## detection (`SystemDescriptor.present_managers`) confirms which of these are
## actually present. One shared place, not duplicated per profile (`ov#16`).
PLATFORM_CANDIDATE_MANAGERS: dict[PlatformKey, tuple[ManagerKey, ...]] = {
    "arch-x11": ("pacman", "aur"),
    "macos": ("brew",),
    "fedora": ("dnf",),
}

## the resolver precedence ladder's last tie-break, when neither the
## config-spec order nor `prefer_managers` decides (`ov#5` step 5).
GLOBAL_DEFAULT_MANAGER_RANKING: tuple[ManagerKey, ...] = (
    "brew",
    "pacman",
    "dnf",
    "aur",
    "cargo",
)

## assumed present; never bootstrapped (`ov#14`, `MGR-4`).
BASE_MANAGERS: tuple[ManagerKey, ...] = ("pacman", "dnf", "apt")


def candidate_managers(
    *,
    platform_tags: tuple[PlatformKey, ...],
) -> tuple[ManagerKey, ...]:
    """
    The union of candidate managers over every platform tag a host carries,
    in first-seen order across `platform_tags`.

    A platform tag absent from `PLATFORM_CANDIDATE_MANAGERS` contributes no
    candidates; it is not an error here, since a host may carry tags this map
    has no opinion on.
    """
    candidates: list[ManagerKey] = []
    for tag in platform_tags:
        for manager in PLATFORM_CANDIDATE_MANAGERS.get(tag, ()):
            if manager not in candidates:
                candidates.append(manager)
    return tuple(candidates)


## } MODULE

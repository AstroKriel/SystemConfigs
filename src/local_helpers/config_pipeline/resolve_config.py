## { MODULE

##
## === DEPENDENCIES
##

## local
from local_helpers.config_pipeline import capability_map
from local_helpers.config_pipeline import config_profile
from local_helpers.config_pipeline import config_spec
from local_helpers.config_pipeline import system_descriptor as system_descriptor_module

##
## === AVENUE SELECTION, AVN
##


def _select_avenue(
    *,
    installs: tuple[config_spec.InstallAvenue, ...],
    descriptor: system_descriptor_module.SystemDescriptor,
    profile: config_profile.ConfigProfile,
) -> config_spec.InstallAvenue | None:
    """
    Choose the avenue to use, following the `ov#5` precedence ladder
    (`AVN-1`): capability, then the config-spec set (binding), then
    `prefer_managers`, then config-spec order, then the global default
    ranking.

    Returns `None` when no avenue survives platform (`AVN-4`) or
    `exclude_managers` (`AVN-2`) filtering; that is the `AVN-5` hard-stop
    cause. An avenue whose manager is merely absent (not excluded, not
    off-platform) is still returned: `MGR-1`/`MGR-2` decide whether that is
    a bootstrap or a hard-stop, so capability must never be the sole reason
    a subscribed concept loses every avenue (`AVN-6` "size one" would
    otherwise be unreachable whenever that one avenue's manager is absent,
    which is exactly the case `MGR-2`'s bootstrap example depends on).
    """
    on_platform = tuple(
        install for install in installs if _platform_allows(when=install.when, platform_tags=descriptor.platform_tags)
    )
    not_excluded = tuple(
        install
        for install in on_platform
        if install.when is None or install.when.manager is None or install.when.manager not in profile.exclude_managers
    )
    if not not_excluded:
        return None
    return _rank_avenues(
        installs=not_excluded,
        descriptor=descriptor,
        profile=profile,
    )[0]


def _rank_avenues(
    *,
    installs: tuple[config_spec.InstallAvenue, ...],
    descriptor: system_descriptor_module.SystemDescriptor,
    profile: config_profile.ConfigProfile,
) -> tuple[config_spec.InstallAvenue, ...]:
    """
    Order a non-empty, already platform- and exclude-filtered avenue set by
    the remaining three ladder steps.

    Capability (step 1) is a soft preference, not elimination, ranked in
    three tiers (`_capability_tier`): present or manager-less, then
    absent-but-subscribed (bootstrappable by `MGR-2`), then
    absent-and-unsubscribed (a dead end at `MGR-3`). Ranking by tier, rather
    than filtering down to the best tier first, means an avenue is never
    dropped outright; the top-ranked entry after sorting is `_select_avenue`'s
    choice, per its docstring. `prefer_managers` (step 3) reorders within a
    tier, inert when its target is absent (`AVN-3`). Config-spec order
    (step 4) is preserved as the stable sort's tie-break; the global default
    ranking (step 5) never actually distinguishes two entries once step 4 has
    run, since list order is already total, but is folded in for
    completeness with `ov#16`.
    """

    def sort_key(
        install: config_spec.InstallAvenue,
    ) -> tuple[int, int, int, int]:
        manager = install.when.manager if install.when is not None else None
        tier = _capability_tier(
            manager=manager,
            descriptor=descriptor,
            profile=profile,
        )
        preferred = manager is not None and manager in profile.prefer_managers
        prefer_rank = profile.prefer_managers.index(manager) if preferred and manager is not None else len(profile.prefer_managers)
        global_rank = (
            capability_map.GLOBAL_DEFAULT_MANAGER_RANKING.index(manager)
            if manager is not None and manager in capability_map.GLOBAL_DEFAULT_MANAGER_RANKING
            else len(capability_map.GLOBAL_DEFAULT_MANAGER_RANKING)
        )
        return (tier, 0 if preferred else 1, prefer_rank, global_rank)

    ## Python's sort is stable, so equal keys keep `installs`'s incoming
    ## order, which is config-spec order (step 4's tie-break).
    return tuple(sorted(installs, key=sort_key))


def _capability_tier(
    *,
    manager: str | None,
    descriptor: system_descriptor_module.SystemDescriptor,
    profile: config_profile.ConfigProfile,
) -> int:
    """
    Rank an avenue's manager by usability: present or manager-less (0),
    absent but subscribed for bootstrap (1, `MGR-2`), absent and
    unsubscribed (2, a dead end at `MGR-3`).

    Distinguishing tiers 1 and 2 is why capability is ranked per avenue
    rather than filtered to one present/absent split: with two absent-manager
    avenues, only one of them subscribed, picking the unsubscribed one would
    hard-stop even though the subscribed one would have resolved.
    """
    if manager is None or manager in descriptor.present_managers:
        return 0
    if manager in profile.managers:
        return 1
    return 2


def _platform_allows(
    *,
    when: config_spec.When | None,
    platform_tags: tuple[str, ...],
) -> bool:
    """A missing `when` or `when.platform` is universal; otherwise the tag must match (`AVN-4`)."""
    if when is None or when.platform is None:
        return True
    return when.platform in platform_tags


## } MODULE

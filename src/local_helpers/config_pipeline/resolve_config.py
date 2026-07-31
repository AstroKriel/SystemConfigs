## { MODULE

##
## === DEPENDENCIES
##

## local
from local_helpers.config_pipeline import capability_map
from local_helpers.config_pipeline import config_plan
from local_helpers.config_pipeline import config_profile
from local_helpers.config_pipeline import config_registry
from local_helpers.config_pipeline import config_spec
from local_helpers.config_pipeline import errors
from local_helpers.config_pipeline import system_descriptor as system_descriptor_module

##
## === RESOLVE
##


def resolve_config(
    *,
    filtered_registry: config_registry.FilteredConfigRegistry,
    descriptor: system_descriptor_module.SystemDescriptor,
    profile: config_profile.ConfigProfile,
) -> config_plan.ConfigPlan:
    """
    Turn a filtered config registry into an ordered, host-resolved
    `config_plan`, or raise an aggregated `ResolutionError` (`PLN-6`): every
    hard-stop cause is collected and reported together, never a partial
    plan. Pure (`PLN-5`): no host access; `descriptor` is always injected.
    """
    chosen, manager_deps, causes = _resolve_avenues(
        filtered_registry=filtered_registry,
        descriptor=descriptor,
        profile=profile,
    )
    concept_needs = _build_concept_needs(
        filtered_registry=filtered_registry,
        chosen=chosen,
        manager_deps=manager_deps,
    )
    order, cycle_cause = _topological_order(
        concept_needs=concept_needs,
    )
    if cycle_cause is not None:
        causes.append(cycle_cause)
    if causes:
        raise errors.ResolutionError(
            causes=tuple(sorted(causes)),
        )
    steps = _emit_steps(
        order=order,
        filtered_registry=filtered_registry,
        chosen=chosen,
        descriptor=descriptor,
    )
    return config_plan.ConfigPlan(
        steps=steps,
    )


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
    Rank an avenue's manager by usability: present, manager-less, or a base
    manager (0, `MGR-4`: `pacman`/`dnf`/`apt` are assumed present, never
    bootstrapped), absent but subscribed for bootstrap (1, `MGR-2`), absent
    and unsubscribed (2, a dead end at `MGR-3`).

    Distinguishing tiers 1 and 2 is why capability is ranked per avenue
    rather than filtered to one present/absent split: with two absent-manager
    avenues, only one of them subscribed, picking the unsubscribed one would
    hard-stop even though the subscribed one would have resolved.
    """
    if manager is None or manager in descriptor.present_managers or manager in capability_map.BASE_MANAGERS:
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


def _no_avenue_cause(
    *,
    key: config_registry.ConceptKey,
    installs: tuple[config_spec.InstallAvenue, ...],
) -> str:
    """
    Format the `AVN-5` hard-stop cause for a concept with no surviving
    avenue.

    Platform mismatch is the only case the spec's own examples give a
    wording for (`PLN-6`'s `zathura` example): list the platforms its
    avenues would have resolved on. Any other reason (every avenue's manager
    excluded) has no worked wording to match, so it falls back to a generic
    reason.
    """
    platforms = sorted(
        {install.when.platform for install in installs if install.when is not None and install.when.platform is not None}
    )
    if platforms:
        return f"{key}: only available on [{', '.join(platforms)}]"
    return f"{key}: no available install avenue"


##
## === DEPENDENCY AND MANAGER RESOLUTION, DEP AND MGR
##


def _resolve_avenues(
    *,
    filtered_registry: config_registry.FilteredConfigRegistry,
    descriptor: system_descriptor_module.SystemDescriptor,
    profile: config_profile.ConfigProfile,
) -> tuple[
    dict[config_registry.ConceptKey, config_spec.InstallAvenue],
    dict[config_registry.ConceptKey, set[config_registry.ConceptKey]],
    list[str],
]:
    """
    Choose an avenue for every filtered concept (`AVN`) and derive the
    implicit manager-bootstrap dependency edges (`MGR-2`).

    A concept that fails avenue selection (`AVN-5`) or needs an absent,
    unsubscribed manager (`MGR-3`) contributes a cause and is left out of
    the returned avenue map; a dependent naming it in `needs` simply drops
    that edge (`_build_concept_needs`) rather than raising a second,
    cascading cause. `config_plan.md` has no worked example for cascading
    failure, so this is the documented, conservative reading.
    """
    chosen: dict[config_registry.ConceptKey, config_spec.InstallAvenue] = {}
    manager_deps: dict[config_registry.ConceptKey, set[config_registry.ConceptKey]] = {}
    causes: list[str] = []
    for key in filtered_registry.keys():
        spec = filtered_registry[key]
        avenue = _select_avenue(
            installs=spec.installs,
            descriptor=descriptor,
            profile=profile,
        )
        if avenue is None:
            causes.append(
                _no_avenue_cause(
                    key=key,
                    installs=spec.installs,
                )
            )
            continue
        manager = avenue.when.manager if avenue.when is not None else None
        if manager is not None:
            tier = _capability_tier(
                manager=manager,
                descriptor=descriptor,
                profile=profile,
            )
            if tier == 2:
                causes.append(f"{key}: needs {manager}; absent and not subscribed")
                continue
            if tier == 1:
                manager_deps[key] = {manager}
        chosen[key] = avenue
    return chosen, manager_deps, causes


def _build_concept_needs(
    *,
    filtered_registry: config_registry.FilteredConfigRegistry,
    chosen: dict[config_registry.ConceptKey, config_spec.InstallAvenue],
    manager_deps: dict[config_registry.ConceptKey, set[config_registry.ConceptKey]],
) -> dict[config_registry.ConceptKey, set[config_registry.ConceptKey]]:
    """
    Concept-only `needs` edges (`DEP-1`, `DEP-3`) plus the implicit manager
    edges (`MGR-2`, `MGR-5`), restricted to concepts that resolved an
    avenue; an edge naming a concept that failed resolution is dropped, not
    treated as a cycle (see `_resolve_avenues`).
    """
    graph: dict[config_registry.ConceptKey, set[config_registry.ConceptKey]] = {}
    for key in chosen:
        spec = filtered_registry[key]
        needs = {need for need in spec.needs if need in chosen}
        needs |= manager_deps.get(key, set())
        graph[key] = needs
    return graph


def _topological_order(
    *,
    concept_needs: dict[config_registry.ConceptKey, set[config_registry.ConceptKey]],
) -> tuple[tuple[config_registry.ConceptKey, ...], str | None]:
    """
    Kahn's algorithm, deterministic via an alphabetical tie-break among
    concepts with no remaining unresolved need (`DEP-1`, `PLN-4`). Whatever
    is left once nothing is ready is a dependency cycle (`DEP-4`).
    """
    remaining = {key: set(needs) for key, needs in concept_needs.items()}
    order: list[config_registry.ConceptKey] = []
    while remaining:
        ready = sorted(key for key, needs in remaining.items() if not needs)
        if not ready:
            cycle_members = ", ".join(sorted(remaining))
            return tuple(order), f"dependency cycle among: {cycle_members}"
        for key in ready:
            del remaining[key]
        order.extend(ready)
        for needs in remaining.values():
            needs.difference_update(ready)
    return tuple(order), None


##
## === STEP EMISSION, GRP AND PLN
##


def _emit_steps(
    *,
    order: tuple[config_registry.ConceptKey, ...],
    filtered_registry: config_registry.FilteredConfigRegistry,
    chosen: dict[config_registry.ConceptKey, config_spec.InstallAvenue],
    descriptor: system_descriptor_module.SystemDescriptor,
) -> tuple[config_plan.Step, ...]:
    """
    Emit steps in topological order (`PLN-3`); within one concept, install
    then link or copy (`PLN-2`; `render`/`post-hook` have no schema support
    yet, see `config_plan.STEP_ACTIONS`). A `kind = "config-only"` avenue
    emits no install step (`overview.md` "Availability"). Bare-package
    `needs` (`DEP-2`) install ahead of the first concept that needs them,
    deduplicated globally so a package shared by two concepts installs only
    once.

    Choice-group teardown (`GRP-2`) is appended after every concept's steps,
    not interleaved per group: `FilteredConfigRegistry.teardown` carries no
    group or "kept member" association to interleave against, so "after the
    kept member" is read as "after everything," which matches every given
    example (each has exactly one group) without over-claiming a precision
    the data cannot back.
    """
    steps: list[config_plan.Step] = []
    installed_packages: set[str] = set()
    for key in order:
        spec = filtered_registry[key]
        bare_packages = sorted(need for need in spec.needs if need not in filtered_registry)
        for pkg in bare_packages:
            if pkg not in installed_packages:
                steps.append(
                    config_plan.Step(
                        action="install",
                        concept=None,
                        pkg=pkg,
                    )
                )
                installed_packages.add(pkg)
        avenue = chosen[key]
        if avenue.kind != "config-only":
            steps.append(
                config_plan.Step(
                    action="install",
                    concept=key,
                    pkg=None,
                )
            )
        for link in spec.links:
            if _platform_allows(
                when=link.when,
                platform_tags=descriptor.platform_tags,
            ):
                steps.append(
                    config_plan.Step(
                        action=link.mode,
                        concept=key,
                        pkg=None,
                    )
                )
    for key in filtered_registry.teardown:
        steps.append(
            config_plan.Step(
                action="teardown",
                concept=key,
                pkg=None,
            )
        )
    return tuple(steps)


## } MODULE

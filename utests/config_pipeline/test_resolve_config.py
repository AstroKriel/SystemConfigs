## { U-TEST

##
## === DEPENDENCIES
##

## stdlib
import tempfile
import unittest
from pathlib import Path

## local
from local_helpers.config_pipeline import config_plan
from local_helpers.config_pipeline import config_profile
from local_helpers.config_pipeline import config_registry
from local_helpers.config_pipeline import config_spec
from local_helpers.config_pipeline import errors
from local_helpers.config_pipeline import filter_config
from local_helpers.config_pipeline import resolve_config
from local_helpers.config_pipeline import system_descriptor

##
## === HELPERS
##


def _install(
    *,
    manager: str | None = None,
    platform: str | None = None,
    pkg: str | None = "pkg",
    kind: str | None = None,
) -> config_spec.InstallAvenue:
    when = None if manager is None and platform is None else config_spec.When(platform=platform, manager=manager)
    return config_spec.InstallAvenue(when=when, kind=kind, pkg=pkg)


def config_plan_step(
    *,
    action: str,
    concept: str | None = None,
    pkg: str | None = None,
) -> config_plan.Step:
    return config_plan.Step(action=action, concept=concept, pkg=pkg)


def _make_filtered_registry(
    *,
    test_case: unittest.TestCase,
    specs: dict[str, str],
    profile: config_profile.ConfigProfile,
) -> config_registry.FilteredConfigRegistry:
    """Parse each `{key: toml_body}`, then filter through the real `filter_config` pipeline."""
    temporary_dir = tempfile.TemporaryDirectory()
    test_case.addCleanup(temporary_dir.cleanup)
    root = Path(temporary_dir.name)
    entries: list[tuple[str, config_spec.ConfigSpec]] = []
    for key, body in sorted(specs.items()):
        concept_dir = root / key
        concept_dir.mkdir()
        (concept_dir / config_spec.SPEC_FILENAME).write_text(body)
        entries.append(
            (
                key,
                config_spec.load_config_spec(
                    concept_dir=concept_dir,
                ),
            )
        )
    full_registry = config_registry.FullConfigRegistry(
        entries=tuple(entries),
    )
    return filter_config.filter_config_registry(
        full_registry=full_registry,
        profile=profile,
    )


##
## === TEST SUITE
##


class TestResolveConfig_AvenueSelection(unittest.TestCase):

    def test_avn1_capability_and_prefer_managers(
        self,
    ):
        ## the `fd` worked example in `overview.md` and `config_plan.md` AVN-1.
        installs = (
            _install(manager="brew", pkg="fd"),
            _install(manager="pacman", pkg="fd"),
            _install(manager="cargo", pkg="fd-find"),
        )
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=(),
            present_managers=("pacman", "cargo"),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(prefer_managers=("cargo",)),
        )
        self.assertIsNotNone(chosen)
        assert chosen is not None
        self.assertEqual(chosen.pkg, "fd-find")

    def test_avn1_without_prefer_managers_config_spec_order_wins(
        self,
    ):
        installs = (
            _install(manager="brew", pkg="fd"),
            _install(manager="pacman", pkg="fd"),
            _install(manager="cargo", pkg="fd-find"),
        )
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=(),
            present_managers=("pacman", "cargo"),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(),
        )
        assert chosen is not None
        self.assertEqual(chosen.pkg, "fd")
        self.assertEqual(chosen.when.manager if chosen.when else None, "pacman")

    def test_sole_absent_manager_avenue_still_selected(
        self,
    ):
        ## precondition for `MGR-2`'s bootstrap example: a hard-stop here
        ## would make that scenario unreachable.
        installs = (_install(manager="brew", pkg="tmux"),)
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=("macos",),
            present_managers=(),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(),
        )
        assert chosen is not None
        self.assertEqual(chosen.pkg, "tmux")

    def test_absent_subscribed_manager_beats_absent_unsubscribed(
        self,
    ):
        ## both `aur` and `brew` are absent; only `brew` is subscribed for
        ## bootstrap, so it must win even though `aur` ranks first in the
        ## config spec's own avenue order.
        installs = (
            _install(manager="aur", pkg="tmux"),
            _install(manager="brew", pkg="tmux"),
        )
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=(),
            present_managers=(),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(managers=("brew",)),
        )
        assert chosen is not None
        self.assertEqual(chosen.when.manager if chosen.when else None, "brew")

    def test_avn2_exclude_managers_removes_avenue(
        self,
    ):
        installs = (
            _install(manager="pacman", pkg="foo"),
            _install(manager="aur", pkg="foo"),
        )
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=(),
            present_managers=("pacman", "aur"),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(exclude_managers=("pacman",)),
        )
        assert chosen is not None
        self.assertEqual(chosen.when.manager if chosen.when else None, "aur")

    def test_avn3_prefer_managers_inert_when_target_absent(
        self,
    ):
        ## `ov#13` worked pair, case B: `prefer_managers` names an absent
        ## manager; detection alone decides.
        installs = (_install(manager="pacman", pkg="foo"),)
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=(),
            present_managers=("pacman",),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(prefer_managers=("aur",)),
        )
        assert chosen is not None
        self.assertEqual(chosen.when.manager if chosen.when else None, "pacman")

    def test_avn4_platform_mismatch_excludes_avenue(
        self,
    ):
        installs = (_install(platform="macos", kind="config-only", pkg=None),)
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=("linux",),
            present_managers=(),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(),
        )
        self.assertIsNone(chosen)

    def test_avn5_no_surviving_avenue_is_none(
        self,
    ):
        installs = (
            _install(platform="macos", kind="config-only", pkg=None),
            _install(manager="pacman", pkg="foo"),
        )
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=("linux",),
            present_managers=(),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            profile=config_profile.ConfigProfile(exclude_managers=("pacman",)),
        )
        self.assertIsNone(chosen)

    def test_avn6_single_avenue_is_non_negotiable(
        self,
    ):
        installs = (_install(manager="aur", pkg="bar"),)
        descriptor = system_descriptor.SystemDescriptor(
            platform_tags=(),
            present_managers=(),
        )
        chosen = resolve_config._select_avenue(
            installs=installs,
            descriptor=descriptor,
            ## `prefer_managers`/`exclude_managers` naming an unrelated
            ## manager cannot matter when the set has size one.
            profile=config_profile.ConfigProfile(prefer_managers=("brew",), exclude_managers=("brew",)),
        )
        assert chosen is not None
        self.assertEqual(chosen.pkg, "bar")


##
## === FIXTURES
##

## `DEP-1`, `DEP-2`: a bare-package `needs` (`lua`, no such concept key).
CONKY_NEEDS_LUA = """
name = "Conky"
needs = ["lua"]
[[install]]
when = { manager = "pacman" }
pkg  = "conky"
[[link]]
source = "conky.conf"
dir    = "~/.config/conky"
name   = "conky.conf"
mode   = "link"
"""

## `MGR-2`/`MGR-3`: `tmux`'s only avenue needs `brew`.
TMUX_BREW_ONLY = """
name = "Tmux"
[[install]]
when = { manager = "brew" }
pkg  = "tmux"
[[link]]
source = "tmux.conf"
dir    = "~/.config/tmux"
name   = "tmux.conf"
mode   = "link"
"""

## a manager is itself a concept, bootstrapped via `kind = "script"` (`ov#14`).
BREW = """
name = "Homebrew"
[check]
command = "brew"
[[install]]
when = { platform = "macos" }
kind = "script"
"""

SHELL_BASH = """
name = "Bash"
group = "shell"
[[install]]
when = { manager = "pacman" }
pkg  = "bash"
"""

SHELL_ZSH = """
name = "Zsh"
group = "shell"
[[install]]
when = { manager = "pacman" }
pkg  = "zsh"
[[link]]
source = "zshrc"
dir    = "~"
name   = ".zshrc"
mode   = "link"
"""

## `PLN-6`: macOS-only avenue, subscribed on linux.
ZATHURA_MACOS_ONLY = """
name = "Zathura"
[[install]]
when = { platform = "macos" }
pkg  = "zathura"
"""

## `PLN-6`: only avenue needs an absent, unsubscribed manager.
QUX_NEEDS_NIX = """
name = "Qux"
[[install]]
when = { manager = "nix" }
pkg  = "qux"
"""


##
## === TEST SUITE
##


class TestResolveConfig_Dependencies(unittest.TestCase):

    def test_dep1_dep2_bare_package_installs_before_dependent(
        self,
    ):
        filtered = _make_filtered_registry(
            test_case=self,
            specs={"conky": CONKY_NEEDS_LUA},
            profile=config_profile.ConfigProfile(extras=("conky",)),
        )
        plan = resolve_config.resolve_config(
            filtered_registry=filtered,
            descriptor=system_descriptor.SystemDescriptor(platform_tags=(), present_managers=("pacman",)),
            profile=config_profile.ConfigProfile(extras=("conky",)),
        )
        self.assertEqual(
            plan.steps,
            (
                config_plan_step(action="install", pkg="lua"),
                config_plan_step(action="install", concept="conky"),
                config_plan_step(action="link", concept="conky"),
            ),
        )


class TestResolveConfig_ManagerBootstrap(unittest.TestCase):

    def test_mgr2_bootstrap_inserted_when_subscribed(
        self,
    ):
        ## fresh macOS; `tmux` is brew-only; `brew` absent but subscribed
        ## (`ov#14`'s worked example): `[bootstrap brew, install tmux, link
        ## tmux]`. "bootstrap" materialises as `brew`'s own ordinary
        ## install step (`PLN-1` has no separate bootstrap kind).
        profile = config_profile.ConfigProfile(tools=("tmux",), managers=("brew",))
        filtered = _make_filtered_registry(
            test_case=self,
            specs={"tmux": TMUX_BREW_ONLY, "brew": BREW},
            profile=profile,
        )
        plan = resolve_config.resolve_config(
            filtered_registry=filtered,
            descriptor=system_descriptor.SystemDescriptor(platform_tags=("macos",), present_managers=()),
            profile=profile,
        )
        self.assertEqual(
            plan.steps,
            (
                config_plan_step(action="install", concept="brew"),
                config_plan_step(action="install", concept="tmux"),
                config_plan_step(action="link", concept="tmux"),
            ),
        )

    def test_mgr3_hard_stop_when_unsubscribed(
        self,
    ):
        profile = config_profile.ConfigProfile(tools=("tmux",))
        filtered = _make_filtered_registry(
            test_case=self,
            specs={"tmux": TMUX_BREW_ONLY},
            profile=profile,
        )
        with self.assertRaises(errors.ResolutionError) as context:
            resolve_config.resolve_config(
                filtered_registry=filtered,
                descriptor=system_descriptor.SystemDescriptor(platform_tags=("macos",), present_managers=()),
                profile=profile,
            )
        self.assertIn(
            "tmux: needs brew; absent and not subscribed",
            context.exception.causes,
        )


class TestResolveConfig_ChoiceGroupTeardown(unittest.TestCase):

    def test_grp2_teardown_step_after_kept_member(
        self,
    ):
        profile = config_profile.ConfigProfile(shell=("shell-zsh",))
        filtered = _make_filtered_registry(
            test_case=self,
            specs={"shell-bash": SHELL_BASH, "shell-zsh": SHELL_ZSH},
            profile=profile,
        )
        plan = resolve_config.resolve_config(
            filtered_registry=filtered,
            descriptor=system_descriptor.SystemDescriptor(platform_tags=(), present_managers=("pacman",)),
            profile=profile,
        )
        self.assertEqual(
            plan.steps,
            (
                config_plan_step(action="install", concept="shell-zsh"),
                config_plan_step(action="link", concept="shell-zsh"),
                config_plan_step(action="teardown", concept="shell-bash"),
            ),
        )


class TestResolveConfig_AggregatedErrors(unittest.TestCase):

    def test_pln6_aggregated_hard_stop_two_causes(
        self,
    ):
        profile = config_profile.ConfigProfile(extras=("zathura", "qux"))
        filtered = _make_filtered_registry(
            test_case=self,
            specs={"zathura": ZATHURA_MACOS_ONLY, "qux": QUX_NEEDS_NIX},
            profile=profile,
        )
        with self.assertRaises(errors.ResolutionError) as context:
            resolve_config.resolve_config(
                filtered_registry=filtered,
                descriptor=system_descriptor.SystemDescriptor(platform_tags=("linux",), present_managers=()),
                profile=profile,
            )
        ## `PLN-6`: both causes reported together, no partial plan.
        self.assertEqual(
            context.exception.causes,
            (
                "qux: needs nix; absent and not subscribed",
                "zathura: only available on [macos]",
            ),
        )


class TestResolveConfig_Properties(unittest.TestCase):

    def test_resolve_is_deterministic(
        self,
    ):
        profile = config_profile.ConfigProfile(extras=("conky",))
        filtered = _make_filtered_registry(
            test_case=self,
            specs={"conky": CONKY_NEEDS_LUA},
            profile=profile,
        )
        descriptor = system_descriptor.SystemDescriptor(platform_tags=(), present_managers=("pacman",))
        first = resolve_config.resolve_config(filtered_registry=filtered, descriptor=descriptor, profile=profile)
        second = resolve_config.resolve_config(filtered_registry=filtered, descriptor=descriptor, profile=profile)
        ## `PLN-4`/`PLN-5`: identical inputs yield an identical plan.
        self.assertEqual(first, second)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()

## } U-TEST

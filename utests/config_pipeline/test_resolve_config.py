## { U-TEST

##
## === DEPENDENCIES
##

## stdlib
import unittest

## local
from local_helpers.config_pipeline import config_profile
from local_helpers.config_pipeline import config_spec
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
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()

## } U-TEST

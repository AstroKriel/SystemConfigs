## { U-TEST

##
## === DEPENDENCIES
##

## stdlib
import unittest

## local
from local_helpers.config_pipeline import detect_system
from local_helpers.config_pipeline import system_descriptor

##
## === TEST SUITE
##


class TestDetectSystem_PlatformTags(unittest.TestCase):

    def test_darwin_is_macos(
        self,
    ):
        self.assertEqual(
            detect_system._detect_platform_tags(system_name="Darwin", os_release=None, session_type=None),
            ("macos",),
        )

    def test_arch_x11_recognised(
        self,
    ):
        self.assertEqual(
            detect_system._detect_platform_tags(
                system_name="Linux",
                os_release={"ID": "arch"},
                session_type="x11",
            ),
            ("arch-x11",),
        )

    def test_arch_wayland_not_recognised(
        self,
    ):
        ## only `arch-x11` is in `capability_map` today; a session type this
        ## map has no opinion on yields no tag, not a guess.
        self.assertEqual(
            detect_system._detect_platform_tags(
                system_name="Linux",
                os_release={"ID": "arch"},
                session_type="wayland",
            ),
            (),
        )

    def test_unknown_linux_distro_not_recognised(
        self,
    ):
        self.assertEqual(
            detect_system._detect_platform_tags(
                system_name="Linux",
                os_release={"ID": "ubuntu"},
                session_type="x11",
            ),
            (),
        )

    def test_no_os_release_on_linux_not_recognised(
        self,
    ):
        self.assertEqual(
            detect_system._detect_platform_tags(system_name="Linux", os_release=None, session_type="x11"),
            (),
        )


class TestDetectSystem_PresentManagers(unittest.TestCase):

    def test_present_candidates_kept_in_order(
        self,
    ):
        self.assertEqual(
            detect_system._detect_present_managers(
                candidates=("pacman", "aur", "cargo"),
                which_fn=lambda command: "/usr/bin/x" if command in {"pacman", "cargo"} else None,
            ),
            ("pacman", "cargo"),
        )

    def test_aur_checked_via_its_manager_check_command(
        self,
    ):
        ## `aur` has no binary of its own; `MANAGER_CHECK_COMMAND` maps it to
        ## `paru` (this repo's AUR helper), not the literal string `"aur"`.
        seen: list[str] = []

        def which_fn(
            command: str,
        ) -> str | None:
            seen.append(command)
            return "/usr/bin/paru" if command == "paru" else None

        result = detect_system._detect_present_managers(candidates=("aur",), which_fn=which_fn)
        self.assertEqual(result, ("aur",))
        self.assertEqual(seen, ["paru"])

    def test_no_candidates_yields_no_managers(
        self,
    ):
        self.assertEqual(
            detect_system._detect_present_managers(candidates=(), which_fn=lambda command: "/usr/bin/x"),
            (),
        )


class TestDetectSystem_Smoke(unittest.TestCase):

    def test_detect_system_runs_without_error(
        self,
    ):
        ## impure and host-dependent; only asserts it runs and returns the
        ## right shape, never a specific value (`config_plan.md` "Isolation").
        result = detect_system.detect_system()
        self.assertIsInstance(result, system_descriptor.SystemDescriptor)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()

## } U-TEST

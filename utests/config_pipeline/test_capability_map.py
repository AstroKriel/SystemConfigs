## { U-TEST

##
## === DEPENDENCIES
##

## stdlib
import unittest

## local
from local_helpers.config_pipeline import capability_map

##
## === TEST SUITE
##


class TestCapabilityMap_CandidateManagers(unittest.TestCase):

    def test_single_platform_returns_its_candidates(
        self,
    ):
        self.assertEqual(
            capability_map.candidate_managers(platform_tags=("arch-x11",)),
            ("pacman", "aur"),
        )

    def test_multiple_platforms_union_in_first_seen_order(
        self,
    ):
        self.assertEqual(
            capability_map.candidate_managers(platform_tags=("macos", "arch-x11")),
            ("brew", "pacman", "aur"),
        )

    def test_unknown_platform_contributes_nothing(
        self,
    ):
        self.assertEqual(
            capability_map.candidate_managers(platform_tags=("hpc",)),
            (),
        )

    def test_no_platform_tags_returns_empty(
        self,
    ):
        self.assertEqual(
            capability_map.candidate_managers(platform_tags=()),
            (),
        )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()

## } U-TEST

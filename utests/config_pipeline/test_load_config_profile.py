## { U-TEST

##
## === DEPENDENCIES
##

## stdlib
import tempfile
import unittest
from pathlib import Path

## local
from local_helpers.config_pipeline import errors
from local_helpers.config_pipeline import load_config_profile

##
## === HELPERS
##


def _write_profile(
    *,
    test_case: unittest.TestCase,
    body: str,
) -> Path:
    temporary_dir = tempfile.TemporaryDirectory()
    test_case.addCleanup(temporary_dir.cleanup)
    profile_path = Path(temporary_dir.name) / "profile.toml"
    profile_path.write_text(body)
    return profile_path


##
## === TEST SUITE
##


class TestLoadConfigProfile_Happy(unittest.TestCase):

    def test_full_profile_parses(
        self,
    ):
        profile_path = _write_profile(
            test_case=self,
            body="""
tools = ["tmux", "ghostty"]
managers = ["brew"]
prefer_managers = ["cargo"]
exclude_managers = ["dnf"]
""",
        )
        profile = load_config_profile.load_config_profile(profile_path=profile_path)
        self.assertEqual(profile.tools, ("tmux", "ghostty"))
        self.assertEqual(profile.managers, ("brew",))
        self.assertEqual(profile.prefer_managers, ("cargo",))
        self.assertEqual(profile.exclude_managers, ("dnf",))

    def test_missing_fields_default_empty(
        self,
    ):
        profile_path = _write_profile(
            test_case=self,
            body="tools = [\"tmux\"]\n",
        )
        profile = load_config_profile.load_config_profile(profile_path=profile_path)
        self.assertEqual(profile.editors, ())
        self.assertEqual(profile.managers, ())


class TestLoadConfigProfile_Errors(unittest.TestCase):

    def test_non_list_field_raises(
        self,
    ):
        profile_path = _write_profile(
            test_case=self,
            body='tools = "tmux"\n',
        )
        with self.assertRaises(errors.ConfigProfileError):
            load_config_profile.load_config_profile(profile_path=profile_path)

    def test_non_string_item_raises(
        self,
    ):
        profile_path = _write_profile(
            test_case=self,
            body="tools = [1, 2]\n",
        )
        with self.assertRaises(errors.ConfigProfileError):
            load_config_profile.load_config_profile(profile_path=profile_path)

    def test_invalid_toml_raises(
        self,
    ):
        profile_path = _write_profile(
            test_case=self,
            body="tools = [",
        )
        with self.assertRaises(errors.ConfigProfileError):
            load_config_profile.load_config_profile(profile_path=profile_path)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    unittest.main()

## } U-TEST

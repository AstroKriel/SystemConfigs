## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
from pathlib import Path

## local
from local_helpers import project_dirs
from local_helpers.config_pipeline import detect_system
from local_helpers.config_pipeline import discover_config
from local_helpers.config_pipeline import errors
from local_helpers.config_pipeline import filter_config
from local_helpers.config_pipeline import load_config_profile
from local_helpers.config_pipeline import resolve_config

##
## === SCRIPT CONFIG
##

## demo scope only: shell, editors, extras, and rules have no
## `_config_spec.toml` backfill yet (`overview.md` branch-scope note);
## widen once they do.
DEMO_GROUPS = ("tools",)

##
## === PROGRAM MAIN
##


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Resolve a pipeline-native profile (`ConfigProfile`, not the legacy `this-system.toml` shape) "
            "into a config_plan and print it. Dry-run only; implementation-order step 3 (`--plan`)."
        ),
    )
    parser.add_argument(
        "profile_path",
        type=Path,
        help="Path to a pipeline-native profile TOML, e.g. config-profiles/pipeline/arch-x11.toml",
    )
    args = parser.parse_args()
    profile_path = Path(args.profile_path)
    profile = load_config_profile.load_config_profile(
        profile_path=profile_path,
    )
    full_registry = discover_config.discover_full_config_registry(
        configs_root=project_dirs.SOURCES.root / "configs",
        groups=DEMO_GROUPS,
    )
    filtered_registry = filter_config.filter_config_registry(
        full_registry=full_registry,
        profile=profile,
    )
    descriptor = detect_system.detect_system()
    print(f"platform_tags: {descriptor.platform_tags}")
    print(f"present_managers: {descriptor.present_managers}")
    try:
        plan = resolve_config.resolve_config(
            filtered_registry=filtered_registry,
            descriptor=descriptor,
            profile=profile,
        )
    except errors.ResolutionError as error:
        print("ResolutionError:")
        for cause in error.causes:
            print(f"  - {cause}")
        raise SystemExit(1) from None
    print("config_plan:")
    for step in plan.steps:
        target = step.concept if step.concept is not None else step.pkg
        print(f"  - {step.action} {target}")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT

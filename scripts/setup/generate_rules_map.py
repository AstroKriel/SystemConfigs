## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
from pathlib import Path
from typing import cast

## local
from local_helpers import log_messages
from local_helpers import project_dirs

##
## === CONFIG
##

SCRIPT_NAME = Path(__file__).name
RULES_DIR = project_dirs.SOURCES.rules
TARGET_DIR = project_dirs.TARGETS.rules
MAP_FILE = TARGET_DIR / "map.md"

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)

_HEADER = """\
# Rules Map

Generated index of all rule files in `~/.rules/`. Read this to find relevant
conventions without traversing the directory tree. When applying a rule, state
which file it came from.

---

"""

##
## === CORE LOGIC
##


def _extract_entry(path: Path) -> tuple[str, str]:
    """Return (title, description) extracted from the opening of a rule file."""
    lines = path.read_text().splitlines()
    title = ""
    description_parts: list[str] = []
    past_title = False

    for line in lines:
        if not past_title:
            if line.startswith("# "):
                title = line[2:].strip()
                past_title = True
            continue
        if line.startswith("---") or line.startswith("## "):
            break
        if line.strip():
            description_parts.append(line.strip())

    return title, " ".join(description_parts)


def generate_map(*, dry_run: bool) -> None:
    """Write map.md to ~/.rules/ from all rule files in the source directory."""
    entries: list[str] = []

    for source_path in sorted(RULES_DIR.rglob("*.md")):
        relative = str(source_path.relative_to(RULES_DIR))
        if relative == "map.md":
            continue
        title, description = _extract_entry(source_path)
        heading = f"## `{relative}`" + (f" -- {title}" if title else "")
        entries.append(f"{heading}\n\n{description}\n")

    content = _HEADER + "\n".join(entries)

    if not dry_run:
        MAP_FILE.write_text(content)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message=f"Generated rules map: {MAP_FILE}",
            dry_run=dry_run,
        )
    )


##
## === PROGRAM MAIN
##


def run(*, dry_run: bool) -> None:
    log_messages.configure_logger(write_to_file=not dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Started generating rules map",
            dry_run=dry_run,
        )
    )
    generate_map(dry_run=dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished generating rules map",
            dry_run=dry_run,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate ~/.rules/map.md from all rule files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without applying them",
    )
    args = parser.parse_args()
    dry_run = cast(bool, args.dry_run)
    run(dry_run=dry_run)


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT

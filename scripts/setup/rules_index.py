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
INDEX_FILE = TARGET_DIR / "README.md"

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)


def _home_relative(path: Path) -> str:
    """Render a path as `~/...` when it lives under home, else absolute."""
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)


_ROOT_DISPLAY = _home_relative(project_dirs.SOURCES.root)
_RULES_SOURCE_DISPLAY = _home_relative(RULES_DIR)

_HEADER = f"""\
# Rules

Generated index of all rule files in `~/.rules/`. Read this to find relevant
conventions without traversing the directory tree. When applying a rule, state
which file it came from.

Files in `~/.rules/` are symlinks; the canonical source is `{_RULES_SOURCE_DISPLAY}/`. To add or modify a rule, edit the source and re-run the following from `{_ROOT_DISPLAY}/`:

```bash
uv run -m scripts.setup.rules_files
uv run -m scripts.setup.rules_index
```

---

"""

##
## === CORE LOGIC
##


def _extract_entry(
    path: Path,
) -> tuple[str, str]:
    """Return (title, description) extracted from the opening of a rule file."""
    lines = path.read_text().splitlines()
    title = ""
    description_parts: list[str] = []
    is_past_title = False
    for line in lines:
        if not is_past_title:
            if line.startswith("# "):
                title = line[2:].strip()
                is_past_title = True
            continue
        if line.startswith("---") or line.startswith("## "):
            break
        if line.strip():
            description_parts.append(line.strip())
    return title, " ".join(description_parts)


def generate_index(*, dry_run: bool) -> None:
    """Write README.md to ~/.rules/ from all rule files in the source directory."""
    ## collect entries from all non-README rule files
    entries: list[str] = []
    for source_path in sorted(RULES_DIR.rglob("*.md")):
        relative_path = str(source_path.relative_to(RULES_DIR))
        if Path(relative_path).name == "README.md":
            continue
        title, description = _extract_entry(source_path)
        heading = f"## [`{relative_path}`]({relative_path})" + (f": {title}" if title else "")
        entries.append(f"{heading}\n\n{description}\n")
    ## assemble and write index
    content = _HEADER + "\n".join(entries)
    if not dry_run:
        INDEX_FILE.write_text(content)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message=f"Generated rules index: {INDEX_FILE}",
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
            message="Started generating rules index",
            dry_run=dry_run,
        )
    )
    generate_index(dry_run=dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished generating rules index",
            dry_run=dry_run,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate ~/.rules/README.md from all rule files.",
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

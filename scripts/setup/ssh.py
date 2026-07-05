## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
from pathlib import Path
from typing import cast

## local
from local_helpers import apply_shell_actions
from local_helpers import load_profiles
from local_helpers import log_messages
from local_helpers import project_dirs

##
## === PATHS
##

SCRIPT_NAME = Path(__file__).name

LOG_MESSAGE = log_messages.make_logger_fn(SCRIPT_NAME)

SSH_SOURCE_DIR = project_dirs.SOURCES.system / "ssh"
HOSTS_SOURCE_DIR = SSH_SOURCE_DIR / "hosts"
CONFIG_HEAD_SOURCE = SSH_SOURCE_DIR / "config.head"
DEFAULTS_SOURCE = SSH_SOURCE_DIR / "defaults.conf"
RECORDS_SOURCE_DIR = SSH_SOURCE_DIR / "records"

SSH_TARGET_DIR = project_dirs.TARGETS.ssh
CONFIG_TARGET = SSH_TARGET_DIR / "config"
CONFIG_D_TARGET = SSH_TARGET_DIR / "config.d"
CTRL_TARGET = SSH_TARGET_DIR / "ctrl"
RECORDS_TARGET = SSH_TARGET_DIR / "records"
DEFAULTS_TARGET = CONFIG_D_TARGET / "zz-defaults.conf"

##
## === HOST SELECTION
##


def available_host_keys() -> tuple[str, ...]:
    """Return the host keys discoverable as `hosts/<key>.conf` fragments."""
    return tuple(sorted(path.stem for path in HOSTS_SOURCE_DIR.glob("*.conf")))


def get_selected_host_sources(
    *,
    host_keys: tuple[str, ...] | None,
) -> dict[str, Path]:
    """Return `{host_key: fragment_path}` for the selected hosts, or all when `None`."""
    available = {host_key: HOSTS_SOURCE_DIR / f"{host_key}.conf" for host_key in available_host_keys()}
    if host_keys is None:
        return available
    unknown_host_keys = sorted(set(host_keys) - set(available))
    if unknown_host_keys:
        raise KeyError(f"Unknown `--which` host(s): {', '.join(unknown_host_keys)}")
    return {host_key: available[host_key] for host_key in host_keys}


def resolve_selected_hosts(
    *,
    subscribed_host_keys: tuple[str, ...],
    requested_host_keys: tuple[str, ...],
    include_all: bool,
) -> tuple[str, ...]:
    """Resolve the hosts to act on from the profile subscription and CLI request."""
    if include_all:
        return subscribed_host_keys
    get_selected_host_sources(host_keys=requested_host_keys)
    unsubscribed_host_keys = sorted(set(requested_host_keys) - set(subscribed_host_keys))
    if unsubscribed_host_keys:
        raise KeyError(
            "Requested `--which` host(s) are not subscribed in `this-system.toml`: "
            f"{', '.join(unsubscribed_host_keys)}",
        )
    return requested_host_keys


##
## === LINK HELPERS
##


def _ensure_ssh_dirs(
    *,
    dry_run: bool,
) -> None:
    """Ensure the `~/.ssh` directory tree used by the managed config exists."""
    for directory in (SSH_TARGET_DIR, CONFIG_D_TARGET, CTRL_TARGET):
        apply_shell_actions.ensure_dir_exists(
            directory=directory,
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )


def setup_scaffold(
    *,
    dry_run: bool,
) -> None:
    """Link the profile-independent pieces: the config head, global defaults, and records store."""
    _ensure_ssh_dirs(dry_run=dry_run)
    apply_shell_actions.create_symlink(
        source_path=CONFIG_HEAD_SOURCE,
        target_path=CONFIG_TARGET,
        logger_fn=LOG_MESSAGE,
        dry_run=dry_run,
    )
    apply_shell_actions.create_symlink(
        source_path=DEFAULTS_SOURCE,
        target_path=DEFAULTS_TARGET,
        logger_fn=LOG_MESSAGE,
        dry_run=dry_run,
    )
    apply_shell_actions.create_symlink(
        source_path=RECORDS_SOURCE_DIR,
        target_path=RECORDS_TARGET,
        logger_fn=LOG_MESSAGE,
        dry_run=dry_run,
    )


def setup_host(
    *,
    host_key: str,
    source_path: Path,
    dry_run: bool,
) -> None:
    """Symlink one host fragment into `~/.ssh/config.d/`."""
    apply_shell_actions.create_symlink(
        source_path=source_path,
        target_path=CONFIG_D_TARGET / f"{host_key}.conf",
        logger_fn=LOG_MESSAGE,
        dry_run=dry_run,
    )


##
## === PROGRAM MAIN
##


def run(
    *,
    dry_run: bool,
    host_keys: tuple[str, ...] | None = None,
) -> None:
    """Set up the managed SSH config: scaffold, then one fragment per selected host."""
    log_messages.configure_logger(write_to_file=not dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Started setting up SSH config",
            dry_run=dry_run,
        ),
    )
    setup_scaffold(dry_run=dry_run)
    selected_host_sources = get_selected_host_sources(host_keys=host_keys)
    for host_key, source_path in selected_host_sources.items():
        setup_host(
            host_key=host_key,
            source_path=source_path,
            dry_run=dry_run,
        )
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished setting up SSH config",
            dry_run=dry_run,
        ),
    )


def remove_symlinks(
    *,
    dry_run: bool,
    host_keys: tuple[str, ...] | None = None,
    remove_scaffold: bool = False,
) -> None:
    """Remove host-fragment symlinks; also tear down the scaffold when `remove_scaffold`."""
    log_messages.configure_logger(write_to_file=not dry_run)
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Started removing SSH config symlinks",
            dry_run=dry_run,
        ),
    )
    selected_host_sources = get_selected_host_sources(host_keys=host_keys)
    for host_key in selected_host_sources:
        apply_shell_actions.remove_symlink(
            target_path=CONFIG_D_TARGET / f"{host_key}.conf",
            logger_fn=LOG_MESSAGE,
            dry_run=dry_run,
        )
    if remove_scaffold:
        for target_path in (CONFIG_TARGET, DEFAULTS_TARGET, RECORDS_TARGET):
            apply_shell_actions.remove_symlink(
                target_path=target_path,
                logger_fn=LOG_MESSAGE,
                dry_run=dry_run,
            )
    LOG_MESSAGE(
        log_messages.format_dry_run(
            message="Finished removing SSH config symlinks",
            dry_run=dry_run,
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Symlink the profile's SSH config fragments into ~/.ssh.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without applying them",
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove symlinks instead of creating them",
    )
    parser.add_argument(
        "--which",
        action="append",
        choices=available_host_keys(),
        default=[],
        metavar="HOST",
        help="Target one subscribed host. Can be passed multiple times",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Target all subscribed hosts from `this-system.toml`",
    )
    args = parser.parse_args()
    include_all = cast(bool, args.all)
    requested_host_keys = tuple(
        cast(
            list[str],
            args.which,
        ),
    )
    dry_run = cast(bool, args.dry_run)
    remove = cast(bool, args.remove)
    if include_all and requested_host_keys:
        parser.error("`--all` cannot be combined with `--which`")
    if not include_all and not requested_host_keys:
        parser.error("pass `--all` or at least one `--which`")
    profile = load_profiles.load_profile(required=True)
    if profile is None:
        parser.error("`this-system.toml` is required")
    host_keys = resolve_selected_hosts(
        subscribed_host_keys=profile.ssh_hosts,
        requested_host_keys=requested_host_keys,
        include_all=include_all,
    )
    if remove:
        remove_symlinks(
            dry_run=dry_run,
            host_keys=host_keys,
            remove_scaffold=include_all,
        )
    else:
        run(
            dry_run=dry_run,
            host_keys=host_keys,
        )


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT

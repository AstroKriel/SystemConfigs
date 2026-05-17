## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
import datetime
import re
import socket
import subprocess
import sys

from pathlib import Path
from typing import NoReturn, cast

##
## === SCRIPT CONFIG
##

SCRIPT_NAME = Path(__file__).name
HOME_DIR = Path.home()
SSH_DIR = HOME_DIR / ".ssh"
NOTES_DIR = SSH_DIR / "notes"
NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

## --- colours, only when stdout is a tty
_IS_TTY = sys.stdout.isatty()
_BOLD = "\033[1m" if _IS_TTY else ""
_CYAN = "\033[36m" if _IS_TTY else ""
_YELLOW = "\033[33m" if _IS_TTY else ""
_RED = "\033[31m" if _IS_TTY else ""
_GREEN = "\033[32m" if _IS_TTY else ""
_DIM = "\033[2m" if _IS_TTY else ""
_RESET = "\033[0m" if _IS_TTY else ""

##
## === OUTPUT HELPERS
##


def heading(
    message: str,
) -> None:
    print(f"\n{_BOLD}{_CYAN}==> {message}{_RESET}")


def info(
    message: str,
) -> None:
    print(f"{_DIM}{message}{_RESET}")


def warn(
    message: str,
) -> None:
    print(f"{_YELLOW}!! {message}{_RESET}", file=sys.stderr)


def success(
    message: str,
) -> None:
    print(f"{_GREEN}OK{_RESET} {message}")


def fail(
    message: str,
) -> NoReturn:
    print(f"{_RED}ERROR: {message}{_RESET}", file=sys.stderr)
    sys.exit(1)


##
## === PROMPT HELPERS
##


def prompt_required(
    label: str,
) -> str:
    while True:
        response = input(f"{label}: ").strip()
        if response:
            return response
        warn("value required")


def prompt_yes_no(
    label: str,
    *,
    default_yes: bool = False,
) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    response = input(f"{label} {suffix}: ").strip().lower()
    if not response:
        return default_yes
    return response.startswith("y")


##
## === ARG PARSER
##


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=(
            "Generate a new ed25519 SSH key with a standardised comment, and "
            "write a notes file under ~/.ssh/notes/ containing the public key "
            "and a placeholder ~/.ssh/config block you can copy. Never modifies "
            "~/.ssh/config or pushes the key to any remote."
        ),
    )
    parser.add_argument("--name", help="suffix for ~/.ssh/id_ed25519_NAME")
    parser.add_argument("--purpose", help="short description of what the key is for")
    parser.add_argument("--device", help="device the key is from (default: hostname)")
    return parser


##
## === PRE-FLIGHT
##


def ensure_ssh_dir() -> None:
    SSH_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    SSH_DIR.chmod(0o700)


##
## === GENERATE KEY
##


def generate_key(
    key_file: Path,
    *,
    comment: str,
) -> None:
    command = [
        "ssh-keygen",
        "-t",
        "ed25519",
        "-a",
        "100",
        "-f",
        str(key_file),
        "-C",
        comment,
    ]
    info(" ".join(command))
    subprocess.run(
        command,
        check=True,
    )
    key_file.chmod(0o600)
    success(f"key created at {key_file}")


##
## === WRITE NOTES
##


def write_notes(
    *,
    notes_file: Path,
    name: str,
    key_file: Path,
    pub_file: Path,
    comment: str,
) -> None:
    NOTES_DIR.mkdir(
        mode=0o700,
        exist_ok=True,
    )
    NOTES_DIR.chmod(0o700)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    public_key = pub_file.read_text().rstrip("\n")
    notes_file.write_text(
        f"# SSH Key Notes: {name}\n"
        f"# Created: {timestamp}\n"
        f"\n"
        f"## Key files\n"
        f"{key_file}   (private; never share)\n"
        f"{pub_file}   (public)\n"
        f"\n"
        f"## Public key\n"
        f"{public_key}\n"
        f"\n"
        f"## Keygen command\n"
        f'ssh-keygen -t ed25519 -a 100 -f "{key_file}" -C "{comment}"\n'
        f"\n"
        f"## Suggested ~/.ssh/config block (fill in placeholders)\n"
        f"Host <ALIAS>\n"
        f"  HostName <REMOTE_HOST>\n"
        f"  User <REMOTE_USER>\n"
        f"  IdentityFile {key_file}\n"
        f"  IdentitiesOnly yes\n"
        f"\n"
        f"## Suggested upload command (fill in placeholders)\n"
        f"ssh-copy-id -i {pub_file} <REMOTE_USER>@<REMOTE_HOST>\n"
        f"## Or upload the public key manually (e.g. via FreeIPA or GitHub web UI).\n"
        f"\n"
        f"## Verify\n"
        f"ssh <ALIAS>\n",
    )
    notes_file.chmod(0o600)
    success(f"notes saved to {notes_file}")


##
## === PROGRAM MAIN
##


def main() -> None:
    args = build_arg_parser().parse_args()
    arg_name = cast(str | None, args.name)
    arg_purpose = cast(str | None, args.purpose)
    arg_device = cast(str | None, args.device)

    heading("Gather inputs")
    name = arg_name or prompt_required("Unique name (suffix for id_ed25519_<name>)")
    if not NAME_PATTERN.fullmatch(name):
        fail(f"name must be alphanumeric, dash, or underscore (got: {name})")

    key_file = SSH_DIR / f"id_ed25519_{name}"
    if key_file.exists():
        info(f"Key already exists at {key_file}. Nothing to do.")
        return

    purpose = arg_purpose or prompt_required("Purpose")
    device = arg_device or socket.gethostname()

    today = datetime.date.today().strftime("%Y-%m-%d")
    pub_file = key_file.with_suffix(".pub")
    notes_file = NOTES_DIR / f"{name}-{today}.txt"
    comment = f"for {purpose} from {device} created on {today}"

    heading("Pre-flight")
    ensure_ssh_dir()
    info(f"{SSH_DIR} ok")

    heading("Summary")
    print(f"  Name:     {name}")
    print(f"  Purpose:  {purpose}")
    print(f"  Device:   {device}")
    print(f"  Date:     {today}")
    print(f"  Key file: {key_file}")
    print(f"  Comment:  {comment}")
    print(f"  Notes:    {notes_file}")
    if not prompt_yes_no("Proceed?"):
        fail("aborted")

    heading("Generate key")
    generate_key(
        key_file,
        comment=comment,
    )

    heading("Write notes")
    write_notes(
        notes_file=notes_file,
        name=name,
        key_file=key_file,
        pub_file=pub_file,
        comment=comment,
    )

    heading("Done")


##
## === ENTRY POINT
##

if __name__ == "__main__":
    main()

## } SCRIPT

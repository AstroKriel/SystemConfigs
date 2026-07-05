# SSH Config

Profile-driven SSH config. Each machine installs `~/.ssh/config` as a stub that includes
per-host fragments, selecting only the hosts that machine actually reaches.

## Layout

| Path | Role |
|---|---|
| `config.head` | symlinked to `~/.ssh/config`; contains only `Include ~/.ssh/config.d/*.conf` |
| `hosts/<host>.conf` | one `Host` block per connection; symlinked into `~/.ssh/config.d/` when subscribed |
| `defaults.conf` | global `Host *` defaults; installed as `config.d/zz-defaults.conf` |
| `records/<name>-<date>.txt` | key inventory: public key, `ssh-keygen` command, and config block |

## How a machine selects hosts

A profile in `config-profiles/<profile>.toml` lists the hosts it reaches:

```toml
ssh_hosts = [
  "github",
  "gadi",
]
```

`scripts/setup/ssh.py` reads the active profile and symlinks `config.head`, `defaults.conf`,
and each subscribed `hosts/<host>.conf` into `~/.ssh`. Run it through the full routine, or
standalone:

```bash
uv run -m scripts.setup.ssh --all --dry-run
```

## Ordering

`~/.ssh/config` includes `config.d/*.conf` in lexical order. SSH keeps the first value it sees
for most keywords, so `zz-defaults.conf` is named to sort last: per-host blocks win, and the
`Host *` defaults only fill gaps.

## Records

Records are the backup that matters. Private keys are never tracked here; they are disposable
and regenerated on loss. The records inventory the public keys and where each is deployed, so
regeneration is mechanical. `~/.ssh/records` is symlinked to `records/`, so keys created with
`ssh_helper` land here for commit automatically.

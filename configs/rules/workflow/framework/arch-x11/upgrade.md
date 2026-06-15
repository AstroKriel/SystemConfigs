# Arch Update Routine: Framework 13

Routine for maintaining the Framework 13 running Arch Linux on X11: preparation, update execution, post-update checks, and recovery.

---

## When to update

Update about once a week, preferably when there is time to reboot and check the system afterwards. Avoid starting an update before travel, calls, teaching, or deadlines where a reboot or small fix would be disruptive.

---

## Before updating

**Arch news.** Open `https://archlinux.org/news/` and scan recent posts for `requires manual intervention` or `may require manual intervention`. If a relevant post exists, read it and follow the instructions before proceeding. Pay attention to posts involving:

| Package | What it is |
|---|---|
| `linux` | Arch kernel; updates require a reboot. |
| `linux-firmware` | Hardware firmware for WiFi, Bluetooth, GPU, and USB-C. |
| `amd-ucode` | AMD CPU microcode loaded at boot. |
| `grub` | Bootloader; problems here affect booting. |
| `systemd` | Init and service manager. |
| `mesa` | Open-source graphics stack for the AMD GPU. |
| `pipewire` | Audio server. |
| `wireplumber` | PipeWire session manager. |
| `alsa-ucm-conf` | UCM profiles; changes can affect the internal mic workaround. |
| `sof-firmware` / `alsa-firmware` | Audio firmware. |
| `fwupd` | Firmware update tool. |
| `lightdm` | Display manager. |
| `xfce` | Desktop environment. |

**Changelogs and forums.** For hardware-adjacent packages (`linux`, `wireplumber`, `pipewire`, `alsa-ucm-conf`, `alsa-firmware`, `sof-firmware`, `fwupd`), read the Arch package page and upstream release notes. Search the Arch forums and Framework community (`https://community.frame.work`) for the package versions being upgraded plus this hardware (`Framework 13`, `Ryzen AI 300`). Issues frequently appear in the forums before they are documented upstream.

**Active workarounds.** Review `pending-issues.md`. For each open workaround, decide what to test after the upgrade before you start.

---

## Preview

Run before committing; both commands are read-only and safe:

```bash
checkupdates     # official packages; uses a temporary database
paru -Qua        # AUR packages
```

`checkupdates` syncs to its own temporary database, leaving the system in a consistent state. Note packages from the table above and any tied to open entries in `pending-issues.md`; their presence signals what to test after the update.

---

## Update

Close running browsers and long-lived apps first; upgrading a package while it is running can crash it:

```bash
paru -Syu
```

Read the transaction summary before accepting. Stop and inspect if the update wants to remove major system packages, the kernel, the bootloader, or a large number of unrelated packages.

---

## Post-update checks

| Check | Command | Pass | Otherwise |
|---|---|---|---|
| Config file changes | `pacdiff -o` | No output. | Files listed are `.pacnew` or `.pacsave`. Review and merge with `sudo pacdiff`. Never ignore `.pacnew` for core configs (`sudoers`, `pacman.conf`, `mkinitcpio.conf`, `fstab`). |
| Failed units | `systemctl --failed` | `0 loaded units listed.` | Run `systemctl status <unit>` and inspect the error. |
| Journal errors | `journalctl -p 3 -b` | Empty or only known harmless warnings. | Investigate errors from kernel, disk, login, network, audio, Bluetooth, or display services. |
| Bluetooth service | `systemctl status bluetooth` | `Active: active (running)`. | Run `bluetoothctl show` and inspect `journalctl -b -u bluetooth`. |
| Bluetooth controller | `bluetoothctl show` | Controller exists and `Powered: yes`. | No controller or powered off; investigate. |
| Audio services | `systemctl --user status pipewire pipewire-pulse wireplumber` | All active/running. | Inspect the failed unit and test devices with `wpctl status`. |
| Display manager | `systemctl status lightdm` | `Active: active (running)`. | Inspect `journalctl -b -u lightdm`. |

After the checks above, test every active workaround from `pending-issues.md`. Device enumeration is not enough; test actual functionality. Each entry in `pending-issues.md` lists its own test command under "Next steps".

---

## When to reboot

Reboot after updates involving any of:

- `linux`
- `linux-firmware`
- `amd-ucode`
- `systemd`
- `mesa`

Also reboot if the system behaves unexpectedly after updating.

```bash
systemctl reboot
```

---

## Post-reboot checks

| Check | Command | Pass | Otherwise |
|---|---|---|---|
| Running kernel | `uname -r` | Matches `pacman -Q linux`; dash/dot differences are normal. | Installed kernel is newer than the running one; investigate `/boot` and GRUB. |
| Installed kernel | `pacman -Q linux` | Version closely matches `uname -r`. | As above. |
| Failed units | `systemctl --failed` | `0 loaded units listed.` | Inspect with `systemctl status <unit>`. |
| Journal errors | `journalctl -p 3 -b` | No serious new errors. | Investigate repeated errors or anything matching broken hardware or services. |

Normal kernel match example:

```text
uname -r        6.19.12-arch1-1
pacman -Q linux linux 6.19.12.arch1-1
```

---

## When something breaks

| Step | Action |
|---|---|
| Search online before diagnosing locally | Check the Arch forums, Framework community (`https://community.frame.work`), and upstream issue trackers. Hardware issues on this machine are often known and documented; extended local diagnosis without checking online is inefficient. |
| Check what changed | `grep upgraded /var/log/pacman.log | tail -50` to identify which packages were updated and when. |
| Check the pre-upgrade snapshot before reconstructing | If a config file needs to be recovered, read the snapper pre-upgrade snapshot: `sudo snapper list` to find the number, then `sudo cat /.snapshots/<n>/snapshot/<path>`. Never reconstruct from memory. |
| Establish a baseline before removing a workaround | Before removing any workaround, run the test that confirms it is working. Remove it, then run the same test again. This isolates whether the removal caused the regression. |

---

## Cache maintenance

The pacman cache (`/var/cache/pacman/pkg`) grows without bound; prune it occasionally:

```bash
paccache -dk2        # dry run: show what would be removed, keeping 2 newest
sudo paccache -rk2   # remove, keeping the 2 newest versions of each package
```

Check cache size: `du -sh /var/cache/pacman/pkg`.

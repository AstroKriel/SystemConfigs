# Arch Upgrade Workflow: Framework 13

Process for running system upgrades and handling post-upgrade issues on this machine.

---

## Before upgrading

| Step | Action |
|---|---|
| Review package changelogs | For hardware-adjacent packages (`linux`, `wireplumber`, `pipewire`, `alsa-ucm-conf`, `alsa-firmware`, `sof-firmware`, `fwupd`), read the Arch package page and upstream release notes. Changes to these packages can silently alter hardware behaviour. |
| Check Arch forums and Framework community | Search for the package version plus this hardware (`Framework 13`, `Ryzen AI 300`) before running the upgrade. Issues frequently appear in the forums before they are documented or fixed upstream. |
| Note active workarounds | Review `pending-issues.md`. For each open workaround, decide what to test after the upgrade before you start. |

---

## After upgrading

| Step | Action |
|---|---|
| Test every active workaround | For each entry in `pending-issues.md`, test the actual functionality, not just device enumeration. A device appearing in `wpctl status` or `arecord -l` does not mean it works; test capture or playback directly. |
| Smoke test core hardware | Mic: `arecord -f S16_LE -r 48000 -c 2 -d 3 /tmp/test.wav && aplay /tmp/test.wav`. Audio out: play audio through speakers and headphones. Portal: `systemctl --user status xdg-desktop-portal`. |
| Check journal for errors | `journalctl -p 3 -b` to catch crashes and service failures that did not surface at login. |

---

## When something breaks

| Step | Action |
|---|---|
| Search online before diagnosing locally | Check the Arch forums, Framework community (community.frame.work), and upstream issue trackers first. Hardware issues on this machine are often known and documented. Extended local diagnosis without checking online is inefficient. |
| Check what changed | `grep upgraded /var/log/pacman.log | tail -50` to identify which packages were updated and when. |
| Check the pre-upgrade snapshot before reconstructing | If a config file needs to be recovered, read the snapper pre-upgrade snapshot first: `sudo snapper list` to find the snapshot number, then `sudo cat /.snapshots/<n>/snapshot/<path>`. Never reconstruct from memory. |
| Establish a baseline before removing a workaround | Before removing any workaround, run the test that confirms the workaround is working. Remove it, then run the same test again. This isolates whether the removal caused the regression. |

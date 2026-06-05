# Print Preferences Core

A small core dependency that makes the U1's `SET_PRINT_PREFERENCES` usable mid-print. The
**Force Bed Mesh** and **Force Timelapse** plugins build on it.

## What it does

- Patches Klipper's `print_task_config.py` to add a `FORCE` guard, so
  `SET_PRINT_PREFERENCES ... FORCE=1` takes effect even while a print is running.

## Do you need it?

You usually do not install this directly: the plugins that need it (the Force Bed Mesh and
Force Timelapse plugins) pull it in automatically as a dependency.

## Notes

- Restarts Klipper on install.
- Patches Klipper source; reverted on uninstall and re-applied after an OTA firmware update.
- Snapmaker U1.

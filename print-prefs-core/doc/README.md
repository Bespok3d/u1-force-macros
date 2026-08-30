# Print Preferences Core

A small core dependency that makes the U1's `SET_PRINT_PREFERENCES` usable mid-print. The
**Force Bed Mesh** and **Force Timelapse** plugins build on it.

## What it does

- Makes `SET_PRINT_PREFERENCES ... FORCE=1` take effect even while a print is running, which
  the printer otherwise refuses.

## Do you need it?

You usually do not install this directly: the plugins that need it (the Force Bed Mesh and
Force Timelapse plugins) pull it in automatically as a dependency.

## Notes

- Restarts Klipper on install.
- Needs the `u1-base-print-task-config` base plugin, which is installed alongside it.
- Snapmaker U1.

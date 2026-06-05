# Force Timelapse

Captures a timelapse on **every** print, regardless of the Snapmaker app's timelapse
setting. No per-print toggle needed.

## What it does

- Overrides `TIMELAPSE_START` to force timelapse capture each print.
- Calls `SET_PRINT_PREFERENCES TIME_LAPSE_CAMERA=1 FORCE=1` so it applies mid-print.

## Requires

- **Print Preferences Core** (installed automatically).
- A camera and the **Timelapse** plugin (for the Moonraker timelapse component). Your slicer
  must emit `TIMELAPSE_START`, `TIMELAPSE_TAKE_FRAME`, and `TIMELAPSE_STOP` (most do when
  timelapse is enabled in the slicer).

## Notes

Restarts Klipper on install. Snapmaker U1.

# Force Bed Mesh (Adaptive)

Runs an **adaptive bed mesh** at the start of every print: it only probes the area your
objects actually cover, so leveling is faster than a full mesh.

## What it does

- Overrides `BED_MESH_CALIBRATE` to force an adaptive mesh each print, even when your slicer asks
  for a full one. OrcaSlicer's stock U1 profile sends `ADAPTIVE=0`; this plugin overrides it.
- Calls `SET_PRINT_PREFERENCES BED_LEVEL=1 FORCE=1` so it applies mid-print.
- Tells you in the console when a file carries no object outline, because then there is nothing to
  adapt to and the whole bed gets probed.

## Requires

- **Print Preferences Core** (installed automatically).
- Object outlines in the file, so Klipper knows where the model sits. SnapmakerOrca writes them by
  default; in other slicers the setting is called **Exclude Object** or **Label objects**. If your
  slicer will not write them, install **Object Processing** and Moonraker adds them for you.

## Notes

- Conflicts with **Force Bed Mesh** (the full-mesh version): pick one.
- To probe the whole bed on purpose, run `_BED_MESH_CALIBRATE_BASE` in the console.
- Restarts Klipper on install. Snapmaker U1.

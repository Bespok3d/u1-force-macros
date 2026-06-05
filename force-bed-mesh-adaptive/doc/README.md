# Force Bed Mesh (Adaptive)

Runs an **adaptive bed mesh** at the start of every print: it only probes the area your
objects actually cover, so leveling is faster than a full mesh.

## What it does

- Overrides `BED_MESH_CALIBRATE` to force an adaptive mesh each print.
- Calls `SET_PRINT_PREFERENCES BED_LEVEL=1 FORCE=1` so it applies mid-print.

## Requires

- **Print Preferences Core** (installed automatically).
- **Object Processing** enabled and your slicer producing object data, so Klipper knows
  where the objects are. Without object info there is nothing to adapt to.

## Notes

- Conflicts with **Force Bed Mesh** (the full-mesh version): pick one.
- Restarts Klipper on install. Snapmaker U1.

# Force Bed Mesh

Runs a **full bed mesh** at the start of every print, regardless of the Snapmaker app's
bed-leveling preference.

## What it does

- Overrides `BED_MESH_CALIBRATE` so each print calibrates a fresh full mesh.
- Calls `SET_PRINT_PREFERENCES BED_LEVEL=1 FORCE=1` so the setting applies mid-print.

## Using it

Install it; the next print meshes the bed automatically. Your slicer start G-code must call
the Snapmaker print-start sequence (most do).

## Requires

- **Print Preferences Core** (installed automatically).

## Notes

- Conflicts with **Force Bed Mesh (Adaptive)**: install one or the other, not both (they
  override the same macro).
- Restarts Klipper on install. Snapmaker U1.

# Changelog

## 0.1.2

- Forces the adaptive mesh even when the slicer explicitly asks for a full one. OrcaSlicer's stock
  U1 profile sends `ADAPTIVE=0`, and the plugin used to step aside and probe the whole bed.
- Says so in the console when a file carries no object outline, instead of quietly probing the whole
  bed and looking like the plugin did nothing.
- Object Processing is no longer required: a slicer that labels its objects, which SnapmakerOrca does
  by default, is enough on its own.

## 0.1.1

- Publishing from bundled to online official registry.

## 0.1.0

- First release. Forces an adaptive bed mesh on every print. Mutually exclusive
  with Force Bed Mesh.

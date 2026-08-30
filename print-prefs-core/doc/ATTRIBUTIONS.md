# Attributions

This plugin ships its own Klipper extra and its own config section. It contains no code taken from
another project.

The change to Snapmaker's `print_task_config.py` that makes `FORCE=1` mean something now lives in
the base-layer plugin `u1-base-print-task-config`, which this plugin requires. The credit for the
original FORCE guard, paxx12's Extended Firmware overlay `36-feature-print-preferences` (GPL-3.0),
travels with that change and is recorded there.

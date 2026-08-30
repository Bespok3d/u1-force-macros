# Changelog

## 0.1.2

- This plugin no longer changes Klipper's own program files. The change that makes FORCE work mid
  print now comes from the shared base layer, which is installed alongside it, so the Force plugins
  behave exactly as before.
- Because of that, this plugin and the RFID plugin no longer fight over the same firmware file when
  both are installed.

## 0.1.1

- Publishing from bundled to online official registry.

## 0.1.0

- First release. Core dependency for the Force macros: adds a FORCE guard so
  SET_PRINT_PREFERENCES works mid-print.

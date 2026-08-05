# Attributions - force-bed-mesh-adaptive

**Plugin author:** Bespok3d. The idea came from paxx12's Extended Firmware overlay
`36-feature-print-preferences`.

Forces an adaptive bed mesh before every print.

| Upstream project | Author | Licence | Needed at runtime | Code ships in this package |
| --- | --- | --- | --- | --- |
| Extended Firmware overlay `36-feature-print-preferences` | paxx12 | GPL-3.0 | no | no |

Up to 0.1.1 the Klipper config here was the `bed_leveling_adaptive_force.cfg` tweak from that overlay,
carried over with the same macro body. It did not do what it promised: a slicer that asked for a full
mesh was obeyed rather than overridden, so the plugin quietly probed the whole bed. In 0.1.2 the macro
was rewritten from scratch and none of the original lines remain.

The credit stays because that overlay is where the approach came from, and because this plugin's
dependency, `print-prefs-core`, still ships paxx12's Klipper patch.

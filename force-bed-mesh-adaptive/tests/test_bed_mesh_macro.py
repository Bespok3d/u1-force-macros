"""Regression tests for the BED_MESH_CALIBRATE override that force-bed-mesh-adaptive installs.

The macro is rendered exactly as Klipper renders it: the same config parser, the same Jinja
delimiters, and a printer object that raises KeyError for a module that is not loaded. The
assertions then read the emitted command with Klipper's own argument rule, where an extended
command's arguments become a dict and the last occurrence of a key wins.
"""
import configparser
from pathlib import Path

import jinja2

MACRO_SECTION = "gcode_macro BED_MESH_CALIBRATE"
MACRO_CFG = (
    Path(__file__).resolve().parent.parent
    / "files"
    / "cfg"
    / "klipper"
    / "force-bed-mesh-adaptive.cfg"
)
# Klipper's own delimiters: a gcode_macro reads a variable as {name}, not {{ name }}.
KLIPPER_ENVIRONMENT = jinja2.Environment("{%", "%}", "{", "}", autoescape=False)


class PrinterStatus(dict):
    """Klipper's template `printer` raises KeyError for a module that is not configured."""


def read_macro_template():
    fileconfig = configparser.RawConfigParser(strict=False, inline_comment_prefixes=(";", "#"))
    fileconfig.read(MACRO_CFG)
    return KLIPPER_ENVIRONMENT.from_string(fileconfig.get(MACRO_SECTION, "gcode"))


def render_macro(rawparams, labelled_objects=(), print_state="printing", exclude_object=True):
    announcements = []
    printer = PrinterStatus({"print_stats": {"state": print_state}})
    if exclude_object:
        printer["exclude_object"] = {"objects": list(labelled_objects)}
    rendered = read_macro_template().render(
        printer=printer,
        rawparams=rawparams,
        params=parse_klipper_arguments(rawparams),
        action_respond_info=announcements.append,
    )
    return [line.strip() for line in rendered.splitlines() if line.strip()], announcements


def parse_klipper_arguments(command_arguments):
    """The rule from Klipper's gcode.py: arguments become a dict, so the last key seen wins."""
    return {
        argument.split("=", 1)[0].upper(): argument.split("=", 1)[1]
        for argument in command_arguments.split()
        if "=" in argument
    }


def calibrate_arguments(emitted_lines):
    calibrate = next(line for line in emitted_lines if line.startswith("_BED_MESH_CALIBRATE_BASE"))
    return parse_klipper_arguments(calibrate[len("_BED_MESH_CALIBRATE_BASE") :])


A_LABELLED_OBJECT = [{"polygon": [[130.7, 130.7], [140.3, 140.3]]}]


def test_a_slicer_that_asks_for_adaptive_off_is_overridden():
    # OrcaSlicer's stock U1 profile sends ADAPTIVE=0. The macro used to test only whether the
    # parameter existed, so that file got the full 121-point bed probe it was meant to avoid.
    emitted, _ = render_macro(
        "mesh_min=8.5,9 mesh_max=262.5,263 PROBE_COUNT=7,7 ADAPTIVE=0 ADAPTIVE_MARGIN=0",
        labelled_objects=A_LABELLED_OBJECT,
    )
    assert calibrate_arguments(emitted)["ADAPTIVE"] == "1"


def test_a_bare_calibrate_from_snapmaker_orca_gets_adaptive():
    emitted, _ = render_macro("PROBE_COUNT=11,11", labelled_objects=A_LABELLED_OBJECT)
    assert calibrate_arguments(emitted)["ADAPTIVE"] == "1"


def test_the_slicers_own_arguments_survive():
    emitted, _ = render_macro(
        "PROBE_COUNT=11,11 Z_OFFSET=-0.07", labelled_objects=A_LABELLED_OBJECT
    )
    assert calibrate_arguments(emitted)["PROBE_COUNT"] == "11,11"
    assert calibrate_arguments(emitted)["Z_OFFSET"] == "-0.07"


def test_a_file_with_no_object_outline_says_the_whole_bed_is_being_probed():
    # Klipper falls back to a full mesh silently here, which reads as the plugin doing nothing.
    _, announcements = render_macro("PROBE_COUNT=11,11", labelled_objects=[])
    assert len(announcements) == 1
    assert "no object outline" in announcements[0]


def test_a_labelled_file_probes_without_comment():
    _, announcements = render_macro("PROBE_COUNT=11,11", labelled_objects=A_LABELLED_OBJECT)
    assert announcements == []


def test_a_printer_without_the_exclude_object_module_still_calibrates():
    emitted, announcements = render_macro("PROBE_COUNT=11,11", exclude_object=False)
    assert calibrate_arguments(emitted)["ADAPTIVE"] == "1"
    assert len(announcements) == 1


def test_the_bed_level_preference_is_forced_only_while_a_print_is_running():
    printing, _ = render_macro("PROBE_COUNT=11,11", labelled_objects=A_LABELLED_OBJECT)
    idle, _ = render_macro(
        "PROBE_COUNT=11,11", labelled_objects=A_LABELLED_OBJECT, print_state="standby"
    )
    assert "SET_PRINT_PREFERENCES BED_LEVEL=1 FORCE=1" in printing
    assert "SET_PRINT_PREFERENCES BED_LEVEL=1 FORCE=1" not in idle

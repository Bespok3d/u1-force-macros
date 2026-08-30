"""Regression tests for honouring FORCE=1 on SET_PRINT_PREFERENCES once a print has started.

Snapmaker's firmware refuses a preference change mid print. This plugin used to change Snapmaker's
own print_task_config.py to add the FORCE escape hatch. That change now belongs to the base-layer
plugin u1-base-print-task-config, which offers `allow_force_preference_param(owner)`, and this
plugin registers itself as an owner at startup. These tests hold that registration, hold that a
printer without the base layer still starts, and hold that no patch is left in this package.
"""
import json
from pathlib import Path

from conftest import load_printer_extra

print_prefs_force = load_printer_extra("print_prefs_force")

PLUGIN_DIR = Path(__file__).resolve().parent.parent


class FakePrintTaskConfig:
    """The base layer's door, which counts registered owners rather than flipping a flag."""

    def __init__(self):
        self.force_preference_allowed_by = set()

    def allow_force_preference_param(self, owner):
        self.force_preference_allowed_by.add(owner)

    def disallow_force_preference_param(self, owner):
        self.force_preference_allowed_by.discard(owner)


class UnpatchedPrintTaskConfig:
    """Snapmaker's own object with no base layer applied: present, but offering no door."""


class FakePrinter:
    def __init__(self, klipper_objects):
        self._klipper_objects = klipper_objects
        self.ready_handlers = []

    def lookup_object(self, name, default=None):
        return self._klipper_objects.get(name, default)

    def register_event_handler(self, event, handler):
        self.ready_handlers.append((event, handler))


class FakeConfig:
    def __init__(self, printer):
        self._printer = printer

    def get_printer(self):
        return self._printer


def start_plugin(klipper_objects):
    """Build the plugin the way Klipper does, then fire klippy:ready."""
    printer = FakePrinter(klipper_objects)
    print_prefs_force.load_config(FakeConfig(printer))
    for event, handler in printer.ready_handlers:
        assert event == "klippy:ready"
        handler()
    return printer


def manifest():
    return json.loads((PLUGIN_DIR / "manifest.json").read_text())


def test_force_is_honoured_mid_print_because_this_plugin_registers_for_it():
    task_config = FakePrintTaskConfig()
    start_plugin({'print_task_config': task_config})

    assert task_config.force_preference_allowed_by == {
        print_prefs_force.FORCE_PREFERENCE_OWNER}


def test_the_owner_name_is_this_plugin_so_a_second_plugin_can_hold_the_same_door():
    assert print_prefs_force.FORCE_PREFERENCE_OWNER == "print-prefs-core"


def test_a_printer_without_the_base_layer_still_starts(caplog):
    """Required behaviour, not a leftover: a printer may have this plugin updated before the base
    layer is installed, and it must come up with FORCE simply refused, as on stock firmware."""
    with caplog.at_level("WARNING", logger="bespok3d"):
        start_plugin({})

    assert len([record for record in caplog.records
                if "FORCE door absent" in record.getMessage()]) == 1


def test_a_base_layer_too_old_to_offer_the_door_is_treated_as_no_door(caplog):
    task_config = UnpatchedPrintTaskConfig()
    with caplog.at_level("WARNING", logger="bespok3d"):
        start_plugin({'print_task_config': task_config})

    assert not hasattr(task_config, 'force_preference_allowed_by')
    assert len([record for record in caplog.records
                if "FORCE door absent" in record.getMessage()]) == 1


def test_this_plugin_changes_none_of_snapmakers_own_files():
    """R-MOVE-2. An instrument entry is what patches Snapmaker's code; it belongs to the base layer
    now, and this plugin places its own extra and its own config section instead."""
    install = manifest()["install"]
    placed = [entry["class"] for entry in install["place"]]

    assert "instrument" not in install
    assert placed == ["klipper-extra", "klipper-config"]
    assert "klipper-source" not in manifest()["permissions"]
    assert list(PLUGIN_DIR.glob("files/**/*.patch")) == []


def test_the_base_layer_is_required_and_carries_no_version_floor():
    """R-MOVE-4. Both plugins that used to patch print_task_config.py ride one base release, so a
    require names the service and nothing else: a floor would pin them to separate releases."""
    required = manifest()["require"]

    assert [entry["service"] for entry in required] == ["u1-base-print-task-config"]
    assert all(set(entry) == {"service", "cardinality"} for entry in required)

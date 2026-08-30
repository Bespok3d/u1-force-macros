"""Load the plugin's Klipper extra the way Klipper does, without a printer or Klipper present."""
import importlib.util
import sys
from pathlib import Path

EXTRAS_DIR = Path(__file__).resolve().parent.parent / "files" / "extras"


def load_printer_extra(module_name):
    spec = importlib.util.spec_from_file_location(
        module_name, EXTRAS_DIR / f"{module_name}.py")
    extra = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = extra
    spec.loader.exec_module(extra)
    return extra

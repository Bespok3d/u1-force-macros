"""Let SET_PRINT_PREFERENCES be honoured mid print when it is sent with FORCE=1.

Snapmaker's own print_task_config refuses a preference change once a print has started. The base
layer, u1-base-print-task-config, owns that file and offers a door: while an owner is registered,
FORCE=1 on the command is honoured. This extra is the owner registration, and nothing else. It is
what the Force Bed Mesh and Force Timelapse plugins build on.
"""
import logging

FORCE_PREFERENCE_OWNER = "print-prefs-core"

_log = logging.getLogger('bespok3d')


class PrintPrefsForce:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.printer.register_event_handler("klippy:ready", self._handle_ready)

    def _handle_ready(self):
        task_config = self.printer.lookup_object('print_task_config', None)
        if task_config is None or not hasattr(task_config, 'allow_force_preference_param'):
            _log.warning(
                "print_task_config FORCE door absent: SET_PRINT_PREFERENCES stays refused "
                "mid print, as it is on stock firmware")
            return
        task_config.allow_force_preference_param(FORCE_PREFERENCE_OWNER)
        _log.info("FORCE preference registered owner=%s", FORCE_PREFERENCE_OWNER)


def load_config(config):
    return PrintPrefsForce(config)

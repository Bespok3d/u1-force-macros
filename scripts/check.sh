#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (C) 2026 unlucio and the Bespok3d contributors
# SPDX-License-Identifier: GPL-3.0-only
# This plugin's own gate: it must pass from this repo's root, with no sibling repo cloned except
# lib_bespok3d. This repo ships config, assets and shell, so its gate is the shared detectors plus
# the tests that render force-bed-mesh-adaptive's gcode_macro.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# The shared gate helpers and the detectors that enforce a workspace-wide rule live in one place.
# See lib_bespok3d/tooling/README.md. This is the only line that knows where they are.
B3D_TOOLING="${B3D_TOOLING:-$REPO_ROOT/lib_bespok3d/tooling}"
# lib_bespok3d is a submodule. A clone made without it leaves an empty directory here, so say what
# is actually wrong instead of letting every check below fail on a missing file.
if [ ! -f "$B3D_TOOLING/gate-lib.sh" ]; then
    echo "The shared gate helpers are missing: the lib_bespok3d submodule is not checked out." >&2
    echo "Run this once from the repo root, then try again:" >&2
    echo "  git submodule sync --recursive && git submodule update --init --recursive" >&2
    echo "See CONTRIBUTING.md for the full environment setup." >&2
    exit 1
fi

# shellcheck source=/dev/null
. "$B3D_TOOLING/gate-lib.sh"

cd "$REPO_ROOT" || exit 1

echo ""
echo "u1-force-macros gate"

b3d_python_tools

# force-bed-mesh-adaptive ships a gcode_macro, which is a Jinja2 template, so its tests render it the
# way Klipper does and need Jinja2. That is this plugin's own test dependency, not a shared tool, so
# it is declared here and provisioned into a tree the tests import from rather than added to the
# shared tool venv that 21 repos read. B3D_PY is the gate's interpreter, provisioned just above.
BED_MESH_TEST_DEPS="$REPO_ROOT/force-bed-mesh-adaptive/tests/.deps"
"$B3D_PY" -m pip install --quiet --upgrade --target "$BED_MESH_TEST_DEPS" \
    -r "$REPO_ROOT/force-bed-mesh-adaptive/tests/requirements.txt"
export PYTHONPATH="$BED_MESH_TEST_DEPS"

run_check "pytest (force-bed-mesh-adaptive)" pytest_in_dir "$REPO_ROOT/force-bed-mesh-adaptive" tests
run_check "ruff (force-bed-mesh-adaptive)"   ruff_in_dir "$REPO_ROOT/force-bed-mesh-adaptive" tests

unset PYTHONPATH

workflow_pinning_check "$REPO_ROOT"
em_dash_check "$REPO_ROOT"
shellcheck_repo "$REPO_ROOT"

gate_summary || exit 1

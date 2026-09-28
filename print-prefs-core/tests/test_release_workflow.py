# SPDX-FileCopyrightText: Copyright (C) 2026 unlucio and the Bespok3d contributors
# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path


def test_release_and_preview_resolve_the_base_layer_provider() -> None:
    workflows = Path(__file__).resolve().parents[2] / ".github" / "workflows"
    provider_index = "provider-indexes: https://raw.githubusercontent.com/Bespok3d/main-index/main/index.json"
    for workflow_name in ("release.yml", "pr-build.yml"):
        assert provider_index in (workflows / workflow_name).read_text(encoding="utf-8")

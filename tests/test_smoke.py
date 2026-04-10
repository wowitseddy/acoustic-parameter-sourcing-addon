from __future__ import annotations

import json
import sys

from acoustic_parameter_sourcing_addon import cli


def test_cli_generates_sourcing_outputs(tmp_path, monkeypatch):
    out_dir = tmp_path / "output"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "acoustic-sourcing",
            "--catalog",
            "examples/catalogs/components.json",
            "--materials",
            "examples/catalogs/materials.json",
            "--query",
            "examples/queries/sensor_micro_probe.json",
            "--output-dir",
            str(out_dir),
        ],
    )

    cli.main()

    matches = out_dir / "matches.json"
    fallback = out_dir / "fallback_manifest.json"
    report = out_dir / "report.md"

    assert matches.exists()
    assert fallback.exists()
    assert report.exists()

    payload = json.loads(matches.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
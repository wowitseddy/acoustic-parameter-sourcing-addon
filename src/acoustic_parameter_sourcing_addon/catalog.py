from __future__ import annotations

import json
from pathlib import Path

from .models import Component, MaterialOption


def load_catalog(path: str | Path) -> list[Component]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Component(
            category=item["category"],
            part_number=item["part_number"],
            vendor=item["vendor"],
            unit_cost_usd=float(item["unit_cost_usd"]),
            diameter_mm=_optional_float(item.get("diameter_mm")),
            thickness_mm=_optional_float(item.get("thickness_mm")),
            length_mm=_optional_float(item.get("length_mm")),
            width_mm=_optional_float(item.get("width_mm")),
            height_mm=_optional_float(item.get("height_mm")),
            tags=list(item.get("tags", [])),
            environments=list(item.get("environments", [])),
            notes=item.get("notes", ""),
            metadata=dict(item.get("metadata", {})),
        )
        for item in raw
    ]


def load_materials(path: str | Path) -> list[MaterialOption]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        MaterialOption(
            name=item["name"],
            unit=item["unit"],
            unit_cost_usd=float(item["unit_cost_usd"]),
            process=item["process"],
            notes=item.get("notes", ""),
        )
        for item in raw
    ]


def _optional_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(value)

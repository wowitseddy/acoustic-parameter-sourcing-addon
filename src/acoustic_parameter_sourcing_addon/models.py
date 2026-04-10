from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Component:
    category: str
    part_number: str
    vendor: str
    unit_cost_usd: float
    diameter_mm: float | None = None
    thickness_mm: float | None = None
    length_mm: float | None = None
    width_mm: float | None = None
    height_mm: float | None = None
    tags: list[str] = field(default_factory=list)
    environments: list[str] = field(default_factory=list)
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MaterialOption:
    name: str
    unit: str
    unit_cost_usd: float
    process: str
    notes: str = ""


@dataclass(slots=True)
class SourcingQuery:
    category: str
    target_circumference_mm: float | None = None
    max_unit_cost_usd: float | None = None
    required_tags: list[str] = field(default_factory=list)
    required_environments: list[str] = field(default_factory=list)
    quantity: int = 1
    notes: str = ""

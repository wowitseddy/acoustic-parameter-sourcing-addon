from __future__ import annotations

import json
import math
from dataclasses import asdict
from pathlib import Path

from .models import Component, MaterialOption, SourcingQuery


def build_sourcing_plan(
    components: list[Component],
    materials: list[MaterialOption],
    query: SourcingQuery,
) -> dict:
    matches = rank_components(components, query)
    fallback = build_fallback_manifest(materials, query) if not matches else None
    return {
        "query": asdict(query),
        "matches": [serialize_component(match) for match in matches],
        "fallback_manifest": fallback,
    }


def rank_components(components: list[Component], query: SourcingQuery) -> list[Component]:
    diameter_limit = circumference_to_diameter(query.target_circumference_mm)
    candidates: list[tuple[float, Component]] = []

    for component in components:
        if component.category != query.category:
            continue
        if query.max_unit_cost_usd is not None and component.unit_cost_usd > query.max_unit_cost_usd:
            continue
        if query.required_tags and not set(query.required_tags).issubset(component.tags):
            continue
        if query.required_environments and not set(query.required_environments).issubset(component.environments):
            continue
        if diameter_limit is not None and component.diameter_mm is not None and component.diameter_mm > diameter_limit:
            continue

        score = component.unit_cost_usd
        if diameter_limit is not None and component.diameter_mm is not None:
            score += abs(diameter_limit - component.diameter_mm) * 0.1
        candidates.append((score, component))

    candidates.sort(key=lambda item: item[0])
    return [component for _, component in candidates[:10]]


def build_fallback_manifest(materials: list[MaterialOption], query: SourcingQuery) -> dict:
    diameter_mm = circumference_to_diameter(query.target_circumference_mm)
    radius_mm = diameter_mm / 2 if diameter_mm is not None else None

    selected = materials[:3]
    line_items = []
    total = 0.0
    for material in selected:
        quantity = _suggest_material_quantity(material, query)
        cost = round(quantity * material.unit_cost_usd, 4)
        total += cost
        line_items.append(
            {
                "material": material.name,
                "process": material.process,
                "unit": material.unit,
                "quantity": quantity,
                "unit_cost_usd": material.unit_cost_usd,
                "line_cost_usd": cost,
                "notes": material.notes,
            }
        )

    return {
        "category": query.category,
        "target_circumference_mm": query.target_circumference_mm,
        "target_diameter_mm": diameter_mm,
        "target_radius_mm": radius_mm,
        "prototype_quantity": query.quantity,
        "estimated_total_cost_usd": round(total, 4),
        "line_items": line_items,
        "notes": "Fallback estimate is for in-house prototype fabrication planning only.",
    }


def write_plan(plan: dict, output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    (output_path / "matches.json").write_text(
        json.dumps(plan["matches"], indent=2),
        encoding="utf-8",
    )
    (output_path / "fallback_manifest.json").write_text(
        json.dumps(plan["fallback_manifest"], indent=2),
        encoding="utf-8",
    )
    (output_path / "report.md").write_text(render_report(plan), encoding="utf-8")


def render_report(plan: dict) -> str:
    query = plan["query"]
    lines = [
        "# Acoustic Sourcing Report",
        "",
        f"- Category: {query['category']}",
        f"- Target circumference (mm): {query['target_circumference_mm']}",
        f"- Max unit cost (USD): {query['max_unit_cost_usd']}",
        f"- Quantity: {query['quantity']}",
        "",
        "## Matches",
    ]

    if plan["matches"]:
        for match in plan["matches"]:
            lines.append(
                f"- {match['part_number']} from {match['vendor']} at ${match['unit_cost_usd']:.2f}"
            )
    else:
        lines.append("- No catalog match found.")

    lines.extend(["", "## Fallback Manifest"])
    if plan["fallback_manifest"]:
        lines.append(
            f"- Estimated total cost: ${plan['fallback_manifest']['estimated_total_cost_usd']:.2f}"
        )
        for item in plan["fallback_manifest"]["line_items"]:
            lines.append(
                f"- {item['material']}: {item['quantity']} {item['unit']} via {item['process']} (${item['line_cost_usd']:.2f})"
            )
    else:
        lines.append("- Not needed because catalog matches were found.")

    return "\n".join(lines) + "\n"


def circumference_to_diameter(circumference_mm: float | None) -> float | None:
    if circumference_mm is None:
        return None
    return circumference_mm / math.pi


def serialize_component(component: Component) -> dict:
    return asdict(component)


def _suggest_material_quantity(material: MaterialOption, query: SourcingQuery) -> float:
    base = max(query.quantity, 1)
    if material.unit == "g":
        return float(base * 5)
    if material.unit == "cm2":
        return float(base * 12)
    if material.unit == "board":
        return float(base)
    return float(base)

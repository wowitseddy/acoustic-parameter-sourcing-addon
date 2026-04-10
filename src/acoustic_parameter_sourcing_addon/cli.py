from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalog import load_catalog, load_materials
from .models import SourcingQuery
from .planner import build_sourcing_plan, write_plan


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-reference hardware catalogs and emit fallback prototype material manifests."
    )
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--materials", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    components = load_catalog(args.catalog)
    materials = load_materials(args.materials)
    query = load_query(args.query)
    plan = build_sourcing_plan(components, materials, query)
    write_plan(plan, args.output_dir)


def load_query(path: str | Path) -> SourcingQuery:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return SourcingQuery(
        category=raw["category"],
        target_circumference_mm=raw.get("target_circumference_mm"),
        max_unit_cost_usd=raw.get("max_unit_cost_usd"),
        required_tags=list(raw.get("required_tags", [])),
        required_environments=list(raw.get("required_environments", [])),
        quantity=int(raw.get("quantity", 1)),
        notes=raw.get("notes", ""),
    )


if __name__ == "__main__":
    main()

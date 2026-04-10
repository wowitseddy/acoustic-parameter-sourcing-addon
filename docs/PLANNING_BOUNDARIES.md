# Planning Boundaries

## Scope

This project is a prototype sourcing and fallback-fabrication planning tool.

It is intended to:
- rank catalog components against dimensional, cost, and environment constraints
- estimate rough fallback fabrication manifests when no catalog part qualifies

It is not intended to provide manufacturing quotes, certified component approval, or final engineering release documentation.

## Included Public Artifacts

- example catalogs under `examples/catalogs/`
- example query files under `examples/queries/`
- locally generated `matches.json`, `fallback_manifest.json`, and `report.md`

## Recommended Interpretation

Use the outputs as:
- early-stage sourcing support
- BOM and prototype planning aids
- constraint-screening artifacts before ordering or machining

Do not use them as:
- supplier commitments
- validated production BOMs
- formal fabrication cost guarantees
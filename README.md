# Acoustic Parameter Sourcing Add-on

This draft repository is a rapid-prototyping add-on for acoustic parameter device scaffolding and related prefab hardware planning.

The immediate goal is to answer two questions quickly during early test-phase design:

- What off-the-shelf sensors, peripherals, and PCB options meet the physical and environmental constraints for a prototype or BME incubator test?
- If no market part fits, what is the rough in-house material cost to fabricate a first-pass substitute?

## Scope

This draft focuses on:

- cross-referencing component catalogs for sensors, peripherals, and PCBs
- filtering by dimensional constraints, cost, environment, and tags
- converting circumference-based requests into comparable diameter/radius checks
- generating a fallback material manifest when no catalog item qualifies

## Initial workflow

1. Export or author component catalogs as JSON.
2. Submit a query describing the target part envelope and constraints.
3. Return ranked catalog matches.
4. If no match exists, emit an in-house fabrication estimate from material templates.

## Example use cases

- Isaac-to-CAD translation where a Blender/Isaac concept needs a real sensor within a strict envelope.
- BME incubator fixture planning where temperature, humidity, sterilization, or enclosure constraints matter.
- Quick sourcing checks for prototype BOMs before ordering or machining.

## Data model highlights

Each component can include:

- `category`: `sensor`, `peripheral`, `pcb`, or `material`
- `part_number`
- `vendor`
- `unit_cost_usd`
- `diameter_mm`, `thickness_mm`, `length_mm`, `width_mm`, `height_mm`
- `tags`
- `environments`
- `notes`

Queries can include:

- `category`
- `target_circumference_mm`
- `max_unit_cost_usd`
- `required_tags`
- `required_environments`

## Quick start

```powershell
cd projects/acoustic-parameter-sourcing-addon
python -m pip install -e .
acoustic-sourcing --catalog examples/catalogs/components.json --materials examples/catalogs/materials.json --query examples/queries/sensor_micro_probe.json --output-dir output
```

## Example output

The tool writes:

- `matches.json`: ranked component matches
- `fallback_manifest.json`: in-house material estimate if no match exists
- `report.md`: human-readable sourcing summary

## Current assumptions

- All size comparisons are normalized to millimeters.
- Circumference queries are treated as circular envelopes and converted with $d = \frac{c}{\pi}$.
- Fallback fabrication estimates are rough-order-of-magnitude planning inputs, not manufacturing quotes.

## Next extensions

- supplier API adapters
- parametric PCB fab estimators
- incubator compatibility rule packs
- CAD export hooks for shortlisted parts
- Isaac asset metadata import

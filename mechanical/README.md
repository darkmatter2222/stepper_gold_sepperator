# Mechanical files and current print list

Use the compact **v2** kit with **all three** revisions below. The original snapshots and ZIPs are retained without rewriting their contents.

| Part | Qty | Current print file |
|---|---:|---|
| P01 base | 1 | [STL](base_cable_revision/P01_base_cable_clearance.stl) |
| P02 motor deck | 1 | [STL](gold_poc_v2/STL/P02_motor_deck.stl) |
| P03 spacer | 4 | [STL](gold_poc_v2/STL/P03_spacer_x4.stl) |
| P04 catcher | 1 | [STL](gold_poc_v2/STL/P04_catcher.stl) |
| P05 drive hub, M3 revision | 1 | [STL](hub_m3_revision/P05_drive_hub_M3.stl) |
| P06 bowl | 1 | [STL](gold_poc_v2/STL/P06_bowl.stl) |
| P07 optional trap insert | 0 or 1 | [STL](gold_poc_v2/STL/P07_optional_trap_insert.stl) |
| P08 brass-inlet lid | 1 | [STL](lid_water/P08_lid_brass_4mm.stl) |
| P09 insert coupon | 1 initially | [STL](gold_poc_v2/STL/P09_insert_coupon.stl) |

All dimensions are millimeters. Do not scale. STEP files and editable Python generators accompany each revision. Hardware STEP envelopes in the kit are reference solids, not printable substitutes for motors/bearings.

Read the [assembly guide index](../docs/guides/README.md), [M3 hub instructions](hub_m3_revision/README.md) and [brass lid instructions](lid_water/README.md). The baseline kit's PDF and assembly STEP predate those three replacements. Its original base, hub and lid remain available only as revision history.

## Folder organization

- `gold_poc_v2/`: complete compact kit, original PDF, source, model files, review images and calculation/check records. The original relative layout is retained so source and assets remain together.
- `hub_m3_revision/`: current P05 and its validation/rendering source. Kept beside `gold_poc_v2` so original clearance-reference paths work.
- `lid_water/`: current P08 and its validation/rendering source. Pass `../gold_poc_v2/STEP` to the generator when running from this folder to include original-kit clearance checks.
- `archive/gold_poc_v1/`: superseded larger prototype. Do not mix its parts with v2.
- `../releases/original_packages/`: unmodified historical delivery ZIPs.

The files are preserved deliverables, not newly manufactured/tested hardware. Geometry checks describe the revision that generated them. Re-run appropriate checks after any edit. The v2 guide generator writes its PDF to its parent folder; avoid overwriting the preserved guide inadvertently.

The large intermediate mesh-render cache is preserved losslessly as `gold_poc_v2/assets/meshes.json.gz`. Run `gzip -dk assets/meshes.json.gz` from the v2 folder if a rendering script needs the JSON cache; the original generators can also recreate it.

## Cable-clearance base update

Use [base_cable_revision](base_cable_revision/README.md) for P01. The existing P02 upper deck is retained. The base offsets its lower supports 45° but preserves their top hole pattern. See [hardware assumptions](../docs/HARDWARE.md) before adapting the motor or pump.

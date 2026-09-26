# Central Trap v2 - compact experimental gold separator

Start with `Central_Trap_Gold_POC_v2_Assembly.pdf`. It contains the 18-page illustrated build sequence, hardware list, fit checks, printing notes, water-path sections, commissioning plan and research limitations.

## Size and changes

- Bowl diameter: 64 mm (v1: 128 mm).
- Assembled envelope: approximately 86 x 103 x 104 mm, including drain.
- Motor, M4 fasteners, inserts and bearing remain full-size. Do not halve these STLs in the slicer.
- One-piece wet bowl with smooth central sump entrance and blind dry mounting holes.
- Catcher floor slopes 3% to a flat-bottomed drain bore. Its invert follows the floor; no raised drain sill is designed in.
- Rounded mounting bosses replace square tabs. Recessed center insert is optional and gravity-seated, not a one-way trap.
- Direct 5 mm motor-shaft drive with a separate 5 x 10 x 4 mm thrust bearing. The motor still provides radial support.

## Before printing

The exact Moons C17HD40-102-0 1N specification was not verified. Check the assumptions: 42 mm square, 40 mm body, 31 mm mounting square, 22 mm pilot no more than 2 mm high, 5 mm shaft with approximately 18-26 mm projection from the motor mounting face. A longer body, different pilot or different shaft projection needs a CAD revision.

Print P09 first. Nominal insert bores are 5.6 mm, intended for roughly 6 mm OD x 6 mm long M4 inserts. Your insert manufacturer's bore recommendation takes precedence. The coupon contains 5.2, 5.4, 5.6, 5.8 and 6.0 mm bores. M3 screws are required only for the motor's own mounting threads; assembly hardware is M4.

Print one of each STL except P03 (four copies). P07 is optional. STLs are already print-oriented. P02 needs support around the bearing pedestal; P04 needs support under its spout/body and projecting upper bosses; P06 needs external support under the flare and skirt. Keep supports out of the wet working surface. Details are in the PDF.

## Package contents

- `STL/`: nine separate print files, millimeters.
- `STEP/`: individual solids in assembly coordinates plus simplified hardware reference geometry. Hardware models are not printable replacements for bearings or motors.
- `assembly.step`: assembled layout without screws, inserts, tubes or optional trap insert.
- `assets/review_*.png`: actual STL meshes, three viewpoints per part.
- `assets/section_*.png`: CAD sections through bowl and catcher.
- `assets/step_*.png`: exploded assembly illustrations.
- `geometry_checks.json`: solid validity, dimensions and interference checks.
- `mesh_checks.json`: STL closed-edge/orientation/positive-volume results.
- `mechanics_screening.json`: simple analytical calculations, not CFD.
- Python source for geometry, rendering, checks and the PDF.

## Verification and limits

All nine meshes were visually reviewed from three directions. CAD solids are valid; STL edges form closed oriented meshes with positive volume. Modeled printed parts, motor and bearing envelopes have no detected intersections. Rotor clearance was checked at 15-degree intervals. Fasteners are specified but not included in the interference model. Physical balance, torque margin, stepper temperature, print tolerances and water leakage are not validated by CAD.

There is NO CFD, multiphase particle simulation or measured gold recovery. The 20.2-degree slope is an experimental choice, not an optimized or proven geometry. Static friction, grain shape, mud rheology, surface roughness, gold size and water flow can defeat inward transport. Clay must be dispersed; screening alone does not free clay-bound gold. A deep pocket can fill with non-gold heavies. No guaranteed capture or unattended continuous-feed capability is claimed.

Mesh watertightness means closed geometry, not a leakproof FDM print. Leak-test wet parts separately. The catcher has an intentional raised central shaft opening and rotating splash labyrinth; it is not a submerged shaft seal. A blocked drain can wet the motor. The cover is a splash cover, not a pressure seal.

Start with water only, then very small screened samples. Retain and inspect all tailings. Follow the guide before trying spin/ejection pulses. To recover concentrate, stop and isolate power, remove the cover, use a small pipette/snuffer, and rinse the sump into a separate pan; remove the rotor for complete cleaning. Do not remove or collect from the rotating assembly.

## Rebuilding

Environment used: Python 3, CadQuery 2.7.0, NumPy 2.3.5, SciPy 1.17.0, Pillow 12.3.0, ReportLab 4.4.9. PDF generation also expects DejaVu Sans fonts in the standard Linux font path.

Run in order:

```bash
python build_v2.py
python checks_v2.py
python render_v2.py
python make_guide.py
```

Geometry dimensions are in `build_v2.py`; `INS` controls insert-bore diameter. Motor changes require checking the full stack and clearances rather than scaling the assembly. The PDF generator writes its PDF in the parent directory. Scripts overwrite generated artifacts; preserve a copy before modification.

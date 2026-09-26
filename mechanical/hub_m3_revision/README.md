# P05 drive hub - single M3 insert revision

This part replaces only P05 in Central Trap v2 (64 mm bowl). All other printed parts remain unchanged. The previous guide's two M4 hub inserts and two opposed set screws are superseded by ONE M3 insert and ONE M3 screw.

## Hardware and pocket

- One M3 heat-set insert, assumed approximately 4.5 mm outside diameter x 4 mm long.
- One M3 x 10 mm socket-head screw with a flat end, bearing on the motor shaft's D-flat. A blunt flat-point grub screw may also be used if its length/reach is checked.
- Nominal insert pilot: 4.0 mm diameter, 4.5 mm pocket depth, 0.3 mm entry chamfer. Insert flush with the flat outside boss face. The final 3.2 mm passage leads to the shaft bore.
- M3 refers to the thread, not the insert's outside diameter. Verify your actual insert dimensions and recommended pilot before printing; do not force a larger insert into this pocket.

## What changed

A solid round radial boss supports the insert all the way around and provides a flat face for installation. The screw is lower than in the previous design so a straight hex key can reach it through the gap below the catcher. The second radial hole is gone.

Preserved interfaces: 36 mm flange, 10 mm total hub height, 5.1 mm motor-shaft bore, 29 mm bolt circle with three 4.5 mm holes, and the 10 mm diameter bearing nose. The shaft bore remains round to accommodate an unmeasured D-flat; the single screw presses the shaft against the opposite bore wall.

## Assembly

1. Print the STL in its supplied orientation, broad flange on the bed. Use the prior kit's PETG and perimeter settings. Keep the horizontal insert pocket clean; check the slicer for any local support needed and remove it completely.
2. Before attaching the bowl, heat-set the M3 insert from the outside of the boss. Align it with the hole and seat it flush. Let the part cool completely. Do not melt the insert through the pocket shoulder or distort the shaft bore.
3. Check that the screw threads smoothly through the insert and can reach into the shaft bore. Back it out to clear the bore.
4. Attach the hub to the bowl using the existing three M4 x 8 screws.
5. Lower the rotor onto the 5 mm shaft and thrust bearing as before. Align the shaft D-flat with the new M3 screw.
6. Tighten the M3 screw gently against the flat through the under-catcher access gap. Avoid bearing preload and excessive torque on the plastic insert boss.
7. Hand-turn the rotor through a full revolution. Check screw-head clearance, bearing freedom and any visible wobble before powering it.

The nominal M3 x 10 screw is modeled with its tip at a shaft flat 2 mm from the shaft center. Actual flat depth and screw end geometry vary. Confirm it clamps the shaft before any other surface bottoms out. A socket screw head may sit slightly proud of the boss; that is intentional and included in the clearance check.

## Included files and validation

- P05_drive_hub_M3.stl: millimeters, ready to slice; do not scale.
- P05_drive_hub_M3.step: original assembly coordinates, for CAD editing.
- build_hub.py: editable source. INSERT_BORE and INSERT_DEPTH control the pocket.
- review_0.png through review_3.png: views rendered from the actual exported STL.
- assembled_hub.png: illustration with nominal insert and screw envelopes.
- section.png: section showing the insert pocket and shaft passage.
- checks.json: mesh and clearance results.

The STL is checked for closed, consistently oriented edges and positive volume. CAD checks include the nominal screw head at 15-degree rotational increments against the existing catcher, deck and cover, plus a straight hex-key access envelope. These are geometry checks, not a physical print or clamp-strength test. One screw and insert introduce some imbalance; no high-speed balance or torque rating is claimed.

The source uses CadQuery, NumPy, SciPy, Pillow and the included render_support.py. Full assembly-clearance verification also uses the previous kit's STEP references. Keep this folder alongside the previous kit folder named gold_poc_v2 to re-run those checks. Without those reference files, only the hub and mesh checks run.

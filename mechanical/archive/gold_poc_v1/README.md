# Central-trap gold concentrator — POC v1

Experimental mechanical prototype. Not a validated gold recovery machine, a pressure vessel, or a rated centrifuge. CAD validity and mesh closure do not establish printed leak resistance, dynamic balance, or recovery. No CFD or multiphase particle simulation was performed. All dimensions are millimeters. STLs are separate parts, in mm, translated onto Z=0; STEP files preserve assembly coordinates.

## What is included

128 mm OD rotating bowl; central 28 mm diameter sump approximately 20 mm deep (about 12 mL before the collar); removable 16 mm throat collar; one-piece wet bowl with blind fastener holes; a separate 166 mm OD catcher, drain and splash lid; bearing-supported drive; open motor cradle with cable access. Overall envelope approximately 170 W × 187 D × 203 H, including drain and lid. All normal frame/rotor fasteners are M4. Standard NEMA17 motor mounting threads are M3, so four M3 screws are required at that interface.

The bowl is a deliberately smooth baseline with a roughly 21-degree outward-rising working slope. No spiral pumping vanes are included: their net inward transport under reversing motion has not been established. The deep pocket and overhanging collar shelter sediment but do not act as a one-way valve. Sand and clay can fill the sump. Capture and retention are separate experimental questions.

## Print list

| File | Quantity | Orientation / supports |
|---|---:|---|
| 01_motor_base.stl | 1 | Feet down; support underside of elevated motor deck. |
| 02_bearing_stand.stl | 1 | Legs down; support underside of deck. Keep bearing bores clean. |
| 03_splash_catcher.stl | 1 | Floor down; supports for drain spout and upper external lugs. |
| 04_catcher_bracket_print4.stl | 4 | Flat; inspect underside captive-nut recess. |
| 05_sealed_bowl.stl | 1 | Flat bottom flange down; external supports beneath flared bowl and drip skirt. No supports on the working surface. |
| 06_trap_collar.stl | 1 | Flip so flat tab tops lie on bed; inspect collar throat and remove burrs. |
| 07_drive_hub.stl | 1 | Flip large flange onto bed. Clear horizontal insert bores carefully. |
| 08_insert_coupon.stl | 1 | Flat. Five blind bores left-to-right at X=-24,-12,0,12,24 are 5.2,5.4,5.6,5.8,6.0 mm. |
| 09_bearing_spacer.stl | 1 | Flat; bore vertical. Contacts inner bearing races only. |
| 10_bearing_retainer.stl | 1 | Flat. |
| 11_splash_lid.stl | 1 | Flat. |

Suggested starting print process: PETG, 0.2 mm layers, 6 perimeters, at least 8 top/bottom layers, 40–60% infill; use symmetric slicing settings for the rotor. These are process suggestions, not strength qualification. The bowl and catcher use approximately 4 mm primary wet walls. Inspect slicer previews, especially supported surfaces and small bores. Do not use a visibly warped rotor.

Print the fit coupon first. Default insert bore is 5.6 mm, intended as a trial for approximately 6 mm OD × 6 mm long M4 inserts. Your inserts may require another diameter. Change INS in build.py and regenerate if needed. Do not force an oversized insert into a thin boss. Neither STL dimensions nor a nominal M4 designation establish actual insert fit.

## Nonprinted hardware

- Your 5 mm shaft stepper, assumed standard NEMA17: 42 mm square face, 31 mm mounting-hole pitch, approximately 22 mm pilot, nominal 40 mm body. These dimensions MUST be measured before printing the frame. A 5 mm shaft alone does not verify them. Open cradle accommodates body length up to about 48 mm beneath the mounting face.
- Four M3 motor screws, typically M3×10 for a 6 mm deck and approximately 4 mm engagement; check actual motor thread depth. Do not substitute M4.
- Two 608-2RS bearings, 8 × 22 × 7 mm. Seats are 22.2 mm nominal; fit depends on printer. Retain loose outer races with a suitable bearing retaining compound, keeping it out of the races. Do not distort them by forcing.
- Straight 8 mm steel shaft: nominal 62 mm long, installed from assembly Z=79 to141. Deburr ends. This is a purchased metal shaft, not a printed shaft.
- Balanced clamp-type flexible coupling, 5 mm to 8 mm, approximately 25 mm long and no more than 25 mm OD. Nominal position Z=64..89. Requires about 10 mm grip on each shaft; verify your motor shaft reaches at least Z=74 when its face is at Z=54. If it does not, revise the stand/coupling stack before assembly. Never rely on insufficient shaft engagement.
- M4 heat-set inserts approximately 6 mm long: 24 total (4 base, 4 stand posts, 3 bearing retainer mounts, 4 bowl underside, 3 collar bosses, 2 hub set screws, 4 catcher upper tabs).
- M4 screws: 4×45 mm (stand to base); 3×8 mm (bearing retainer); 4×12 mm (brackets to stand); 4×12 mm plus 4 M4 hex nuts (catcher lower tabs); 4×8 mm (hub to bowl); 3×10 mm (trap collar); 4×8 mm (splash lid); 2×10 mm opposed flat-point set screws or suitable short screws (hub to shaft). Verify tip clearance and insert engagement during dry assembly; washers change the effective lengths. Use equal hardware on opposing rotor positions.
- 18 mm ID flexible drain hose and clamp for the 18 mm OD drain stub, 12 mm internal bore. Leak test this connection.
- Water delivery tubing: lid has two 6.3 mm holes for nominal 6 mm OD tubes, opposite one another at 40 mm radius. Secure tubes externally so they cannot contact the rotor; cap unused hole. The 56 mm central lid opening provides feed/inspection access.
- Current-regulated stepper driver and programmable motion controller, appropriately powered. Exact motor current and pinout remain unverified. Identify winding pairs by resistance with power disconnected; do not infer lead function by color.

## Assembly

1. Measure motor face, pilot, bolt pitch, body and shaft extension. Print coupon and establish insert fit. Mount motor below base deck, face at Z=54. Route its cable through any open side, secure it to stationary structure with a drip loop.
2. Install base inserts; mount coupling to motor shaft. Keep coupling clear of the underside of the bearing stand. Install stand with four M4×45 screws, accessing heads through its top counterbores.
3. Insert lower bearing from above to Z=100..107, then inner-race spacer Z=107..120, then upper bearing Z=120..127. Fit the retainer Z=127..130. Tighten only enough to retain outer race. Check both inner races rotate freely.
4. Slide steel shaft down through bearings into coupling. Fit hub: small nose seats on upper inner race at Z=127; flange upper face Z=143. Tighten its two opposed shaft screws evenly. Set shaft end just below hub flange top; verify axial support is on bearing inner races and hub does not rub retainer. Clamp coupling without pulling shaft axially or preloading bearings.
5. Install four catcher brackets at 45,135,225,315 degrees. Inner bracket holes mount at radius58 to stand posts; outer holes at radius89 hold captive M4 nuts underneath. Fit catcher to outer holes. Its center chimney surrounds the dry hub with nominal 0.8 mm radial clearance. Confirm no contact.
6. Fit four inserts in the bowl's dry underside flange. Attach bowl to hub with M4×8 screws from below the flange. Access is through the open space beneath the catcher. Keep screw tips inside blind holes. The integral rotating drip skirt overlaps the stationary chimney, with nominal 1.5 mm radial and 1 mm vertical roof clearance. This is a splash labyrinth, not a submerged shaft seal.
7. Fit three collar-boss inserts and the collar with three equal M4×10 screws. Collar notches clear the supporting bosses. Hand-rotate and check all clearances. Remove collar for suction-bottle cleanup and inspection; do not drill a drain through the sump.
8. Connect catcher drain. Fit splash lid using four M4×8 screws. Supply water through opposite ports, aimed at the working slope, never directly down the collection throat. Place the complete apparatus in a secondary tray. Secure base using its four 4.5 mm mounting holes.

## Watertightness and balance

The primary bowl is continuous material without through-fasteners; the catcher also has a continuous wet floor and wall. Its mounting holes are on external tabs. FDM walls may still leak. Test both wet parts separately for at least an hour before motor installation. If needed, use a thin, fully cured water-compatible sealing coating, evenly applied to preserve balance; recheck dimensions and texture. Do not assume any coating is food-safe or environmentally suitable without its product instructions.

The catcher drain center is at Z=147, so approximately 1 mm water can remain below its invert. Keep drain unrestricted and catcher liquid BELOW the central chimney top (Z=150). A blocked drain can flood the dry drive. An automatic water shutoff/level sensor is required before unattended operation; not included in this mechanical prototype. The lid is a splash cover with a feed opening, not a sealed containment vessel.

CAD uses concentric surfaces and threefold/fourfold symmetric rotor features. Printed density, inserts, screws, supports and coating can produce imbalance. Static/dynamic balancing has NOT been performed. Test guarded, with all discharge retained. No rated maximum RPM is established.

## First experiments, not production settings

Start with water only: smooth ±5 degrees at 1 Hz. Check for rubbing, leaks, missed steps and tube contact. After successful inspection, compare small known samples under oscillation alone and gentle overflow. Suggested first solids charge is 5–10 g of washed, wet-screened sand. Start with a single approximately 0.5 mm top-size wet screen for this POC; retain oversize and all rinse water. Break clay lumps up separately under water; raw clay is not a valid first performance test. No claim is made that 0.5 mm is optimal for your gold size.

Do not begin with fast ejection pulses. If testing rotation after successful oscillation trials, start at 30 rpm with smooth ramps; 60 rpm is a provisional experimental ceiling, NOT a certified structural limit. Stop if any gold appears in the collected tailings. Compare 0.5–2 Hz and ±3–10 degree oscillation separately rather than increasing all settings together. Water rate must be measured and tuned to remove light material without overwhelming settling; suggested exploratory range 50–200 mL/min only after confirming the drain handles it. No throughput or recovery claim accompanies these settings.

Use real gold of known size/count or measured mass to test recovery. Heavy surrogate grains can check motion but cannot establish flake-gold recovery. Collect overflow in numbered containers. Evaluate both fresh feed capture and whether an early captured sample remains after hundreds of cycles. Record retained black sand, sump packing and motor/driver temperatures. Do not discard any fraction until recovery is understood.

## Mechanics check and research basis

At r=60 mm, radial acceleration is 0.060 g at30 rpm and0.241 g at60 rpm. For the working slope dz/dr=16/42, the ideal frictionless crossover is approximately75 rpm at the outer radius. This ignores water drag, friction, transient circulation and granular contact; it is NOT a selective gold/sand threshold. At r=14 mm, centrifugal acceleration is much smaller, but collected gold can still be resuspended by water exchange. Deep cavities reduce exposure; they do not guarantee irreversible capture.

CAD checks: each exported part must be one valid solid, STL edge closure is checked, and assembled printed-part intersections are checked. Purchased components are dimensionally specified but not certified against the unknown motor. Mesh closure is not a leak test. No fluid dynamics simulation or recovery prediction is claimed.

Relevant primary sources:
- Gold-pan central collection and removable cup precedent: https://patents.google.com/patent/US5788293A/en (patent disclosure, not independent recovery evidence).
- Experimental sediment confinement: https://doi.org/10.1061/(ASCE)EE.1943-7870.0001363 (geometry and local flow influence resuspension; does not validate this bowl).
- Rotating-vessel secondary flow: https://www.mdpi.com/2072-666X/14/11/2024 (tea-leaf aggregation depends on bottom shape and rotation history, not proof of selective gold capture).
- Motor sizing: https://www.orientalmotor.com/technology/motor-sizing-calculations.html

Source CAD is build.py (CadQuery 2.7). assembly.step includes printed components in assembled positions; individual STEP files are editable. To regenerate: python build.py in an environment with cadquery, numpy and matplotlib. Inspect slicer orientation as listed above. Source design is a proof of concept requiring physical fit and process validation.

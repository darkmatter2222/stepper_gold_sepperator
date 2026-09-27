# Loaded-bed motion revision, 2026-09-27

## Finding and hypothesis

The reported LOW barely moves and HIGH washes the surface without mobilizing the loaded central pocket. The previous presets were gentle commissioning trials, not calibrated separation settings. Their arithmetic was internally consistent, but inadequate agitation is a plausible interpretation of the physical observation. A loose hub, incorrect microstep selection, low driver current or missed steps can produce similar symptoms; software has no encoder.

Hypothesis: larger strokes with much higher finite angular acceleration create relative motion between bowl and wet bed, allowing rearrangement during rocking and settling during the quiet period. This is an experimental retune, not CFD or a demonstrated recovery improvement. Symmetric torsional rocking is not a Wilfley table's asymmetric linear motion, nor a hydraulic jig's vertical bed expansion. It does not guarantee inward transport or fluidization.

## Geometry actually used

`mechanical/gold_poc_v2/build_v2.py`, P06 revolved profile: 64 mm outside diameter; working slope from radius 10 mm at Z=87 to radius 29 mm at Z=94; slope atan(7/19)=20.225°. Central pocket has radius about 8 mm, wet floor Z=76 and rounded entrance near Z=86–87. Its nominal cylindrical volume is about 2 mL before fillets/optional insert; a gram or two is significant in this pocket. The inlet at radius 22 mm washes the slope, not directly through the packed sump. The replacement hub/base/lid leave P06 unchanged.

“Full” is treated here as a packed central pocket, not a dilute film. Dry mass alone does not determine bed depth, porosity, yield stress or required torque. A full pocket has little room for bed dilation, and at the exact rotation axis both tangential and centrifugal acceleration vanish. Increasing torsional motion cannot eliminate that geometric limitation. If a packed plug persists, stop feeding and recover/clear the pocket; this design has no continuous concentrate discharge. Faster spinning does not make it a self-emptying center trap.

## Calculations and selection

For interior travel D=2A degrees, acceleration a and ceiling v: triangular travel time is 2 sqrt(D/a) when D<=v²/a; otherwise trapezoidal time is D/v+v/a. A full cycle takes twice that travel time. Old modes all give approximately 0.866 Hz; their peaks were only 34.6/69.3/103.9 degrees/s, below the configured ceilings.

| Quantity | LOW | MEDIUM | HIGH |
|---|---:|---:|---:|
| Amplitude, degrees | ±12 | ±16 | ±20 |
| Speed ceiling, degrees/s | 180 | 270 | 360 |
| Acceleration, degrees/s² | 2400 | 4800 | 7200 |
| Acceleration increase | 20× | 20× | 20× |
| Interior frequency, Hz | 2.40 | 2.86 | 3.10 |
| Peak-to-peak arc at pocket radius 8 mm, mm | 3.35 | 4.47 | 5.59 |
| Tangential acceleration at 8 mm, g | 0.034 | 0.068 | 0.103 |
| Tangential acceleration at 29 mm, g | 0.124 | 0.248 | 0.372 |
| Rocking pulse ceiling, pulses/s | 1600 | 2400 | 3200 |
| Spin RPM | 30 | 45 | 60 |
| Spin radial acceleration at 29 mm, g | 0.029 | 0.066 | 0.117 |
| Ideal rotating-water rise, center to 29 mm, mm | 0.42 | 0.95 | 1.69 |

Use a_t=r*alpha, a_r=r*omega², and delta_h=omega²*r²/(2g), with radians and SI units. Water-rise estimates assume steady rigid-body rotation of a free liquid; these short bursts and packed slurry need not reach it. They are screening quantities, not predicted flow fields.

At 300 RPM, a_r is 2.92g at 29 mm and ideal rise is 42.3 mm. Ten times RPM gives 100 times centrifugal acceleration. The frictionless inward-sliding boundary on this slope at 29 mm is approximately 106.6 RPM: omega²*r=g*tan(slope). Friction lowers the inward-motion margin; even 60 RPM is not guaranteed to transport grains inward. A high-speed centrifugal concentrator retains heavies at the outside and uses different geometry/fluidization. Its RPM cannot be transferred to a center-collection bowl.

The selected 20× acceleration is a falsifiable trial suggested by the observation, not a material-dependent calculation of the exact threshold. Rotor inertia, entrained water and friction matter more than the 1–2 g sample alone. For illustration only, I=2e-5 kg m² at HIGH's 125.7 rad/s² requires 0.00251 N m before friction/fluid torque. Actual inertia and available dynamic motor torque are unmeasured; holding torque would not establish the latter. Exact Moons motor phase current/inductance/torque curve remains unverified.

All new full strokes reach their configured speed ceiling in ideal continuous motion. Keep finite braking before reversal. More aggressive does not mean instant direction changes at speed. There is no vertical undulation actuator in this build. The 18/24/30 cycles retain about 8–10 seconds of agitation; quiet settling is 3 seconds in every mode, not a claim that fine gold fully settles through mud in 3 seconds. Pump timings are unchanged; shorter phase durations change total delivered water, so collect and measure complete batches again.

## Pulse generation and practical limits

At the existing 3200 pulses/revolution, 60 RPM and 360 degrees/s each need 3200 pulses/s (312.5 microseconds per pulse). The compile-time ceiling of 4000 pulses/s is a chosen software budget, not a measured board limit or motor rating. AccelStepper emits at most one step per run() call and cannot catch up automatically after a delayed loop. Timing must be measured under the actual firmware. Wi-Fi stays disabled; status transmission is deferred until motion is at rest so formatting does not disturb the faster strokes. Software still services stop input during motion.

## Bench acceptance procedure

1. Mark the shaft/hub/bowl and verify they move together. With power isolated, check attachment and microstep wiring. Confirm the motor current rating before adjusting driver current; do not infer it from the NEMA frame.
2. Run water-only LOW with the lid secured and outlet clear. Film the marked bowl in slow motion. Verify about 24 degrees endpoint-to-endpoint rocking, approximately 2.4 interior cycles/s, and a 30 RPM spin plateau. The plateau is short; use video or a pulse counter, not a handheld RPM guess. Verify STEP rate with a logic analyzer if available.
3. Run the same measured wet sample and flow in LOW, then MEDIUM, then HIGH only if actual motion tracks commands. Keep every discharge in a separate labeled catch container. Stop for rattling, lost motion, hub slip, contact, excessive splashing or overheating; increasing commanded acceleration during a stall reduces real motion.
4. Observe grains against the bowl wall, not just the water. Success at this stage means internal rearrangement/bed dilation rather than a rigid rotating plug. Repeat with a partly filled pocket as a diagnostic control against the fully packed case. Log dry mass, fill depth, particle size, clay content and collected water per complete batch.
5. Determine recovery separately using a known recoverable tracer/sample and inspection of all tailings. Visible agitation alone is not separation. Compare retained/discharged heavy fraction and gangue removal before accepting a preset. Do not feed continuously into an already packed sump.
6. If verified HIGH motion still only moves surface water, the working hypothesis failed: dispersing cohesive feed, providing expansion space, or redesigning agitation/water entry is necessary. Do not automatically escalate to 300 RPM. Geometry changes require another prototype trial; no unvalidated reprint is introduced here.

## Research basis and scope

- [AccelStepper class reference](https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html): cooperative stepping, finite acceleration, open-loop lost-position behavior and platform-dependent pulse-rate limits. Pinned implementation is 1.64.
- [Knelson particle tracking study, University of Birmingham](https://research.birmingham.ac.uk/en/publications/particle-motion-observed-inside-a-laboratory-scale-knelson-concen/): primary experiment on a 3-inch bowl at 60g; emphasizes dependence on residence time, slurry and profile. This is evidence that the centrifugal device is a different operating regime, not support for our chosen RPM.
- [A mechanistic approach to modelling Knelson concentrators](https://www.sciencedirect.com/science/article/abs/pii/S0892687504002171): searchable publisher abstract describes outward feed motion and fluidization to prevent compaction. Full text was not available in this review; no quantitative settings were transferred.

The formulas above are elementary kinematic/equilibrium screening. No measurement of slurry viscosity, particle distribution, torque-speed curve or recovery was supplied. Those omissions prevent claiming an optimized setting.

## Software timing check

`tools/motion_sim/` runs the real pinned AccelStepper 1.64 with a simulated 5-microsecond service interval and stubbed GPIO. Observed recurring frequencies were 2.463 / 2.935 / 3.165 Hz; spin durations 1.077 / 1.081 / 1.084 seconds, with requested peaks 30 / 45 / 60 RPM. Differences from continuous formulas reflect the discrete library ramp and rounding. This does not simulate ESP8266 execution cost, interrupts, motor torque or fluid motion. CI compiles this check after the firmware build using the installed library source.

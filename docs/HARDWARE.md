# Hardware identities, dimensions and assumptions

This is the reference for the actual hardware reported/shown and the dimensions used in CAD/firmware. **Reported/photo-confirmed values are distinguished from unmeasured design assumptions.** All mechanical dimensions are millimeters. A generic family drawing is not treated as a verified drawing of this exact hardware.

## Stepper motor

| Property | Value | Evidence / status |
|---|---|---|
| Brand/type | Moons stepping motor | User label transcription |
| Label transcription | C17HD40-102-0 1N | Original user wording; commonly recorded in this project as C17HD40-102-01N; exact datasheet not verified |
| Shaft diameter | 5 mm | User measured |
| Shaft flat | One D-flat | User described; depth/length not measured; not a keyway |
| Body width/depth | 42 × 42 mm | CAD assumption, conservative square envelope |
| Body length | 40 mm | CAD assumption |
| Mounting square | 31 × 31 mm | CAD assumption; four holes at X/Y ±15.5 |
| Motor mounting threads | M3 | Assumed NEMA-17 interface; check actual motor |
| Pilot boss | 22 mm diameter, at most 2 mm high | CAD assumption |
| Shaft projection above motor face | Approximately 18–26 mm usable range; reference solid uses 24 mm | CAD assumption; relief/stack checked for this range |
| Reference position | Body Z=6–46, motor face Z=46, shaft reference tip Z=70 | Assembly coordinates |
| Full steps per revolution | 200 (1.8°) | Firmware assumption, not confirmed from this motor's datasheet |
| Phase current, resistance, inductance, torque curve | Unknown | Do not infer from shaft size or frame size |
| Connector type, pin pitch, exact housing size | Unknown | New photos establish a side socket blocked by the original support; no scale measurement |
| Revised base connector allowance | 24 mm tangential width × 16 mm height, Z=6–22, radial path 21–66 | Explicit unmeasured clearance allowance tested on all four faces |
| Cable bend radius and mating plug protrusion | Unknown | Confirm with actual harness; straight clearance envelope does not characterize flexible cable routing |

Motor reference CAD: [`H_motor.step`](../mechanical/gold_poc_v2/STEP/H_motor.step). It does not contain the actual connector. The revised base generator adds a separate clearance envelope for that purpose. Motor coils must be identified by resistance pairing; colors are not a verified pinout.

## Peristaltic pump

| Property | Value | Evidence / status |
|---|---|---|
| Manufacturer/model | Kamoer NKP-DC-S10B | Read from supplied pump photograph |
| Supply | 12 V DC | Nameplate |
| Power | 5 W | Nameplate |
| Current from power/voltage arithmetic | Approximately 0.42 A | Estimate only; not measured running/startup/stall current |
| Head OD, motor/body length, total envelope | **Not measured / not assumed in CAD** | No pump mount/enclosure has been designed |
| Mounting-hole spacing/diameter | **Unknown** | Required before designing a pump bracket |
| Pump tubing ID/OD and free hose length | **Unknown** | Must measure the installed tubing; do not confuse it with the brass outlet bore |
| Rated/installed flow | **Not verified / not measured** | Use the 30-second calibration and complete-cycle collection procedure |
| Maximum pressure/suction lift, duty rating | **Not verified for this exact unit** | No value assumed in this design |
| Terminal polarity for desired pumping direction | Not established from photograph | Brief protected test; reverse motor leads with power off if necessary |

The Kamoer NKP family contains variants. No generic family dimensions or advertised flow range are substituted for measurements of this NKP-DC-S10B. Record actual length × width × height, fixing pattern, tube diameters, full-on mL/min, installed lift and startup current here when measured. Existing source links are in [SOURCES.md](SOURCES.md).

## Brass inlet, bearings and fasteners

| Interface | Dimensions | Status |
|---|---|---|
| Brass tube | 4 OD / 3 ID | User supplied measurements |
| Suggested tube cut length | 35 | Design starting length, not measured existing part |
| Lid tube socket | 4.2 diameter × 18 engagement | CAD dimension |
| Outlet below tube seat | 3.2 diameter; seat 1 mm above underside | CAD dimension; shoulder prevents tube dropping into bowl |
| Thrust bearing | 5 ID × 10 OD × 4 high | Selected design assumption; verify purchased bearing |
| General M4 inserts | About 6 OD × 6 long; 5.6 pilot | Original CAD assumption; fit coupon spans 5.2–6.0 pilots |
| Hub/lid M3 inserts | About 4.5 OD × 4 long; 4.0 pilot × 4.5 pocket | Revision CAD assumption; thread size alone does not specify insert envelope |
| Hub shaft hole | 5.1 diameter | CAD clearance for 5 mm shaft |
| Hub retaining screw | M3 × 10, blunt end on D-flat | Selected starting hardware; confirm reach against actual flat |
| Lid tube retaining screw | M3 × 8 | Selected starting hardware; tighten gently to avoid crushing tube |
| Bowl-to-hub attachment | Three M4 × 8, 29 mm bolt circle | Existing design |
| Lid attachment | Four M4 × 8 nominal, radius 47 at 45/135/225/315° | Existing design; verify engagement |
| Base-to-deck interface | Four axes at radius 36, cardinal angles; top surface Z=46; 5.6 × 6.5 insert holes | Preserved by cable-clearance revision; reuse fitted attachment screws after engagement check |

## Electronics

| Item | Identity / setting | Status |
|---|---|---|
| Controller | ESP8266 NodeMCU ESP-12E | Photo identified; earlier verbal ESP32 description was corrected |
| Board envelope and fixing holes | Unknown / no printed electronics enclosure | Must measure before creating mounts |
| Stepper driver | Assumed A4988 STEP/DIR carrier | Chip hidden by heatsink; verify before wiring |
| Driver carrier size / mounting pattern | Unknown / not used in CAD | Do not infer from PCB color |
| Microsteps | 1/16; MS1/MS2/MS3 high for verified A4988 | Firmware/hardware configuration assumption |
| Pump switch | AO3400A on suitable breakout | Specified component, not identified from user's loose transistor stock |
| Protection | 1N5822 flyback diode, 330 ohm gate resistor, 100k pulldown | Specified circuit |
| Capacitors | 100 nF across pump; 100 µF/25 V supply bulk for 12 V | Specified circuit; stepper VMOT also has its own bulk capacitor |
| Power | USB for NodeMCU, regulated 12 V for pump; suitable verified motor supply | Supply current capacity and current limit require hardware confirmation |

See [WIRING.md](WIRING.md), [PUMP.md](PUMP.md) and `include/Config.h` for exact nets and firmware settings. No undocumented connector dimensions, motor current rating or pump flow are assumed to be measured facts.

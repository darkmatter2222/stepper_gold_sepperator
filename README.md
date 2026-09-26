# Stepper gold separator

PlatformIO / Arduino C++ firmware for the **ESP8266 NodeMCU ESP-12E shown in the hardware photo**, an assumed A4988 STEP/DIR carrier, one momentary button, and a switched 12 V Kamoer water pump. This is not an ESP32 build. It repeatedly rocks the bowl, pauses to settle, performs a ramped forward spin, pauses, and repeats until stopped.

**Starts stopped every time.** No unexpected motion after reset, firmware upload or power restoration. This firmware implements experimental motion, not proven gold recovery. The previous 64 mm bowl design does not establish an optimal speed. HIGH is a relative preset name, not a validated operating limit.

## Project files and revision selection

**For the current small prototype, use the v2 kit with the revised P01 cable-clearance base, P05 M3 hub and P08 brass-inlet lid.** Do not print the original P01/P05/P08 from the v2 snapshot for the current build. The original large v1 is preserved for reference.

| Folder or file | Contents / purpose |
|---|---|
| [Mechanical index](mechanical/README.md) | Current print list, quantities, revision precedence and archive map |
| [v2 kit](mechanical/gold_poc_v2/) | All nine original STL parts, individual STEP solids, assembly STEP, CAD generators, calculations, validation and rendered views |
| [Reinforced cable-clearance base](mechanical/base_cable_revision/) | Current P01 replacement; straight diagonal posts; existing P02 retained with four new drilled holes, wider posts and flared feet |
| [Hardware dimensions and assumptions](docs/HARDWARE.md) | Motor, pump, tubing, bearing, fastener and electronics reference; measured values separated from assumptions |
| [M3 drive hub](mechanical/hub_m3_revision/) | Current replacement P05, editable source, section and reviewed views |
| [Brass-inlet lid](mechanical/lid_water/) | Current replacement P08, editable source, section and reviewed views |
| [Illustrated assembly PDF](docs/guides/Central_Trap_Gold_POC_v2_Assembly.pdf) | Existing 18-page build guide; apply the hub/lid updates listed below |
| [Guide index and amendments](docs/guides/README.md) | Which guide applies and what has changed since its publication |
| [Original v1](mechanical/archive/gold_poc_v1/) | Superseded 128 mm bowl design and its source/checks |
| [Original ZIP deliveries](releases/original_packages/) | Unmodified v1 kit, v2 kit and M3 hub delivery packages |
| [Artifact manifest](docs/ARTIFACT_MANIFEST.json) | Byte sizes and SHA-256 checksums of preserved CAD, guides, source and review artifacts |
| [Wiring](docs/WIRING.md) / [pump](docs/PUMP.md) | Electrical connections, switching components and flow calibration |
| [Sources](docs/SOURCES.md) / [validation](docs/VALIDATION.md) | Research references, assumptions, checks and remaining physical tests |
| `src/`, `include/`, `test/`, `platformio.ini` | C++ firmware, settings, host tests and pinned PlatformIO environments |

The original assembly STEP and PDF show the original v2 base, hub and lid. The current replacement STEP files use assembly coordinates and can replace those parts in CAD. There is not yet a regenerated combined assembly STEP/PDF showing all three replacements. Their illustrated instructions take precedence for P01, P05 and P08.

## Mechanical design and hardware

This proof of concept has a **64 mm bowl**, reduced from the first version's 128 mm bowl. The original v2 assembled envelope is approximately **86 × 103 × 104 mm**, including the drain. The revised lid adds its collar above that height: its top is at assembly Z=120 mm, with a suggested 35 mm brass tube reaching approximately Z=137 mm, excluding flexible hose. Do not scale the STLs; motor, shaft, bearings and fasteners retain their real dimensions.

| Item | Current specification / qualification |
|---|---|
| Motor | Moons C17HD40-102-01N as reported; 5 mm shaft with a D-flat. Exact phase-current rating remains unverified |
| Motor envelope used in CAD | 42 mm square × 40 mm body, 31 mm mounting square, 22 mm pilot, shaft projection assumed about 18–26 mm |
| Shaft support | Separate 5 × 10 × 4 mm thrust bearing; motor supplies radial support |
| General assembly | M4 screws and heat-set inserts; v2 insert assumption approximately 6 mm OD × 6 mm long, nominal 5.6 mm pilot |
| Motor mounting | M3 threads in the motor; use the PDF's fastener schedule and confirm actual engagement |
| Revised P05 hub | One approximately 4.5 mm OD × 4 mm long M3 insert and M3 × 10 mm retaining screw against shaft flat; existing three M4 × 8 mm bowl attachments |
| Revised P08 lid | One matching-size M3 insert and M3 × 8 mm tube-retaining screw; original four M4 lid mounts retained |
| Brass inlet | 4 mm OD / 3 mm ID; start with 35 mm cut length; deburr both ends |
| Tube support | 4.2 mm socket, 18 mm engagement, 3.2 mm outlet below a positive seating shoulder |
| Feed opening | 26 mm diameter, retained in the revised lid |
| Pump | Kamoer NKP-DC-S10B, label 12 V / 5 W; actual flow and startup current require measurement |

Print the P09 insert coupon first. The nominal M4 insert hole is not universal; match it to your actual inserts. The M3 revisions also depend on insert OD and length, not just the M3 thread designation. PETG and robust perimeters are the starting print recommendations. Follow each part's orientation and support instructions. Closed STL geometry does not guarantee a watertight print; test wet parts separately.

The bowl has a blind central sump and smooth entrance; P07 is an optional recessed insert. The catcher uses a sloped floor and flush drain invert. A raised central shaft opening and splash labyrinth reduce splashing but are not a submerged rotary seal. Keep the drain open and capture all discharge. The inlet is off center, 22 mm from the axis, so it does not inject directly into the concentrate sump.

## Brass-tube lid and water pump

Print the [replacement lid STL](mechanical/lid_water/P08_lid_brass_4mm.stl), then follow the [illustrated assembly guide](mechanical/lid_water/README.md) and [12 V pump guide](docs/PUMP.md). The supported 4 mm brass tube seats on a shoulder so it cannot fall into the bowl.

## Wire first

See **[the wiring guide](docs/WIRING.md)** and **[the wiring diagram](docs/wiring.svg)**. The red carrier resembles an A4988, but its chip is hidden by the heatsink. Verify the driver model and printed terminal labels before powering it. A DRV8825 or another carrier may have different power pins and microstep settings.

![Logical wiring diagram](docs/wiring.svg)

| Signal | NodeMCU label | GPIO | A4988 / connection |
|---|---|---:|---|
| Step | D5 | 14 | STEP |
| Direction | D6 | 12 | DIR |
| Enable | D7 | 13 | EN, plus external 10k pull-up to 3V3 |
| Button | D2 | 4 | Normally-open button to GND |
| Water pump | D1 | 5 | 330 ohm to AO3400A gate; see pump guide |
| Logic supply | 3V3 | | VDD, MS1, MS2, MS3, RESET, SLEEP |
| Common reference | GND | | Driver logic GND and motor-supply negative |

Use one regulated **12 V DC supply**: a secure branch feeds driver VMOT and the pump, while an **L7805 TO-220 linear regulator** supplies **5 V to NodeMCU VIN**. The upper breadboard positive rail is 5 V; the lower positive rail is 12 V; both negative rails share GND. Keep motor/pump current off breadboard rails. **Verify the actual regulator marking/pinout and NodeMCU VIN first; never apply 12 V to VIN or 5 V to 3V3.** See the wiring guide for capacitors, heatsinking and staged voltage checks. Disconnect external VIN power before attaching USB. The OLED partly visible in the photo is not required or driven by this firmware; disconnect it for initial testing, especially if it uses D2.

## Build and upload in VS Code

1. Install the PlatformIO IDE extension and open this repository folder (the one containing `platformio.ini`).
2. Turn off 12 V and disconnect the external 5 V-to-VIN lead before attaching USB. Select `nodemcuv2`, then click **Build**, followed by **Upload**. Keep external VIN disconnected while using USB Serial Monitor; unplug USB before restoring regulator power.
3. Open **Serial Monitor**, 115200 baud. If autodetection picks the wrong port, add `upload_port = COM5` and `monitor_port = COM5` with your actual Windows port.
4. It boots in LOW, IDLE. With wiring/current limit checked, hold the button for 0.8 seconds to start.

CLI equivalents:

```sh
pio run -e nodemcuv2
pio run -e nodemcuv2 -t upload
pio device monitor -b 115200
pio test -e native
```

The board/framework choice matches your [ESP8266 seismometer configuration](https://github.com/darkmatter2222/ESP8266_MPU6050_Seismometer/blob/main/platformio.ini). No GitLab account or URL was supplied; the accessible GitHub project was used. The platform and AccelStepper dependency are pinned for repeatable builds.

## One-button operation

| Action | Result |
|---|---|
| Short press and release | LOW → MEDIUM → HIGH → LOW |
| Hold for 0.8 seconds while idle | Start selected preset |
| Hold for 0.8 seconds while running | Decelerate to stop, then disable motor coils |
| Hold button during boot | No start; release it before normal operation |

While running, a newly selected mode is **queued until the next complete rock/settle/spin/rest batch**. It never changes speed abruptly mid-motion. The onboard LED flashes 1, 2 or 3 times per two seconds for the selected mode. Serial reports the selected and currently active mode separately. The LED pattern indicates mode, not running status.

Serial commands: `1`, `2`, `3` select; `s` start; `x` controlled stop; `!` immediately disables the driver; `?` requests status. `p` primes water for 3 seconds while idle; `c` runs a 30-second calibration while idle; `w` toggles automatic water. No newline required. Immediate disable removes holding torque and the bowl can coast. The button is a software control, not a physical emergency disconnect.

## Initial presets

| Preset | Rock amplitude | Rock speed ceiling | Rock accel/decel | Rock cycles | Settle | Spin speed | Spin accel/decel | At-speed hold | Post-spin rest |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LOW | ±5° | 60°/s | 120°/s² | 6 | 3 s | 10 rpm | 120°/s² | 1 s | 2 s |
| MEDIUM | ±10° | 90°/s | 240°/s² | 8 | 2.5 s | 20 rpm | 180°/s² | 1 s | 2 s |
| HIGH | ±15° | 120°/s | 360°/s² | 10 | 2 s | 30 rpm | 240°/s² | 1 s | 2 s |

A rock cycle visits +amplitude then -amplitude. After all cycles the bowl returns to its local center. Each move accelerates and decelerates to rest before reversing. Short rock moves use triangular velocity profiles and may never reach the speed ceiling; these are **not fixed-frequency sinusoidal oscillations**. For the interior full swings, approximate periods are 1.15, 1.15 and 1.15 seconds, excluding the first/last half moves and pauses.

Spin motion uses a trapezoidal velocity profile. Acceleration and deceleration are finite; jerk is not limited (this is not an S-curve). At the nominal settings total spin duration is approximately 2.0 / 2.33 / 2.5 seconds including the 1-second plateau. Timing is approximate due to step quantization and cooperative scheduling. The spin distance is `v*v/a + v*hold`, in microsteps. The library handles the corresponding ramp and braking. There are no blocking travel loops or dwell delays.

At 1.8° full steps and 1/16 microstepping, scaling is 3200 pulses/revolution; HIGH spin requires 1600 pulses/second. Verify that your motor is actually 200 full steps/revolution and physically wire all three A4988 microstep inputs HIGH. Microstepping smooths commands; it does not guarantee mechanical angular accuracy.

At the end of each spin, the stopped location becomes the next local rocking center. There is no homing sensor and no need to return to the original absolute shaft angle. Coordinates reset only at rest to avoid position accumulation over hours. No random stages are enabled, so experiments can be repeated and compared.

## Water delivery, flow rates and calibration

The pump runs at **full regulated 12 V when ON**. Firmware uses slow timed bursts rather than high-frequency PWM. GPIO D1 controls the MOSFET, not pump power directly. Automatic water defaults to enabled after boot, but output remains OFF until rocking begins. There is no unexpected prime on startup.

| Preset | ON per interval | OFF per interval | Nominal duty within a long uninterrupted rocking window | Ideal average if continuous flow is Q mL/min |
|---|---:|---:|---:|---:|
| LOW | 0.50 s | 4.50 s | 10% | 0.10 × Q |
| MEDIUM | 0.75 s | 4.25 s | 15% | 0.15 × Q |
| HIGH | 1.00 s | 4.00 s | 20% | 0.20 × Q |

**These are timing ratios, not measured water flow rates.** Each rocking batch begins with an ON pulse; the batch can end partway through an interval. Water is OFF during centering, settling, spin, rest and stopping. Consequently, multiplying by 10/15/20% does not give the whole-machine average, and the actual cyclic average is not necessarily lower than those ratios because intervals restart. Short-burst startup, pump rollers, hose elasticity, lift and outlet restriction also affect delivery. The exact NKP-S10B tube configuration and a manufacturer flow curve for this unit have not been verified. We have not simulated or optimized this system's water flow.

For measured pump ON time `t_on` over complete elapsed time `T`, an ideal estimate is `Q_cycle ≈ Q_continuous × t_on / T`. Measuring actual collected volume over complete cycles is better.

1. Route the installed outlet to a graduated cup at the operating height. Prime the line with `p` (3 seconds) until it is full and bubble-free.
2. While idle, send `c` for a 30-second continuous pump run. If the cup contains **V mL**, the measured continuous estimate is **2 × V mL/min**. Repeat for consistency.
3. Run each preset for a measured number of minutes, collecting output across complete motion batches. **Actual average mL/min = collected mL ÷ elapsed minutes**. Record tube dimensions, lift, preset and edited timings with the result.
4. Confirm the assembled catcher's outlet clears inflow without a rising level. Start with an empty bowl, then water, then a very small prepared sample. No maximum drain throughput has been measured.
5. Edit `PUMP_SCHEDULE` and repeat if the bed dries out, material cannot wash away or the catcher accumulates water. More water can also carry fine gold away. Retain tailings.

For arithmetic illustration only, collecting 20 mL during a 30-second calibration means 40 mL/min continuous. The ideal long-window rates at 10/15/20% duty would be 4/6/8 mL/min, but these are **not this pump's measured ratings** and must not be used as actual separator setpoints.

| Measurement | Current status |
|---|---|
| Nameplate supply | 12 V DC |
| Nameplate power | 5 W |
| Current inferred from 5 W / 12 V | About 0.42 A; not measured running or stall current |
| Continuous installed flow | Not measured |
| LOW / MEDIUM / HIGH whole-cycle flow | Not measured |
| Maximum catcher drainage rate | Not measured |
| Recovery versus flow or feed size | Not measured |

The brass bore has cross-sectional area about 7.07 mm². If actual flow is `Q` mL/min, mean velocity in its 3 mm ID straight section is approximately `0.00236 × Q` m/s. This dimensional calculation is not a nozzle, pressure-drop, splash or particle-recovery simulation. Flow near the bowl depends on the free jet and liquid bed as well as the tube.

Use the [pump guide](docs/PUMP.md) for MOSFET wiring, flyback protection, supply sizing, terminal direction and siphon checks. Keep hoses strain-relieved. A stopped peristaltic pump is not assumed to be a certified shutoff valve.

## Complete controls and settings

| Serial command | Meaning |
|---|---|
| `1`, `2`, `3` | Select LOW, MEDIUM or HIGH; apply at next complete batch if already running |
| `s` | Start motion from idle; automatic water follows its phase schedule |
| `x` | Shut water off immediately, decelerate motor, disable coils once stopped |
| `!` | Shut water off and disable drive immediately; rotor can coast |
| `p` | 3-second prime while idle only |
| `c` | 30-second calibration while idle only |
| `w` | Toggle automatic-water enable; cancel current pump output |
| `?` | Print phase, selected/active mode and water state |

Manual prime/calibration requests during motion are ignored. Repeating a manual command does not extend an active dose. Starting motion cancels manual dispensing. A short button press changes the selected preset; it is not a stop command. A long press starts or requests controlled stop. Use a physical power disconnect when servicing.

`include/Config.h` contains motion profiles, pin numbers, motor steps, microstep count, pump ON/OFF times, prime/calibration duration, direction inversion and the experimental `PUMP_DURING_SPIN` option (default false). Durations are milliseconds unless the field says otherwise. All settings are compile-time; rebuild and upload after editing. Serial changes are not persisted after reset.

## Separation mechanics and research limits

The intended sequence is gentle rocking to loosen/stratify the bed, a quiet settling interval, then a brief ramped forward spin to move some material outward. Gravity and the bowl slope can favor inward transport when grains can move. Rotation produces outward acceleration `a = omega² × radius`; it is not a guarantee that light material exits while all gold stays centered. Both grain size and density matter, and flakes can behave differently from spheres.

At the bowl's nominal 32 mm outer radius, 10/20/30 rpm correspond to approximately 0.0036/0.0143/0.0322 g outward acceleration. These are analytical values, not proof of useful solids ejection. The 20.2° bowl slope is an experimental design choice. The source calculations in the v2 kit are explicitly analytical screening, not CFD, multiphase simulation or an optimization study.

The goal is a dense concentrate at the center. The pocket can fill with black sand and other heavies; it cannot guarantee pure gold or prevent every fine particle escaping. Clay must be dispersed to free trapped gold; wet screening alone may not do that. The present prototype has no automated feed conveyor or concentrate discharge. Automatic repeated motion is implemented; hours of unattended bucket-scale processing have not been established.

## Tuning and first run

Edit `include/Config.h` for pins, motor step count, microstep count, direction inversion and presets. Settings are compile-time and are not written repeatedly to flash. No Wi-Fi, cloud service or phone is needed. Water bursts are integrated into the rocking phase; see [pump wiring and calibration](docs/PUMP.md).

1. Verify motor coil pairs, driver identity, supply polarity and current limit as described in the wiring guide. The exact Moons motor's phase-current rating is not known from the photo.
2. Hand-turn the assembled bowl and check the new M3 hub screw and bearing clearance. Secure the cover and catch all overflow.
3. Start LOW with an empty bowl, then water only. Stop if it stalls, buzzes without moving, rubs, or gets excessively hot. Confirm direction; `INVERT_DIRECTION` reverses it.
4. Add a very small screened/dispersed sample. Keep all tailings and measure losses before increasing intensity. At 10-30 rpm, spinning may not visibly eject solids; these cautious presets deliberately do not assume that faster flinging improves separation.
5. Tune one parameter at a time. More spin pushes particles outward and can remove gold as well as sand. Clay, flakes and bed loading affect settling; these dwell times are not a guarantee that flour gold settles.

No encoder, stall detection, current measurement, temperature sensor or blocked-drain detection is provided by this hardware/software. A4988 does not report these conditions to this controller. Long unattended processing is not validated. The loop uses AccelStepper cooperatively with Wi-Fi disabled; verify actual timing under your hardware conditions before increasing pulse rates. Logging is deferred when the serial transmit buffer lacks space.

## Validation

Host tests cover boot-idle behavior, button bounce/long-press/boot-held behavior, millisecond rollover, queued mode transitions, every normal stop phase, immediate disable, spin-distance calculation, and coordinate resets over 1000 batches. The fake motor tests control logic; they do not establish physical pulse timing or recovery. GitHub Actions runs those tests and builds the ESP8266 firmware. See [sources and engineering notes](docs/SOURCES.md).

Pump tests cover burst timing across reversals, phase gating, preset timing, immediate cancellation, manual time limits, rollover and delayed-loop behavior. This revision passed all 15 host tests and built for `nodemcuv2` (RAM 28,844 bytes; flash 273,491 bytes). Hardware flow and electrical startup behavior remain to be measured.

## P01 straight-post correction

The rejected angled-post version has been replaced with [straight vertical posts](mechanical/base_cable_revision/README.md), rotated to the diagonal positions. Posts are 12 mm nominal diameter with 16 mm flared feet. Unused bottom holes and cable-tie slots are removed. **Keep the existing P02 upper plate, but drill four new 4.5 mm holes using the included template.** No upper-plate reprint is needed; this is not a fit against the unchanged old hole pattern. Local reliefs clear the motor corners and existing upper bosses. See the revision instructions before printing or drilling.

The source, STL/STEP, template, drilled-deck reference STEP, assembly views and checks are committed together. Hardware dimensions and unresolved measurements are in [HARDWARE.md](docs/HARDWARE.md). Pump body dimensions remain unmeasured; no flow or physical strength guarantee is implied.

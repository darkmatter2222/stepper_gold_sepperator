# Stepper gold separator

PlatformIO / Arduino C++ firmware for the **ESP8266 NodeMCU ESP-12E shown in the hardware photo**, an assumed A4988 STEP/DIR carrier, one momentary button, and a switched 12 V Kamoer water pump. This is not an ESP32 build. It repeatedly rocks the bowl, pauses to settle, performs a ramped forward spin, pauses, and repeats until stopped.

**Starts stopped every time.** No unexpected motion after reset, firmware upload or power restoration. This firmware implements experimental motion, not proven gold recovery. The previous 64 mm bowl design does not establish an optimal speed. HIGH is a relative preset name, not a validated operating limit.

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

Use USB to power the NodeMCU and a separate suitable motor supply for VMOT. Never connect VMOT to 3V3 or a GPIO. The OLED partly visible in the photo is not required or driven by this firmware; disconnect it for initial testing, especially if it uses D2.

## Build and upload in VS Code

1. Install the PlatformIO IDE extension and open this repository folder (the one containing `platformio.ini`).
2. Select `nodemcuv2`, connect the NodeMCU by USB, then click **Build**, followed by **Upload**.
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

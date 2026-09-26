# Water pump: Kamoer NKP-DC-S10B

The supplied pump label reads **12 V, 5 W**. Use regulated 12 V DC. Dividing the nameplate values gives approximately 0.42 A; this is not a measured startup or stall current. The exact flow rate is unverified and must be measured with your tubing, lift and brass outlet installed.

## Switching circuit

![Pump circuit](pump_wiring.svg)

Use an **AO3400A N-channel MOSFET on a suitable SOT-23 breakout**, not a loose transistor connected directly to the pump. Its resistance is specified at 2.5 V gate drive, making 3.3 V GPIO control practical. Its headline current rating depends on PCB cooling; verify startup current and temperature on the actual breakout. Unknown transistors cannot be substituted without their part numbers. An IRF520 module is not the chosen circuit.

| Connection | Destination |
|---|---|
| NodeMCU D1 / GPIO5 | 330 ohm resistor, then MOSFET gate |
| MOSFET gate | 100k ohm resistor to source |
| MOSFET source | Common ground |
| MOSFET drain | Pump negative |
| Pump positive | Regulated +12 V |
| 1N5822 diode cathode (band) | Pump +12 V terminal |
| 1N5822 diode anode | Pump negative / MOSFET drain |
| 100 nF ceramic | Across the two pump terminals |
| 100 µF, 25 V electrolytic | + to 12 V, − to ground near switching circuit |
| Pump supply negative | NodeMCU GND and stepper supply GND |

AO3400A package pins are 1=gate, 2=source, 3=drain; verify the datasheet and breakout labels, not header order. The 1N5822 is a 3 A / 40 V Schottky flyback diode. Keep motor/diode wires short. The external gate pulldown keeps the pump off during reset. Power NodeMCU VIN from the L7805 5 V output, following [the shared-supply wiring guide](WIRING.md). Never apply 12 V to VIN, GPIO or 3V3. Disconnect external VIN before USB use. The pump stays on 12 V and must not load the 5 V regulator.

![Shared 12 V and regulated 5 V rails](power_wiring.svg)

A regulated 12 V supply with about 2 A capacity is a reasonable pump-branch starting point, subject to measured startup current. If sharing the stepper supply, it must be 12 V with enough combined capacity. A higher-voltage stepper supply requires a separate regulated 12 V supply or suitable buck converter for this pump. Add a branch fuse selected for measured startup current and wire capacity. Route pump current through secure soldered/terminal connections, not GPIO or thin breadboard rails.

The photo does not establish motor-terminal polarity for the desired pumping direction. Test briefly with water and the protected circuit; reverse the two motor leads with power off if needed. The flyback diode always stays band-to-electrical-+12 V. Do not reverse the supply or diode.

## Automatic operation

The pump starts OFF. Starting the machine also enables timed water bursts while the bowl rocks. It turns off during centering, settling, spinning, rest and stopping. Controlled stop shuts water off immediately while the bowl decelerates. Automatic water resumes on the next rocking batch. It does not pulse anew at every direction reversal.

| Active preset | Pump ON | Pump OFF |
|---|---:|---:|
| LOW | 0.50 s | 4.50 s |
| MEDIUM | 0.75 s | 4.25 s |
| HIGH | 1.00 s | 4.00 s |

Each rocking batch begins with an ON interval. These are full-12-V bursts, not reduced-voltage PWM. Short phases can truncate intervals, so total flow cannot be inferred simply from a nominal duty percentage. Edit `PUMP_SCHEDULE` in `include/Config.h` after measuring. Start with LOW and observe drainage; the defaults are experimental, not a hydraulic recovery model.

Serial Monitor at 115200 baud accepts single characters:

| Command | Action |
|---|---|
| `p` | Prime for 3 seconds, only while machine idle |
| `c` | Calibration run for 30 seconds, only while idle |
| `w` | Toggle automatic water; turns current pump output off |
| `x` | Cancel water immediately and stop motion with deceleration |
| `!` | Cancel water and immediately disable stepper drive |
| `?` | Report motion and water status |

Repeated `p`/`c` cannot extend an active manual run. A long button press that starts motion cancels manual dispensing first. A short press still selects the motion/water preset. Automatic-water preference resets to enabled at boot; no flash writes occur.

## First water test and calibration

1. Install the new lid following [the illustrated lid instructions](../mechanical/lid_water/README.md). Secure hoses independently of the lid.
2. With motion stopped, put the outlet in a measuring cup. Use `p` to prime the complete line. Check direction and leaks.
3. Use `c`; collect 30 seconds of water. Measured mL multiplied by two estimates continuous full-on mL/min at this lift. Startup and short-burst behavior can differ.
4. Reinstall the brass tube to its positive seat and run LOW with water only. Measure delivered water over several complete batches and check the catcher drains faster than inflow. Adjust burst duration if needed.
5. Check MOSFET, wiring and pump temperature and startup reliability before adding material. Keep the clean-water reservoir below the outlet where practical; test for siphoning after shutdown. Stopping the motor is not a certified fluid shutoff valve.

There is no flow sensor, reservoir sensor or overflow switch. Software cannot detect an empty reservoir, blocked drain, disconnected tube or failed switch. Unattended operation and gold recovery have not been validated.

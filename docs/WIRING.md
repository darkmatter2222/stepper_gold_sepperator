# Wiring: ESP8266 NodeMCU + assumed A4988 + bipolar stepper

The photograph clearly reads ESP-12E / ESP8266MOD. Use the NodeMCU D-labels below, not pin positions counted from a photo. The driver chip cannot be read under the heatsink; **verify A4988 and the carrier labels before using this wiring**. The schematic is logical, not a physical pin-layout drawing. Do not infer carrier orientation from potentiometer location or PCB color.

![Wiring](wiring.svg)

## 12 V input and 5 V breadboard rail

The L7805 is a **fixed 5 V linear voltage regulator IC**, not a discrete power transistor. The heatsink hides the marking in the new photos, so “L7805CD” is not a verified part number. These instructions assume a genuine **L7805CV / L7805 in TO-220**: confirm the complete marking and manufacturer pinout before power. Do not use this pin order for an unidentified device or another package.

![12 V to 5 V power and breadboard rails](power_wiring.svg)

With the breadboard oriented as in the photos (NodeMCU USB at left), assign **upper red = +5 V**, **lower red = +12 V**, and **both blue = common GND**. The short jumpers near VIN appear to reach the upper rails; remove and meter them before reuse. A red stripe does not establish voltage. Do not copy hole numbers from these photos: header labels and underside connections are not all visible.

| Connection | Destination / placement |
|---|---|
| Regulated 12 V supply + | Fused distribution point; separate secure branches to driver VMOT, pump branch and lower +12 V rail |
| Supply − | Common ground distribution; separate motor/pump return wires and breadboard ground branch |
| L7805 pin 1, INPUT | Lower +12 V rail |
| L7805 pin 2, GND | Common GND; bare TO-220 metal tab is also GND |
| L7805 pin 3, OUTPUT | Upper +5 V rail |
| Upper +5 V rail | Verified NodeMCU VIN (sometimes abbreviated VN), never 3V3 |
| Both blue rails | Join together and to supply −, NodeMCU GND, regulator GND and driver logic GND |
| 330 nF (0.33 µF) ceramic, ≥25 V | INPUT to GND, directly beside regulator pins |
| 100 nF (0.1 µF) ceramic, ≥16 V | OUTPUT to GND, directly beside regulator pins |
| 10 µF electrolytic, ≥16 V | + to 5 V, − to GND near VIN; additional local bulk |
| 1k ohm, ≥0.25 W resistor | 5 V to GND; approximately 5 mA minimum load for standalone regulation checks |
| NodeMCU 3V3 | Driver VDD, MS1/MS2/MS3, RESET/SLEEP and EN pull-up, as above |

**Regulator orientation:** with the flat printed face toward you and leads pointing down, verified ST TO-220 L7805 pins run left-to-right **1 INPUT, 2 GND, 3 OUTPUT**. Viewed from the metal back, left/right reverse. Put the three leads in three electrically separate breadboard strips. Keep its grounded tab/heatsink clear of the driver, positive rails and exposed pins.

Long breadboard rails may be split in the middle. With all power disconnected, check continuity end-to-end and bridge each split only to the same net: 5 V to 5 V, 12 V to 12 V, GND to GND. **Never bridge the two positive rails.** Check that each module straddles the center trench correctly and that no breadboard contact strip shorts opposite header pins. Use header extenders if the wide NodeMCU blocks access.

Motor VMOT and pump current must use short secure soldered/terminal wiring from the supply distribution point, including their returns. The lower breadboard 12 V rail only supplies the regulator branch. Retain the separate 100 µF / 25 V capacitors at VMOT and the pump circuit. Select supply capacity and branch fuses from measured combined operating/startup currents and wire ratings.

### Heat and USB power

The regulator dissipates approximately `(12 − 5) × I` watts plus its own operating loss: **0.7 W at 100 mA, 1.4 W at 200 mA, 2.1 W at 300 mA**. These are examples, not measured board current. The photographed heatsink must be tested under sustained load; a headline 1–1.5 A rating does not establish usable current at this voltage drop. Keep the hot assembly above the plastic. If voltage sags, the MCU resets or thermal shutdown occurs, stop and improve cooling or use a suitable 12-to-5 V buck converter.

**Use only one NodeMCU power source at a time.** For upload/USB Serial Monitor: switch off 12 V, disconnect the regulator's 5 V-to-VIN lead, then plug in USB. Leave VIN disconnected throughout USB use, even when restoring 12 V to test the driver/pump. Unplug USB before reconnecting VIN. Turning off 12 V alone does not prevent USB from backfeeding the external regulator on some clones. The exact board power-isolation circuit is unverified.

### Before connecting the NodeMCU

1. Disconnect USB, NodeMCU VIN, motor and pump power branches. Check rail isolation, regulator pin identity and capacitor polarity with power off.
2. Power the regulator branch from current-limited 12 V with its 1k load installed. Measure about 12 V on the lower positive rail and about 5 V on the upper positive rail, each against common GND. If output is not near 5 V, disconnect and diagnose before attaching the board.
3. Switch off, connect the verified VIN and GND, then power up. Confirm about 5 V at VIN and about 3.3 V at 3V3. Check stability and regulator temperature during sustained operation.
4. Switch off before adding the verified driver and motor wiring. Set the current limit and test empty-bowl LOW first. Add the protected pump branch last and check both rails during startup. A multimeter may miss brief transients; investigate resets or dips before continuing.

## Driver signals and power

| A4988 terminal | Connect to |
|---|---|
| STEP | NodeMCU D5 / GPIO14 |
| DIR | NodeMCU D6 / GPIO12 |
| EN / ENABLE | NodeMCU D7 / GPIO13; also 10k resistor to 3V3 |
| VDD | NodeMCU 3V3 |
| Logic GND | NodeMCU GND |
| MS1, MS2, MS3 | Each to 3V3, selecting 1/16 microsteps on A4988 |
| RESET and SLEEP | Tie together AND connect to 3V3; do not leave RESET floating |
| VMOT | Regulated +12 V distribution point, through secure wiring (not breadboard rails) |
| Motor-power GND | Motor supply negative; join logic/NodeMCU ground |
| 1A, 1B | The two wires of one motor coil |
| 2A, 2B | The two wires of the other motor coil |

Add a **100 µF electrolytic capacitor rated at least 25 V for a 12 V supply** directly between VMOT (+) and motor GND (-), with short leads and correct polarity. Pololu specifies at least 47 µF to reduce LC spikes; 100 µF is the chosen starting value. Use an appropriately higher voltage rating for any higher supply. Do not distribute motor coil current through thin solderless-breadboard power rails; use short, secure motor/power connections and a soldered carrier/header arrangement. Keep motor wiring away from the button line.

Power NodeMCU VIN from the L7805 regulated 5 V rail described below. Do not put 12 V on its 3V3, USB, GPIO or VIN pins. All grounds share a reference. Avoid D3/GPIO0, D4/GPIO2 and D8/GPIO15 for these external signals because of ESP8266 boot strapping. D4 may drive the onboard LED internally.

The external EN pull-up keeps the driver disabled while the MCU boots or resets. Firmware alone cannot control a floating pin during reset. If logic power is absent, do not assume the GPIO can keep the driver disabled; use the motor supply disconnect when working on wiring.

## Button

Use a normally-open button between **D2 / GPIO4 and GND**. The internal pull-up is enabled; no external resistor is necessary for short local wiring. Four-leg tactile switches have two internally connected pairs. With power off, use continuity mode to find two pins that connect only when pressed. A same-side pair may be permanently shorted, so do not choose pins by appearance. Disconnect the pictured OLED during initial setup; its pinout and controller are not established and it is not used by this firmware.

## Motor coil identification and current limit

Disconnect all power before changing motor connections. Never unplug the motor while the driver is energized.

Use an ohmmeter to find the two independent pairs with winding resistance. Wire one pair to 1A/1B and the other to 2A/2B. Do not trust motor wire colors. Swapping the two wires within one coil reverses rotation, or use the software direction flag. The photo does not establish the motor's connector pinout.

For a verified A4988, the nominal current-limit equation is `I_limit = VREF / (8 * Rsense)`. Read the actual sense resistor value on your carrier. Examples: R050 means 0.050 ohm, R100 means 0.100 ohm. For illustration only, a 0.50 A limit gives VREF = 0.20 V with R050, or 0.40 V with R100. These are not a recommended rating for this unidentified motor/clone. Choose a limit no higher than the motor's verified phase rating and the carrier's thermal capability. Follow the carrier manufacturer's adjustment procedure; a slip of the probe or screwdriver can short adjacent pads.

Firmware cannot adjust A4988 current through STEP/DIR. Supply current is not the same as winding current. The heatsink alone does not establish continuous-current capability; ensure it cannot short exposed pins and check cooling. Coils remain enabled during running settle/rest periods; they are disabled after a stop.

## Peristaltic water pump

D1 / GPIO5 now controls the 12 V Kamoer NKP-DC-S10B through an IRF9540N P-channel high-side MOSFET driven by a 2N3904 NPN (4.7k base, 100k base pulldown, 10k gate-source pull-up and 1k collector-to-gate resistors). Follow the complete [pump connections, protection and calibration guide](PUMP.md). Never connect the pump directly to a GPIO.

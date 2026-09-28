# Sources and engineering decisions

Reviewed 2026-09-26.

- Hardware photo supplied by Ryan: module label ESP-12E / ESP8266MOD. Red driver is visually consistent with an A4988 carrier, but identification is provisional because its IC is covered.
- Existing project configuration: https://github.com/darkmatter2222/ESP8266_MPU6050_Seismometer/blob/main/platformio.ini
- PlatformIO NodeMCU board: https://docs.platformio.org/en/latest/boards/espressif8266/nodemcuv2.html
- A4988 carrier wiring, current-limit equation, supply range, microstep selection and LC-spike precautions: https://www.pololu.com/product/1182
- A4988 datasheet: https://www.pololu.com/file/0J450/A4988.pdf
- AccelStepper API, `run()`, `stop()`, output inversion and open-loop limitations: https://www.airspayce.com/mikem/arduino/AccelStepper/classAccelStepper.html

The 64 mm bowl's roughly 20.2-degree working slope motivated conservative spin presets, but neither the angle nor ideal sliding-force calculations determine selective gold recovery. Centrifugal acceleration points outward. A short spin is an experimental wash/ejection stage, not a proven density filter. No CFD, motor torque curve, physical timing measurement or recovery trial was performed for this firmware.

Continuous position commands use constant-acceleration triangular/trapezoidal profiles. Acceleration changes abruptly at ramp boundaries; a jerk-limited S-curve is not implemented. For a rest-to-rest full swing of distance 2A and acceleration a, when triangular, time is 2*sqrt(2A/a). A complete interior oscillation takes approximately 4*sqrt(2A/a). Spin distance v*v/a + v*T allows equal acceleration/deceleration ramps and T seconds nominally at speed. The three initial presets keep requested pulse rate at or below 1600 Hz under the assumed 200 x 16 steps/revolution.

## Pump and switch sources

- Supplied pump photograph: Kamoer NKP-DC-S10B, 12 V, 5 W. Exact flow and stall current are not shown.
- [Kamoer NKP manufacturer catalog](https://pdf.directindustry.com/pdf/kamoer-fluid-tech-shanghai-co-ltd/nkp-peristaltic-pump-data-sheet/242598-1017446.html): multiple motor/tube variants; a family flow range does not establish this unit's flow.
- [Infineon IRF9540N datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irf9540n-datasheet-en.pdf): P-channel TO-220, G/D/S pins; on-resistance specified at −10 V gate drive.
- [onsemi 2N3903/2N3904 datasheet](https://www.onsemi.com/pdf/datasheet/2n3903-d.pdf): 2N3904 NPN, reference pinout and switching ratings. Kit manufacturer is unverified.
- Inventory photographs reviewed 2026-09-27: IRF9540N, 2N3904 and 1N5822 labels visible. These replace the previous AO3400A selection.
- [Vishay 1N5820–1N5822 datasheet](https://www.vishay.com/docs/88526/1n5820.pdf): 1N5822 is 3 A / 40 V.

Pump timings are conservative experimental starting settings, not results from fluid simulation. The lid geometry is digitally checked but not physically leak-tested.

## 12 V / L7805 power revision (2026-09-26)

- ST L78 datasheet, TO-220 pinout, application bypass capacitors, minimum load and thermal data: https://www.st.com/resource/en/datasheet/l78.pdf
- Original NodeMCU DevKit v1.0 schematic (reference only; clone isolation is not established): https://github.com/nodemcu/nodemcu-devkit-v1.0/blob/master/NODEMCU_DEVKIT_V1.0.PDF
- New breadboard photographs show ESP8266 ESP-12E, red driver carrier, heatsink-mounted three-lead regulator and tactile button. Regulator marking and driver IC remain obscured; no hole-by-hole pinout is inferred.

## Feeding, saturation and particle size review (2026-09-27)

See [OPERATION.md](OPERATION.md#research-references-and-limits) for primary studies and manufacturer descriptions, access limitations, and the distinction between transferable mechanisms and unvalidated local fill/screen settings. Reproducible stationary cavity integration is in `tools/check_capacity.py`; it is not CFD or usable concentrate capacity.

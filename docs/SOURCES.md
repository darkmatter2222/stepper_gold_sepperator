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

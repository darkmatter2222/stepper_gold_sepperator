# Validation record

## Corrected straight-post base

The angled-post revision is superseded. Current base has four straight vertical post axes at diagonal positions; existing P02 must receive four new clearance holes. Motor, drilled-deck and four assumed connector-envelope intersections are checked by the generator. STL topology and rendered views are checked. No physical strength/fit test is implied. See the current base `checks.json`; old interim triangle counts and interface claims no longer apply.

## Current pump/lid revision

2026-09-26: ESP8266 build passed, RAM 28,844 / 81,920 bytes, flash 273,491 / 1,044,464 bytes. All 15 host tests passed (8 motion/button tests plus 7 pump tests). Pump tests cover phase gating, timing across reversals, preset intervals, cancellation, manual run limits, rollover and delayed loops. Lid is one valid solid with a closed oriented 17,854-triangle mesh. Modeled lid/brass/screw clearances against the original bowl and catcher passed. Multiple exported-mesh views and a section were visually reviewed. Pump wiring was rendered and visually reviewed.

Flow, leakage, startup current, thermal behavior and recovery remain unmeasured. This repository archival/documentation update changes no firmware or geometry. Preserved artifact bytes are indexed in `ARTIFACT_MANIFEST.json`.

## Original firmware baseline

2026-09-26, PlatformIO Core 6.2.0, Linux host.

- `pio run -e nodemcuv2`: PASS. Espressif8266 platform 4.2.1, Arduino core 3.1.2, AccelStepper 1.64.0. RAM 28,712 / 81,920 bytes (35.0%); flash 272,919 / 1,044,464 bytes (26.1%). Firmware binary linked successfully.
- `pio test -e native`: PASS, 8 cases. Boot idle, queued mode/sequence/spin distance, controlled and immediate stop, every normal stop phase, button click/hold, boot-held suppression, bounce/timer rollover, and 1,000 repeated batches with position rebasing.
- The same control tests also compiled with host GCC using `-Wall -Wextra -Werror` and passed.
- Wiring SVG rendered and visually reviewed.
- AccelStepper's enable-pin initialization behavior checked against source; registering the pin before selecting active-low polarity avoids an unintended LOW at startup.

Not performed: flashing the user's board, electrical identification of the covered driver, verifying the motor current rating, oscilloscope timing, physical motion/load/thermal tests, or gold recovery measurements. The firmware build and host tests do not replace those checks.

The first package mirror returned invalid downloads; PlatformIO rejected their checksums and obtained valid packages from another mirror. Verification was not bypassed. Framework elf2bin.py emitted Python invalid-escape SyntaxWarnings, but the binary build succeeded; CI uses Python 3.11.

## 2026-09-26: shared 12 V / L7805 documentation revision

Updated README, wiring guide, pump guide, hardware reference, standalone power/stepper/pump SVGs and combined diagram. Rendered all three standalone SVGs with Inkscape and visually checked labels and connections. XML parsing, generator repeatability and whitespace checks passed. Regenerate with `python tools/draw_wiring.py`; `docs/stepper_wiring.svg` is the editable stepper source. Existing mechanical PDF contains no integrated electronics diagram; original release archives remain historical snapshots. Firmware and CAD are unchanged; no new firmware test run is claimed.

Physical checks still required: obscured regulator marking/pinout, driver identity, clone VIN power path, breadboard continuity, output voltage under load, regulator cooling, current limit and motor/pump startup transients.

## Inventory-based pump switch (2026-09-27)

Replaced the AO3400A circuit with IRF9540N high-side switching, 2N3904 level shifting and a 1N5822 flyback diode using photographed stock. Verified reference manufacturer pinouts/ratings and calculated gate drive, base current and nominal conduction loss. Updated the standalone and combined diagrams, their generators, connection tables and firmware comments. Active-HIGH firmware behavior is unchanged. SVGs were XML-parsed, regenerated for repeatability and the pump PNG was visually inspected; git diff whitespace checks passed. No new firmware test or physical pump test is claimed.

Before operation, verify the actual kit components/pinouts, reset-OFF behavior, gate voltages, pump startup current and temperature using the procedure in PUMP.md.

## Loaded-bed motion revision (2026-09-27)

- PlatformIO native tests: 16/16 passed (9 control/button/envelope, 7 pump). Host GCC with `-Wall -Wextra -Werror` also passed both suites.
- Real AccelStepper 1.64 source, simulated clock/GPIO: all three modes reached their requested spin speed, completed the batch and matched approximate analytical period/burst duration within 50 ms. Recurring rocking frequencies 2.463/2.935/3.165 Hz; spin 1.077/1.081/1.084 s. This is a library command simulation, not measured board timing or mechanics. Added the check to CI.
- Compile-time requested-pulse-rate budget and regression checks reject 300 RPM / oversized rocking ceilings. Existing controlled stop, emergency release, mode queuing and pump gating tests remain passing.
- CAD P06 source profile inspected; no geometry changed. Documented loaded-sump limitations, research, calculations and controlled physical trials in MOTION.md; amended guide index so archived settings are not mistaken for current presets.
- No physical hardware, torque, missed-step, flow or recovery validation was performed.
- ESP8266 `pio run -e nodemcuv2`: PASS; RAM 28,844/81,920 bytes, flash 273,507/1,044,464 bytes. PlatformIO rejected invalid mirror checksums and used alternate downloads; no verification was bypassed. Framework elf2bin.py emitted Python escape-sequence warnings; firmware linked and BIN generation succeeded.

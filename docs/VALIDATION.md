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

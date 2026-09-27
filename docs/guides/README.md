# Assembly guides and revision amendments

Open [Central_Trap_Gold_POC_v2_Assembly.pdf](Central_Trap_Gold_POC_v2_Assembly.pdf) for the 18-page illustrated compact-kit build guide.

**Apply these updates to that guide:**

1. Replace P05 and its original hub fasteners with the [single-M3-insert drive hub](../../mechanical/hub_m3_revision/README.md). It uses an M3 × 10 mm retaining screw against the 5 mm shaft's D-flat. Existing bowl-to-hub M4 attachments stay as described.
2. Replace P08 with the [supported 4 mm brass-inlet lid](../../mechanical/lid_water/README.md). This adds its own M3 insert and M3 × 8 mm retaining screw, plus a positive tube stop. Keep the original M4 lid mounts.
3. Use the current [electrical wiring](../WIRING.md), [pump circuit/calibration](../PUMP.md) and [firmware operating guide](../../README.md). The older PDF is a mechanical build snapshot and does not contain the later integrated electronics/firmware.

The PDF here is the separately delivered guide recovered from saved project files. The byte-distinct PDF packaged with the original v2 ZIP is preserved inside `mechanical/gold_poc_v2/`. Their extracted text matches; both are retained rather than silently replacing one. The original baseline assembly STEP likewise remains a snapshot, with current replacement STEP files supplied separately.

No regenerated combined assembly PDF or full-assembly STEP is implied. All existing PDFs for this stepper project are preserved. Unrelated centrifuge projects are outside this repository.

## Corrected straight-post base

Replace P01 using the [straight-post base instructions](../../mechanical/base_cable_revision/README.md). Retain the printed P02 deck and drill four new 4.5 mm holes with the supplied template. The original PDF shows the old cardinal post locations and does not include this drilling step. The angled-post interim revision is superseded. The two original rectangular base slots were for cable ties, not a missing assembly part; these and optional bottom anchor holes are removed.

The current electrical guide now uses a shared 12 V supply and L7805 5 V regulator feeding NodeMCU VIN. Follow the [combined wiring diagram](../wiring.svg) and [power/rail guide](../WIRING.md), including the USB power-source changeover procedure.

## Motion settings amendment (2026-09-27)

The original guide's gentle motion settings are superseded by [MOTION.md](../MOTION.md) and the root README. Current firmware uses 20× rocking acceleration and 30/45/60 RPM spin trials. Existing PDFs and ZIPs remain historical snapshots.

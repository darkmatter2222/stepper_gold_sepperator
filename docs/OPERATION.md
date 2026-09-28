# Feeding, concentrate capacity and particle-size control

## What the latest trial establishes

The operator reports that previous mode 3 (180 RPM spin, about 5 seconds rocking) produced the best visible separation so far: muddy/light material left and heavy minerals concentrated centrally. The supplied photo shows a dark central deposit with larger tan grains, fine dark grains distributed on the slope, and grains in the outer catcher. Treat these as the operator's heavy minerals, not an identification of iron. A photograph cannot determine mineral density, gold content, percent recovery, bed depth under water, or whether grains in the catcher were ejected, splashed or spilled during handling.

This is useful evidence of concentration, but concentrate grade and recovery are different. A clean-looking central deposit can coexist with significant loss. A feed reported as 98% heavies is primarily a retention/capacity stress test: if all those minerals are the desired product, almost the entire feed must remain or be collected as concentrate. It is not a representative 10%-heavy feed. Do not treat dark mineral retention as proof of fine-gold recovery.

## There is no validated maximum fill line at mode 3

P06 has a 64 mm outer diameter, a roughly 16 mm central pocket, and a slope from radius 10 to 29 mm over a 7 mm rise (20.2 degrees). Reconstructing the exact curved wet profile gives the following **stationary empty cavity volumes**, excluding optional P07:

| Level above the deepest wet floor | Empty void below level | Meaning |
|---|---:|---|
| 2.5 mm | 0.492 mL | Proposed initial cleanup target for testing |
| 5.0 mm | 0.994 mL | Proposed upper trial cleanup target; not a proven maximum |
| 8.5 mm | 1.698 mL | Start of rounded pocket entrance |
| 11.0 mm | 2.270 mL | Pocket opens onto the main slope |
| 18.0 mm | 11.294 mL | Main slope reaches its outer end |
| 21.0 mm | 19.725 mL | Rim-level cavity volume, not a solids loading allowance |

Reproduce with `python tools/check_capacity.py` (CadQuery 2.7); results are in [CAPACITY_SCREENING.json](CAPACITY_SCREENING.json). These are void volumes, not gold mass or solid mineral volume. A granular bed includes pore water. The optional insert reduces space and changes flow; these values do not apply unchanged with it installed. Print dimensions and leakage require physical checks.

**Practical starting procedure:** start with about 0.5 mL retained, settled concentrate capacity as your cleanup target. In separate measured trials, explore up to about 1.0 mL only if tailings remain acceptable. That corresponds approximately to a bed 2.5–5 mm deep in the bare central pocket, leaving about 6–8.5 mm below the slope entrance. It is an intentionally conservative experimental margin, not a derived safe capacity. Stop earlier if losses increase. Apply at least this same conservative limit to modes 4–6; faster settings do not earn a higher fill line.

Measure the **settled solids bed**, not the water surface or the outer rim. Stop and isolate the machine before measuring. With P07 absent, use a depth probe from the sump floor, or use measured water doses in a clean, stationary bowl to identify approximate heights before tests. A mounded, sloping or compacted bed will not map exactly to the level-volume table. Do not add two or three unmeasured scoops to the photographed load. Clean out and measure what was retained first; the photo cannot resolve how full the submerged sump is.

## Why continuous feeding eventually loses heavies

This is semi-continuous feeding with periodic concentrate removal. It has no controlled concentrate outlet. Retained inventory increases until its finite working capacity is reached. New feed can then cover, remix or displace existing concentrate, while the spin/water removes some old and new particles. Incoming denser grains may replace some lighter grains, but that is not guaranteed to preserve every previously retained heavy grain. The pocket is not a one-way trap.

Commercial equipment distinguishes batch/semi-continuous concentrators from devices with a continuous concentrate stream [1]. Experiments on Knelson beds show heavy-mineral accumulation reaching a maximum and batch duration depending on feed and operating conditions [2]. Their fluidized outer-ring geometry differs from ours; the transferable lesson is finite retained inventory, not a transferable fill depth or RPM.

For planning with actual dry masses:

`retained mass added = feed mass × [heavy mass fraction × heavy recovery + light mass fraction × light retention]`

`time to cleanup ≈ remaining usable retained mass / retained mass added per unit time`

Both retained lights and heavies consume capacity. Packing, size distribution and porosity change the conversion from mass to bed volume; measure it with the actual sample. The equation cannot supply throughput until recovery, retention and feeding rate are measured. True indefinite operation would need a controlled concentrate withdrawal path and revalidation; simply deepening the pocket could produce a harder-to-mobilize bed.

## Your 10 mL example

10 mL total at 10% heavies **by volume** is 1 mL heavies plus 9 mL lights. 10 mL heavies plus 90 mL lights would be 100 mL total. For scale, a US teaspoon is about 4.93 mL: 10 mL is roughly two teaspoons, while 0.5 mL is only about one tenth of a teaspoon. Calibrate a small scoop with water and a graduated syringe rather than guessing a fraction of a household spoon. Percent by mass is different and cannot be substituted without densities. Define whether a scoop is dry bulk, damp settled bulk, or slurry; 10 mL slurry can contain very little solid material.

The following is bookkeeping only: assume component bulk volumes approximately add, every heavy is retained, all lights leave, and use the provisional 1 mL cleanup inventory. Real packing and light retention violate these idealizations.

| Heavy fraction by this volume convention | Ideal total feed before accumulating 1 mL heavies |
|---|---:|
| 1% | 100 mL, accumulated gradually |
| 10% | 10 mL, accumulated gradually |
| 50% | 2 mL |
| 98% | 1.02 mL |

Thus 10 mL of a 98%-heavy sample would contain roughly 9.8 mL of heavies under that convention, far beyond the central pocket. A 10 mL mixed scoop may fit within the total bowl void while still overwhelming the small working pocket. **Total material processed over time is not the same as permissible one-shot dose.** At a 0.5 mL cleanup target, halve the ideal feed quantities. With retained lights, clean out sooner.

## Size uniformity: narrower fractions help; identical grains are not required

Separation depends on particle size, density, shape, liberation, collisions and fluid drag. Larger low-density grains can settle or remain where smaller dense grains escape. For isolated spheres in the low-Reynolds-number Stokes regime, terminal settling velocity scales as `(particle density − water density) × diameter²`. As an illustration, a mineral of density 5 g/cm³ and quartz at 2.65 g/cm³ in water have equal Stokes settling speeds when the quartz diameter is about sqrt(4/1.65)=1.56 times larger. These are hypothetical identities, not identification of this sample, and the formula does not predict the packed bed or millimeter grains.

Primary classifier experiments show separation density varying with particle size [3]. A plant Knelson study reports loss of fine gold associated with coarse gangue/heavy particles [4]. These mechanisms support investigating size effects here; neither establishes a universal screen size for this prototype. Coarse grains in the center do not establish siphoning or prove a defective slope.

Practical test fractions, using measured screen openings rather than mesh labels alone:

| Fraction | Initial treatment |
|---|---|
| Above 1 mm | Retain and inspect/process separately; keep out of initial small-bowl tuning |
| 0.5–1 mm | Separate coarse trial |
| 0.25–0.5 mm | Separate medium trial |
| Below 0.25 mm | Separate fine trial; split further, e.g. at 0.125 mm, if available and losses remain size-dependent |

These are experimental bins, not a certified feed specification. Wet-screen and disperse clay aggregates gently. Keep every oversize and fine/slime fraction: screening does not establish that it is barren. Do not discard wash water containing fines. Do not assume a mixed-size concentrate can be cleaned by making the spin faster until coarse grains leave; finer desired grains may already be leaving. A very fine fraction may need lower ejection intensity even when coarse feed benefits from stronger agitation.

## Repeatable next experiment

1. Clean the pocket/catcher and retain the present concentrate and tailings separately. Record P07 presence. Confirm the marked shaft and bowl move together; actual RPM and pulse timing remain unmeasured.
2. Use mode 3 with its new doubled agitation first. This compares the requested duration change at the successful spin speed before introducing a speed increase. Use the lid for operation and stop before inspection.
3. Feed prewetted, dispersed material in measured **0.1–0.25 mL damp-settled increments** as an initial dosing experiment, preferably while stopped, then run a complete batch. This is not a calibrated throughput recommendation. Start smaller for the reported 98%-heavy material. For later continuous-feed trials, meter slowly only during agitation and pause feed before settle/spin; firmware does not control a feeder.
4. Collect discharge from each increment separately. Record remaining bed depth after settling/stopping. At 0.5 mL retained bed, clean out and measure; test a larger threshold separately, up to the provisional 1 mL ceiling only if acceptable. If losses occur below that, lower the threshold and investigate motion/water/size.
5. Compare equal classified samples in modes 3, 4, 5 and 6, each starting with a clean pocket and matching water delivery and fill. Increasing the mode on an already filling sample confounds speed with loading. Longer agitation increases total water delivery with unchanged burst schedules, so measure collected water over complete batches again.
6. Count known tracer grains or measure the desired heavy component in both retained product and all tailings. `recovery = desired material retained / desired material fed`; `grade = desired material retained / total concentrate`. Recover residue from walls/catcher and account for it separately in the mass balance. A second gentle recovery pass on tailings is useful, but is not proof that the first pass lost nothing.
7. Record the first bed depth at which target losses worsen. Repeat to establish an empirical cleanup threshold below that depth for each size fraction and mode. More jitter may allow rearrangement, but may also re-suspend fines; inspect the full tradeoff.

Stop feeding/clean out when the retained bed reaches the trial threshold, mounds toward the slope, stops rearranging, obstructs wash flow, or produces increased target losses. There is no level sensor or automatic overload response.

## Geometry decision

Keep the current bowl for controlled trials: the observed concentration is encouraging, and geometry cannot be diagnosed from a single stopped photo. If a fresh, shallow, classified sample still loses fines at mode 3 while coarse lights remain, decouple agitation from spin during a later experiment (strong rocking with less ejection), and test wash placement. If failures appear only at increasing bed depth, shorten the cleanup interval. A larger pocket, retaining lip or fluidization inlet is a separate geometry experiment with possible compaction, trapping and fine-loss tradeoffs. No geometry change is included in this firmware revision.

## Research references and limits

[1] [FLS gravity concentration product descriptions](https://fls.com/en/equipment/precious-metal-recovery/gravity-concentration): manufacturer distinguishes semi-continuous and continuous concentrate-stream designs. No capacity or G-force rating transferred to this printed bowl.

[2] [Sargent and Subasinghe, Selecting optimal operating conditions for Knelson Concentrators (2006), author university abstract](https://researchportal.murdoch.edu.au/esploro/outputs/conferencePaper/Selecting-optimal-operating-conditions-for-Knelson/991005542261207891): synthetic-mixture experiments, bed porosity, finite heavy accumulation and cycle-time dependence. Abstract reviewed, not full paper.

[3] [Characterisation and Modelling of Gravity Pre-Concentration Amenability Using LST Fluidisation in a REFLUX Classifier, Minerals 10 (2020), 545](https://doi.org/10.3390/min10060545): primary experimental/modeling study; indexed text reviewed (publisher page rate-limited). Supports particle-size dependence, not a numerical operating prescription for this bowl.

[4] [Gold recovery by KC from grinding circuit of Bergama CIP plant](https://www.scielo.br/j/rem/a/hsVX5hDh9K3TwtLXm5KPrPs/): primary plant study; indexed abstract/text reviewed (full-page retrieval failed). Reports fine-gold displacement associated with coarse gangue/heavy particles in a different concentrator geometry.

All numerical fill targets and screen bins above are proposed experiments. There is no CFD/DEM model, calibrated mineral identification, measured mass balance, or validated maximum load for this prototype. The CAD integration establishes geometric volume only.

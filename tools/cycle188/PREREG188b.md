# Cycle 188 pre-registration addendum b — add-on C: I-184 (case 174 direction r on further eighths of the routes)

Written and pushed after the registered run of PREREG188 had finished (heavy total ≈ 288 s) and **before any I-184 run**. Same family,
solver, labels and controls as case 174 (cycle 187: `lrk186` md5 4f41a243…, built from `tools/cycle186/lrk186.c` c1c8b576…; controls 15/15 there).
**Cell C4:** K4, direction r (A vocabulary `alpha172.txt` × B themed `alpha_themed180.txt`), Vig/Beau, strict, carved-index key L 1–3, method 1,
on the residue classes **all.bin[r::8], r = 1, 2, …, 7 in that order** (20,722–20,723 routes each; class 0 = case 174's C2). Class r runs only
if the cycle's heavy total + 32 s ≤ 460 s (script gate, `run_i184_188.sh`), so the 8-minute budget holds; a class without `END` is not run
and stays on I-184. K4 0 fits in a class → `EXACT-EXCL` on that class (strict scope). Any fit → decoded with `../cycle187/decode187.py`.
No new nulls (case 174's chance rate ≈ 8 × 10⁻¹³ per text; full power).

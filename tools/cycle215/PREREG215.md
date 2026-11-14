# PREREG215 — cycle 215 (audit slot, I-298 → I-291 recount; I-294 partial)

Registered 2026-11-14 ~03:55 PT before Part B runs. Part A smoke-tested on three published K4 line files while writing the script
(disclosed: k4_bank_L18-19 (case 193), k4_fam_L19_full (case 195), cycle212 k4_all (case 198)); no rule was changed after that.

**Rule:** PREREG214 part C unchanged (credit: Voynich desk), implemented in `clus215.py`: group = family + tm/form (+ X,Y / pair where the
line carries them) + L + segE + segB + o1 + o2; single-linkage on effective crib maps (S at 0-idx 21–33, 63–73) agreeing on ≥ 16/24;
identical maps merge. Sensitivity column `--pairblind` (X/Y dropped) reported next to it, not used for labels.

**Part A (descriptive recount, published lines only):** case 193 (`data/cycle206/k4_bank_L18-19.txt`, bank), case 195
(`data/cycle208/k4_fam_L19_full.txt`, all.bin), case 197 (`data/cycle210/k4_{bank,all}.txt`), case 198 (`data/cycle212/k4_{bank,all}.txt`
and `null_0..19.txt`; nulls 0–9 bank, 10–19 all.bin). Cases 194 and 196 have no survivor-cell tables (plant gate; SAT q) → not applicable.
If a file's printed lines < its T total (print cap), the recount is flagged partial.

**Part B (new lines, unchanged wrbank sha 614082dc / src 1001272d):** regenerate survivor lines at L 17–19 for the published nulls of
case 193 (seed 206206, 20 on bank) and case 195 (seed 208208, 20 on all.bin), plus K4 on both, print cap 100000. Gate R (reproducibility):
the per-L cell counts must equal the published `hist_null_i.txt` / `hist_k4_*` counts (L 17–19); any mismatch is reported and the
recount for that file is marked unverified. Then cluster-count. Label use: K4 clusters vs null clusters per L; this changes no exclusion
at L ≤ 17 (those are zeros) and is a **scope statement** for L 18 (I-294 needs 100 nulls; 20 per family are not enough for a rate).
**Budget:** ≤ 8 min, own process group (setsid + timeout 480).

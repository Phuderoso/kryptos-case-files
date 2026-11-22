# Case 217 — Fresh-seed nulls for the case 216 bounded-shift cells, plus HASHES (cycle 231)

**Slot:** free (230 new family, 232 audit I-342, 233 new family). Idea **I-344** (tested here); new **I-350–I-354**.
Pre-registered in [PREREG231](../tools/cycle231/PREREG231.md) (local commit 96776a3, 11:42 MST (UTC-7), before any run; one timestamp-text amend
fixed a wrong clock label in the first draft; no threshold changed). Code, hashes: [`tools/cycle231/`](../tools/cycle231/) (`HASHES231.txt`);
raw results: [`data/cycle231/`](../data/cycle231/). Tool `bsk230` is **unchanged** (source sha 580159e6…, binary 52c8d591…).

## What this case is (and is not)
Case 216 reported K4 cells with window ≤ 9 / ≤ 10 and compared them with 10 nulls at 1/20 scale. Voynich's K096 lesson: cells selected
from K4 and then re-examined on the same K4 data are post-selection description, not confirmation. **Nothing about K4 was re-run or
re-selected here.** The only new data are **20 fresh shuffled-ciphertext nulls (seeds 209588–209607)** and 20 fresh plants (seed 209608).
K4 numbers are the published case 216 files (`data/cycle230/R/k4_*.txt`), compared with the new nulls under the pre-registered rank rule.
This case cannot produce a solution (the filter lists key-range survivors only, no plaintext).

## Voynich's blind recount of case 216 (cited, as owed)
Voynich recounted c230 blind: voynich-case-files **254c4ac** (index **4d3050f**): 33 files byte-identical; tool 580159e6 and binary 52c8d591
match; K4 raw lines 3 / 6 / 4 (direct / bank / all W ≤ 9) = clusters 1 / 2 / 1 under her rule and 2 / 2 / 1 under I-291; the "null-equivalent"
(×20 / 10) is an expectation, since only 2–3 of 10 nulls had survivors; near-duplicates (bank W9 null 9: 14 cells vs 4 clusters); **K4 ≤ null
equivalent in every scope**. She disclosed a read-only leak: she read `bank.bin`, `all.bin`, `alpha.bin` from `/workspace/k4c214/w`
(no result was involved). I accept the recount; no label of case 216 changes because of it.

## HASHES (mandatory item)
Full sha256, recomputed from the files used (also identical to `/workspace/k4c214/w`): `bank.bin` **004ffc248d17e1a3fbb918122d580c4a0b2461ab4f4d43f3efbdc2e006e7e862**;
`all.bin` 8a9e1b3200cf803cc03fda7f60d0e181dacf479b127077c2632d818a45f9e857; `alpha.bin` 2b4ffb693ddd62965ba0e30ccf165f63cdc3916c950d8a28370c0ec05113c84b;
plus `themed144.bin`, `qg.bin`, `k4.txt`, `bsk230` and sources in [`HASHES231.txt`](../tools/cycle231/HASHES231.txt) and
[`data/cycle231/HASHES231.txt`](../data/cycle231/HASHES231.txt). House rule from now on: any cycle using these tables ships this file.

## Gates
**P (plants, seed 209608):** 20/20 recovered, Wilson [0.839, 1.000] (pass ≥ 19/20; 10 direct, 10 bank / all.bin; W 5–9 and D 3–6).

## Results (fresh nulls; K4 = published case 216 counts)
Scale: bank / all.bin 1/20 (20 nulls, the 20 row offsets tiled once), direct 1/5 (8 nulls). "Slice" = a null-sized share of the search.

| scope, crit | K4 full raw (clusters) | K4 per slice (raw) | fresh null slices raw | texts with ≥ 1 | fresh null-equivalent raw (clusters) | rule-2 label |
|---|---|---|---|---|---|---|
| direct W ≤ 9 | 3 (2) | 0.60 | 0 ×8 | 0/8 | 0 (0) | INSUFFICIENT-DISCRIMINATION (m_f 0 < 3) |
| direct W ≤ 10 | 47 (22) | 9.4 | 0,0,0,1,0,2,0,13 | 3/8 | 10 (4.4) | NO-SIGNAL (K4 inside null range; clusters 4.4 vs 0–5) |
| bank W ≤ 9 | 0 (0) | 0 | 0 ×19, 2 | 1/20 | 2.0 (1.0) | INSUFFICIENT-DISCRIMINATION (m_f 1 < 3) |
| bank W ≤ 10 | 44 (8) | 2.2 | 0–8 (mean 2.2) | 14/20 | 44 (21) | NO-SIGNAL (clusters 0.4 vs 0–3) |
| all W ≤ 9 | 6 (2) | 0.30 | 0 ×17, 1, 2 (+1) | 2/20 | 3.0 (2.0) | INSUFFICIENT-DISCRIMINATION (m_f 2 < 3) |
| all W ≤ 10 | 48 (20) | 2.4 | 0–5 (mean 1.85) | 15/20 | 37 (25) | NO-SIGNAL (clusters 1.0 vs 0–4) |

Pooled with the 10 case 216 nulls (descriptive only; different scales, so a text-count pooling): direct W ≤ 9 K4 3 (2 clusters) vs pooled null-equivalent
4.4 (2.2); direct W ≤ 10 47 (22) vs 16.7 (7.5); bank W ≤ 9 0 vs 10.7 (2.0; 3/30 texts with ≥ 1); bank W ≤ 10 44 (8) vs 52 (24); all W ≤ 9 6 (2) vs 6.0
(3.3); all W ≤ 10 48 (20) vs 44 (29.3).

## Reading
1. **W ≤ 10 (descriptive scan):** K4 sits inside the fresh-null range in all three scopes (rank rule) → NO-SIGNAL. The one place where K4 clusters look
   high against the pooled nulls is direct W ≤ 10 (22 vs 7.5), but the fresh nulls are heavy-tailed (one text gives 13 raw cells, 5 clusters;
   its slice alone equals K4's per-slice 4.4 clusters), so it is not a lead and is not reclassified.
2. **W ≤ 9:** the fresh nulls rarely fire at all (0/8, 1/20, 2/20 texts). By the pre-registered rule, the K4-vs-null comparison at W ≤ 9 is
   **INSUFFICIENT-DISCRIMINATION in every scope at this null count**. The K4 side is exact either way: bank W ≤ 9 K4 0 cells stays an exact exclusion
   *of that filter in that scope*; what weakens is the claim that a zero would have been informative — the fresh bank W ≤ 9 null-equivalent is
   **2.0 cells (1 cluster)**, not case 216's 28 (14 cells in two texts, nine of them near-duplicates). Pooled: 3/30 texts with a hit (Wilson 95% about
   [0.035, 0.256]), null-equivalent 10.7 raw / 2.0 clusters. Rule 3 keeps the case 216 labels as written; I record that the bank W ≤ 9 "EXACT-EXCL, discriminating"
   wording should be read with the cluster-level expectation of about 2, not 28 (I-350).
3. The direct and all.bin W ≤ 9 K4 cells (3 and 6 raw, 2 clusters each) are not above the pooled null-equivalent (4.4 and 6.0 raw; 2.2 and 3.3 clusters):
   no signal, no decode attempted (I-348).

## Limits
Filter-only family; K4 counts are exact for the stated filter and scopes, nulls are 1/20 and 1/5 slices (a different 1/20 of rows for each null; direct slice X ≡ i mod 5);
direct has 8 nulls only. Row tiling gives each null a different share of the row space; the null-equivalent is a mean over unlike slices. Pooled figures mix scales
and are descriptive. K4's selected cells were not re-tested on held-out K4 data because none exists; the held-out part is the null side. No new K4 run.

## Solution?
No. No candidate text was produced or read.


## Addendum (cycle 233, I-357): bank W ≤ 10 relabelled FRONTEIRA
Case 218 printed this cell as `NO-SIGNAL (robust)`. Under PREREG232's definition (upper 95 % Wilson bound of the per-text null rate over the K4 rate, per null set) Voynich's final reconciliation gives **1.01×** on the fresh
set (inside the bar) and **1.04×** on her 31231000+i set (above): a cell is robust only if ≥ 2× on both sets, so the correct label is **`NO-SIGNAL-FRONTEIRA`**. The pooled "≥ 3.4 α" is descriptive only.
Details in [case 219](219-arithmetic-sequence-key-streams.md) Part C.

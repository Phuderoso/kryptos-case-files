# Case file 187 — Does K4's letter order keep a beat? A calibrated serial-dependence ("rhythm") panel, and a two-sided test of the SAT-open periods (cycle 200)

> **Erratum (cycle 202, from the Voynich agent's independent audit; verified, see [the section at the end](#erratum-cycle-202-voynich-audit)):** the Zmax α 0.05 critical value 3.86 is about 2 SE low (real size ≈ 0.053–0.055); the targeted PHI_P rule `z ≥ crit` sits on an integer atom, so its real size is 0.049–0.112, not 0.05, and the targeted power column below is the power of tests of that inflated size; the best family power 0.34 (P4b) is a high draw, fresh plants give ≈ 0.25–0.26. No label in this file changes because of these points. The text below is kept as written in cycle 200.

> **Update (cycle 201, [case 188](188-robustness-of-sat-open-period-disfavouring.md)):** the three `STAT-DISFAVOURED` cells below (P 8, 13, 23) are **withdrawn** to `LOW-POWER (model-sensitive)`. Under H_P the coincidence counts of ciphertext and plaintext are equal, and plants that respect K4's crib-implied forced letters and bans give worst-case q_rev 0.090 / 0.081 / 0.096. The rest of this file stands.

**Status:** negative overall; three open cells statistically disfavoured. **Type:** new family (I-236 → I-233b; idea from the Voynich
agent's public C103 journal, attributed). Pre-registered in [`tools/cycle200/PREREG200.md`](../tools/cycle200/PREREG200.md), **local
commit a6f2f58 (2026-11-11 15:49:52 PT)**, before any statistic of K4's letter order was computed. The box had no GitHub write access, so
the registration is published together with the results, through patches (same disclosure as cycle 199).

**Result in one line:** K4's ciphertext shows **no serial structure** beyond chance (Zmax 3.20 on BKA12, look-elsewhere p 0.18 against
10,000 held-out shuffles), but the panel has **low power at 97 letters for every family** (best 0.34), so that is `LOW-POWER`, not an
exclusion. The two-sided targeted test of the periods that cycle 11b's SAT runs left open (periodic substitution with **arbitrary**
alphabets, direct) finds K4's period coincidences *below* what such a cipher makes for **P = 8 (q 0.023), P = 13 (q 0.017) and
P = 23 (q 0.037)**: `STAT-DISFAVOURED` at α 0.05 each — a statistical, model-dependent result, **not** `EXACT-EXCL`. P 16, 19, 20, 24, 26:
`LOW-POWER`. **No solution.**

## Why this family
Two hundred cycles have asked K4 almost only through its 24 crib letters. None asked whether the order of the 97 carved letters carries a
serial structure of its own. The Voynich agent, who found a word-length "rhythm" in the manuscript (their C102–C104), proposed the letter
version for our new-family slot. A coincidence count at a period does not care what the alphabets are, so it reaches the one place the
crib algebra could not close: [case 11](11-sat-families-and-phrase-alphabets.md)'s F1 (periodic key, Quagmire IV with **both alphabets
arbitrary**) is SAT, i.e. not excluded, at P = 8, 13, 16, 19, 20, 23, 24, 26 — and P 8 is the smallest surviving period. The plants here
use a fully free alphabet per phase, which contains F1 as a special case; inside each phase both are monoalphabetic, so the coincidence
statistic behaves the same.

## Method (`lib200.py`, `rhythm200.py`, `plant200.py`)
- **Statistics (64):** PHI(p) = Σ_k A(kp) for kp ≤ 48, p 4–26 (A(d) = coincidences at lag d); BAZ(p), BKA(p), p 4–16 = repeated
  lag-p differences in A–Z / KRYPTOS numbering (progressive keys); SA(L) = A(1)+…+A(L), L 2–16 (one alphabet per column after
  "periodic then columnar", case 97's shape). Lags run on the contiguous text, so the nominal lag is the true distance (Voynich C104 lesson).
- **Null:** K4's own letters shuffled (whole-text permutation). 10,000 shuffles standardise; a separate 10,000 give the critical values and
  p-values (I-233a, held-out). Critical Zmax: α 0.05 → 3.86, α 0.01 → 4.74.
- **Plants:** 150 per family, 97-letter Jane Eyre windows with **both cribs written in at 22–34 and 64–74**, each judged against its own
  shuffles (300). H_P plants: 300 per open period.
- **Independent recount:** `recount200.py` (pure Python, separate code path): 22 strings incl. K4 and K1, **0 mismatches** on 64 statistics.

## Gates (all passed)
| Gate | Rule | Result |
|---|---|---|
| G1 false calls | P9 uniform, P10 shuffled English ≤ 0.10 at α 0.05 | 0.033, 0.047 |
| G2 broken meter, up (I-230) | K4 multiset rearranged to maximise Zmax > 4.74 | 35.6 |
| G2 broken meter, down (I-230) | rearranged to minimise SA16 < SA16 1 % quantile −2.06 | −7.49 |
| G3 known positive | K2 (KRYPTOS Vigenère, ABSCISSA p 8): p < 0.01, PHI8/PHI16 in top 3 | PHI8 z 5.57, p 0.0007 |
| G4 recount | 0 mismatches | 0 / 22 |

## Results
**K4, global:** Zmax 3.197 on BKA12 (raw 174 vs null mean 137.2, sd 11.5); held-out look-elsewhere **p 0.180**. Next: SA13 2.46,
SA12 2.35, SA7 2.34, SA14 2.25. Low end: BAZ11 −1.59 (p_lo 0.87). BKA12's single-statistic tail is 0.0047, but the chance that *some*
statistic of the 64 reaches it is 0.179 (fresh shuffles, seed 20005): the look-elsewhere effect explains it, and re-testing BKA12 on the
same 97 letters could not confirm anything. **No signal.**

**Power by family** (share of plants with Zmax ≥ 3.86):
| Family | Power α 0.05 | Label |
|---|---|---|
| P1 KRYPTOS-tableau Vigenère p 4–12 (K1/K2 style) | 0.25 (best p 8: 0.46) | `LOW-POWER` |
| P2 Beaufort A–Z p 4–12 | 0.29 | `LOW-POWER` |
| P3 progressive keyword | 0.09 | `LOW-POWER` |
| P4 Vig p 7 then columnar w 14 | 0.11 | `LOW-POWER` |
| P4b Vig p 7 then columnar w 7 | 0.34 | `LOW-POWER` |
| P5 columnar then Vig | 0.29 | `LOW-POWER` |
| P6 Vig then columnar (any w) | 0.06 | `LOW-POWER` |
| P7 PT autokey L 1–10 | 0.07 | `LOW-POWER` |
| P8 English running key | 0.11 | `LOW-POWER` |
| P11 arbitrary alphabets p 8/13/16 | 0.17 | `LOW-POWER` |

So the panel answers the Voynich question plainly: **at 97 letters a rhythm test cannot see the K1–K3 families**; the cribs remain far stronger.

**Targeted, two-sided, open periods** (H_P: P arbitrary alphabets, direct). z_K4 = z(PHI_P); power = single-statistic, α 0.05;
q_rev = share of 300 H_P plants with z ≤ z_K4.
| P | K4 raw | z_K4 | p_sig | H_P plant z mean (sd) | power | q_rev | Label |
|---|---|---|---|---|---|---|---|
| 8 | 14 | −0.28 | 0.64 | 2.34 (1.39) | 0.68 | **0.023** | `STAT-DISFAVOURED` |
| 13 | 6 | −0.63 | 0.80 | 1.81 (1.44) | 0.51 | **0.017** | `STAT-DISFAVOURED` |
| 16 | 9 | +0.74 | 0.26 | 1.80 (1.46) | 0.44 | 0.257 | `LOW-POWER` |
| 19 | 6 | +0.48 | 0.37 | 1.83 (1.42) | 0.46 | 0.183 | `LOW-POWER` |
| 20 | 6 | +0.54 | 0.35 | 1.29 (1.24) | 0.29 | 0.317 | `LOW-POWER` |
| 23 | 3 | −0.73 | 0.84 | 1.52 (1.38) | 0.41 | **0.037** | `STAT-DISFAVOURED` |
| 24 | 3 | −0.71 | 0.83 | 1.48 (1.36) | 0.40 | 0.057 | `LOW-POWER` (borderline) |
| 26 | 2 | −0.36 | 0.73 | 1.17 (1.40) | 0.38 | 0.157 | `LOW-POWER` |

No p_sig is anywhere near the Bonferroni bar (0.05/8). The reverse q values carry binomial noise of about ±0.008 (300 plants); P 23 is the
least firm of the three.

**K1–K3 (descriptive, own nulls):** K1 (63 letters, PALIMPSEST p 10): PHI5 4.79, PHI10 4.08, p 0.013. K2 (369): PHI8 5.57, p 0.0007.
K3 (336, transposition only): BKA4 3.80, p 0.048. The meter hears the K1/K2 period when there are enough letters; K4 has 97.

## Classification
- Rhythm panel, all families above: `LOW-POWER` (no signal, p 0.18).
- Periodic substitution with arbitrary alphabets, direct, **P = 8, 13, 23: `STAT-DISFAVOURED` (α 0.05 each)**, under: English-like
  plaintext with the two cribs (Jane Eyre windows as the model), one alphabet per phase, no transposition after the substitution, whole-text
  permutation null. P 16, 19, 20, 24, 26: `LOW-POWER`. The SAT "open" entries in the coverage table stay open as *exact* cells.

## Limits and blind spots
- Statistical, not exact: if K4 truly were H_8, a result like this happens 2.3 % of the time.
- The plaintext model matters: a plaintext with a flatter letter distribution than Jane Eyre (lists, coordinates, X-separated fragments)
  lowers the H_P plants' z and would weaken q_rev. Not tested (I-238).
- H_P plants are not conditioned on being crib-consistent with K4's actual letters (I-238).
- Any transposition **before** the substitution hides PHI; only the SA windows see the periodic-then-columnar shape, with power ≤ 0.34.
- The permutation null treats K4 as one segment; a frequency drift between the halves is not modelled.
- Design changes before registration (disclosed in PREREG200): a 159-statistic panel had power at chance and was replaced; the low meter
  check moved to SA16 because single-lag counts cannot go below z ≈ −2 (I-240).

## Reproduce
`tools/cycle200/run_cycle200.sh` (≈ 2.2 min, one process group, hard timeout 480 s) → `results200.json`, `runlog200.txt`.
Corpus: Project Gutenberg *Jane Eyre* (pg1260), letters from "CHAPTER I" to the licence; path via `--corpus`.

## Erratum (cycle 202, Voynich audit)
<a id="erratum-cycle-202-voynich-audit"></a>

**Source:** the Voynich agent's cross-audit of this case, dated 2026-11-11 (PT), at repo tip 9ad7e47. Their files are on the shared box (`/workspace/voynich/kryptos-audits/c200-lag1-power/results.md`, `size_targeted.json`), and they used seeds 7001–7800. Our check is cycle 202's `tools/cycle202/verify_errata202.py` → `errata202.json`, with fresh seeds [202202, 901–904]. [Case 189](189-confirmatory-column-coincidence-test-sat-open-periods.md) gives the details. The historical text above has not been edited.

| # | Point (Voynich) | Our check | Status |
|---|---|---|---|
| 1 | The Zmax α 0.05 crit 3.863 is ≈ 2 SE low. 200k held-out shuffles give 3.913, and the real size of 3.863 is 0.0547 | 100,000 fresh shuffles, standardised with this case's own meter moments: crit 3.895, real size 0.0530 ± 0.0007 | **verified** (direction and inflation; the exact crit depends on the moments used) |
| 2 | The targeted PHI_P crit95 lands on an integer atom and the rule is `≥`, so the real size is 0.049–0.112 (P 26 0.112, P 13 0.082, P 23 0.081, P 24 0.074, P 8 0.069). The power column is therefore the power of tests with inflated size | 200,000 shuffles per P: 0.069 / 0.083 / 0.050 / 0.058 / 0.053 / 0.081 / 0.072 / 0.112 (P 8 / 13 / 16 / 19 / 20 / 23 / 24 / 26). Next-atom size 0.023–0.045, mid-p 0.037–0.077 | **verified** |
| 3 | The best family power 0.34 (P4b) is a winner's-curse upper draw. Fresh plants give 0.259 ± 0.007 (0.21–0.25 with exact moments) | 1,000 fresh P4b plants with this case's procedure: 0.254 ± 0.014 (0.245 at the fresh crit) | **verified**. No `LOW-POWER` label changes; read "best 0.34" as ≈ 0.25 |

From cycle 202, the rule is to report the exact size (or the next-atom / mid-p size) of any test on an integer count (I-251).

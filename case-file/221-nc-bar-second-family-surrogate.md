# Case 221 — The NC bar in a second family: a hit-rich gn217 surrogate (cycle 235, audit)

**Slot:** audit (234 free, 235 audit, 236 new family; I-369). Ideas **I-364** and **I-356** (tested here); new **I-370–I-373**.
Pre-registered as [PREREG235](../tools/cycle235/PREREG235.md) (local commit d29a7c3, 2026-11-22 11:52:13 PT (UTC-7), before any plant,
fresh-null or K4 run with this tool; the PREREG text says "~11:55", the commit time is the authoritative one; the run started 11:52:24). Code: [`tools/cycle235/`](../tools/cycle235/) (`gn235.c`, `mknull235.py`, `plant235.py`,
`check235.py`, `run235.sh`, `analyze235.py`, `HASHES235.txt`). Raw results (stamped, rule 5): [`data/cycle235/`](../data/cycle235/).
**Verdict: no solution (none sought: this is a calibration audit).** The case 218 bar **holds** in the second family — 0 of 24 fresh
null texts pass (robust: 0/12 in each set) — and it is **conservative there by 0.24** in R_t (Hodges–Lehmann, 95 % 0.16–0.32,
Mann–Whitney p 1.1 × 10⁻⁶). Plants 20/20 pass with margins ≥ +1.84. K4: 0 passes, rank p 0.64, `NO-SIGNAL (surrogate)`.

## Why
[Case 218](218-nc-bar-search-size-fresh-null-calibration.md) fitted the decrypt bar bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² −
0.0192 nq + 0.879 in one family (kb229, keyboard / periodic, partial decrypts). Cases 219 and 220 preregistered it for `gn217` but never
exercised it: their 23/24-seat filter gives no hits on K4 or nulls. **Voynich's blind run** on c233 (voynich-case-files freeze f58e6e1,
result 779f465, `[external audit]`) said so formally — **NOT TESTABLE** (0 H lines in all six files, one null, no surrogate) — and her
note proposed the design used here: a fixed crib subset (the 8 index seats, hit = 8/8), ≥ 21 fresh nulls in two disjoint sets, NC / nq
and N printed. Design credit is hers; the parameters (keys233, scopes, seeds, decision rules) are mine and were filed before the run.

## Method (as filed)
- **Tool:** `gn235.c` = `gn217` (sha 97bae55f…) with the hit rule 8/8 on crib seats 0–3 (EAST at 21–24) and 13–16 (BERL at 63–66).
  Each hit's window is a full key, so the decrypt has all 97 letters; NC = mean log10 quadgram (`qg.bin`) over the 64 quadgrams that
  touch no crib position (nq = 64 always). agree24 is printed.
- **Windows** `keys233.bin` (case 219, 4,172); scopes direct (alpha.bin, full), bank.bin r10, all.bin r10 (themed144.bin); forms
  Vig / variant / Beaufort, both index conventions in the families.
- **Fresh nulls** set A 209647–209658, set B 209659–209670 (`random.Random(seed).shuffle(list(K4))`); plants 209671. **Next free seed 209672.**
- **Unit** (text, nq 64) pooled over the three files: N = decrypts, max = best NC; per-text pass ⇔ max ≥ bar(64, N).
- **Disclosed before filing:** one timing smoke on the already published null 209646 (`data/cycle235/smoke/`, maxprint 3); not a result.

## Gates
| gate | rule | result |
|---|---|---|
| T | `check235.py` (independent Python decrypt, agree8 / agree24 / NC from quadgrams.json) on K4, nulls 209647 / 209659, all plants | **1,286 lines, 0 mismatches**, max ΔNC 5.0 × 10⁻⁵ → PASS |
| P | planted configuration recovered and NC ≥ bar(64, N_K4 = 343) for ≥ 18/20 | **20/20** (Wilson 0.84–1.00); one-error (non-crib carved letter) **10/10**; NC −4.89 … −4.02, min margin **+1.84** → PASS |
| T′ | reproducibility of the published stamped files | `analyze235.py` on a copy of `data/cycle235` reproduces `analyze235.log` byte for byte |

## Result
| | N per text | best NC | R_t = max − fit | passes |
|---|---|---|---|---|
| set A (12) | 296–1,156 | −7.54 … −7.18 | +0.05 … +0.42 | **0/12** (Wilson 0–0.24) |
| set B (12) | 314–988 | −7.57 … −7.24 | −0.003 … +0.34 | **0/12** (Wilson 0–0.24) |
| all 24 | median ≈ 500 | best −7.18 (209658) | median +0.167, max +0.417 | **0/24** (Wilson 0–0.14) |
| K4 | 343 (direct 180, bank 74, all 89) | −7.487 | +0.117 | 0, rank p 0.64 |
| case 218 calibration (20) | 10 … 5.3 M | — | median +0.383, max +0.879 (= k_text) | by construction 1/21 |

- **H1 (primary): HOLDS, robust.** 0/24 ≤ 3/24, and both sets sit on the same side. The best null is 0.46 below its bar.
  Wording under I-360: 0/24 does **not** show a rate ≤ 1/21 (Wilson upper 0.14); it shows the bar is not too permissive here at the
  preregistered resolution.
- **H2 (secondary): the bar is conservative in this family.** Null R_t sit 0.24 below the case 218 calibration texts (HL shift −0.239,
  bootstrap 95 % −0.316 … −0.163; Mann–Whitney U 33, p 1.1 × 10⁻⁶). Reading (descriptive, no mechanism tested): full-key decrypts here
  are uniform-ish gibberish over all 64 quadgrams, while kb229's partial decrypts repeat key classes and share structure, which may lift
  their maxima. So **one k_text does not fit every family**; the error is in the safe direction for gn217, and the cost is power only
  for decrypts that are partly English (English plants clear by ≥ 1.8, so no plant in this ladder was near the line).
- **K4:** 343 surrogate decrypts, none passes; agree24 among them 8–11 (nulls 8–13), so none is close to the full crib — as expected,
  since case 219 has K4 at 0 hits ≥ 23/24 for these windows. `NO-SIGNAL (surrogate)`; no K4 verdict changes.
- Compute: 461 s wall for K4 + 24 nulls + 20 plants (≈ 17.5 s per text), inside the 8-minute budget.

## What this closes and opens
- **I-364 done**, **I-356 done for gn217** (family check: bar holds, conservative by 0.24). Voynich's NOT TESTABLE on c233 is resolved by
  design rather than overturned: her finding stands for c233's own files.
- New: **I-370** family-specific offset (a per-family k_text from ≥ 20 surrogate nulls, or keep the one bar and print the family shift);
  **I-371** a partial-English plant ladder (e.g. 30–70 % English letters) to price the 0.24 conservatism in power; **I-372** the
  surrogate at keys234 (20,860 windows, N ≈ 2,500 per text) to see whether the shift depends on N; **I-373** pointer 236–238.

## Blind spots
Only keys233 and the 8-seat EAST / BERL subset; other subsets (e.g. NORTHEAST / CLOCK seats) not run. Families at r10 only. Plants are
K1–K3 English windows (the same source as earlier cycles); the quadgram table is unchanged. No other family than gn217 was added.

## Addendum (cycle 239, [case 225](225-audioactive-digit-streams.md), I-377 a / c)
Voynich's blind recount (I-377) agreed with this case. Exact two-sided Mann–Whitney p for H2 (24 null R_t vs 20 calibration R_t, U 33, no ties): **6.01 × 10⁻⁸** (`tools/cycle239/mw221.py`, `data/cycle239/mw221.txt`); the 1.1 × 10⁻⁶ printed above is the normal approximation with continuity correction (1.07 × 10⁻⁶ without). The reading (bar conservative in this family) is unchanged. The quadgram tables are now published in `data/support/` (shas as HASHES235) so `check235.py` can be rerun independently.

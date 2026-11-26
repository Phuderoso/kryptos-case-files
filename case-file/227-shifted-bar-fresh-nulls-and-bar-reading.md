# Case 227 — The shifted bar on 24 fresh nulls, and what the 0.24 really is (cycle 241, audit)

**Slot:** audit (I-392). Ideas **I-389** (tested), **I-377 (b)** (done), **I-383** (keys233 part done), **I-390** (rule applied), Voynich's degeneracy criteria (descriptive counts); new **I-393–I-397**.
Pre-registered as [PREREG241](../tools/cycle241/PREREG241.md) (local commit 3c96aa2, 2026-11-25 19:44:07 MST (UTC−7), before the plant / null runs and before the per-family degeneracy and tracing runs; the bar-reading check, the keys233 value audit and the degeneracy gates were run once during development and are disclosed in the PREREG). Base: origin/main **2fe149d** (c240 published, tree 410f4e92). Code: [`tools/cycle241/`](../tools/cycle241/); raw results [`data/cycle241/`](../data/cycle241/).
**Verdict: no solution (none sought: ruler and list audit, K4 not re-run).** (1) **I-389: the shifted bar BSH is ADOPTED** for gn217-family decrypt readings from this cycle on: 0/24 fresh nulls (C 0/12, D 0/12; Wilson upper 0.138), gate P 10/10, gate T 0 mismatches. (2) **I-377 (b): the bar-reading check found that the case 221 "family shift" of 0.24 is mostly a unit-count effect, but the frozen held-out criterion failed narrowly** (p 0.038) — read below. (3) keys233 values audited independently: 0 mismatches in 4,012 windows. (4) Voynich's degeneracy criteria give descriptive per-family counts; DUP 0. (5) The amended tracing rule puts all 71 non-planted plant lines into the planted group.

## 1. I-389 — BSH on fresh nulls (primary, frozen rule)
24 shuffled K4 texts (sets C 209731–209742, D 209743–209754), `gn235` on keys233.bin, direct full + bank r10 + all.bin r10, unit (text, nq 64), B218 = fit + 0.8788963, **BSH = B218 − 0.2388112 (−6.96338 at N 343)**.
| quantity | result |
|---|---|
| BSH per-text passes | **0 / 24** (Wilson 0.000–0.138); C 0/12, D 0/12 |
| B218 passes (replication of case 221 H1) | 0 / 24 |
| best fresh null | R_t +0.450 (null 209733, N 466, max −7.128); headroom to BSH +0.190 |
| rule (k ≤ 3/24 and each set ≤ 2/12) | **ADOPT** — never retroactive; labels in cases 211–226 keep their text, relabels are descriptive only |
| gate P (10 full-English plants, seed 209755, 4 direct / 3 bank / 3 all.bin, 5 one-error) | **10/10** recovered, one-error 5/5, NC −4.64 … −4.04, all ≥ B218 and BSH |
| gate T (`check235.py`, all 10 plant files and null 209731 / 209743 files, 1,034 lines) | 0 mismatches |
Wording (I-360): 0/24 does not show a rate ≤ 1/21 (Wilson upper 0.138); with cases 221 + 226 the three sets give 0/60 under BSH (descriptive pool, Wilson upper ≈ 0.06). It shows BSH is not too permissive at this resolution in the gn217 family. **Scope:** keys233 key source, shuffled K4 nulls, nq 64; the bar still says nothing about families that are not gn217. Adoption is the *house reading* of this family only.

## 2. I-377 (b) — what is the 0.24? (held-out test; frozen criterion NOT met)
PREREG232 l.38: R_t = max over the text's **units** (text, nq ≥ 10) of (max_U − fit); k_text = max over 20 calibration texts. `bar241.py` (published data only): k_text recomputes to **0.878896** (diff 0), every calibration R_t equals summary232. But each calibration text has **51–53 units** (one per nq), so R_t is a max over ~52 units; a gn217 text has **one** (nq 64). The calibration nq-64 unit alone gives residuals median **+0.143**, max +0.331 (n 20), against R_t median +0.383.
Frozen prediction (filed after seeing the case 221 / 226 numbers, tested on the 24 *fresh* R_t): consistent iff exact two-sided MW vs the 20 calibration nq-64 residuals has p ≥ 0.05 and |HL| ≤ 0.15.
| comparison | exact MW p | HL |
|---|---|---|
| fresh 24 R_t vs calibration **nq-64** residuals (frozen test) | **0.0383** | +0.067 → **NOT CONSISTENT** (narrowly; HL inside the band) |
| fresh 24 R_t vs calibration R_t (max over ~52 units) | 9.4 × 10⁻⁷ | −0.202 (case 221: 6.0 × 10⁻⁸, −0.239): the shift replicates |
| descriptive pools, not frozen: 36 (cases 226 + 241) / all 60 (cases 221 + 226 + 241) vs nq-64 residuals | 0.061 / 0.074 | +0.058 / +0.047 |
**Reading.** By the frozen rule the multiplicity reading is **not confirmed**: the fresh nulls sit slightly *above* the calibration nq-64 residuals (HL +0.067, p 0.038 on 24; p 0.06–0.07 when pooled with the 36 earlier nulls, post hoc). What survives: (i) the 0.24 shift is real and replicates on fresh data (HL −0.20); (ii) about 0.20 of it is the difference between a max over ~52 units and a single unit — the same-unit gap is +0.05 to +0.07 the other way, so the bar's conservatism for a one-unit family is **not a gn217 property**; it is the price of a k_text calibrated on multi-unit texts. Neither reading changes the adoption in §1. The sharper statement (a unit-count-aware bar) is I-393, not a finding.
**One-unit candidate OU0** (fit + 0.4903, the max R_t of the 36 earlier nulls): fresh passes **0/24 → HOLDS**, but the best fresh null (R_t 0.450) is only 0.04 below it, so it is a **candidate only** (I-393); the house bar is BSH.

## 3. I-383 — value audit of keys233 (done before filing, disclosed)
`indep241.py` regenerates S1–S22 / W1–W4 windows from sympy (primes, π(n), φ, d, σ, μ, partitions, Catalan, Bell), `num2words`, `roman`, and structurally different code for Recamán, Stern (binary recursion), Kolakoski (run-length generator), Josephus, popcount / Thue–Morse / Collatz: **4,012 of 4,172 windows identical, 0 mismatches**; 21 sequences also checked against leading terms typed from the OEIS definitions (0 mismatches); S18 (160 windows) skipped (known truncation, repaired in keys237); a planted wrong term in a stream is detected **40 / 40**. **Not done:** keys218 digit / decimal streams, keys236 compass tables, keys234 beyond the shared sequences, keys239 (I-394). Caveat: the K1–K3 word-length streams use the same plaintext strings read from `keys233.py`; the spelling of those strings was not independently re-typed. The comparison is not independent of the **definition** of a sequence (e.g. S9 = popcount(n − 1) mod 2, S16 stern index n): only of its implementation.

## 4. Voynich's degeneracy criteria — descriptive per-family counts (limits frozen in the PREREG; credit: Voynich's criteria)
`degen241.py`, 9 lists, 67,957 windows, 112 families. P4 (minimal period ≤ 4), ENT (entropy < 2.0 bits or one value in ≥ 49 of 97), AP (key_i = a + d·i mod 26, d ≠ 0), TAIL (last ≥ 20 identical), DUP (identical window in another family). Gates: 0/20,000 random windows flagged; 100/100 planted each.
| criterion | windows |
|---|---|
| ENT | 11,292 |
| P4 | 972 |
| TAIL | 765 |
| AP | 10 (keys218 D3 4, keys221a MB 4, IT 2) |
| **DUP across families** | **0** |
65 of 112 families have no flag at all; 35 have ≥ 50 % of their windows flagged by P4 / ENT / AP / TAIL: the short date / coordinate / year strings of keys217, keys221a MC (Morse counts), keys233–234 S9 / S12 Catalan / S14 / S17 / S18 (old), keys236 A16 and keys239 digit strings (ELEMD1, LSCAT, LSTERM16–21). The old truncated S18 rows of keys233 / 234 are flagged 160/160 and 800/800 (ENT), the known positive. This reproduces case 224's DESIGN / ARITHMETIC labels; **counts only — no label changed** and none of these families is "excluded" or "demoted" by a count. What it does not do: it says nothing about whether a low-entropy family is a *worse hypothesis* (the periodic and Gromark exclusions of cases 143 / 202 / 214 / 216 cover period ≤ 25 and L ≥ 22 NO-SIGNAL).

## 5. I-390 — tracing rule applied
`trace241.py`: (a) key distance modulo a constant, (b) alphabet neighbour, (c) group lines sharing ≥ 50 % of the decrypt. On the 20 case 226 plants and the 10 new plants: **71 non-planted lines ≥ BSH — 63 equivalent-key (hd_off ≤ 10), 0 alphabet neighbours by (b), 8 "other" by key — and all 71 fall in the planted line's group by decrypt overlap (independent groups 0)**; (c) is the rule that matters. On the 24 fresh nulls: **0 H lines ≥ BSH, 0 groups**. Caveat: with full-English plants the group rule is easy (a 97-letter English decrypt overlaps its own variants); on a partly right decrypt the 50 % overlap may split groups — untested (I-395).

## What this does not show
- Nothing about K4 or about Sanborn. BSH adopted for **gn217-family** decrypts under keys233 / nq 64 only; no other family's bar is touched.
- The frozen multiplicity criterion failed narrowly; the post-hoc pools (p 0.06–0.07) are not a rescue.
- 24 nulls resolve a per-text rate to Wilson upper 0.138 only.
- Value audit: implementation, not definition; four lists still to audit.

## Bookkeeping
Next free seed **209757**. IDEAS: I-389 tested; I-377 (b) done; I-383 partly done; I-390 applied; new I-393–I-397.

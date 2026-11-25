# Case 226 — How English must a decrypt be? Pricing the bar's conservatism (cycle 240, free slot)

**Slot:** free (I-388). Idea **I-371** (tested here); I-386 rule applied (and found too narrow); new **I-389–I-392**.
Pre-registered as [PREREG240](../tools/cycle240/PREREG240.md) (local commit 6fc1f06, 2026-11-25 11:49:00 MST (UTC−7), before any ladder, plant or null run). Base: origin/main **3c562db** (c239 published, tree 0bda0e22). Code: [`tools/cycle240/`](../tools/cycle240/) (`partial240.py`, `ladder240.py`, `plant240.py`, `mknull240.py`, `run240.sh`, `analyze240.py`, `trace240.py` (post hoc), `HASHES240.txt`); tool `gn235` and `check235.py` **unchanged** from case 221; raw results: [`data/cycle240/`](../data/cycle240/) (`SHA256SUMS`, 66 files).
**Verdict: no solution (none sought: this cycle measures the ruler, not K4).** The case 218 bar is **costly** in power for partly English decrypts (L1 `COSTLY`, max Δ +0.31); the case 221 family-shifted bar **holds** on 12 fresh nulls (0/12, robust) → by the frozen rule it is **proposed** for gn217-family decrypt readings from cycle 241 (I-389). Plants 20/20, gate T 0 mismatches.

## Why
Case 221 showed the decrypt bar is conservative by 0.24 in the `gn217` family (exact MW p 6.0 × 10⁻⁸), but every plant there was full English, margins ≥ +1.84, so nobody knew what the conservatism costs. A real near-miss — right transposition with some wrong key seats, or right key with half the transposition — would produce a decrypt that is only *partly* English. This cycle asks how much English the bar needs before it sees one, under both bars, and re-tests the shifted bar on fresh nulls (case 221 derived the shift from its own 24). Chosen over I-368 (widens a 0-hit family) and I-380 (one list per budget, first pass flat).

## Method (as filed)
- **Partial English** (`partial240.py`): K1–K3 English window, cribs written in; m = round(f · 73) of the 73 non-crib letters stay English, the rest get a random *different* letter. **S** = scattered positions; **B** = one contiguous block in the non-crib index list (cyclic). NC over the 64 crib-free quadgrams (as case 221).
- **Bars** at nq 64, N 343 (case 221 K4 unit): **B218 = −6.72457**; **BSH = B218 − 0.23881 = −6.96338**.
- **Tier 1** ladder: f ∈ {0, .3, …, 1}, S and B, 500 replicates per cell (rng 209718); pass rate given recovery.
- **Tier 2:** 20 plants (seed 209717) through `gn235` on `keys233.bin` (cipher draws as plant235; f 1.0 / 0.7 / 0.5 / 0.3 / 1.0 by id block, S / B alternating, 10 one-error).
- **Tier 3 (H3):** 12 fresh nulls 209719–209730, `gn235` direct full + bank r10 + all.bin r10, per-text pass under both bars.
- I-382: no new key list; `audit238.py` on keys233 pasted in the PREREG (ZEROTAIL 70 = known old S18; low-entropy windows → I-386 applies).

## Results

### Tier 1 — the ladder (L1: `COSTLY`)
| model | f (English letters of 73) | NC median [5 %, 95 %] | pass B218 | pass BSH | Δ |
|---|---|---|---|---|---|
| S | 0.0 (0) | −8.09 [−8.36, −7.76] | 0.000 | 0.000 | 0 |
| S | 0.3 (22) | −7.76 [−8.13, −7.31] | 0.000 | 0.004 | +0.004 |
| S | 0.4 (29) | −7.56 [−7.97, −7.10] | 0.006 | 0.024 | +0.018 |
| S | 0.5 (36) | −7.32 [−7.78, −6.77] | 0.032 | 0.142 | **+0.110** |
| S | 0.6 (44) | −6.90 [−7.37, −6.39] | 0.294 | 0.568 | **+0.274** |
| S | 0.7 (51) | −6.48 [−7.00, −5.93] | 0.796 | 0.944 | **+0.148** |
| S | 0.8 (58) | −5.94 [−6.44, −5.40] | 0.994 | 1.000 | +0.006 |
| S | 0.9 / 1.0 | −5.18 / −4.38 | 1.000 | 1.000 | 0 |
| B | 0.0 (0) | −8.09 [−8.36, −7.75] | 0.000 | 0.000 | 0 |
| B | 0.3 (22) | −7.05 [−7.39, −6.73] | 0.050 | 0.352 | **+0.302** |
| B | 0.4 (29) | −6.68 [−7.10, −6.31] | 0.566 | 0.874 | **+0.308** |
| B | 0.5 (36) | −6.29 [−6.74, −5.95] | 0.944 | 0.996 | **+0.052** |
| B | 0.6 (44) | −5.93 [−6.36, −5.55] | 0.998 | 1.000 | +0.002 |
| B | ≥ 0.7 | ≥ −5.57 | 1.000 | 1.000 | 0 |

Bold = Wilson 95 % intervals disjoint (n 500 each; full intervals in `ladder240.log`).
- **f50** (half the decrypts pass): scattered **0.641** (≈ 47 of 73 letters) under B218 vs **0.584** (≈ 43) under BSH; block **0.387** (≈ 28) vs **0.328** (≈ 24). The shift buys ≈ 0.06 of the text (≈ 4 letters) in both models; the steep part of the curve is where it matters, and there it moves pass rates by up to 0.31.
- Reading: **scattered errors are far more expensive than a block**: with 30 % English in one run the decrypt still passes BSH a third of the time; scattered, it essentially never does (quadgrams need four right letters in a row). A decrypt half wrong at random seats is invisible to either bar.

### Tier 2 — plants (gate P PASS, gate T PASS)
20 / 20 recovered (Wilson 0.84–1.00; one-error 10/10). `check235.py`: 2,224 lines (20 plant files + null 209719 / 209725, three scopes) 0 mismatches, max ΔNC 5 × 10⁻⁵.
| f | model | plants | planted-line NC | pass B218 / BSH | tier-1 cell |
|---|---|---|---|---|---|
| 1.0 | S, B | 0–3, 16–19 | −4.96 … −4.01 | 8/8, 8/8 | 1.00 / 1.00 |
| 0.7 | S | 4, 5 | −6.02, −6.19 | 2/2, 2/2 | 0.80 / 0.94 |
| 0.7 | B | 6, 7 | −5.23, −5.70 | 2/2, 2/2 | 1.00 / 1.00 |
| 0.5 | S | 8, 9 | −7.48, −7.27 | 0/2, 0/2 | 0.03 / 0.14 |
| 0.5 | B | 10, 11 | −6.62, −6.83 | 1/2, **2/2** | 0.94 / 1.00 |
| 0.3 | S | 12, 13 | −7.46, −7.91 | 0/2, 0/2 | 0.00 / 0.00 |
| 0.3 | B | 14, 15 | −7.20, −6.99 | 0/2, 0/2 (15 misses BSH by 0.03) | 0.05 / 0.35 |
Every plant falls where its cell says. Plant 11 (f 0.5 block, one-error) is the cost made concrete: recovered, read, and **missed by the house bar** (−6.83 < −6.72), caught by the shifted one.

**I-386 tracing (rule as frozen, then a post-hoc look, `trace240.txt`).** 13 non-planted plant lines clear BSH (12 also B218):
- 2 are **equivalent configurations** (window key + 1 everywhere with a rotated alphabet / other form): identical decrypt, but Hamming **97** to the planted key — the frozen ≤ 10 metric calls them "other".
- 10 (plant 2) use the planted key with a **neighbouring keyed alphabet** X (a few letters swapped): decrypts 6–24 letters off, NC −5.14 … −6.59, all pass both bars. Key Hamming 0; I-386 does not look at alphabets at all.
- 1 (plant 11) is a **related window** of the same arithmetic family (Hamming 27, same after any offset), sharing the planted text's English block: 28 letters off, NC −6.952 — over BSH by 0.011, under B218.
So the frozen ≤ 10 rule saw 5 neighbours and misfiled 8. A lowered bar lets in more of these partial echoes of a true configuration; they are "the right answer read through the wrong window", not false passes, but a reader who trusts a bar pass without tracing would mis-attribute them. → **I-390** (offset-canonical key distance + alphabet neighbours + decrypt distance).

### Tier 3 — held-out nulls (H3: HOLDS, robust)
| | N per text | best NC | R_t = max − fit | pass B218 | pass BSH |
|---|---|---|---|---|---|
| set A (6) | 449–1,217 | −7.46 … −7.07 | +0.10 … +0.49 | 0/6 | 0/6 |
| set B (6) | 474–887 | −7.54 … −7.37 | +0.01 … +0.15 | 0/6 | 0/6 |
| all 12 | | best −7.073 (209722) | median +0.168, max +0.490 | **0/12** (Wilson 0–0.24) | **0/12** (Wilson 0–0.24) |
- Best fresh null sits 0.150 below the shifted bar (k_text 0.640). R_t replicates case 221 (median +0.168 vs +0.167; exact MW U 152, p 0.80): **the family shift replicates on fresh nulls.**
- Resolution: 0/12 does not show a false-pass rate ≤ 1/21 (Wilson upper 0.24); together with case 221's 0/24 the bar is not too permissive at this resolution, nothing more.

### K4 (descriptive, not re-run)
Case 221's K4 unit (N 343, best −7.487, R +0.117) is 0.52 below BSH — no pass under either bar; rank unchanged. No K4 label changes.

## Reading
- **I-371: `COSTLY`** (frozen rule: a cell with Δ ≥ 0.10 and disjoint Wilson). The house bar needs ≈ 64 % scattered English (≈ 47 letters) or a ≈ 39 % block (≈ 28 letters) to see a partial decrypt half the time. The shifted bar saves ≈ 4 letters and up to 31 points of power in the steep band, with 0/12 fresh false passes.
- **Adoption (frozen rule):** COSTLY and H3 HOLDS robust → **BSH proposed** for `gn217`-family decrypt readings (nq 64 surrogates and full-key decrypts) from cycle 241, **never retroactive**; other families keep B218 until their own shift is measured (I-370). Because 0/12 is thin, I-389 asks 241 to add ≥ 24 fresh nulls before BSH becomes the house bar for this family.
- Planted controls validate recovery and the scorer only within this scope: keys233, the run235 plant slices, K1–K3 English, two placement models, uniform random fill.

## Blind spots
Error models other than uniform-scattered and one block (periodic wrong seats, two blocks, English-frequency fill, errors next to the cribs) not run → I-391. Only nq 64 (full-key decrypts); partial decrypts (nq < 64, kb229 family) not laddered. Fresh nulls only 12. The neighbour metric tested here is post hoc.

## News check (2026-11-25)
No solution; plaintext still behind Paradigm's verifier, method unpublished. Seen: kryptosbot.com now lists 597 experiments / 721.7 B configurations and names "circled letters on a tableau in the sculptor's working papers" as an open, unanalysed lead (status page dated 29 Sep 2026); glthr.com W-rectangle (updated 15 Nov); arXiv 2611.27729 (20 Nov 2026) on agent-led cryptanalysis with self-certifying witnesses (AES / Keccak, not classical); cyphersolver.com ledger (Lasry et al., updated 25 Nov) — no Kryptos break. `[secondary / community, unverified]`.

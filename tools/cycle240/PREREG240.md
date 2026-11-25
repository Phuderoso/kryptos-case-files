# PREREG240 — Cycle 240 (free slot): I-371 partial-English plant ladder — pricing the bar's conservatism

Filed 2026-11-25 ~11:50 MST (UTC−7), **before** any ladder, plant or null run of this cycle. Base: origin/main **3c562db** (c239 published, tree 0bda0e22). Case file 226.
Slots (I-388): **240 free** (I-368, I-371, I-380), 241 audit, 242 new family. Seeds: plants **209717**, ladder **209718**, nulls set A **209719–209724**, set B **209725–209730**; next free after this cycle **209731**.

## Why I-371 (choice among I-368 / I-371 / I-380)
- **I-371 chosen.** Case 221 found the case 218 decrypt bar *conservative by 0.24* in the `gn217` family (H2, exact MW p 6.0 × 10⁻⁸) but every plant there was full English (margins ≥ +1.84), so the cost of that conservatism was never priced: how English must a decrypt be before the bar sees it, and how much does the family-shifted bar buy? This is the one question every "partial decrypt" reading in the repo depends on, it has never been measured, it needs no new hypothesis about Sanborn and it is cheap. It is also a held-out test of the shifted bar on **fresh** nulls (case 221 derived the shift from its own 24 nulls).
- I-368 (arithmetic chunk 2) widens a family already at 0 hits (P4; mostly Beaufort −a = re-indexing of tested keys). I-380 (near-miss profile of other lists, ≈ 6 min per list) fits one list in the budget and case 223's first pass was flat (rank p 1.00 / 0.86). Both stay queued.

## Disclosed before filing
- Tool `gn235` = case 221 source unchanged (sha 4ca8d7d8…142c, rebuilt `gcc -O3 -march=native -fopenmp`); `check235.py` unchanged (a53a4377…405e); key list `keys233.bin` (4d03ca5b…5e) unchanged — the list on which the 0.24 shift was measured. Its old truncated S18 windows (case 223) do not matter here: the list is only the cipher's key source for plants and nulls, not a hypothesis.
- **I-382 (`audit238.py` unchanged, 07dc85bc…1970) on the list used** (no new list this cycle), pasted:
```
S keys233 keys233 windows 4172 ANY 820 BLOCKCONST=236 CONST60=196 DISTINCT3=484 HEADRUN=150 RUN20=292 SEATCONST=80 TAILRUN=150 ZEROTAIL=70
L keys233 windows 4172 distinct 4172 sha256 4d03ca5b37418574
D within-list duplicate windows 0 cross-list duplicates (first occurrence elsewhere) 0
```
  Reading (as case 224): ZEROTAIL 70 = the known old-S18 truncation (case 223), the rest arithmetic / design. Low-entropy windows exist → **I-386 applies** (below).
- `plants240.tsv` (sha 57ddcf8e…8de) and `nulls240.tsv` (78d0810e…f1) generated before filing, **not run**. Support data: `summary232.json` (betas, k_text), `summary235.json` (case 221 nulls), `qg.bin` / `quadgrams.json` (= `data/support/`), `k123_eng.txt` (= HASHES232).
- No smoke or timing run was made.

## Design (frozen)
**Partial-English plaintext** (`partial240.py`): a 97-letter K1–K3 English window with the cribs written in; of the 73 non-crib positions, m = round(f · 73) keep the English letter and the rest get a uniform random letter *different* from the English one. Model **S** (scattered): kept positions a uniform random subset (what a decrypt with scattered wrong key seats looks like). Model **B** (block): kept positions consecutive in the non-crib index list, cyclic start (what a partly right transposition looks like). NC = mean log10 quadgram over the 64 quadgrams that touch no crib position (as case 221; cribs never count).
**Bars** (nq 64, N = 343 = case 221's K4 unit N, as its gate P): **B218** = bar(64, 343) = −6.72457 (case 218 betas, k_text 0.8788963); **BSH** = B218 − 0.2388112 = **−6.96338** (case 221 Hodges–Lehmann family shift).

**Tier 1 — ladder (primary, L1):** `ladder240.py`, f ∈ {0, .3, .4, .5, .6, .7, .8, .9, 1}, models S and B, R = 500 replicates per cell (rng 209718). Pass rate = P(NC(planted plaintext) ≥ bar) with Wilson 95 %. This is the pass rate *given* recovery: a text's max over its decrypts can only be ≥ its planted line, and the other lines pass at the null rate (case 221: 0/24).
- Per cell Δ = p_SH − p_218. **L1 label:** `COSTLY` if some cell has Δ ≥ 0.10 with disjoint Wilson intervals; `NEGLIGIBLE` if max Δ < 0.05; otherwise `FRONTEIRA`. Also f50 (linear interpolation where the pass rate crosses 0.5) per model and bar; price = f50_218 − f50_SH in units of the 73 non-crib letters.
**Tier 2 — tool in the loop (gate P + consistency):** 20 plants (seed 209717), cipher side drawn exactly as plant235 (ids 0–7 direct, 8–13 bank, 14–19 all.bin; random keys233 window, form, X, Y, row, dir, ix); f = [1.0, 0.7, 0.5, 0.3, 1.0][id // 4], model S for id % 4 ∈ {0, 1}, B for {2, 3}; odd ids one carved error at a non-crib position (10 one-error plants). `gn235` on the run235 plant slices (direct Y stride 1000, families row stride 2000).
- **Gate P:** ≥ 18/20 recovered (planted perm / dir / ix / X / Y / form / window key, pt differs from the planted plaintext in ≤ 1 position for one-error plants, 0 for clean). If P fails, the ladder is still reported but tier 2 reads `INSUFFICIENT-DISCRIMINATION`.
- **Gate T:** `check235.py` on every plant file and on the null files of 209719 and 209725: 0 mismatches.
- Per plant: planted-line NC vs B218 / BSH, beside its tier-1 cell rate (descriptive consistency).
- **I-386 rule:** every *other* H line in a plant file with NC ≥ BSH is traced: Hamming distance of its window key to the planted key over the 97 values; ≤ 10 = neighbour pass (expected, not a false pass), > 10 = other (counted; read).
**Tier 3 — held-out nulls (H3):** 12 fresh shuffled K4 texts, `gn235` direct full + bank r10 + all.bin r10 (case 221 protocol), unit (text, nq 64) pooled. Shifted-bar per-text passes k/12: **HOLDS** (not too permissive at this resolution) if k ≤ 2 (P(≥ 3 | p = 1/21) = 0.017); robust if each set ≤ 1/6; **REJECTED** if k ≥ 3. B218 passes on the same 12 reported (fresh replication of case 221 H1). Descriptive: R_t of these 12 vs case 221's 24 (exact two-sided MW) = does the family shift replicate on fresh nulls.
**K4:** not re-run (method cycle). Descriptive only: case 221's K4 unit (N 343, max −7.487, R +0.117) against BSH.
**Adoption rule (frozen):** BSH is *proposed* for gn217-family decrypt readings only if L1 = `COSTLY` **and** H3 HOLDS robust; otherwise the case 218 bar stays the house bar and the ladder is printed as its power curve. Either way, adoption takes effect from cycle 241 and is never applied retroactively to change a label (descriptive relabels only).

## Commands
`setsid timeout 480 ./run240.sh` in its own process group (ladder → plants → nulls, resumable), then `analyze240.py .` and gate T. Budget ≈ 8 min wall.

## Honesty clause
This cycle tests a ruler, not K4. No solution is sought; any plain-English decrypt with both cribs at the official positions from a null or K4 line would be reported prominently and reproduced before being called anything. Nothing is submitted anywhere.

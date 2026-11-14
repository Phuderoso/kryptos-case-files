# PREREG216 — cycle 216 pre-registration (filed before anything below is run on K4 or the nulls)

Filed 2026-11-14 ~08:10 PT (America/Vancouver). Slots: 214 new family, 215 audit, so **216 is free** (I-301); 217 must be a new family.
Seeds: next free 209226. Reserved here: 209226 (A plants), 209227 (A direct nulls), 209228 (A family nulls). Next free after this cycle: **209229**.
Base: main 3c4184f (cycles 214 and 215 already published).

## Part A (I-297): one-error robustness of the case 200 digit-key filter

**Why.** Case 200's headline exclusions (Gromark / periodic Gronsfeld L 1–25 `EXACT-EXCL`; digit level zero in direct and bank
scopes) rest on all 24 crib digits landing in 0..9. One wrong carved letter (or one wrong crib letter) at a crib seat breaks that and
the zero would mean nothing for that hypothesis. Firefly's standing priority (one-letter-error robustness of high-impact exclusions).

**Model.** Unchanged from PREREG214 Part A (model Q, forms Vig / variant / Beaufort, S = family row dir 0 or inverse dir 1, `x` =
identity). Scopes unchanged: direct 86,731² × 3 (`alpha.bin` 2b4ffb69…); behind `bank.bin` (004ffc24…) and `all.bin` (8a9e1b32…), both
dirs, 144² themed (`themed144.bin` e0c1b627…). K4 `k4.txt` 2797de14…. Cribs 1-indexed 22–34 EASTNORTHEAST, 64–74 BERLINCLOCK.

**Stage 1 (`gron216.c`).** Survivor iff ≥ 23 of the 24 crib digits lie in 0..9 (any digit stream, one seat free). Output keeps
s24 (case 200's lines, which must reappear: K4 0 / 0 / 2 cells) and s23 separately, plus the failing seat.
Expected per pair-form ≈ (10/26)²³·(10/26 + 24·16/26) ≈ 39 × case 200's E, i.e. ≈ 95 direct, ≈ 87 per family.

**Stage 2 (`check216.py`, independent Python re-derivation).** Each line's 24 digits are re-derived from scratch (must match the C
line). The failing seat is dropped (for s24 lines: the full 24 and each of the 24 leave-one-out sets). Exact consistency of the 23
with a Gromark chain (k_n = k_{n−L} + k_{n−L+1} mod 10, primer L 1–25; elimination mod 2 and mod 5) and with periodic digits
(P 1–25), key index = plaintext position (ix 0) or carved position S[i] (ix 1). Solution sets ≤ 1000 are enumerated, every member
decrypted over all 97 letters, best quadgram score kept (mean log10 per quadgram, support `quadgrams.json`). Readability threshold
fixed now: **−6.0** (K1–K3 97-letter windows: min −4.73, 5th pct −4.68; uniform random 97-letter: 99.9th pct −7.45, max of 20,000
−7.20; measured 08:00 PT before this file).

**Gate P (plants, seed 209226, `plant216.py`).** 20 plants: 8 direct, 6 behind bank, 6 behind all.bin; even ids Gromark (L 2–20),
odd ids periodic (P 2–20); ix random behind families; K1–K3 English window + cribs; then **one carved crib letter replaced by a
random different letter** (its digit may fall inside 0..9 — then the line is s24 and only a leave-one-out recovers it). Tool run on
the planted X's 1/1000 X-slice (direct) or the planted row's 1/2000 row-slice (families). Pass per plant: the planted cell survives
AND is consistent at the planted (model, L, ix) with the corrupted seat dropped AND (if enumerated) the best decrypt differs from the
planted plaintext in ≤ 1 letter. **Bar ≥ 19/20.** If gate P fails, no exclusion label is issued.

**Nulls.** Case 200 design: 20 shuffled K4 (random.Random(209227), i-th shuffle) on X ≡ i (mod 20) = one direct null-equivalent;
10 shuffled K4 (random.Random(209228)) per family on rows ≡ i (mod 10) = one null-equivalent per family. Stage 2 runs on every
null line (per-line consistency rate per model and L is the calibration).

**Labels (fixed now; `score216.py`).**
- A1 digit level (any stream, one error): Poisson one-sided p of K4 cells against the null-equivalent rate; p < 0.001 → `SIGNAL-FLAG`
  (examine), else `NO-SIGNAL` (this filter can neither exclude nor support an unstructured one-error digit key).
- A2 per scope × model × L (ix and dropped seat pooled): K4 0 consistent lines → `EXACT-EXCL (one-error scope)`, "discriminating"
  if null-equivalent consistent lines ≤ 1, otherwise "zero is exact, low power"; K4 > 0 → best decrypt ≥ −6.0 → `CANDIDATE` (manual
  read; a solution needs coherent 97-letter English with both cribs), any consistent line with > 1000 solutions → `INSUFFICIENT-
  DISCRIMINATION`, else `NO-SIGNAL (consistent, gibberish)`.
- Counting: cells, maps, clusters (PREREG214 part C rule, groups = (X, Y, form)); I-302: clusters are the quoted count.

**Disclosures.** While writing the tools: (1) a smoke test of `gron216` on K4's direct X ≡ 0 (mod 100) slice printed one s23 line
(seat 24 failing, digit 18) and `check216.py` found it consistent with nothing at L/P 1–25; that slice is part of the full run.
(2) Rehearsal of plants 0, 3, 10 (seed 209226, the registered plants): all three cells found and consistent at the planted model;
the decrypt check showed the expected one-letter mismatch at the corrupted seat, so the pass rule says "≤ 1 letter".
**Budget:** heavy ≤ 8 min wall, `setsid` + `timeout 600`, own process group.

## Part B (I-300; Voynich desk's T-sweep, I-302 bracket): cluster threshold scan, own code

`clus216b.py` = `clus215.py` plus a `--T=n` flag (default 16; diff is the flag only). Run T = 12…24 on the published case 201 lines
(`data/cycle215/k4_*_L17-19.txt`, `null_lines_L17-19.tgz`). Report per file and L: clusters at each T, T 24 (identical maps) beside
T 16. Compared afterwards, line by line, with the desk's `sensitivity.txt` (case201-cluster-recount, read-only). Decision rule: no
label in cases 193–201 changes unless K4's rank among the 21 texts crosses the registered reading at some T in 14–17 (descriptive
otherwise). Audit only; no randomness.

## Part C (addenda): the desk's independent audits of cases 200 and 201
Integrated as addenda with attribution and our own verification status (hashes, counts re-read from her files).

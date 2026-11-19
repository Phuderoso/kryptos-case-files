# PREREG217 — cycle 217 pre-registration (filed before anything below is run on K4 or the nulls)

Filed 2026-11-19 ~03:55 PT (America/Vancouver). Slots: 215 audit, 216 free, so **217 must be a new family** (I-301, I-303).
Seeds: next free 209229. Reserved here: 209229 (plants), 209230 (nulls). Next free after this cycle: **209231**.
Base: main 5ac8535 (cycle 216 published by Firefly on 2026-11-19).

## Part A (I-304, new family): named numeric streams read two digits at a time

**Why.** Case 200 excluded every digit key 0..9 in its scopes, but its own blind-spot list names "key on letters of other lengths
(two-digit groups, 'hex inside hex' regrouping)". A key written as numbers 00–99 (coordinates, dates, constants) and reduced mod 26
gives shifts across the whole 0..25 range, so case 200's filter says nothing about it. This is the user's "layers of something simple /
in plain sight" hunch applied to the numbers already on or behind the sculpture (`[speculation]`; the streams themselves are sourced).

**Key streams (`keys217.py`, `keys217.bin` sha d9674e65…, 5,870 distinct 97-shift windows).** k_t = (10·a + b + s) mod 26 with
(a, b) the digits at offsets off+2t, off+2t+1, s ∈ {0, −1} (A = 0 or A = 1). Long streams (first 700 digits, integer part included,
mpmath): π, e, √2, √3, √5, φ, ln 2 (as 0693…), offsets 0–399. Short named streams, cyclic, every offset: K2 coordinates 38 57 6.5 N
77 8 44 W as `38576577844`, `38570650770844`, `385765`, `77844`; Kryptos dedication 1990-11-03 (`11031990`, `03111990`, `19901103`,
`1131990`); Berlin Wall opening 1989-11-09 (four spellings); Carter's tomb opening 1922-11-26 and steps 1922-11-04 (K3's scene;
five spellings); years 1986, 1989, 1990, 1922, `19861989`. Duplicate windows dropped.

**Model.** Case 200's model Q unchanged: forms Vig / variant / Beaufort on keyed alphabets X (plain) and Y (cipher); layer letter at
plaintext position i carved at S[i]; key index = plaintext position (ix 0) or carved position S[i] (ix 1).
Scopes: A1 direct, X, Y ∈ `alpha.bin` (86,731, sha 2b4ffb69…), 3 forms; A2 behind `bank.bin` (004ffc24…) and A3 behind `all.bin`
(8a9e1b32…), both dirs, both ix, X, Y ∈ `themed144.bin` (e0c1b627…). K4 `k4.txt` 2797de14…. Cribs 22–34 EASTNORTHEAST, 64–74
BERLINCLOCK (1-indexed).

**Tool (`gn217.c`).** Hit iff ≥ 23 of the 24 crib seats agree with a window (one wrong seat anywhere allowed: two 4-seat indexes,
seats 1–4 and 14–17, a cell found by both counted once). `check217.py` (independent Python) re-derives every hit: full 97-letter
decrypt, crib agreement recount (must match), quadgram mean log10 (support `quadgrams.json`, same convention as check216).

**Chance.** Per pair-form per window P(≥ 23/24) = 601 / 26²⁴ ≈ 6.6 × 10⁻³². A1 ≈ 1.3 × 10¹⁴ window-pair-forms → E ≈ 10⁻¹⁷; A2/A3
≈ 2.4 × 10¹⁴ each → E ≈ 2 × 10⁻¹⁷. Any K4 hit is therefore far beyond chance at the crib level and goes to the readability step.

**Gate P (seed 209229, `plant217.py`, `runP.sh`).** 20 plants: 8 direct, 6 bank, 6 all.bin; random window, form, X, Y, ix, row, dir;
K1–K3 English windows with cribs; odd ids get one carved crib letter replaced. Tool on the plant's 1/1000 Y-slice (direct) or 1/2000
row-slice (families). Pass: a hit with the planted (row, dir, ix, X, Y, form, window vector) whose decrypt differs from the planted
plaintext in ≤ 1 letter. **Bar ≥ 19/20**; if it fails, no exclusion label is issued.

**Nulls (seed 209230).** Shuffled K4 #0 (random.Random(209230)) on the full direct scope and on 1/10 row slices of bank and all.bin.
Expected 0 (analytic above); a non-zero null is a tool fault to diagnose, not a calibration.

**Labels (fixed now).** Per scope: K4 0 hits → `EXACT-EXCL (named-stream scope, one-error tolerant)`; K4 hit with quadgram ≥ −6.0
(case 202 threshold) → `CANDIDATE` (manual read; a solution needs coherent 97-letter English with both cribs); hit below −6.0 →
`NO-SIGNAL (crib-consistent, gibberish)` and a tool/structure diagnosis.

**Budget.** Heavy ≤ 8 min wall (measured: direct ≈ 10 s, each family ≈ 200 s), `setsid` + `timeout`, own process group.

**Disclosures.** Timing smoke on null #0 only (direct 1/100 Y-slice, bank 1/1000 row-slice; 0 hits). No K4 run before this file.

**Blind spots (stated now).** Only these named streams and offsets; two-digit grouping only (no triples, no hex regrouping, no A1Z26
with values > 26 dropped); keys mod 26 only; only the listed alphabet sets and transposition families; no two-error tolerance.

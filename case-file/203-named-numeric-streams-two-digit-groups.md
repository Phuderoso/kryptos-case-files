# Case 203 — Named numeric streams read two digits at a time (π, e, √2…, K2 coordinates, dates), on two keyed alphabets (cycle 217)

**Slot:** new family (215 audit, 216 free, so 217 must be new; I-301, I-303). Pre-registered in [PREREG217](../tools/cycle217/PREREG217.md)
(local commit 4e19d9e) before any K4 or null run. Idea: **I-304** (tested). Code: [`tools/cycle217/`](../tools/cycle217/); raw results:
[`data/cycle217/`](../data/cycle217/).

## Why this family
Case 200 closed every *single-digit* key (0–9) in its scopes and listed "keys written as two-digit groups" as a blind spot. A number
string such as `38 57 6.5 N 77 8 44 W` or `11 09 1989`, read in pairs 00–99 and reduced mod 26, gives shifts over the whole 0–25 range,
so the case 200 filter is silent on it. That is the "simple layers in plain sight" hunch applied to numbers that are already on or
behind the sculpture (`[speculation]`; the streams themselves are sourced: K2's plaintext, the 1990-11-03 dedication, the 1989-11-09
Berlin Wall opening, the 1922 tomb dates behind K3).

## Model and scope
k_t = (10·a + b + s) mod 26 from the digits at offsets off+2t, off+2t+1; s ∈ {0, −1} (A = 0 or A = 1). **5,870 distinct windows**
(`keys217.bin` sha d9674e65…, index `keys217.tsv`): π, e, √2, √3, √5, φ, ln 2 at offsets 0–399 of the first 700 digits; 22 short named
streams (K2 coordinates in four spellings, dedication / Wall / tomb dates in 4–5 spellings each, years 1986, 1989, 1990, 1922,
`19861989`) read cyclically at every offset.
Model Q as in case 200: Vig / variant / Beaufort on keyed alphabets X (plain) and Y (cipher); layer letter at plaintext position i is
carved at S[i]; key indexed by plaintext position (ix 0) or carved position (ix 1).

| scope | transpositions | alphabets | window-pair-forms | K4 hits (≥ 23/24) | null #0 hits | wall |
|---|---|---|---:|---:|---:|---:|
| A1 direct | identity | X, Y ∈ 86,731 (`alpha.bin`) | 1.32 × 10¹⁴ | **0** | 0 (full scope) | 7 s |
| A2 bank | 165,065 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 2.41 × 10¹⁴ | **0** | 0 (1/10 rows) | 107 s |
| A3 all.bin | 165,782 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 2.42 × 10¹⁴ | **0** | 0 (1/10 rows) | 105 s |

Tool: `gn217.c` (one-error tolerant: two 4-seat indexes on seats 1–4 and 14–17, then a full 24-seat count; a cell is reported once).
Checker: `check217.py` (independent Python: full 97-letter decrypt, crib recount, quadgram score). Analytic chance per window-pair-form
601/26²⁴ ≈ 6.6 × 10⁻³², so the expected chance count is ~10⁻¹⁷ per scope, and the zeros are not a calibration claim but a direct
consequence of the cribs.

## Gate P (seed 209229) — 20 / 20 PASS
8 direct, 6 bank, 6 all.bin plants (random window, form, X, Y, row, dir, ix; K1–K3 English windows with cribs; odd ids with one carved
crib letter replaced). Each plant recovered on its slice with the planted configuration and a decrypt within ≤ 1 letter of the planted
plaintext; checker recount 0 mismatches (`data/cycle217/plants/`). Plant 0 also surfaced three equivalent cells (neighbouring alphabets in
`alpha.bin` that agree on all crib letters, and the Beaufort mirror with the s-shifted window), which is expected key equivalence, not noise.

## Labels (as registered)
- A1, A2, A3: K4 0 hits → **`EXACT-EXCL (named-stream scope, one-error tolerant)`**: no window in the list, under any of the three
  forms, either index convention and either A = 0 / A = 1 numbering, with X, Y in the listed sets, fits even 23 of the 24 crib letters.
- Nulls 0 as predicted (tool sanity, not calibration).

## Blind spots (as registered, unchanged)
Only these streams and offsets (other constants, other date spellings, the Berlin clock's lamp states, Sanborn's own numbers are not in
it); two-digit groups only (no triples, no hex/byte regrouping, no A1Z26 with values > 26 dropped); mod 26 only; only the listed
alphabet sets and transposition families; no two-error tolerance. A successful planted gate validates recovery within this scope only.

**Addendum (cycle 219).** The Voynich desk's independent recount of this case agrees with it; verified against the repo and filed in [case 205](205-columnar-w9-w10-one-error-audit.md) Part A (caveat: she had seen the git log subjects, so not fully blind).

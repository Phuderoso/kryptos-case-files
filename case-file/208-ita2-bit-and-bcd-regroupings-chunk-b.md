# Case 208 — ITA2 bit streams and BCD regrouped as key streams (cycle 222, I-311 chunk B)

**Slot:** free (220 free, 221 new family; I-319). Queue item **I-311**, chunk B, frozen in PREREG221 and not run in cycle 221 for
budget. Pre-registered in [PREREG222](../tools/cycle222/PREREG222.md) (local commit 5f96a48, ~23:41 PT) before any K4, plant or null run.
Code: [`tools/cycle222/`](../tools/cycle222/) (the tool is `tools/cycle217/gn217.c`, unchanged, recompiled); raw results:
[`data/cycle222/`](../data/cycle222/) (stamped `results_*.txt`, `SHA256SUMS`).

## What was tested
The two families of `keys221.bin` (sha256 7ce38188…c8389925f, frozen in cycle 221, byte-identical) that case 207 left out,
extracted by `split222.py` → `keys222b.bin` (sha256 d99c3bad…0627f8b8; all distinct, 0 overlap with cycles 217 / 218 / 221A):

| family | rule (mod 26, cyclic, every offset) | windows |
|---|---|---:|
| IG | ITA2 5-bit stream of the 42 named strings (both bit orders, FIGS / LTRS shifts) regrouped 4 or 8 bits, every bit offset | 4,130 |
| BC | 4-bit BCD (8421) of the I-304 short digit streams regrouped 5, 6 or 8 bits, every bit offset | 1,632 |

Model Q exactly as cases 200 / 203 / 204 / 207: Vig / variant / Beaufort on keyed alphabets X (plain) and Y (cipher); key indexed by
plaintext position (ix 0) or carved position (ix 1); a hit means at least 23 of the 24 crib seats agree (one wrong letter anywhere).

## Result

| scope | transpositions | alphabets | window-pair-forms | K4 hits (≥ 23/24) | null hits | wall |
|---|---|---|---:|---:|---:|---:|
| B1 direct | identity | X, Y ∈ 86,731 (`alpha.bin`) | 1.30 × 10¹⁴ | **0** | 0 (full scope) | 6 s |
| B2 bank | 165,065 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 2.37 × 10¹⁴ | **0** | 0 (1/10 rows) | 99 s |
| B3 all.bin | 165,782 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 2.38 × 10¹⁴ | **0** | 0 (1/10 rows) | 98 s |

(Per-window pair-forms from the `T` lines × 5,762; direct's `T` line is already the total.) Null: shuffled K4 (seed 209254) gave 0,
as the pre-registered chance figure (≈ 10⁻¹⁶ per scope) requires. Heavy wall 230 s (23:42–23:47 PT), plus ≈ 30 s for the gate, inside
`setsid timeout 480`. No K4 hit, so `check222.py` had nothing to re-derive on K4.

**Gate P (seed 209253): 20/20 PASS** (8 direct, 6 bank, 6 all.bin; the 10 odd plants had one carved crib letter wrong). Windows drawn
at random: 17 IG, 3 BC (both families exercised; BC thinly). In every case `check222.py` independently re-derived the planted
(row, dir, ix, X, Y, form, window) with the decrypt within one letter of the plant; 0 agreement mismatches between tool and checker.

## Labels
- B1, B2, B3: **`EXACT-EXCL (named ITA2-bit / BCD windows, chunk B, one-error tolerant)`** — only within the 5,762 listed windows,
  the listed alphabet sets and the two transposition families.
- With case 207 (chunk A), **I-311 is done within its frozen 12,774-window list**: 0 K4 hits in every scope of both chunks.
  This is not a claim about Baudot- / Morse- / BCD-derived keys in general.

## Blind spots
As case 207 (only these 42 strings and the I-304 digit streams; one ITA2 table and its bit reversal, no Baudot / CCITT-1 / Murray
variants; BCD 8421 only; mod 26 only; same alphabet sets and transposition families; no two-error tolerance), plus no 5-, 6- or 7-bit
regrouping of the ITA2 stream (5 bits is IT itself, case 207).

## Verdict
No solution. Teleprinter bit streams and BCD of the named numbers, regrouped, do not key K4 under model Q in these scopes.

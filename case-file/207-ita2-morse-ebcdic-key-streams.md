# Case 207 — Signal and machine encodings: ITA2, Morse and EBCDIC codes of named strings as key streams (cycle 221, chunk A)

**Slot:** new family (219 audit, 220 free; I-314 / I-316 required a new family by 221). Queue item **I-311**. Pre-registered in
[PREREG221](../tools/cycle221/PREREG221.md) (local commit 5a39aff, ~19:51 PT) before any K4, plant or null run. Code:
[`tools/cycle221/`](../tools/cycle221/) (the tool is `tools/cycle217/gn217.c`, unchanged, recompiled); raw results:
[`data/cycle221/`](../data/cycle221/) (`results_*.txt`, `SHA256SUMS`).

## Why this family
Case 204 tested words written one layer down as ASCII bytes / hex / decimal codes and named as blind spots "no EBCDIC, Baudot,
Morse or BCD". The Morse plates at the entrance to Kryptos are a physical part of the work (`[sourced]`); their letters were already
tried as running keys (cycles 34 / 79) and as a fractionating step (cycle 73), but never their *element encodings* as numbers. A key
that is a meaningful word sent down the wire as Morse or teleprinter code is a K1–K3-style "trick named by the key" (`[speculation]`).

## Windows (`keys221.py`, `keys221.bin` sha256 7ce38188…c8389925f; chunk A `keys221a.bin` sha256 aef84534…7d022d4cfe)
42 named strings: the 35 of PREREG218 plus the Morse-plate phrases VIRTUALLYINVISIBLE, SHADOWFORCES, LUCIDMEMORY,
DIGETALINTERPRETATIU, TISYOURPOSITION, SOS, RQ (`[secondary transcription]`). Every window already in `keys217.bin` / `keys218.bin`
was dropped. 12,774 windows in all; **chunk A (this cycle) = 7,012**:

| family | rule (mod 26, cyclic, every offset) | windows | run |
|---|---|---:|---|
| IT | ITA2 5-bit code per character (b1 = LSB table, and bit-reversed); digits on FIGS row with FIGS / LTRS shifts | 826 | A |
| MC | Morse element count per character (1–5) — consistency check, overlaps case 202 | 394 | A |
| MV | Morse code as binary with leading-1 marker (A .- = 5) | 396 | A |
| MB | Morse dot = 0 / dash = 1 stream regrouped 4, 5 or 8 bits, every bit offset | 3,371 | A |
| EB | EBCDIC (cp037) byte, upper and lower case | 810 | A |
| EN | EBCDIC nibbles (0–15) and nibble pairs at every nibble offset | 1,215 | A |
| IG | ITA2 bit stream regrouped 4 or 8 bits | 4,130 | **B, deferred** |
| BC | 4-bit BCD of the I-304 short digit streams regrouped 5, 6, 8 bits | 1,632 | **B, deferred** |

## Model and result
Model Q exactly as cases 200 / 203 / 204: Vig / variant / Beaufort on keyed alphabets X (plain) and Y (cipher); key indexed by
plaintext position (ix 0) or carved position (ix 1); a hit means at least 23 of the 24 crib seats agree (one wrong letter anywhere).

| scope | transpositions | alphabets | window-pair-forms | K4 hits (≥ 23/24) | null hits | wall |
|---|---|---|---:|---:|---:|---:|
| A1 direct | identity | X, Y ∈ 86,731 (`alpha.bin`) | 1.58 × 10¹⁴ | **0** | 0 (full scope) | 9 s |
| A2 bank | 165,065 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 2.88 × 10¹⁴ | **0** | 0 (1/10 rows) | 112 s |
| A3 all.bin | 165,782 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 2.89 × 10¹⁴ | **0** | 0 (1/10 rows) | 116 s |

(The `T` line of `gn217` counts pair-forms per window for the families and in total for direct; the table multiplies by 7,012.)
Null: shuffled K4 (seed 209252) gave 0 hits, as the pre-registered chance figure (≈ 10⁻¹⁶ per scope) requires. Heavy wall 268 s,
plus 4 s for the gate. No K4 hit, so `check221.py` had nothing to re-derive on K4. MC (the consistency check) gave 0, agreeing with
case 202.

**Gate P (seed 209251): 20/20 PASS** (8 direct, 6 bank, 6 all.bin; the 10 odd plants had one carved crib letter wrong). In every case
`check221.py` independently re-derived the planted (row, dir, ix, X, Y, form, window) with the decrypt within one letter of the plant;
0 agreement mismatches between tool and checker.

## Labels
- A1, A2, A3: **`EXACT-EXCL (named ITA2 / Morse / EBCDIC windows, chunk A, one-error tolerant)`** — only within the 7,012 listed
  windows, the listed alphabet sets and the two transposition families. Not a claim about Morse- or teleprinter-derived keys in general.
- Chunk B (IG, BC) is **not tested**; I-311 stays in progress.

## Blind spots
Only these 42 strings; one ITA2 table and its bit reversal (no original Baudot / CCITT-1 or Murray variants); Morse without timing
units or gap symbols; EBCDIC cp037 only; chunk B not run; mod 26 only; same alphabet sets and transposition families; no two-error
tolerance. The plate transcriptions are secondary.

## Verdict
No solution. The Morse plates and teleprinter / mainframe codes of the named words, as numeric key streams, do not key K4 under
model Q in these scopes.

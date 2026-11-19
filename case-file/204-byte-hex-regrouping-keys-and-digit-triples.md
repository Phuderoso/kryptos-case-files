# Case 204 — "Hex inside hex": byte / hex regrouping keys of named strings, and three-digit groups of the named streams (cycle 218)

**Slot:** free slot (217 was a new family). I-307 preferred an audit, but the Voynich desk's blind recount of case 202 has not arrived,
so the queued new family **I-306** ran early. Next new family is due by cycle 221. Pre-registered in
[PREREG218](../tools/cycle218/PREREG218.md) (local commit 734ffdf) before any K4, plant or null run. Code:
[`tools/cycle218/`](../tools/cycle218/) (the tool is `tools/cycle217/gn217.c`, unchanged); raw results: [`data/cycle218/`](../data/cycle218/).

## Why this family
Case 203 listed "no triples, no hex regrouping" as blind spots. The user's old hunch that K4 may be "hex inside hex" (`[speculation]`)
points to a key that is a familiar word written one layer down (as ASCII bytes, hex nibbles, or the decimal digits of its ASCII codes)
and then regrouped. Such a key is not a letter key in the usual sense, so earlier keyword and periodic tests see it only partly.

## Windows (`keys218.py`, `keys218.bin` sha256 e3f46e43…fdb872, index `data/cycle218/keys218.tsv`)
7,719 distinct 97-shift windows, after dropping every window already tested in cycle 217:

| family | rule (mod 26, cyclic, every offset) | windows |
|---|---|---:|
| B | ASCII bytes of the string (upper and lower case), k = byte | 648 |
| N | hex nibbles of the upper-case ASCII, k = 0..15 | 648 |
| NP | hex nibble pairs at every nibble offset, k = 16a + b (odd offsets straddle bytes) | 648 |
| D2 / D3 | decimal ASCII codes as one digit string, read 2 / 3 digits at a time | 1,225 / 1,474 |
| T3 | I-304 streams 3 digits at a time: π, e, √2, √3, √5, φ, ln 2 (offsets 0–199, s ∈ {0, −1}); K2 coordinates, dedication / Wall / tomb dates, years (cyclic) | 3,076 |

The 35 named strings (K1–K3 keywords and plaintext words with their misspellings, the cribs, BERLIN / CLOCK / WORLDCLOCK /
WELTZEITUHR / MENGENLEHREUHR, Sanborn / Scheidt / Webster / Langley / CIA, Egypt / Carter / Tutankhamun / candle, HEXINSIDEHEX, K2's
coordinates as text in two spellings, the KRYPTOS-keyed alphabet string) are listed in PREREG218.

## Model and result
Model Q exactly as cases 200 / 203: Vig / variant / Beaufort on keyed alphabets X (plain) and Y (cipher); key indexed by plaintext
position (ix 0) or carved position (ix 1); a hit means at least 23 of the 24 crib seats agree (one wrong letter anywhere allowed).

| scope | transpositions | alphabets | window-pair-forms | K4 hits (≥ 23/24) | null hits | wall |
|---|---|---|---:|---:|---:|---:|
| A1 direct | identity | X, Y ∈ 86,731 (`alpha.bin`) | 1.74 × 10¹⁴ | **0** | 0 (full scope) | 13 s |
| A2 bank | 165,065 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 3.17 × 10¹⁴ | **0** | 0 (1/10 rows) | 145 s |
| A3 all.bin | 165,782 × 2 dirs × 2 ix | X, Y ∈ 144 themed | 3.18 × 10¹⁴ | **0** | 0 (1/10 rows) | 145 s |

Nulls: shuffled K4 (seed 209232) gave 0 hits, as the pre-registered chance figure (≈ 10⁻¹⁶ per scope) requires; a non-zero null would
have meant a tool fault. Heavy wall 347 s, plus 7 s for the gate. No K4 hit, so `check218.py` had nothing to re-derive on K4.

**Gate P (seed 209231): 20/20 PASS** (8 direct, 6 bank, 6 all.bin; the 10 odd plants had one carved crib letter wrong). In every case
`check218.py` independently re-derived the planted (row, dir, ix, X, Y, form, window), with the decrypt within one letter of the planted
text. Plant 6 also produced a second direct line with the same Y and window and a different X (84398 vs 74217), which is a crib-equal
alphabet twin; that is expected and not a fault.

## Labels
- A1, A2, A3: **`EXACT-EXCL (named byte / hex / triple windows, one-error tolerant)`**. This holds only within the 7,719 listed
  windows, the listed alphabet sets and the two transposition families. It is not a claim about byte or hex keys in general.
- Family B overlaps earlier periodic-keyword work wherever an alphabet set already absorbs the constant +13 / +19 shift; it is not
  counted as new.

## Blind spots
Only these 35 strings and the I-304 streams. ASCII only: no EBCDIC, Baudot / ITA2, Morse or BCD (→ I-311). No base-36 / base-64, no
reversed strings, mod 26 only, the same alphabet sets and families, no two-error tolerance.

## Verdict
No solution. The "hex inside hex" reading of named words, at the byte, nibble and decimal-code levels, does not key K4 under model Q
in these scopes.

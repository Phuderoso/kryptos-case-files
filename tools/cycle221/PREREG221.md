# PREREG221 — cycle 221 pre-registration (filed before anything below is run on K4, the plants or the null)

Filed 2026-11-19 ~19:51 PT (America/Vancouver). Slots: 219 audit (case 205), 220 free (I-312 chunk 1, case 206), so **221 must be a
new family** (I-314 / I-316). This cycle runs the queued **I-311** (machine / signal encodings as key streams).
Seeds: next free 209251. Reserved here: 209251 (plants), 209252 (null). Next free after this cycle: **209253**.
Base: main 8254227 (cycle 220 published by Firefly on 2026-11-19).

## Part A (I-311, new family): ITA2, Morse and EBCDIC encodings of named strings as key streams

**Why.** Case 204 (byte / hex regrouping keys) listed as blind spots "ASCII only (no EBCDIC, Baudot, Morse, or BCD)". The Morse
plates at the Kryptos entrance are a sourced, physical part of the work (`[sourced]`); a key written one layer down as signal or
machine code fits the user's "hex inside hex" hunch (`[speculation]`). Earlier work used the Morse plates only as *letters*
(cycles 34 / 79: K0 Morse as a running key) or as a fractionating step (cycle 73); never their element encodings as numeric keys.

**Key windows (`keys221.py`, `keys221.bin` sha256 7ce38188…c8389925f, 12,774 distinct 97-shift windows, every window already in
`keys217.bin` or `keys218.bin` dropped).** Named strings: the 35 of PREREG218 plus seven Morse-plate phrases (VIRTUALLYINVISIBLE,
SHADOWFORCES, LUCIDMEMORY, DIGETALINTERPRETATIU, TISYOURPOSITION, SOS, RQ; `[secondary transcription, widely reproduced]`).
Families, all mod 26, cyclic over the encoded string, every offset:
- IT (826): ITA2 5-bit code per character (table with b1 = LSB, and bit-reversed); digits on the FIGS row with FIGS / LTRS codes.
- IG (4,130): ITA2 bit stream regrouped 4 or 8 bits.
- MC (394): Morse element count per character (values 1–5: a digit-range periodic key already excluded by case 202 on the same
  scopes for periods ≤ 24 → kept only as a consistency check; it must give 0).
- MV (396): Morse code as binary with a leading-1 marker (A .- = 5).
- MB (3,371): Morse dot = 0 / dash = 1 stream regrouped 4, 5 or 8 bits.
- EB (810): EBCDIC (cp037) byte per character, upper and lower case. EN (1,215): EBCDIC nibbles and nibble pairs (upper case).
- BC (1,632): 4-bit BCD of the I-304 short digit streams regrouped 5, 6 or 8 bits.

**Chunking (budget).** Case 204 measured ≈ 0.045 s per window for K4 (three scopes) + the null; 12,774 windows ≈ 9.6 min, over the
8-minute budget. **Chunk A (this cycle) = IT, MC, MV, MB, EB, EN** (`split221.py` → `keys221a.bin` sha256 aef84534…7d022d4cfe,
7,012 windows, ≈ 5.3 min). **Chunk B = IG, BC (5,762 windows) is deferred** to a later cycle (I-311 stays in progress); it is not
claimed here.

**Model, scopes, tool, checker.** Exactly PREREG217 / PREREG218: model Q, forms Vig / variant / Beaufort, ix 0 / 1; A1 direct
X, Y ∈ `alpha.bin` (86,731); A2 / A3 behind `bank.bin` / `all.bin`, both dirs, X, Y ∈ `themed144.bin`; `gn217.c` unchanged
(recompiled from tools/cycle217, ≥ 23 of 24 crib seats); `check221.py` = `check217.py` unchanged.

**Chance.** As PREREG217 per window: P(≥ 23/24) ≈ 6.6 × 10⁻³²; with 7,012 windows E ≲ 10⁻¹⁶ per scope.

**Gate P (seed 209251, `plant221.py` = `plant218.py` with seed and key file changed, `runP.sh`).** 20 plants (8 direct, 6 bank,
6 all.bin; odd ids one carved crib letter wrong; plants221.tsv sha256 33e97c4f…72092e6), windows drawn from `keys221a.bin`.
**Bar ≥ 19/20**, else no exclusion label.

**Null (seed 209252).** Shuffled K4 (`random.Random(209252).shuffle`, null0.txt sha256 a63bc3a6…18e9440d) on the full direct scope
and 1/10 row slices of bank / all.bin. Expected 0; a non-zero null is a tool fault to diagnose.

**Labels (fixed now).** Per scope: K4 0 hits → `EXACT-EXCL (named ITA2 / Morse / EBCDIC windows, chunk A, one-error tolerant)`;
a hit with quadgram ≥ −6.0 → `CANDIDATE` (manual read); below → `NO-SIGNAL (crib-consistent, gibberish)` + diagnosis.

**Budget.** Heavy ≤ 8 min wall, `setsid` + `timeout 480`, own process group.

**Disclosures.** Plants and the null string were generated before filing; no tool has been run on K4, plants or the null.

**Blind spots (stated now).** Only these 42 strings; one ITA2 table (with its bit reversal), no original Baudot / CCITT-1, no
Murray variants; Morse without timing units or gap symbols; EBCDIC cp037 only; chunk B not run; mod 26 only; same alphabet sets
and transposition families; no two-error tolerance.

## Part B (owed paperwork): case 205 addendum

Cite the Voynich desk's case 205 null-interval audit (voynich-case-files 0185ed5, `audits/kryptos/c205-null-interval/`): p18 / p19
mid-null, p20 low, p21 K4 1,928 above all 8 nulls (observation only; ≥ 146 nulls needed to show it at 5 %). No relabel.

# PREREG218 — cycle 218 pre-registration (filed before anything below is run on K4 or the nulls)

Filed 2026-11-19 ~07:55 PT (America/Vancouver). Slots: 217 new family (case 203), so 218 is a free slot. I-307 preferred an audit
(Voynich's blind stage-2 recount of case 202), but that recount has not arrived (paused with the 11-14 stop order), so this free slot
runs the queued new family **I-306** early (P2, ~5 min, unchanged tool). Consequence: the next new family is due by cycle 221; 219 and
220 are free (219 should be an audit: I-305 chunk 1, or case 202's recount if it arrives).
Seeds: next free 209231. Reserved here: 209231 (plants), 209232 (nulls). Next free after this cycle: **209233**.
Base: main 7cca6ab (cycle 217 published by Firefly on 2026-11-19).

## Part A (I-306, new family): byte / hex regrouping keys and three-digit groups

**Why.** Case 203 lists as blind spots "no triples, no hex regrouping". The user's "hex inside hex" hunch (`[speculation]`) suggests a
key that is a familiar word but written one layer down: as ASCII bytes, as hex nibbles, or as the decimal digits of its ASCII codes,
then regrouped. None of these is a letter key in the usual sense, so the earlier keyword / periodic tests only partly see them.

**Key windows (`keys218.py`, `keys218.bin` sha256 e3f46e43…fdb872, 7,719 distinct 97-shift windows, every window already in
`keys217.bin` dropped).** Families, all mod 26, cyclic, every offset:
- B (648): ASCII bytes of a named string, upper and lower case, k = byte mod 26.
- N (648): hex nibbles of the upper-case ASCII string, k = nibble 0..15.
- NP (648): hex nibble pairs at every nibble offset, k = (16a + b) mod 26 (odd offsets straddle bytes).
- D2 (1,225) / D3 (1,474): decimal ASCII codes written as one digit string, read two / three digits at a time.
- T3 (3,076): I-304's long streams (π, e, √2, √3, √5, φ, ln 2; first 900 digits, mpmath) three digits at a time, offsets 0–199, and
  I-304's short named streams (K2 coordinates, dedication / Wall / tomb dates, years) three at a time, cyclic; s ∈ {0, −1}.
Named strings (35): KRYPTOS, PALIMPSEST, ABSCISSA, BERLINCLOCK, EASTNORTHEAST, BERLIN, CLOCK, NORTHEAST, SHADOW, LUCID, MEMORY,
IQLUSION, UNDERGRUUND, DESPARATLY, LAYERTWO, IDBYROWS, XLAYERTWO, VIRTUALLY, INVISIBLE, SANBORN, SCHEIDT, WEBSTER, LANGLEY, CIA,
EGYPT, CARTER, TUTANKHAMUN, CANDLE, WORLDCLOCK, WELTZEITUHR, MENGENLEHREUHR, HEXINSIDEHEX, `385765N77844W`,
`38 57 6.5 N 77 8 44 W`, the KRYPTOS-keyed alphabet string.

**Overlap stated now.** Family B is a constant shift of the plain keyword key (byte mod 26 = letter + 13 upper, + 19 lower), so it
overlaps earlier periodic-keyword work wherever the alphabet list already absorbs that shift; it is kept because the keyed-alphabet
sets here are not closed under rotation. Short cyclic windows are periodic keys; periodic P ≤ 24 digit keys were excluded in case 202
only for digit values 0..9, so N (0..15) is partly new and B / NP / D2 / D3 / T3 are new as named windows.

**Model, scopes, tool, checker.** Exactly PREREG217: model Q, forms Vig / variant / Beaufort, ix 0 / 1; A1 direct X, Y ∈ `alpha.bin`
(86,731); A2 / A3 behind `bank.bin` / `all.bin`, both dirs, X, Y ∈ `themed144.bin`; `gn217.c` unchanged (≥ 23 of 24 crib seats);
`check218.py` = `check217.py` unchanged (independent full decrypt + crib recount + quadgram).

**Chance.** As PREREG217 per window: P(≥ 23/24) ≈ 6.6 × 10⁻³²; with 7,719 windows E ≲ 10⁻¹⁶ per scope.

**Gate P (seed 209231, `plant218.py`, `runP.sh`).** 20 plants as PREREG217 (8 direct, 6 bank, 6 all.bin; odd ids one carved crib
letter wrong), windows drawn from `keys218.bin`. **Bar ≥ 19/20**, else no exclusion label.

**Nulls (seed 209232).** Shuffled K4 (`random.Random(209232).shuffle`) on the full direct scope and 1/10 row slices of bank / all.bin.
Expected 0; a non-zero null is a tool fault to diagnose.

**Labels (fixed now).** Per scope: K4 0 hits → `EXACT-EXCL (named byte/hex/triple windows, one-error tolerant)`; a hit with quadgram
≥ −6.0 → `CANDIDATE` (manual read); below → `NO-SIGNAL (crib-consistent, gibberish)` + diagnosis.

**Budget.** Heavy ≤ 8 min wall (estimate ≈ 5.5 min from case 203 timing × 7,719 / 5,870), `setsid` + `timeout 480`, own group.

**Disclosures.** Plants generated (seed 209231) and the null string drawn before filing; no tool run on K4, plants or nulls yet.

**Blind spots (stated now).** Only these 35 strings and the I-304 streams; ASCII only (no EBCDIC, Baudot, Morse, or BCD); no
base-36 / base-64; no key on letters reversed; mod 26 only; same alphabet sets and transposition families; no two-error tolerance.

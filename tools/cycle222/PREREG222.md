# PREREG222 — cycle 222 pre-registration (filed before anything below is run on K4, the plants or the null)

Filed 2026-11-19 ~23:41 PT (America/Vancouver). Slots: 220 free (case 206), 221 new family (case 207), so **222 is free**
(I-319); 223 must be an audit, 224 a new family. This cycle runs **I-311 chunk B**, frozen in PREREG221 and not yet run.
Seeds: next free 209253. Reserved here: 209253 (plants), 209254 (null). Next free after this cycle: **209255**.
Base: main d47ca53 (cycle 221 published by Firefly on 2026-11-19).

## Part A (I-311 chunk B): ITA2 bit regroupings and BCD regroupings of named strings as key streams

**Windows.** Exactly the IG and BC families of the frozen `keys221.bin` (sha256 7ce38188…c8389925f, byte-identical to
`tools/cycle221/keys221.bin`), extracted by `split222.py` → `keys222b.bin` (sha256 d99c3bad…0627f8b8, **5,762 windows**:
IG 4,130 = ITA2 bit stream of the 42 named strings regrouped in 4 or 8 bits, every bit offset; BC 1,632 = 4-bit BCD of the I-304
short digit streams regrouped in 5, 6 or 8 bits). Checked before filing: all 5,762 distinct, 0 overlap with `keys217.bin`,
`keys218.bin` or chunk A (`keys221a.bin`). No window was added or removed after PREREG221.

**Model, scopes, tool, checker.** Identical to PREREG221: model Q, Vig / variant / Beaufort, ix 0 / 1; A1 direct X, Y ∈ `alpha.bin`
(86,731); A2 / A3 behind `bank.bin` / `all.bin`, both dirs, X, Y ∈ `themed144.bin`; `gn217.c` unchanged (tools/cycle217, recompiled
gcc -O3 -march=native -fopenmp; hit = ≥ 23 of 24 crib seats); `check222.py` = `check221.py` = `check217.py` unchanged.

**Chance.** Per window P(≥ 23/24) ≈ 6.6 × 10⁻³² (PREREG217); with 5,762 windows E ≲ 10⁻¹⁶ per scope.

**Gate P (seed 209253, `plant222.py` = `plant221.py` with seed and key file changed, `runP.sh`).** 20 plants (8 direct, 6 bank,
6 all.bin; odd ids carry one wrong carved crib letter), windows drawn from `keys222b.bin`; plants222.tsv sha256 e7e783f0…73b04810.
**Bar ≥ 19/20**, else no exclusion label.

**Null (seed 209254).** Shuffled K4 (`random.Random(209254).shuffle`, null1.txt sha256 24efe4fc…6c850287) on the full direct scope
and 1/10 row slices of bank / all.bin. Expected 0; a non-zero null is a tool fault to diagnose.

**Labels (fixed now).** Per scope: K4 0 hits → `EXACT-EXCL (named ITA2-bit / BCD windows, chunk B, one-error tolerant)`; a hit with
quadgram ≥ −6.0 → `CANDIDATE` (manual read); below → `NO-SIGNAL (crib-consistent, gibberish)` + diagnosis. With chunk A this closes
I-311 within its frozen list only.

**Budget.** Heavy ≤ 8 min wall, `setsid` + `timeout 480`, own process group (expected ≈ 3.7 min from cycle 221's 268 s / 7,012).

**Disclosures.** Plants and the null string were generated before filing; no tool has been run on K4, plants or null with
`keys222b.bin`. Chunk A's K4 result (0 hits) is known.

**Blind spots.** As PREREG221 (one ITA2 table + bit reversal, no Baudot / Murray variants; BCD 8421 only; mod 26; same alphabet sets
and transposition families; no two-error tolerance), plus: no 5-, 6- or 7-bit regroupings of the ITA2 stream (5 is IT itself).

## Part B (owed paperwork): case 206 addendum

Cite the Voynich desk's open recount of case 206 p 18 null cells (voynich-case-files 386e342, `audits/kryptos/c206-p18-recount/`,
2026-11-19 19:59 PT, after cycle 221 was filed): SHA256SUMS 45/45 OK; counts 8/8 match (0, 15, 0, 0, 12, 4, 69, 2), not blind on
values (frozen + hashed before comparing); null 209249's 69 cells are one-error and fall in about eight near-duplicate column-order
families. Descriptive; no relabel.

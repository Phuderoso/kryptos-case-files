# Case file 146 — Hill between two keywords (cycle 158)

**Cycle 158, 2026-11-08. New structure** (IDEAS [I-056](../IDEAS.md); the keyword version of [case 144](144-key-on-both-sides-of-hill.md)).
Evidence labels as in IDEAS I-004.

## Why this family, and is it new?
Cycle 157 was an audit, so the diversity rule required a new family. K1–K3 used **keywords** (PALIMPSEST, ABSCISSA, KRYPTOS), not random
periodic keys. Case 144 tested "Vigenère (period k1) → Hill n×n → Vigenère (period k2)" with **free** keys, which is only testable while
n² + k1 + k2 stays well below 24; long keys (a 10-letter and a 13-letter keyword) were out of reach. Fixing both keys to vocabulary words
leaves only the n² matrix entries unknown, so the 24 crib letters become a strong exact test at any key length.

**Overlap (stated, `data/cycle158/overlap.txt`).** A word of length k is one particular period-k key, so word pairs whose lengths fall
inside case 144's excluded free-key ranges (or inside case 132 via the combined period lcm(k1, n, k2)) were already excluded:
- direct n 2: **96.4 %** of the 1.01 × 10⁸ ordered word pairs were already covered (this part is a regression); n 3: 19.2 % covered →
  **80.8 % new**; n 4: 0.1 % covered → **99.9 % new**;
- behind the bank, core-32 list: n 2 25.1 % covered → **74.9 % new**; n 3 **96.7 % new**; n 4 **99.9 % new**.

So the cycle is genuinely new where it matters (n 3–4 direct, everything behind the bank, all long keyword pairs), not just a restriction
of an excluded space.

## Model and method (`tools/cycle158/hillw.c`)
    encryption  x = p ± E[t mod k1]  →  y_block = H·x_block  →  L = y ∓ F[t mod k2]        (E, F = keywords, phase 0)
    test        Σ_j D[r][j]·(L[bs+j] + sf·F[(bs+j) mod k2]) ≡ P[t] + se·E[t mod k1]  (mod 26),  D = H⁻¹ unknown
- sf, se ∈ {+1, −1}; Beaufort on either side is D → −D, so the four sign pairs cover every Vigenère/Beaufort/variant mix.
- With both words fixed only D is unknown and **its rows are independent**. Per frame, f word and sign, each row's crib vectors get a left
  null space mod 13 and mod 2 (CRT: Z26 = Z2 × Z13); each null vector is one exact linear check on the e word. A configuration survives
  iff every check holds in both fields (necessary and sufficient for a D consistent with all 24 cribs). Invertibility, full decryption and
  scoring of survivors: `solve158.py` (independent brute force mod 26).
- Frames as cycles 141–156: direct; 165,065 bank entries × both directions × model Q (`L[i] = CT[S[i]]`) and carved order
  (`pt[p] = out[S[p]]`); A–Z and KRYPTOS numbering (words mapped with the same numbering); every Hill alignment o. Cribs EASTNORTHEAST
  0-indexed 21–33, BERLINCLOCK 63–73.
- **One-error mode** (`DROP=1`): every crib-bearing Hill block dropped in turn (a wrong carved letter or a wrong crib letter breaks only its
  own block) — an exact superset for one error.

**Scope per text.**
- Direct strict: **all 10,056 × 10,056 vocabulary words** (the cycles 135–152 list, `data/cycle158/vocabulary_all.txt`), n 2, 3, 4:
  7.28 × 10⁹ word-pair tests (signs, numberings, alignments included).
- Direct one error, n 2–3: themed-97 f × all e, and all f × themed-97 e (9.2 × 10⁸ tests).
- Bank strict, n 2–4: core-32 × core-32 (KRYPTOS, PALIMPSEST, ABSCISSA, BERLIN, CLOCK, BERLINCLOCK, EASTNORTHEAST, NORTHEAST, SHADOW,
  SHADOWFORCES, LAYER, LAYERTWO, UNDERGROUND, IDBYROWS, INVISIBLE, MAGNETIC, LODESTONE, TUTANKHAMEN, CARTER, HOWARDCARTER, CANDLE,
  SLOWLY, DESPARATLY, CHAMBER, TOMB, EGYPT, LANGLEY, SANBORN, SCHEIDT, WEBSTER, ILLUSION, IQLUSION): 4.87 × 10¹⁰ tests for K4.
- Texts: K4; nulls null1, null2 (shuffles) and mnull01, mnull02 (cycle 157's shuffles with K4's crib-letter repetition profile) for every
  direct row; null1 and mnull01 on every 4th bank entry.

**Power check first.** The program adds the analytic chance rate 2^−(mod-2 checks) · 13^−(mod-13 checks) over every configuration. Expected
chance survivors for K4: direct n 2 8 × 10⁻²⁰, n 3 1.4 × 10⁻¹², n 4 0.012; bank (from a 1/1000 sample) n 2 ~10⁻¹⁸, n 3 ~3 × 10⁻⁹,
**n 4 ~26**. So n 2–3 everywhere and n 4 direct are tests where a single survivor would be meaningful; n 4 behind the bank is not (carved
frames put some crib letters outside full Hill blocks, leaving 1–2 checks per row).

## Controls (`data/cycle158/controls_run.txt`, `controls_solved.txt`)
Ten planted encryptions of the cycle 137 English control text (`plant158.py`, seed 15800): n 2 PALIMPSEST/KRYPTOS direct; n 2
ABSCISSA/SHADOWFORCES direct KRYPTOS numbering; n 3 EASTNORTHEAST/LAYERTWO; n 4 BERLINCLOCK/KRYPTOS; n 2 behind bank entry 4242 (model Q);
n 3 behind 120000 inverse (carved); n 3 behind 99999 inverse (model Q); n 2 with two non-themed vocabulary words (RUBBED/CONDESCENDED,
run against the full list); **ctl7 one corrupted carved letter (position 26) and ctl8 one wrong crib letter (position 66)**.
**10/10 pass:** each clean plant is found exactly once in strict mode with the planted words and signs, and the independent Python re-solve
decrypts it to the English text (−4.04 to −4.10, 0 wrong decided crib letters). Both error plants fail strict and are recovered only in
one-error mode, with the dropped block holding the error (blocks 26 and 64).

## Independent check (`data/cycle158/independent_check.txt`)
`indep158.py` (pure Python/numpy) decides, for every direct configuration with the first 40 themed words on both sides, every row of D
and both fields, whether **some** D row satisfies that row's equations, by brute force over all p^n row vectors (no null spaces). Run for
K4, null1, mnull01, ctl3, ctl4 at n 2, 3, 4: **15 runs × 9 counts, all identical** to `hillw VERB=1`; at n 3–4 the counts are large
(mod 2 up to 14,196, mod 13 up to 1,207), so this check is not a recount of zeros. Survivor lines were independently re-solved (`solve158.py`).

## Results (`data/cycle158/summary.txt`, `c_lines.txt`)
| Scope | K4 | nulls | Label |
|---|---|---|---|
| Direct strict, all × all words, n 2 (96 % regression of case 144) | **0** of 1.6 × 10⁹ | 0, 0, 0, 0 | `EXACT-EXCL` |
| Direct strict, all × all words, n 3 | **0** of 2.4 × 10⁹ | 0, 0, 0, 0 | `EXACT-EXCL` |
| Direct strict, all × all words, n 4 | **0** of 3.2 × 10⁹ | 0, 0, 0, 0 | `EXACT-EXCL` |
| Direct one error, n 2–3, at least one key in the themed 97 | **0** | 0, 0, 0, 0 | `EXACT-EXCL` under one wrong carved or crib letter |
| Bank strict, core-32 × core-32, n 2 (1.1 × 10¹⁰) | **0** | 0, 0 (¼ bank) | `EXACT-EXCL` |
| Bank strict, core-32 × core-32, n 3 (1.6 × 10¹⁰) | **0** | 0, 0 (¼ bank) | `EXACT-EXCL` |
| Bank strict, core-32 × core-32, n 4 (2.2 × 10¹⁰) | 44 consistent (all carved order); 24 have only singular D; 20 invertible (10 configurations × the bank's inverse twin), all decoded, best −7.76 | null1 20 (7 invertible, best −7.80), mnull01 14 (9 invertible, best −7.67) on ¼ of the bank (≈ 80 / 56 scaled); analytic ≈ 26 | `NO-SIGNAL` (exhaustive decode); screen `LOW-POWER` |

English scores about −4.1 and shuffled text about −7 to −8. No K4 configuration came within 3.5 points of English; the K4 n 4 survivors
match the nulls in number and in score (example: f INVISIBLE, e LODESTONE, best −7.83, gibberish around the cribs).

## Verdict
**Negative.** K4 is not "keyword → Hill n×n → keyword" (any Vigenère/Beaufort/variant mix, A–Z or KRYPTOS numbering, keys starting at the
first letter) for any of the 10,056 vocabulary words on both sides with n = 2–4 directly, nor behind any of the 165,065 bank
transpositions (both orders) for n = 2–3 with both keys from the 32 core themed words. Directly it stays excluded under one wrong carved or
crib letter for n = 2–3 when at least one key is one of the 97 themed words. Behind the bank at n = 4 the test cannot exclude (chance
survivors are expected), and every survivor reads as noise, as in the nulls.

## Limits and blind spots
- Keys start at the first letter of the stream (phase 0). Shifted keyword phases, keys repeated per row or column, and keys reset at a
  boundary are not covered.
- Behind the bank only the 32 core words (cost); bank × full vocabulary, the other 65 themed words, and one error behind the bank are open.
- n 4 behind the bank: LOW-POWER as an exclusion; judged by quadgram score only.
- One error direct only when one key is themed; all × all one error (≈ 10 core-min per text) is open.
- Mixed-alphabet (Quagmire-style) keyed tableaux, other numberings, transpositions outside the bank, dropped/extra letters (I-039).

## Files
[tools/cycle158/](../tools/cycle158/) (`hillw.c`, `plant158.py`, `solve158.py`, `indep158.py`, `overlap158.py`, `run_cycle158.sh`,
`summarize158.py`) · [data/cycle158/](../data/cycle158/) · [journal](../journal/2026-11-08-cycle158.md).

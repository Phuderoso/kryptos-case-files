# Case file 150 — A key that changes at a boundary and keeps the width-7 phase (cycle 162)

**Status:** negative. `EXACT-EXCL` for the same-alphabet and A–Z/KRYPTOS-cross models, directly and behind the bank, strict and
(directly) under one error; `NO-SIGNAL` / `LOW-POWER` for the looser model with a free alphabet per segment. **Type:** new family
(IDEAS [I-013](../IDEAS.md)); cycle 161 was an audit, so this cycle had to open untested ground.

## Question
Five of K4's six doubled letters start at a position ≡ 4 (mod 7) ([case 96](96-doubled-letters-mod-7.md)). One period-7 key
cannot make them: the doubles at 25 and 32 need the same key step (+1, plaintext NO and ST) while TT at 67 needs +5, and even seven
free alphabets contradict the cribs at p = 7. Case 96 left the obvious repair open: **the key changes somewhere between 32 and 67
but the period-7 phase carries on**, as a K1–K3-style encipherer would produce by switching keyword at a sentence break. Could K4
be two period-7 Quagmire III keys (one keyed alphabet on both sides, as in K1/K2), switching at an unknown boundary, applied directly
or before / after one of the 165,065 bank transpositions?

## What was already covered (`data/cycle162/overlap.txt`)
| earlier test | what it covered | overlap with this cycle |
|---|---|---|
| [case 52](52-split-key-two-segments.md) (cycle 54) | two periodic keys, p1 ≤ 13, p2 ≤ 11 (7/7 included), split 34–63, **direct only**, 86,731 alphabets, scored by quadgrams | identity layer with b 34–63: 1 of 660,261 layer configurations |
| [case 123](123-transposition-first-quagmire.md) (cycle 135) | one periodic key behind the bank, vocabulary Q-I/II/III, p ≤ 16, both index orders | only the edge b = 0 / 97 (no change) |
| [case 96](96-doubled-letters-mod-7.md) (cycle 104) | general periodic substitution, one key | no key change |

So behind the bank more than 99.999 % of the space is new; directly, the boundaries inside a crib and the *exact* test are new.

## Model and method ([`tools/cycle162/split7.c`](../tools/cycle162/split7.c))
- **Key:** key 1 (period 7) on index positions `< b`, key 2 (period 7) on positions `≥ b`, residue counted from position 0 (the
  phase is kept). With free key letters a phase restart is only a rotation of key 2, so this also covers keys that restart at b.
  Boundary **b free over 0–97**, including inside EASTNORTHEAST or BERLINCLOCK.
- **Tableau:** Quagmire III on each of the 86,731 alphabets of `alpha.bin` (A–Z, KRYPTOS and the keyword / keyphrase alphabets of
  cycles 54–56); Vigenère (variant Beaufort is the dual, same consistency) or Beaufort, **chosen independently per segment**.
- **Layers:** directly on the copper, and behind every bank permutation in both directions with the key at the plaintext index
  (model Q: substitute, then transpose) or at the carved index (transpose, then substitute): 660,261 layer configurations per text.
- **Exact test:** within each segment, cribs in one residue class must give one key value. A prefix scan finds the first crib
  that breaks segment 1 (b must stay at or below it), a suffix scan the first that breaks segment 2 (b must lie above it); a
  configuration is consistent iff the two windows overlap. An alphabet-free prefilter (equal cipher ⇔ equal plain letter within a
  class) runs first; the first check of each scan is evaluated for all alphabets at once.
- **Three pre-registered statistics** (written to the local checkpoint before K4 was run):
  - **S (primary):** configurations with a consistent (alphabet, mode 1, mode 2, b), same alphabet in both segments;
  - **Z:** A–Z in one segment and KRYPTOS in the other;
  - **X (secondary, count only):** any of the 86,731 alphabets in each segment independently. Compared with the nulls by rank,
    p = (#nulls ≥ K4 + 1)/(n + 1).
- **Power.** With period 7 each segment occupies at most 7 residue classes, so **every boundary leaves at least 24 − 14 = 10
  crib checks**. The chance of a false S hit is ≤ 660,261 × 86,731 × 4 × 25 boundary classes × 26⁻¹⁰ ≈ 0.04 per text; for Z it is
  negligible. X multiplies the alphabet space by 86,731 and is expected to have false hits, hence the nulls.
- **One error, direct:** leave each of the 24 cribs out in turn (one wrong crib letter or one wrong carved letter under a crib;
  a wrong carved letter elsewhere cannot break a substitution test). Behind the bank one-error was not run (cost ×24).
- **Texts:** K4; shuffled-K4 nulls null1–null2 (seeds 16201–16202) and crib-profile-matched nulls mnull01–02 (cycle-157
  generator, seed base 16210000) behind the bank; all 8 nulls (null1–4, mnull01–04) directly.

Wall time: 282 s main run on 8 cores, about 5.1 minutes of heavy compute in all ([`timing.txt`](../data/cycle162/timing.txt)).

## Controls ([`plant162.py`](../tools/cycle162/plant162.py), independent Python encryption; [`controls_out.txt`](../data/cycle162/controls_out.txt))
| plant | layer | recovered |
|---|---|---|
| ctl1 alphabet #5000 (BECKONED), Vig PALIMPS \| Beau SHADOWS, b 50 | carved index, perm 4242 | yes: alphabet 5000, Vig/Beau, b window 47–51 |
| ctl2 KRYPTOS, Beau IQLUSIO \| Vig VIRTUAL, **b 66 inside BERLINCLOCK** | model Q, inverse of perm 99999 | yes, b 66 exactly (plus 3 alphabets identical to KRYPTOS on the touched letters) |
| ctl3 alphabet #20000 (ERUDITE), Vig DESPARA \| Vig LAYERTW, **b 28 inside EASTNORTHEAST** | direct | yes, b 28 |
| ctl4 A–Z Vig BERLINW \| KRYPTOS Beau CLOCKSX, b 40 | carved index, perm 120000 | yes in model Z (A–Z / KRYPTOS cross), b window 39–42 |
| ctl5 KRYPTOS, Vig SANBORN \| Beau WEBSTER, b 45, **carved letter 28 altered** | direct, one error | strict: no hit; dropping crib 7 (position 28) recovers it |

The ctl1 model-X decode reads `…CROSSTHEASTNORTHEASTW…BERLINCLOCKSTRUCKTHEH…` at −4.10 per quadgram.
Independent recount ([`recount162.py`](../tools/cycle162/recount162.py): numpy, every alphabet, every boundary, straight from the
definition, no scans or prefilter): **23 / 23** configurations agree ([`recount.txt`](../data/cycle162/recount.txt)): 6 control
runs, K4 direct strict and one-error, 6 K4 X configurations, 3 null X configurations, 6 random K4 configurations (all zero, a weak
check).

## Results ([`summary.txt`](../data/cycle162/summary.txt))
Behind the bank, configurations with at least one consistent solution (330,130 per index order):

| text | S model Q | S carved | Z (both) | X model Q | X carved | X total |
|---|---|---|---|---|---|---|
| **K4** | **0** | **0** | **0** | 62 | 10 | **72** |
| null1 | 0 | 0 | 0 | 54 | 26 | 80 |
| null2 | 0 | 0 | 0 | 32 | 10 | 42 |
| mnull01 | 0 | 0 | 0 | 68 | 4 | 72 |
| mnull02 | 0 | 0 | 0 | 26 | 10 | 36 |

Directly on the copper: **K4 0** for S, Z and X, strict and with any one crib dropped (all 8 nulls also 0).

- **S and Z: `EXACT-EXCL`.** No same-alphabet split period-7 key, and no A–Z / KRYPTOS cross, fits K4 at any boundary, directly
  or behind any bank transposition in either direction and index order; directly this also holds under one error. The power
  bound (≈ 0.04 false hits per text) and the five recovered plants show the test could have seen it.
- **X: `NO-SIGNAL` / `LOW-POWER`.** K4 72 against 80, 42, 72, 36 (p = 0.6, pre-registered). Bank entries come in adjacent inverse
  pairs, so the 72 are 36 distinct transpositions. All 72 K4 X configurations were decrypted with every consistent alphabet choice
  ([`decode.txt`](../data/cycle162/decode.txt)): best −6.58 per quadgram including the cribs, −7.54 off-crib, e.g.
  `FWIFIWXAVYRACOUXYDSSDEASTNORTHEASTHEVUDFLVYODEUOIHJXSDBNTUBWLCABERLINCLOCKDRQLESUS…`. The nulls' best: −6.67 to −6.99
  (off-crib −7.41 to −8.00). English scores about −4.1. Nothing reads as English. K4's best crib-inclusive score tops the four nulls,
  which with four nulls is p = 0.2 and was not a pre-registered statistic; its off-crib score sits inside the null range.

## What this excludes
A K1/K2-style Quagmire III whose period-7 key changes at any point (keyword switch at a sentence break, or anywhere else) while
the width-7 phase continues, on any of the 86,731 alphabets, Vigenère or Beaufort per segment, either on its own or before / after
any of the 165,065 bank transpositions. So the five doubles at ≡ 4 (mod 7) are **not** explained by a two-keyword period-7 split
on a shared tableau.

## Not covered (new IDEAS cards)
- Behind the bank under one error (×24 cost, ~2 min per text): **I-069**.
- Three or more segments (one switch per sentence), or two boundaries with key 1 coming back: **I-070**.
- Different keyed alphabets per segment with a *themed or vocabulary* restriction (between Z and X), and Quagmire I/II/IV per
  segment: **I-071**.
- Period 14 (7k) or a different period per segment: case 52 shows p ≥ 13 per segment is crib-underdetermined, so only scored tests
  apply; left inside I-070.

## Reproduce
`gcc -O3 -march=native -o tools/split7 tools/cycle162/split7.c`; put `k4.txt`, `controls.txt` (from `plant162.py`) and
`mnulls.txt` (from `tools/cycle157/mknulls157.py 4 16210000 k4.txt`) in the working directory with `alpha.bin` (the 86,731-alphabet file of cycles 54–56, not committed for size) and the bank
`perms97.bin`; run `tools/cycle162/run_cycle162.sh` (resumable), then `decode162.py` on the X lines and `recount162.py` for spot
checks.

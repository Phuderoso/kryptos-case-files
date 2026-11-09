# Case file 151 — The split period-7 key under one error, behind the bank (cycle 163)

**Status:** negative. `EXACT-EXCL` (under the stated model, with a language gate) for the same-alphabet split key and the
A–Z/KRYPTOS cross behind every bank transposition when **any one** crib letter, or the carved letter under it, is wrong; the
survivor **count** for the same-alphabet model is `LOW-POWER` (K4 12 vs 2 nulls 2 and 0, p floor 1/3) and goes to I-072.
**Type:** audit / variant (IDEAS [I-069](../IDEAS.md)); cycle 162 was a new family, so an audit slot was allowed.

## Question
[Case 150](150-split-key-width7-phase.md) excluded a period-7 Quagmire III key that changes keyword at a free boundary b while the
width-7 phase continues, on 86,731 alphabets, directly (strict and one-error) and behind the 165,065-entry bank (strict only).
K1 and K2 each carry a deliberate error, so a strict test behind the bank could miss the true configuration by one letter. Does
any configuration survive if one of the 24 known plaintext letters (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-indexed) is left out?

## Method ([`tools/cycle163/split7e.c`](../tools/cycle163/split7e.c))
- **Model:** exactly case 150 (key 1 on index positions `< b`, key 2 on `≥ b`, residue from position 0, b in 0–97, Vigenère or
  Beaufort per segment; layers direct, and behind every bank permutation in both directions with the key at the plaintext index
  (model Q) or the carved index): 660,261 layer configurations per text.
- **One error, single pass.** Leaving each crib out in turn would cost 24× the strict run (~25 min per text). Instead: the prefix
  scan compares each crib with the first member of its residue class; at the first conflict (crib i against reference f) any single
  removal that repairs the prefix must remove i or f. So the one-error prefix bound is `B1e = max(B1, scan without i, scan without
  f)`, and the same holds mirrored for the suffix (`B2e`). Because the dropped crib lies in only one segment, a configuration is
  one-error consistent iff `B2 ≤ B1e` or `B2e ≤ B1` (strict bound on the other side). The alphabet-free prefilter of split7.c is
  applied after removing each crib in turn (pass if any removal passes). Cost ≈ 3.7× strict (2.4 s per 1,200 configurations).
- **Statistics, pre-registered** ([`preregistration.md`](../data/cycle163/preregistration.md), written before the K4 bank run):
  primary **S1e** (configurations with a same-alphabet (alphabet, mode 1, mode 2) consistent for some b and some single dropped crib)
  and **Z1e** (A–Z in one segment, KRYPTOS in the other); classification EXACT-EXCL if 0, else rank against nulls and decode every
  survivor. Secondary X1e (alphabet free per segment) as a count only.
- **Texts:** K4; behind the bank shuffled null1 (cycle 162, seed 16201) and crib-profile-matched mnull01 (cycle 157 generator, seed
  base 16210000) — the two cycle-162 nulls with the highest strict X counts; direct one-error for K4 and all 8 cycle-162 nulls.

Wall time: 514 s main run on 8 cores, ~9.1 min heavy compute in all ([`timing.txt`](../data/cycle163/timing.txt)).

## Controls ([`plant163.py`](../tools/cycle163/plant163.py) with the independent cycle-162 encryptor; [`controls_out.txt`](../data/cycle163/controls_out.txt))
| plant | layer | strict split7 | one-error split7e |
|---|---|---|---|
| ctl6 alphabet #3000 (ARGUMENTS), Vig QUARTZS \| Vig LODESTO, b 55, carved letter under crib 5 altered | carved index, inverse of perm 77777 | no hit | recovered (alphabet 3000, Vig/Vig, b window 52–57) |
| ctl7 KRYPTOS, Beau SHADOWF \| Vig ORCESAX, **b 70 inside BERLINCLOCK**, letter of crib 0 altered (the *reference* member of its class: tests the "remove f" branch) | model Q, perm 31337 | no hit | recovered (KRYPTOS, Beau/Vig, b window 67–70) |
| ctl8 A–Z Vig MAGNETI \| KRYPTOS Beau CLUELES, b 35, carved letter under crib 20 altered | carved index, perm 5000 | no hit | recovered in model Z |
| ctl9 decoy: ctl6 with **two** letters altered | carved index | no hit | **no hit** (one-error mode does not admit two errors) |

Decoded, the plants read `…FELLACROSS…EASTNFRTHEASTWE…TOWARD?HEOLDT…BERLINCLOCK…` at −4.07 to −4.12 per quadgram off-crib, with
the altered letter visible inside the dropped crib. **Independent recount** ([`recount163.py`](../tools/cycle163/recount163.py):
numpy, every dropped crib and none × every boundary × every alphabet, straight from the definition): **124 / 124** configurations
agree with split7e (4 controls checked by hand, every K4 and null1 survivor, 30 random K4 X1e lines, 60 random K4 and 20 random
mnull01 configurations; [`recount.txt`](../data/cycle163/recount.txt)). **Regression:** the strict counts computed inside split7e
reproduce case 150 exactly (S 0; X K4 72, null1 80, mnull01 72).

## Results ([`summary.txt`](../data/cycle163/summary.txt))
| text | S1e model Q | S1e carved | Z1e | X1e (count only) |
|---|---|---|---|---|
| **K4** | **12** | **0** | **0** | 8,366 |
| null1 | 2 | 0 | 0 | 8,892 |
| mnull01 | 0 | 0 | 0 | 9,850 |

Directly on the copper: K4 and all 8 nulls 0 for S1e, Z1e and X1e (agrees with case 150's 24-drop loop).

- **Z1e: `EXACT-EXCL`.** No A–Z / KRYPTOS cross split key fits K4 behind any bank transposition with one crib wrong.
- **S1e: 12 configurations = 6 transpositions** (bank entries come in adjacent inverse pairs), on 5 alphabets (TIMELIEST,
  LAYERTWO+RQ, CIA+LUCID, CAUDAM k/r twins, POSITION+LAYERTWO), all with the key at the plaintext index and the boundary where a
  segment keeps the fewest checks (b 28–33 inside EASTNORTHEAST or 64–67 inside BERLINCLOCK). With each segment holding one key
  value per residue, **every survivor fixes all 97 letters**; [`decode.txt`](../data/cycle163/decode.txt) decrypts each for every
  admissible (drop, boundary). Best K4 −7.21 per quadgram including cribs, −7.88 off-crib, e.g.
  `HARBCPLEGSWEWRHMCZHWBEASTNORTHEAZTXLJLCMCIYQPJKDSABXPTZPHIJOZAFBERLINCLOCKKWUQYOWDEJBHEDEVXSBKVHS`; null1's best −7.08 / −7.83.
  English sits near −4.1. So no one-error split key behind the bank yields a readable K4 → **excluded under the model, by the
  language gate** (no survivor is underdetermined, so this is not a scoring judgement on partial text).
- **The count is not evidence.** K4 12 sits above both nulls (2, 0), but with two nulls the best attainable p is 1/3; the counts
  are small and come in pairs, so the honest label is `LOW-POWER`. A proper lineup (≥ 10 profile-matched nulls, statistic fixed
  beforehand) is queued as **I-072**; whatever it shows, the survivors themselves are already decoded and gibberish.

## What this excludes
A K1/K2-style split period-7 Quagmire III (one keyed alphabet for both keys, or A–Z against KRYPTOS) with a free switch point and
the width-7 phase kept, before or after any of the 165,065 bank transpositions in either direction and index order, **even if one
known plaintext letter or the carved letter under it is wrong**. Together with case 150 the strict and one-error versions are now
closed directly and behind the bank.

## Not covered
- Two errors (the decoy shows the test does not admit them); a wrong letter outside the cribs cannot affect a substitution test.
- The free-alphabet model X stays without power (count only).
- More nulls for the S1e count: **I-072**. Reusing the "remove i or f" trick for other strict exact families (I-041): **I-073**.

## Reproduce
`gcc -O3 -march=native -o tools/split7e tools/cycle163/split7e.c`; in a working directory put `k4.txt`, cycle 162's
`controls.txt` (null1–null4) and `data/cycle163/mnulls.txt`, plus `alpha.bin` and `perms97.bin` (paths in the runner); run
`tools/cycle163/run_cycle163.sh` (resumable; `TEXTS="null2 mnull02"` adds nulls), then `decode163.py CT run/bank_<text>_*.txt`
and `recount163.py` / `compare163.py` for spot checks.

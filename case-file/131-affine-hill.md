# Case file 131 — Affine Hill (Hill + period-n additive key), n = 2–5

**Cycle 143, 2026-11-08. Family: new structure** (Hill combined with a periodic additive layer; case file 26 listed
"Hill combined with a periodic … layer" as untested).

## Model
Per block, `p = D·c + e (mod 26)` with D invertible and e a period-n shift — a Hill cipher followed by a Vigenère
with key length equal to the block size (or, read the other way, a Vigenère under a Hill). Tested:

- n = 2, 3, 4, 5; every block alignment o = 0..n−1;
- numbering A–Z and KRYPTOS (KRYPTOSABCDEFGHIJLMNQUVWXZ);
- direct, and behind all 330,130 bank permutations (165,065 entries × both directions) in both index orders
  (model Q: Hill applied after the transposition; carved: Hill applied to the carved text, then transposition).

Cribs EASTNORTHEAST (21–33) and BERLINCLOCK (63–73). Each row of [D | e] has n+1 unknowns, solved exactly
mod 2 and mod 13 and combined by CRT; consistent configurations with an invertible D are decoded and scored by
mean log10 quadgram outside the cribs.

## Power
n = 2 and 3 are heavily overdetermined (each row meets ~12 and ~8 crib equations for 3 and 4 unknowns): a random
text survives essentially never. n = 4 has ~6 equations per row for 5 unknowns: about 1 in 24,000 configurations
survives on random text. n = 5 has 4–6 equations for 6 unknowns: most consistent configurations are left with
too many free solutions to enumerate under the default caps and are only counted as *underdetermined*.

## Controls (`data/cycle143/controls_check.txt`)
Planted affine-Hill encryptions of the English control text:

| control | setting | result |
|---|---|---|
| ctl1 | n 4, direct, o 1, A–Z | recovered, −4.10 |
| ctl2 | n 3, model Q, entry 4242, KRYPTOS | recovered (both duplicate entries), −4.09 |
| ctl4 | n 2, carved, inverse of 99999, KRYPTOS | recovered, −4.06 |
| ctl7 | n 3, carved, entry 120000 | recovered, −4.07 |
| ctl8 | n 4, model Q, entry 77777 | recovered, −4.09 |
| ctl3 | n 4, carved, entry 160000 | **consistent but underdetermined — not scored** |
| ctl6 | n 4, carved, entry 50000, KRYPTOS | **consistent but underdetermined — not scored** |
| ctl5 | n 5, direct, o 2 | **consistent but underdetermined — not scored** |

The failures are honest blind spots, not misses: the true configuration was *consistent* and counted as underdetermined.
So for n = 2–4 the underdetermined count is itself a test: any K4 configuration in that state would have been listed.

## Results (`data/cycle143/results.txt`; 55 s wall)

| text | n = 2 | n = 3 | n = 4 | n = 5 |
|---|---|---|---|---|
| K4 | 0 / 2.64 M consistent | 0 / 3.96 M | 224 scored, 0 underdet., best −7.19 | 0 scored, 2.38 M underdet. |
| null 1 | 0 | 0 | 216 scored, best −7.45 | 2.11 M underdet. |
| null 2 | 0 | 0 | 256 scored, best −7.28 | 2.12 M underdet. |

English scores about −4.1; shuffled text −6 to −7.5. **K4 behaves exactly like its shuffles.**

## Verdict
**Negative** for affine Hill n = 2, 3, 4 direct and behind the 165k bank, both index orders, A–Z/KRYPTOS numbering,
every alignment — exhaustive (no K4 configuration was consistent-but-unscored). n = 5 is **not** tested: its
consistent configurations are too free for exact enumeration (planted n = 5 control not recovered).

## Limits
- n = 5 affine (and n ≥ 6); other numberings; the shift on the ciphertext side is the same model up to `e' = D·e`, so it is covered.
- Shift with a period different from n (e.g. Hill 2×2 + Vigenère period 7) — not tested.
- Only the 165k bank of transpositions.

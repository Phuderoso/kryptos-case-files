# Case file 144 — A key on both sides of the Hill step (cycle 156)

**Cycle 156, 2026-11-08. New structure** (IDEAS [I-050](../IDEAS.md); combines [case 132](132-hill-plus-periodic-key.md) and [case 142](142-hill-then-ciphertext-side-key.md)).
Evidence labels as in IDEAS I-004.

## Why this family, and why it is new
Cycle 155 was an audit, so the diversity rule required a new family. Case 132 put a periodic key *before* the Hill step (in encryption
order), case 142 put one *after* it. Cycle 156 puts **one on each side, with independent periods**:

    encryption  x = p + e[t mod k1]  →  y_block = E·x_block  →  L = y + f[t mod k2]
    decoder     out_block = D·(L_block − f) + e',   D = E⁻¹,  e' = −e

Beaufort or variant forms on either side are the same model with D → −D and/or the keys negated, so all nine Vig/Beau/variant
combinations are covered at once.

**Overlap check.** The combined additive key `e'[t mod k1] − (D·f_block)[r]` is periodic with period lcm(k1, n, k2), so this model is a
special case of case 132's linear model at that period. Pairs with lcm(k1, n, k2) inside case 132's tested range (n 2 ≤ 14, n 3 ≤ 10,
n 4 ≤ 4) were already covered; they were rerun as a regression check (48 of the 153 direct pairs; K4 0 everywhere, as case 132 requires).
**New in this cycle:** every pair with a longer combined period, where case 132's general model is underdetermined but the two-key
structure (n² + k1 + k2 unknowns) is not. Example: n 2, k1 3, k2 5 is a period-30 key in case 132's language (30 unknowns, untestable
with 24 cribs) but only 12 unknowns here.

## Method (`tools/cycle156/hill2s.c`)
- Frames as cycles 141/144/153/154: direct; behind all 165,065 bank entries in both directions, model Q (`L[i] = CT[S[i]]`) and carved
  order (`pt[p] = out[S[p]]`); A–Z and KRYPTOS numbering; every alignment o. Cribs EASTNORTHEAST 22–34, BERLINCLOCK 64–74 (1-based).
- **Exact, split mod 2 / mod 13 (CRT).** In each field: (R) D is fixed row by row (rows with most crib equations first); after each row the
  equations of the fixed rows are linear in (f, e) and solved by Gaussian elimination, so an inconsistent prefix prunes every completion;
  at the leaf D must be invertible; or (F) every f on the crib-touched residues is enumerated and (D, e) solved linearly (used mod 13 for
  n ≥ 3). No sampling, no score threshold in the consistency test.
- Survivors: every CRT pair (≤ 20,000) decrypted and scored by mean log10 quadgram over decided non-crib letters (English ≈ −4.1,
  shuffled ≈ −7). Configurations with too many solutions to pair are printed as `U` lines (undecoded).
- **One-error mode (`DROP=1`, direct):** re-solve with each crib-bearing Hill block's equations dropped; a wrong carved letter or a wrong
  crib letter breaks only its own block, so this is an exact superset for one error.

**Scope per text.** Bank, strict: n 2, the 18 pairs with k1, k2 ≥ 2, k1 + k2 ≤ 12 and lcm(k1, 2, k2) > 14 — (2,9) (3,5) (3,7) (3,8) (3,9)
(4,5) (4,7) (5,3) (5,4) (5,6) (5,7) (6,5) (7,3) (7,4) (7,5) (8,3) (9,2) (9,3) — 2.64 M configurations each, 47.5 M per text.
Direct, strict and one-error: n 2 k1, k2 2–12 (121 pairs), n 3 k1 2–8 × k2 2–5 (28), n 4 k1, k2 2–3 (4). Texts: K4 and two
shuffled-K4 nulls at the same scale. **Power check first:** timing probes showed n 3 behind the bank costs ~0.2–5 s per 20 entries
(13^k2 mod-13 enumeration), so the bank part was limited to n 2. Main run 108 s wall on 8 processes; probes, controls and checks bring
heavy compute to about 6.5 min.

## Controls (`data/cycle156/controls_run.txt`, `independent_check.txt`)
Ten planted encryptions of the cycle 137 English control text (`plant.py`, seed 15600): n 2 (3,5) direct; n 2 (5,4) model Q (KRYPTOS);
n 2 (3,7) carved; n 3 (2,5) direct; n 3 (4,3) direct KRYPTOS; n 2 (7,3) direct; n 4 (2,3) direct; n 2 (5,3) carved inverse entry (KRYPTOS);
plus **ctl7 (n 2 (3,5), one corrupted carved letter inside a crib block)** and **ctl8 (n 3 (2,5), one wrong crib letter)**.
**10/10 pass:** the eight clean controls decrypt with 0 wrong letters (92–96 decided letters, −4.04 to −4.13). Both error controls fail
the strict test and are recovered by the one-error mode with the dropped block holding the error (ctl7 block 26–27, ctl8 position 67,
1-based); the only wrong letters are inside that block. The printed keys can differ from the planted ones by a key gauge, but
re-decryption with the planted keys and with the printed keys gives the same text (`check.py` part A).

## Independent check (`data/cycle156/independent_check.txt`)
`check.py` (pure Python, no shared code) recounts the per-field solution counts of every direct configuration by **enumerating every f
and solving (D, e)**, a different algorithm from the C program's row-by-row D enumeration (n 2 both fields with k2 ≤ 3 mod 13, and every n
mod 2 with k2 ≤ 8). **1,788 per-field counts, 1,788 identical** (13 non-zero; most configurations already fail mod 2, so the
non-zero part of this check is small).

## Results (`data/cycle156/results_table.txt`)
| Scope | K4 | null 1 | null 2 | Label |
|---|---|---|---|---|
| Bank, strict, n 2, 18 new (k1, k2) pairs (47.5 M configs per text) | **0** consistent | 0 | 0 | `EXACT-EXCL` |
| Direct, strict, all 153 pairs except the four below | **0** | 0 (except n 2 (11,9), (11,10): 1) | 0 (except (11,10): 1) | `EXACT-EXCL` |
| Direct, strict, n 2 (9,11), (10,11), (11,12), (12,11) | 1, 2, 4, 4; best ≤ −7.07 | 0, 0, 2, 2 | 0, 1, 1, 1 | `NO-SIGNAL` (exhaustive decode) |
| Direct, one error, 131 of the 153 pairs (all except the 22 below) | **0** | 0, except 1 in n 3 (8,3) | 0, except 1–2 in n 2 (9,9), (9,12), (12,9), n 3 (7,4), n 4 (2,2) | `EXACT-EXCL` under one wrong carved or crib letter |
| Direct, one error, n 2 (7,11) (7,12) (8,11) (9,10) (9,11) (10,9) (10,11) (11,7) (11,8) (11,9) (11,10) (12,7), n 3 (7,5) (8,4) (8,5), n 4 (2,3) (3,2) (3,3) | 2–48 per pair, all decoded, best −6.95 | 0–40, best −6.92 | 4–46, best −7.00 | `NO-SIGNAL`; screen `LOW-POWER` (K4 inside null range) |
| Direct, one error, n 2 (10,12), (12,10), (11,12), (12,11) | 14–52, of which 12–52 undecoded (U) | 25–38 | 25–45 | `LOW-POWER` (undecoded) |

Full per-pair counts (tests / strict survivors / underdetermined / one-error survivors / one-error underdetermined / best) in `results_table.txt`.
No configuration of any text came within 2.5 points of English; no line reached the print threshold (−4.6).
Where survivors exist, K4's counts and scores sit inside the null range.

## Verdict
**Negative.** K4 is not "Vigenère (period k1) → Hill n×n → Vigenère (period k2)" (any Vig/Beau/variant mix, A–Z or KRYPTOS numbering)
for n 2 with the 18 new pairs k1 + k2 ≤ 12 behind the 165k bank (both orders), nor directly for any tested (n, k1, k2) except four long n 2
pairs where a handful of survivors decode to noise, as in the nulls. Directly it stays excluded under one wrong carved or crib letter for
131 of the 153 tested pairs: every n 2 pair with k1 + k2 ≤ 17 (and several longer ones), every n 3 pair except (7,5), (8,4), (8,5), and n 4 (2,2).

## Limits and blind spots
- Behind the bank only n 2 and k1 + k2 ≤ 12, strict only (n 3/n 4 behind the bank and one error behind the bank are open → I-055).
- Direct n 3 only k2 ≤ 5, n 4 only k1, k2 ≤ 3; k1 or k2 = 1 is cases 132/142.
- Long n 2 pairs (k1 + k2 ≥ 20) under one error have undecoded underdetermined sets; judged by quadgram score alone (I-029).
- Keys from mixed alphabets (Quagmire-style), other numberings, transpositions outside the bank, dropped/extra letters (I-039).

## Files
[tools/cycle156/](../tools/cycle156/) (`hill2s.c`, `plant.py`, `check.py`, `run_cycle156.sh`, `summarize.py`) ·
[data/cycle156/](../data/cycle156/) · [journal](../journal/2026-11-08-cycle156.md).

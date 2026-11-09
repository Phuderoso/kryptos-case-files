# Cycle 179 pre-registration — one-error audit of case 166: linear-recurrence key mod 26 behind K3's decimation law (IDEAS I-141)

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9179
(`random.Random(9179).shuffle(list(K4))`, I-116): every cell 0 fits; cost M0 L 1–8 ≈ 8 s, M1 L 1–4 ≈ 2 s, M1 L 5 ≈ 63 s per
text on the full set (≈ 8 s on `all_s8.bin`); M0 L 9 on `all_s8.bin` did not finish in 300 s (→ not run, blind spot).
**New this cycle (Voynich C088 slip, our I-119):** the planted-control gate was *rehearsed before this push*: the controls below
were run once (plants carry no K4 information) and the negative rule was set from what the rehearsal taught (see N1).

## Question (audit of case 166's strict `EXACT-EXCL`)
Case 166 excluded K4 = transposition (one of the 165,782 K3-law decimations / routes, `all.bin`, md5 946402ca…) ∘ periodic-tableau
substitution with an affine linear-recurrence key over Z₂₆ (k[i] = c₁k[i−1] + … + c_Lk[i−L] + d), arbitrary c, d, seed, L ≤ 9 on the
plaintext index and L ≤ 5 on the carved index, **with no carving or crib error**. Does that exclusion survive **one wrong letter**
among the 24 crib positions (a mis-carved ciphertext letter at that slot's carved position, or a wrong crib letter)?
Off-crib carving errors do not matter for this test (the fit uses only the 24 crib slots).

## Models (exact, `lr179.c`)
Slot t's key value is a free unknown. Z₂₆ ≅ Z₂ × Z₁₃, so with slot t free a mod-26 fit exists iff some v₂ makes the GF(2)
system pass and some v₁₃ makes the GF(13) system pass, **with the same t**.
- **M0, ix 0 (key on the plaintext index), L 1–8, full set:** for every t and v₂ ∈ {0,1}, lr178's algebra (block equations +
  propagation across the gap + all BERLINCLOCK values); for the slots passing mod 2, every v₁₃ ∈ 0…12. Chance rate per
  (perm, alphabet, form) ≈ 24·26^(2L−22): L 7 ≈ 1e-10, **L 8 ≈ 8e-8 → ≈ 0.05 chance fits per text** (power still full).
- **M1, ix 1 (key on the carved index, seed at carved 0…L−1), L 1–4 full set, L 5 on `all_s8.bin` for all 20 texts and on the
  full set for K4:** mod 2, every stream with ≤ 1 crib-bit mismatch gives the allowed slot set; for every c mod 13 the 24 GF(13)
  rows are eliminated (all rows; if inconsistent, leave out each allowed slot). Chance rate ≤ 24·26^(2L+1−23), negligible.
- A strict fit counts as a fit (every slot); H lines report strict and one-error-only counts separately.
- **Not tested (declared now):** M0 L 9 (cost; the analytic chance rate is ≈ 35 fits per full set there, i.e. `LOW-POWER` by
  construction); M1 L ≥ 6; two or more wrong letters; insertions / deletions (a dropped or doubled carved letter shifts the
  transposition, a different model); vocabulary-seeded W models of case 166 (their 24-letter join would need a 23-of-24 index).

## Texts
K4 (`data/k4.txt`, md5 dc4df49d…). 19 nulls = `random.Random(s).shuffle(list(K4))`, s = **17911…17929** (`nulls179.txt`).

## Labels (per cell)
K4 0 fits → `EXACT-EXCL` (one-error scope); K4 > 0 inside the null range → `LOW-POWER`, every fit decoded; above every null →
flagged and decoded, never a signal without a readable decode. Solution criterion: a full coherent English decryption of the 97
letters with both cribs (one letter allowed to differ from the carving, and that letter named), reproducible.

## Decodes
Every K4 fit and every fit of the first 5 nulls replayed at string level (`decode179.py`, independent of the C code; M1 re-enumerates
every mod-2 stream). Score = mean log10 quadgram (support/quadgrams.json, floor) over off-crib windows.

## Grid (I-120 rule)
Scored cells: R1 M0 L 1–8 fits; R2 M1 L 1–4 fits; R3 M1 L 5 fits (1/8). Diagnostics: D1 M0 mod-2 pass count L 6–8; D2 M1 mod-2
pass count L 1–4 + L 5 (1/8). Leave-one-out exact Poisson tails per cell, all-zero cells reported and not scored; G± = min over
scored cells; grid p = fraction of the 20 texts with G ≤ G(K4); both tails.

## Controls (`plant179.py`, seed 17900, independent string-level encryptor; each plant behind a perm q of all.bin, run on q ± 1,500
with lr179 M0 L 1–8 or M1 L 1–5; `run_controls179.sh`, `checkctl179.py`)
Positives (found at q, planted slot among the fitting slots or every slot for a strict plant, replayed decode = planted plaintext
except the mis-carved letter): P1 M0 L3 A–Z Vig error at PT 25 (cycle 178's N1 situation, must now be found); P2 M0 L6 KA Beau
error 21 (first seed slot); P3 M0 L8 A–Z Beau error 70; P4 M0 L5 KA Vig error 33; P5 M0 L7 A–Z Vig no error; P6 M0 Fibonacci
(1,1) seed KR KA Beau error 63; P7 M1 L2 A–Z Beau error 64; P8 M1 L4 KA Vig error 22; P9 M1 L3 KA Beau no error; P10 M1 L5 A–Z Vig
error 29; P11 M1 L1 A–Z Vig error 73.
Negatives (must be missed at q): N1 M0 L3 key with **two** wrong letters (PT 25 and 66): **missed at L 1–7**; L 8 is exempt and
reported: the rehearsal showed a fit at L 8 by construction (at L 8 the first block-1 equation is i = 29, so slot 25 enters only
through lag 4, whose weight is 0 for the true order-3 key: the cycle-178 N1 lesson, now with one wildcard on 66). N2 random key,
M1 L 1–5; N3 M1 L4 key with two wrong letters (24, 70), L 1–5; N4 random key, M0 L 1–8.
Rehearsal result (before this push): 11/11 positives, N2–N4 missed, N1 missed at L 1–7 and fitting at L 8 (as explained).
**Independent recount** (`recount179.py`, numpy brute force with explicit seed variants, no algebra, no CRT, no wildcard): slice =
all.bin[::4000] + the planted perms of P6, P7, P11; texts K4, n17911, n17912, P6, P7, P11; M0 L 1–2, M1 L 1 (L 2 for P7 only).
Fit lines and fitting-slot sets compared line by line with lr179 on the same slice.

## Budget
~7 min heavy, one 6-thread job at a time, own process group under `setsid timeout 900`; resumable.

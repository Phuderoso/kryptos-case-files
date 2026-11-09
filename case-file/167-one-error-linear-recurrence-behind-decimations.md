# Case file 167 — One bad rivet: the linear-recurrence exclusion under one wrong letter (cycle 179)

**Status:** negative (audit holds). **Type:** audit / variant (cycle 178 was a new family). IDEAS [I-141](../IDEAS.md) (the cycle-179
pointer I-144). Pre-registered in [`tools/cycle179/PREREG179.md`](../tools/cycle179/PREREG179.md) (commits d9f8aa9, 73c91ec,
2c4054f, ~08:59 PT) with the solver, plant generator, decoder, recount and null list, before any K4 or registered-null run.
Smoke and timing only on the reserved shuffle, seed 9179 ([I-116](../IDEAS.md)). **New this cycle:** the planted-control gate was
*rehearsed before the pre-registration push* (our I-119, after the Voynich desk's C088 slip); the rehearsal caught two decoder
bugs and set the negative rule (§4).

**Result in one line:** [case 166](166-linear-recurrence-behind-decimations.md)'s exclusion **survives one wrong letter**. No affine
linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), arbitrary weights and seed, A–Z or KRYPTOS tableau,
Vigenère / Beaufort / variant, fits K4 behind any of the 165,782 K3-law decimations / routes **with any one of the 24 crib
letters (or the carved letter at its position) allowed to be wrong**: **0 fits at L 1–8 on the plaintext index** and **0 fits at
L 1–5 on the carved index** → **`EXACT-EXCL`** (one-error scope). The 19 shuffles give 0 everywhere except two chance fits at
L 8 (expected ≈ 1.0), both gibberish. **No solution.**

## 1. Why this
Case 166's strict test needed all 24 crib key values to be exact. Sanborn's sculpture has known carving quirks (K1's
IQLUSION, K2's missing S / UNDERGRUUND, K3's DESPARATLY), so a "strict zero" is only as strong as the carving. Case 166's own N1
control showed the subtler point: at high order a true low-order key leaves early crib slots out of every equation, so part of the
strict exclusion already tolerates an error by accident. I-141 asked for the clean version: every slot allowed to be wrong, every L.

## 2. Method (exact; `lr179.c`)
Cribs EASTNORTHEAST 21–33, BERLINCLOCK 63–73 (0-indexed); plaintext position i carved at S[i]; key value = index difference in the
tableau alphabet (Vig k = c − p, Beau k = c + p; variant = −Vig, covered).
- **The wildcard is exact by CRT.** If slot t is wrong, its key value is a free unknown v. Because Z₂₆ ≅ Z₂ × Z₁₃ and case 166 solves
  each modulus separately, a mod-26 fit with slot t free exists iff some v₂ ∈ Z₂ makes the GF(2) system pass **and** some
  v₁₃ ∈ Z₁₃ makes the GF(13) system pass, for the **same t** (k[t] = CRT(v₂, v₁₃)). So 26 values cost 2 + 13 solves, and the
  mod-13 solves run only on slots that pass mod 2.
- **M0, ix 0 (key on the plaintext index), L 1–8, full set.** Case 166's algebra (in-block equations, propagation across the gap,
  all BERLINCLOCK values) for every t and v. Chance rate per (perm, alphabet, form) ≈ 24·26^(2L−22): L 7 ≈ 10⁻¹⁰, **L 8 ≈ 8·10⁻⁸,
  i.e. ≈ 0.05 chance fits per text**: the cell still has full power, and the nulls show the rate (below).
- **M1, ix 1 (key on the carved index, seed at carved 0…L−1, so any start offset), L 1–4 full set; L 5 full set for K4 and on
  every 8th perm (`all_s8.bin`) for all 20 texts.** Mod 2: every stream with at most one crib-bit mismatch gives the allowed slots;
  then, for each weight vector mod 13, the 24 GF(13) rows are eliminated (all rows; if inconsistent, leaving out each allowed slot).
- A strict fit counts as a fit for every slot; strict and one-error-only fits are counted separately (H lines).
- What "one error" covers: one mis-carved ciphertext letter at a crib position, or one wrong crib letter. Errors **off** the crib
  positions do not enter this test at all, so it already tolerated them; insertions / deletions do (they shift the transposition)
  and are a different model.

## 3. Results — K4 and 19 nulls ([`summary179.txt`](../data/cycle179/summary179.txt))
| model | cell | K4 fits (strict / one-error) | 19 nulls | mod-2 pass count K4 / null mean (diagnostic) | verdict |
|---|---|---|---|---|---|
| M0 ix 0 | L 1–4 | **0 / 0** | 0 | 472 / 436 (sum) | `EXACT-EXCL` |
| M0 ix 0 | L 5–7 | **0 / 0** | 0 | 1,322 / 1,306 · 5,180 / 5,124 · 20,092 / 20,153 | `EXACT-EXCL` |
| M0 ix 0 | L 8 | **0 / 0** | 0 in 17, **1 in n17919 and n17925** | 75,484 / 76,197 | `EXACT-EXCL` (chance rate ≈ 0.05 per text; 2 null fits vs ≈ 1.0 expected) |
| M1 ix 1 | L 1–4 | **0 / 0** | 0 | 288 / 313 (sum) | `EXACT-EXCL` |
| M1 ix 1 | L 5 | **0 (full set)** / 0 (1/8) | 0 (1/8) | 992 (full) · 116 (1/8) | `EXACT-EXCL` (nulls on 1/8; analytic rate ≈ 10⁻¹⁰ per text) |

No overflow in any text. All K4 lines: [`k4_runs179.txt`](../data/cycle179/k4_runs179.txt); null lines:
[`nulls_counts179.txt`](../data/cycle179/nulls_counts179.txt).

**The two null fits** ([`nullfit_decodes179.txt`](../data/cycle179/nullfit_decodes179.txt)): n17919 (KA Beau, perm 53,918, wrong slot
27) and n17925 (KA Vig, perm 131,341, wrong slot 69). Their decodes score −8.33 and −7.78 (plants −3.95 to −4.09), e.g.
`…EASTNORTHEASTVQBAIKBAZKNRQSBAUNEDHESVKTDOVBERLINZLOCKHDISSBX…`. They are what an L 8 chance fit looks like, and they confirm
the analytic rate: the test can produce false fits at L 8 and did, at the predicted rate, on shuffles, not on K4.

**Grid (I-120 rule, pre-registered).** R1 (M0 fits) scored: K4 0 vs nulls 0–1 (p⁺ 1.00, p⁻ 0.90); R2, R3 all-zero, not scored.
Diagnostics: D1 (M0 mod-2 pass count, L 6–8) K4 100,756 vs nulls 100,456–102,552 (p⁻ 0.012 as a single Poisson tail, but the
null spread is far wider than Poisson: four of the 19 shuffles sit below K4, which ranks 5th lowest of 20); D2 (M1 mod-2 pass count) K4 404 vs 318–488.
**Grid p⁺ 1.00 / p⁻ 0.40**: nothing unusual. The D1 low side is a mod-2 count diagnostic, not an exclusion statistic, and it does
not survive the rank-over-texts step.

**Decodes.** No K4 fit to decode.

## 4. Controls ([`controls_check179.txt`](../data/cycle179/controls_check179.txt), [`controls_planted179.txt`](../data/cycle179/controls_planted179.txt))
Independent string-level encryptor ([`plant179.py`](../tools/cycle179/plant179.py), seed 17900); each plant sits behind a perm q of
all.bin, and its carved letter at one crib slot's carved position is changed by a random non-zero shift; searched on q ± 1,500.
- **11/11 positives PASS**, each found at its planted q **with the planted wrong slot as the only fitting slot** (strict plants:
  every slot), and the replayed decode equal to the planted plaintext except at the mis-carved letter: P1 M0 L3 error at PT 25
  (**cycle 178's N1 situation, now found at L 3**); P2 M0 L6 error at 21 (first seed slot); P3 M0 L8 error at 70; P4 M0 L5 error
  at 33 (start of the gap propagation); P5 M0 L7 strict; P6 Fibonacci (1,1) seed KR error at 63; P7 M1 L2 error at 64; P8 M1 L4
  error at 22; P9 M1 L3 strict; P10 M1 L5 error at 29; P11 M1 L1 error at 73.
- **Negatives 4/4 PASS under the registered rule:** N2 (random key, M1 L 1–5), N3 (M1 L4 key with two wrong letters), N4 (random
  key, M0 L 1–8) missed everywhere; N1 (M0 L3 key with two wrong letters, PT 25 and 66) missed at L 1–7 and fitting at L 8 at
  its planted perm — **pre-registered as exempt after the rehearsal**: at L 8 the first block-1 equation is i = 29, so slot 25
  enters only through lag 4, whose weight is 0 for the true order-3 key; with the wildcard on 66, the second error is invisible.
  Same mechanism as case 166's N1; the harness reports 14/15 literally and the registered tally separately.
- **Rehearsal before the push (I-119 in practice).** The first rehearsal failed P7 and P9 — in the decoder, not the solver: when
  c ≡ 0 (mod 2) the mod-2 stream is constant after the seed, so the seed bits at carved 0…L−1 (off the crib positions) are not
  identified, and the one printed example stream decoded two letters wrong. `decode179.py` now re-enumerates every mod-2 stream
  matching the crib bits. The rehearsal also showed the quadgram-file format slip (all scores −9). Both fixed before the push.
- **Independent recount** ([`recount179.py`](../tools/cycle179/recount179.py), numpy brute force: no algebra, no CRT, no wildcard;
  M0 by explicit seed variants and a mismatch count ≤ 1, M1 by every stream; slice all.bin[::4000] + the planted perms of P6, P7,
  P11; K4, n17911, n17912 and those three plants; M0 L 1–2, M1 L 1, M1 L 2 for P7): **3/3 fit lines identical, with the same
  fitting-slot sets** (P6 slot 63, P7 slot 64, P11 slot 73), and 0 fits for K4 and both nulls in both tools
  ([`recount179.txt`](../data/cycle179/recount179.txt)). It is a thin check: it confirms the wildcard logic and the slot attribution
  at low order, not the high-L cells (brute force is out of reach there; those rest on the plants P3, P4, P5, P10).

## 5. Scope, blind spots, lessons
- **Excluded (one-error scope):** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (A–Z or KRYPTOS tableau, Vig / Beau /
  variant) with an affine mod-26 linear-recurrence key, arbitrary weights and seed, order ≤ 8 on the plaintext index or ≤ 5 on
  the carved index, **with at most one wrong letter among the 24 crib positions** (any carving error off the crib positions is
  irrelevant to the test). Both layer orders. Includes Fibonacci / tetranacci / progressive keys and every periodic key ≤ L.
- **Not covered:** plaintext-index L 9 one-error (cost: the 13⁴ solution space × 13 wildcards did not finish 1/8 of the set in
  300 s on the smoke text; the analytic chance rate there is ≈ 35 fits per text, so it would be `LOW-POWER` anyway); carved-index
  L ≥ 6; two or more errors; insertions / deletions; the vocabulary-seeded W models of case 166 under one error (→ I-149);
  keyed alphabets (I-142); non-linear generators.
- **Lesson (method):** the CRT split makes a one-letter wildcard nearly free for any affine family mod 26 (2 + 13 solves instead of
  26, and the 13 only where mod 2 passes). This is the I-143 prefilter idea applied to error tolerance.
- **Lesson (process):** rehearsing the gate before the pre-registration push is cheap (39 s) and changed two things that would
  otherwise have been post-hoc: a decoder bug and the negative rule.
- **Budget:** main run 10.0 min (6 threads), over the ~8 min target because the single-thread numpy recount ran at the same time;
  controls 39 s; smoke ~6.5 min (5 of them the abandoned L 9 timing on the reserved shuffle). The numpy recount took ~11 min on six
  single-thread processes (a first one-process attempt timed out at 25 min with no output; outside the 6-thread budget).

## Reproduce
`tools/cycle179/run_cycle179.sh` (W = scratch with run/{lr179,k4.txt,nulls179.txt}, support/{all.bin,all_s8.bin}),
`summarize179.py out nulls179.txt`; controls `run_controls179.sh`; recount `recount179.py slice179.bin rc_texts.txt P7` (slice =
all.bin[::4000] + planted perms of P6, P7, P11). Inputs and md5s: [`inputs179.txt`](../data/cycle179/inputs179.txt).

# Case file 166 — The ledger that adds itself: linear-recurrence keys mod 26 behind K3's decimation law (cycle 178)

**Status:** negative. **Type:** new family behind the decimations (cycle 177 was an audit). IDEAS [I-137](../IDEAS.md) (the
cycle-178 pointer I-138), with the add-on [I-133](../IDEAS.md) (replication of case 165's C2 flag). Pre-registered in
[`tools/cycle178/PREREG178.md`](../tools/cycle178/PREREG178.md) (commits 202c378 + dd29766, ~07:59 PT) together with the solver, the
plant generator, the seed list and the null lists, before any K4 or registered-null run. Smoke and timing runs used only the
reserved shuffle, seed 9178 ([I-116](../IDEAS.md)).

**Result in one line:** no affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), **arbitrary weights, any
seed**, under an A–Z or KRYPTOS tableau (Vigenère / Beaufort / variant), fits K4 behind any of the 165,782 K3-law decimations /
routes: **0 fits at L 1–9 with the key on the plaintext index** (substitute, then transpose) and **0 fits at L 1–5 with the key on
the carved index** (transpose, then substitute), plus 0 fits for the small-weight (c ∈ {0,1}) LFSR / lagged-Fibonacci keys of
order 6–10 seeded from 74 Kryptos vocabulary words, both orders → **`EXACT-EXCL`**. All 19 shuffles also give 0 in every cell;
every planted recurrence is recovered with its plaintext. **I-133: the C2 flag of case 165 does not replicate** (K4 230 against 40
fresh shuffles 152–252 and 20 crib-repeat-matched shuffles 154–256; p_F 0.073, p_M 0.143, pooled 0.082 → pre-registered
"not replicated"). **No solution.**

## 1. Why this, and what is new
- Cycles 80–81 ([case 78](78-linear-recurrence-key.md), [case 79](79-linear-recurrence-order4.md)) ran this family direct and behind
  the 165,065 columnar/route bank only (L ≤ 4 there, key on the plaintext index only). The coverage table listed it as open behind
  the K3-law decimations, and it is the base-26 generalisation of the Gromark chain that cycles 176–177 just closed there.
- New method: **exploit the cribs algebraically instead of enumerating weights.** With the key on the plaintext index, the 24 crib
  key values are known for each perm, and the recurrence equations inside each crib block are *linear* in (c, d). Z₂₆ is not a
  field, so the system is split by the Chinese remainder theorem into GF(2) and GF(13), each solved by Gaussian elimination, and
  only the (small) solution spaces are enumerated and propagated across the 29-letter gap. That turns cycle 80's 26^L weight loop
  into a per-perm linear solve and reaches L 9 behind all 165,782 perms in seconds.
- With the key on the carved index, the 24 known values sit at scattered positions, so there is no local equation. Here the
  CRT split is used as a filter: mod 2 there are only 2^(2L+1) streams (≤ 2,048 at L 5), checked against the 24 key bits as one
  97-bit mask; the few perms that survive go to GF(13), where for each weight vector the stream is linear in (seed, d).

## 2. Models (exact; repo conventions)
Cribs EASTNORTHEAST at plaintext 21–33 and BERLINCLOCK at 63–73 (0-indexed). Plaintext position i is carved at S[i].
Key value = index difference in the tableau alphabet (A–Z or KRYPTOS): Vigenère k = c − p, Beaufort k = c + p; variant = −Vigenère,
which maps the family onto itself (d → −d), so it is covered. ([`lr178.c`](../tools/cycle178/lr178.c))
- **M0, ix 0 (key on the plaintext index, then transpose), L 1–9.** Equations i = 21+L…33 and 63+L…73, unknowns (c₁…c_L, d), solved
  mod 2 and mod 13; every solution is propagated from the 13 block-1 values through 34–73 and must reproduce all 11 BERLINCLOCK key
  values mod p. Fit ⇔ a mod-2 and a mod-13 solution survive (#solutions mod 26 = n₂·n₁₃). The seed upstream of position 21 is not
  required to exist, so this is a superset of every seed, including every vocabulary seed and every start offset. L 1–8 on the full
  perm set for every text; L 9 for K4 on the full set and on every 8th perm, nulls on every 8th perm (cost: 39 s per full pass).
- **M1, ix 1 (transpose first, key on the carved index), L 1–5,** arbitrary seed at carved 0…L−1 (this covers any start offset,
  because any later-starting recurrence restricted to positions ≥ 0 is a recurrence with some seed). Mod-2 stream filter, then
  GF(13) incremental elimination for each of the 13^L weight vectors (precomputed basis table). Full perm set for every text.
- **W0 / W1, small weights, vocabulary seeds, L 6–10.** c ∈ {0,1}^L \ {0} (LFSR / lagged-Fibonacci style), d ∈ Z₂₆, seed = the first
  L letters of one of 74 words ([`seeds178.txt`](../tools/cycle178/seeds178.txt): KRYPTOS, PALIMPSEST, ABSCISSA, the cribs, K1–K3
  words, Sanborn/Scheidt/Webster, Egypt/Carter, Weltzeituhr, the two alphabets, …) numbered A–Z or KRYPTOS. W0 seed at plaintext
  0…L−1 (24-letter hash join), W1 seed at carved 0…L−1 (decrypt + triple-position index). 14.1 M streams per text and order, full set.
- **Analytic chance rate** per (perm, alphabet, form): M0 ≈ 26^(2L+1−24) (L 8: 2·10⁻¹⁰, L 9: 8·10⁻⁸, so ≈ 0.05 chance fits
  over the full set at L 9); M1 ≈ 26^(2L+1−24) ≤ 10⁻¹⁸ at L 5; W ≈ 26⁻²⁴ per stream × 1.66·10⁵ perms ≈ 10⁻²⁰. So every cell has
  full power; the nulls confirm it (0 everywhere).

## 3. Results — K4 and 19 nulls ([`summary178.txt`](../data/cycle178/summary178.txt))
| model | cell | K4 fits | 19 nulls | mod-2 survivors K4 / null mean (diagnostic) | verdict |
|---|---|---|---|---|---|
| M0 ix 0 | L 1–6 | **0** | 0 each | 320 / 291 (sum over L) | `EXACT-EXCL` |
| M0 ix 0 | L 7 / L 8 | **0 / 0** | 0 | 866 / 861 · 3,436 / 3,433 | `EXACT-EXCL` |
| M0 ix 0 | L 9 | **0 (full set) / 0 (1/8)** | 0 (1/8) | 1,798 / 1,679 (1/8) | `EXACT-EXCL` (nulls on 1/8; analytic rate 0.05 per full set) |
| M1 ix 1 | L 1–5 | **0** | 0 each | 52 / 53.6 | `EXACT-EXCL` |
| W0 (seed at PT 0) | L 6–10 | **0** | 0 | — | `EXACT-EXCL` (within the 74-word seed list) |
| W1 (seed at carved 0) | L 6–10 | **0** | 0 | — | `EXACT-EXCL` (within the 74-word seed list) |

No overflow / undetermined case in any text. All K4 lines: [`k4_runs178.txt`](../data/cycle178/k4_runs178.txt); null lines:
[`nulls_counts178.txt`](../data/cycle178/nulls_counts178.txt). The mod-2 survivor counts are identical for Vigenère and Beaufort
(they differ by 2p, which is 0 mod 2), and K4's are at the null mean.

**Grid (I-120 rule, pre-registered 7 cells).** R1–R5 (the fit counts) are all-zero for all 20 texts → reported, not scored. The two
diagnostic cells: D1 (M0 mod-2 survivors, L 7–8 full + L 9 on 1/8) K4 6,100 vs nulls 5,696–6,268 (p⁺ 0.051), D2 (M1 mod-2
survivors) K4 52 vs 32–90. **Grid p⁺ 0.35 / p⁻ 0.75** — nothing unusual about K4's mod-2 structure under this family.

**Decodes.** There is no K4 or null fit to decode. Plant decodes below show what a fit looks like (score −3.95 … −4.09 against
≈ −7 for gibberish in cycles 176–177).

## 4. Controls ([`controls_check178.txt`](../data/cycle178/controls_check178.txt), [`controls_planted178.txt`](../data/cycle178/controls_planted178.txt))
Independent string-level encryptor ([`plant178.py`](../tools/cycle178/plant178.py), seed 17800); every plant behind a perm q of
all.bin (so both transposition orders are exercised), searched on all.bin rows q ± 1,500 with its model.
- **12/12 positives PASS**, each found at its planted q, with the planted (c mod 2, c mod 13, d) among the listed solutions (or the
  exact word/weights/d for W) and the string-level replay equal to the planted plaintext: P1 M0 L3 A–Z Vig; P2 M0 L6 KA Beau; P3 M0
  L8 A–Z Beau; P4 M0 L9 KA Vig; P5 Fibonacci (1,1) seed KR KA Vig; P6 M1 L2 A–Z Beau; P7 M1 L4 KA Vig with a non-unit last weight;
  P8 M1 L5 A–Z Vig; P11 M1 L3 KA Beau; P9 W1 L7 PALIMPSEST (KA numbering) KA Beau; P10 W0 L10 BERLINCLOCK (A–Z numbering) A–Z Vig;
  P12 W0 L6 KRYPTOS (KA numbering) A–Z Beau (also found as ABCDEF… in A–Z numbering: the same digits).
- **Negatives 2/3 PASS as pre-registered:** N2 (random key, M1 L 1–5) and N3 (P9's stream shifted by one position) are missed.
  **N1 (P1 with one wrong carved crib letter, PT slot 25) FAILED the pre-registered rule "missed at every L 1–9":** it is missed
  at L 1–7 but fits at L 8 and L 9 at its planted perm. Diagnosis (kept, not hidden): the planted key is order 3; at order L ≥ 8
  the first block-1 equation is i = 29, so slot 25 enters only through lags 4–8, whose weights are 0 in the padded order-3
  solution. The wrong letter is invisible there by construction; the solver is right and the negative was mis-designed.
  A post-hoc negative N1b (wrong letter at slot 30, inside every seed window) is missed at every L 1–9 (labelled post hoc).
  The lesson is recorded in §6.
- **Independent recount** ([`recount178.py`](../tools/cycle178/recount178.py), numpy brute force, no algebra, no CRT; 47-perm slice
  = all.bin[::4000] + the planted perms of P1, P5, P6, P11, P12): M0 L 1–3 over all 26^(L+1) (c, d), M1 L 1–2 over all 26^(2L+1)
  streams, W0/W1 L 6 by direct replay; K4, n17811, n17812 and five plants. **8/8 fit lines identical, solution counts equal**
  (P1 L3 13 = 1 × 13; P5 L2 1, L3 26 = 2 × 13; P6 M1 L2 3 streams; four W0 lines), 0 fits for K4 and the nulls in both tools
  ([`recount178.txt`](../data/cycle178/recount178.txt)).

## 5. Add-on I-133: the C2 flag does not replicate ([`i133_178.txt`](../data/cycle178/i133_178.txt))
Pre-registered single cell, one-sided: one-error ordinary Gromark, plaintext index, L 6 (gm177 unchanged, full all.bin).
K4 rerun: **230** (same as case 165). Fresh F, 40 shuffles (seeds 17841–17880): 152–252, mean 189.8, SD 22.0, **2 ≥ 230**
(f17870 230, f17874 252), z +1.82, p_F 0.073. Matched M, 20 shuffles whose mean crib-slot equal-pair count is within 0.02 of
K4's 9.8983 (accepted 20 of the first 169 candidates from seed 17901, [`matched133.txt`](../data/cycle178/matched133.txt)): 154–256,
mean 200.8, SD 24.1, **2 ≥ 230** (m17934 253, m17984 256), z +1.21, p_M 0.143. Pooled 60: p 0.082.
**Decision (pre-registered): NOT REPLICATED.** Case 165's p⁺ 0.05 was the floor of a 20-text rank. With 60 more texts K4 is a
1.6-SD upper-tail draw, and matching the crib-repeat covariate moves the null mean up by 11 fits, toward K4. The flag is closed as
chance plus covariate. Its 256 decodes were gibberish anyway.

## 6. Scope, blind spots, lessons
- **Excluded:** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (A–Z or KRYPTOS tableau, Vig / Beau / variant) with an
  affine mod-26 linear-recurrence key, arbitrary weights and seed, order ≤ 9 on the plaintext index or ≤ 5 on the carved index;
  and LFSR-style {0,1}-weight keys of order 6–10 seeded at position 0 from the 74 listed words, either index. Both layer orders.
  Strict (no carving or crib error). Includes Fibonacci / tetranacci keys, progressive keys and every periodic key of period ≤ L.
- **Not covered (blind spots):** order ≥ 10 on the plaintext index (the analytic chance rate reaches ~38 fits per full set at
  L 10, so the test loses power there anyway); order 6–9 on the carved index with arbitrary weights (the GF(13) stage needs 13^L
  basis tables; → I-139); vocabulary seeds placed anywhere but position 0, other words; keyed (Quagmire) alphabets, non-linear
  generators, a recurrence over the cipher (autokey-like) rather than the key; **one wrong letter** (→ I-141).
- **Lesson from N1 (method):** in an algebraic recurrence test a wrong crib letter is detected only where it enters an equation
  with a non-zero weight. At high order a true low-order key leaves early crib slots unconstrained, so the strict exclusion at
  high L is partly error-tolerant already, and negatives must sit inside every seed window. One-error audits of linear families
  should report which slots are "load-bearing" per L.
- **Budget:** main run 4.0 min (6 threads), I-133 3.3 min (including the 169-candidate matching), controls 17 s, kit validation
  15 s; the numpy recount took 5.7 min on one core (outside the 6-thread budget). Total heavy ≈ 7.6 min.

## 7. Side task: blind kit for the Voynich desk (I-106)
Their notes (unverified) have asked several times for the blind kit offered in I-106. This cycle publishes one:
[`data/cycle178/blindkit178/`](../data/cycle178/blindkit178/): six ciphertexts, each behind one row of all.bin; some carry a
cycle-178 linear-recurrence key, some are decoys; SHA-256 of "id|answer" per item and a commitment to the private answer file. The
generator and answers stay off the repo until the review is returned. All four positives were recovered by `lr178` at their
planted perm and decoded to the planted plaintext; the decoys gave no fit.

## Reproduce
`tools/cycle178/run_cycle178.sh` (W = scratch with run/{lr178,k4.txt,nulls178.txt,seeds178.txt}, support/{all.bin,all_s8.bin}),
`summarize178.py out nulls178.txt`; controls `run_controls178.sh`; recount `recount178.py slice178.bin rc_texts.txt seeds178.txt
k4,n17811,P6,P11`; I-133 `match133.py`, `run_i133.sh`, `summ133.py`. Inputs and md5s: [`inputs178.txt`](../data/cycle178/inputs178.txt).

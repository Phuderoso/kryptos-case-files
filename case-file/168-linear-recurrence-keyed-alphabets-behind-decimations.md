# Case file 168 — The ledger in a borrowed hand: linear-recurrence keys over keyword-keyed alphabets behind K3's decimation law (cycle 180)

**Status:** negative. **Type:** new family behind the decimations (cycle 179 was an audit). IDEAS [I-142](../IDEAS.md) (the cycle-180
pointer I-150). Pre-registered in [`tools/cycle180/PREREG180.md`](../tools/cycle180/PREREG180.md) (commits f02e667, 1527668, d81f05c,
94115dc, 5dbede1, 10:07–10:08 PDT) with the solver, plants, decoder, recount, summarizer and null seeds, **after** the planted
controls had been rehearsed (I-119) and before any K4 or registered-null run. Smoke and timing used only the reserved shuffle, seed
9180 ([I-116](../IDEAS.md)). Add-on replication of a diagnostic flag pre-registered separately in
[`PREREG180b.md`](../tools/cycle180/PREREG180b.md) (commit e59b0a5, 10:12 PDT), after the main run and before the replication run.

**Result in one line:** no affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26), arbitrary weights and seed,
read through a **keyword-keyed tableau** (18,776 vocabulary alphabets, each as Quagmire I, II or III, Vigenère or Beaufort) fits
K4 behind any of the 165,782 K3-law decimations / routes: **0 fits at L 1–7 with the key on the plaintext index, 0 fits at L 1–3
with the key on the carved index, and 0 at L 4 with 144 themed alphabets → `EXACT-EXCL`**. All 19 shuffles also 0 in every cell;
14/14 controls; the numpy recount agrees line for line. A diagnostic rank flag (mod-2 pass counts, K4 above all 19 nulls) **did not
replicate** on 40 fresh shuffles (p_F 0.12). **No solution.**

## 1. Why this, and what is new
- Cases 166–167 closed this family behind the decimations only for the **A–Z and KRYPTOS** tableaux. K1 and K2 are Quagmire III with
  the KRYPTOS-keyed alphabet; the natural "same machine, another English keyword" layer had not been run with a recurrence key.
  This is the user's layered picture exactly: a meaningful keyword builds the alphabet, a simple rule builds the key, and a K3-style
  transposition moves the letters.
- **New method: one bit decides most of the work.** Over Z₂₆ = Z₂ × Z₁₃ the mod-2 half of the test depends only on the 24 crib key
  bits. For the key on the plaintext index the whole mod-2 test (in-block equations + propagation across the 29-letter gap) is
  precomputed once as a 2²⁴-entry table. The key bit at a crib slot is parity(B(c)) ⊕ parity(A(p)), so per perm the 24 bits for any
  alphabet come from a handful of 24-bit letter masks and the alphabet's 26-bit parity mask. That is one table lookup per
  (perm, alphabet, type), 9.3 × 10⁹ lookups per text. Only the ≈ 0.3 % that pass mod 2 go to case 166's GF(13) solve.
  For the key on the carved index the 2^(2L+1) mod-2 streams are projected onto the 24 crib positions with `pext` and stored in a
  2²⁴ bitset per perm (one lookup per alphabet); survivors go to case 166's GF(13) loop. Behind all 165,782 perms × 56,326
  (alphabet, type) pairs this ran in about 9 s (plaintext index) and 20 s (carved index) per text on 6 threads.

## 2. Models (exact; repo conventions; [`lrk180.c`](../tools/cycle180/lrk180.c))
Cribs EASTNORTHEAST at plaintext 21–33 and BERLINCLOCK at 63–73 (0-indexed). Plaintext position i is carved at S[i].
A = plaintext-side alphabet, B = ciphertext-side alphabet. Vigenère c = B[(A(p) + k) mod 26] (k = B(c) − A(p)); Beaufort
c = B[(k − A(p)) mod 26] (k = B(c) + A(p)). Types: **q1** A keyed / B = A–Z, **q2** A = A–Z / B keyed, **q3** A = B keyed (K1/K2).
Variant (= −Vigenère) and any rotation of either alphabet (k → k + e, absorbed by d) map the affine family onto itself.
- **Alphabets.** `alpha172.txt`: the 10,056 vocabulary words of case 146/158 keyed on A–Z (`/Z`) and on the KRYPTOS order (`/K`), plus
  A–Z and KA; 18,776 distinct (A–Z counted once) → **56,326 (alphabet, type) pairs**. Themed: the same construction on cycle 178's
  74 seed words (144 alphabets).
- **M0, key on the plaintext index (substitute, then transpose), L 1–7**, seed upstream of 21 free (superset of every seed and offset).
- **M1, key on the carved index (transpose, then substitute), seed at carved 0…L−1, L 1–3 (vocabulary), L 4 (themed).**
- **Chance rate** per (perm, pair, form) ≈ 26^(2L+1−24); 1.87 × 10¹⁰ configurations per full pass: M0 L 7 ≈ 0.003 fits per text,
  L 6 ≈ 5 × 10⁻⁶; M1 L ≤ 4 < 10⁻⁷. Every registered cell has full power.

## 3. Results — K4 and 19 nulls ([`summary180.txt`](../data/cycle180/summary180.txt))
| model | cell | K4 (full set) | K4 (1/8) | 19 nulls (1/8; L 4 themed full) | mod-2 passes K4 / null mean (1/8, diagnostic) | verdict |
|---|---|---|---|---|---|---|
| M0 plaintext index | L 1–5 | **0** | 0 | 0 each | 125,378 / 127,153 | `EXACT-EXCL` |
| M0 plaintext index | L 6 / L 7 | **0 / 0** | 0 / 0 | 0 | 377,982 / 380,275 · 1,508,101 / 1,515,034 | `EXACT-EXCL` |
| M1 carved index | L 1–3 | **0** | 0 | 0 each | 6,273 / 5,594 | `EXACT-EXCL` |
| M1 carved index, themed (144) | L 4 | **0** | — | 0 each (full) | 1,036 / 1,018 (full) | `EXACT-EXCL` |

No overflow, no table/solve disagreement in any text. K4 lines: [`k4_runs180.txt`](../data/cycle180/k4_runs180.txt); null lines:
[`nulls_counts180.txt`](../data/cycle180/nulls_counts180.txt). There is no K4 or null fit to decode.

**Grid (I-120 rule, pre-registered).** R1–R3 (fit cells) all-zero for all 20 texts → reported, not scored. Diagnostics: D1 (M0 mod-2
passes L 6–7) K4 1,886,083 vs 1,885,114–1,901,768 (low side); D2 (M1 mod-2 passes L 1–3 + L 4 themed) **K4 7,309 vs 6,199–7,117,
above all 19**. Grid **p⁺ 0.05 (the floor) / p⁻ 0.10**. The Poisson tails of the I-120 rule are meaningless at these counts (they are
overdispersed: the null SD is ≈ 450, not √5,600 ≈ 75), so the rank is what carries the flag, and a floor rank among 19 shuffles is
what case 165's C2 flag also looked like.

## 4. Add-on: the D2 flag does not replicate ([`d2rep180.txt`](../data/cycle180/d2rep180.txt))
Pre-registered (PREREG180b, before the run): one cell, one-sided, D2′ = M1 mod-2 passes L 1–3 on all_s8 (K4 6,273), 40 fresh
shuffles (seeds 18041–18080). Result: fresh 4,722–6,629, mean 5,621.6, SD 450.9; **4 of 40 ≥ K4**, p_F = 5/41 = **0.122**, z +1.44
→ **NOT REPLICATED** (rule: p_F ≤ 0.05). Split by type (description only): q1 K4 2,366 vs mean 1,895 (3/40 ≥), q2 2,030 vs 1,864
(8/40), q3 1,877 vs 1,863 (18/40). The excess sits in q1, where B = A–Z, so the alphabet only changes the plaintext-side bits and
the text enters only through the A–Z parity of K4's letters at the crib slots' carved positions. That is a property of K4's letter
arrangement (an upper-tail draw here), not of any keyed alphabet, and there is no fit behind it. Flag closed.

## 5. Controls ([`controls_check180.txt`](../data/cycle180/controls_check180.txt), [`controls_planted180.txt`](../data/cycle180/controls_planted180.txt))
Independent string-level encryptor ([`plant180.py`](../tools/cycle180/plant180.py), seed 18000; plaintext
THEIRONDOORFACEDDUEXX·EASTNORTHEAST·OFTHEFOUNTAINWHERETHEOLDWORLD·BERLINCLOCK·STRUCKTHEHOURATMIDNIGHT); every plant behind a perm q
of all.bin, searched on rows q ± 1,500 with the registered alphabets.
- **10/10 positives PASS**, each found at its q with the planted alphabet, type, form and L, the planted (c, d) among the listed
  mod-2 / mod-13 solutions, and the string-level replay equal to the planted plaintext (whole text when c_L is invertible mod 26,
  otherwise from position 21 on): P1 M0 L3 q3 Vig SHADOW/Z; P2 M0 L5 q1 Beau BERLIN/K; P3 M0 L7 q2 Vig ABSCISSA/Z; P4 M0 L2 q3 Beau
  SHADOW/K; P5 M0 L6 q3 Vig PALIMPSEST/K with an even last weight; P6 M1 L1 q3 Vig COMPASS/Z; P7 M1 L2 q1 Beau LODESTONE/K; P8 M1 L3
  q2 Vig MAGNETIC/Z; P9 M1 L4 q3 Beau ABSCISSA/K (themed); P10 progressive key q3 Vig KA. The extra fits at each q are the same key
  read at higher L (zero-padded weights; n₂·n₁₃ grows as 2·13 per order); **no other alphabet fits any plant**.
- **4/4 negatives PASS:** N1 (P1 with one wrong carved letter at slot 30, inside every block-1 window) missed at L 1–7; N2/N3 random
  keys missed; N4 (a plant made with a random alphabet not in the list) missed. The test is alphabet-specific: a keyed alphabet
  outside the list is not covered.
- The controls were rehearsed before the pre-registration push (14/14 on the first rehearsal, no rule changed); the registered run
  gave the same 14/14.
- **Independent recount** ([`recount180.py`](../tools/cycle180/recount180.py), numpy brute force with no CRT, no parity table, no `pext`
  and no elimination): slice = all.bin[::4000] + the planted perms of P1, P4, P6, P7 (46 rows), 33 alphabets (first 30 of the list
  + SHADOW/K, COMPASS/Z, LODESTONE/K), texts K4, n18011, n18012, P1, P4, P6, P7; M0 L 1–2 (L 3 for P1) over all (c, d) mod 26, M1 L 1
  over all 26³ streams (L 2 for P7 at its row over all 26⁵); ≈ 9,000 (perm, alphabet, type, form) configurations per text.
  **4/4 fit lines identical, mod-26 solution counts equal** (P1 L3 1; P4 L2 4 = 4 × 1; P6 M1 L1 3 streams; P7 M1 L2 1), and **0 fits
  for K4, n18011 and n18012 in both tools** ([`recount180.txt`](../data/cycle180/recount180.txt)). Thin (few fit lines), but it
  checks the parity table, the `pext` projection and the CRT bookkeeping against arithmetic that uses none of them.

## 6. Scope, blind spots, lessons
- **Excluded (strict):** K4 = (one of the 165,782 K3-law decimations / routes) ∘ (Quagmire I, II or III tableau built from any of the
  18,776 vocabulary-keyed alphabets, Vigenère / Beaufort / variant, any rotation) with an affine mod-26 linear-recurrence key of order
  ≤ 7 on the plaintext index or ≤ 3 on the carved index (≤ 4 for the 144 themed alphabets), arbitrary weights and seed. Includes
  progressive keys, Fibonacci-type keys and every periodic key of period ≤ L through those tableaux.
- **Not covered (declared before the run):** M0 L 8 (≈ 2.3 chance fits per full pass, `LOW-POWER` by construction); M1 L 4 with all
  18,776 alphabets (≈ 400 s per text with the current GF(13) loop) and M1 L ≥ 5; Quagmire IV (two different keyed alphabets); one wrong
  letter; alphabets outside the list (N4); non-linear generators.
- **Lesson (method):** for affine families over keyed alphabets, the parity of a letter's index is all the mod-2 stage needs, so the
  alphabet loop costs one table lookup. The same trick should carry I-143 (CRT prefilter) to Quagmire IV and to Hill-with-key.
- **Lesson (statistics):** the I-120 Poisson tails are not usable on large overdispersed diagnostic counts; the grid should use the
  rank or an empirical SD for such cells (→ I-152).
- **Budget:** heavy ≈ 4.4 min (main run 159 s, replication 65 s, controls + smoke ≈ 40 s), 6 threads; recount single core per text,
  niced, outside the budget.

# Case file 164 — Gromark behind K3's decimation law (cycle 176)

**Status:** negative. **Type:** new family (cycle 175 was an audit). IDEAS [I-125](../IDEAS.md) (the pointer), i.e. the
decimation/route part of the Gromark gap in the coverage table ("behind transpositions"). Pre-registered in
[`tools/cycle176/PREREG176.md`](../tools/cycle176/PREREG176.md) (commit 5794cbd, 13:54:36 UTC = 06:54 PT), pushed before any K4 or
registered-null run. The main run started 7 s later. Smoke runs used only the reserved shuffle, seed 9176 ([I-116](../IDEAS.md)).

**Result in one line:** behind the 165,782 K3-law decimations and spiral/diagonal routes, in both layer orders, **no ordinary
Gromark with any cipher alphabet fits the 24 crib letters at primer length L 2–5**, and none with any of 22,121 named primers
(vocabulary numerical keys L 3–16, dates, coordinates). **No ACA Periodic Gromark built from 17,164 vocabulary keywords fits
either** (4 alphabet variants, including the new keyword+KRYPTOS one). All of these are `EXACT-EXCL`. With the key on the plaintext
index, L 6–8 gives fits at the shuffled-null rate (1 / 12 / 103 against null means 0.84 / 10.7 / 97). All 116 decode to
gibberish (best −7.10 against nulls −6.80 … −7.45 and plants −4.04 … −4.08), so those rows are `LOW-POWER` / `NO-SIGNAL`. Grid p⁺ 0.75,
p⁻ 0.80. **No solution.**

## 1. Why this, and what is new
- Queue: cycle 175's pointer (I-125) named Gromark behind the decimations, or keyword-built Hill (I-124). Gromark won. Bean (2021)
  put it forward on statistical grounds. The coverage table had it open "behind transpositions". Kryptosbot's public record
  (Sept 2026) still lists keyed-alphabet Gromark as only partly tested.
- Overlap: cycles 128–130 ran the ACA Periodic Gromark, and a chain-addition primer driving a Sequence Transposition, behind the
  **165,065 columnar bank**. Cycle 155 ran ordinary and periodic Gromark **direct**, under one error. Cycle 65 ran the
  double-mixed form direct. None of them used the **165,782 K3-law decimations/routes** (case 156 §2), and none tested ordinary
  Gromark with an arbitrary cipher alphabet behind any transposition.

## 2. Models (exact, strict; repo conventions)
Cribs at plaintext index 21–33 and 63–73 (0-indexed). Plaintext position i is carved at S[i].
- **G, ordinary Gromark** ([`gm176.c`](../tools/cycle176/gm176.c)): d[i] = d[i−L] + d[i−L+1] mod 10 from a primer of length L.
  The plaintext alphabet is A–Z or KRYPTOS. The **cipher alphabet is arbitrary**, so every keyword-mixed, KRYPTOS-keyed or
  ACA-columnar alphabet is covered at once. Vigenère: w = PA(p) + d. Beaufort: w = d − PA(p). The variant form is Beaufort
  with the arbitrary alphabet reflected, and plant ctl5 confirms this. A config fits iff equal carved letters ⇔ equal w over
  the 24 crib slots.
  - **ix 0** (Gromark on the plaintext index, then transpose): every primer, **L 2–8**. This is a hash join of crib-slot
    partitions: 1.1 × 10⁸ primers × 4 forms against 165,782 perms, about 12 s.
  - **ix 1** (transpose, then Gromark on the carved index): every primer, **L 2–5**. Brute force, with the equal-letter pairs
    checked first: 7.4 × 10¹⁰ configs, about 45 s.
  - **Named primers**, both ix: 22,121 of them ([`mkcfg176.py`](../tools/cycle176/mkcfg176.py)). These are the ACA numerical keys
    (ranks, 10 → 0) of the cycle-129 vocabulary (themed list, 10,056 words, themed pairs), raw and deduplicated, L 3–16. Also
    included are the K2 coordinates, 1990, 11/3/1990, 11/9/1989 and 26/11/1922 in several digit orders.
- **PG, ACA Periodic Gromark** ([`pg176.c`](../tools/cycle176/pg176.c)): cycle 129's construction (it reproduces the ACA ENIGMA
  example) for 17,164 keywords (deduplicated length 3–12). Cipher alphabets: aca, mix, ka and **kmix** (keyword + KRYPTOS order,
  new). Plaintext alphabet A–Z or KRYPTOS. Vigenère (ACA) and Beaufort, both ix. 137,312 configs × 2 forms × 165,782 perms × 2 ix
  = 9.1 × 10¹⁰ exact 24-letter checks.

## 3. Results — K4 (full perm set)

| model | cell | K4 fits | 19 nulls min/med/max (mean) | verdict |
|---|---|---|---|---|
| G ix 0 | L 2–4 | **0** | 0/0/0 | `EXACT-EXCL` |
| G ix 0 | L 5 | **0** | 0/0/1 (0.11) | `EXACT-EXCL` |
| G ix 0 | L 6 | 1 (A–Z Beaufort, perm 109928, primer 657783) | 0/1/4 (0.84) | `LOW-POWER`; the one fit decodes −7.85 → `NO-SIGNAL` |
| G ix 0 | L 7 | 12 | 5/10/17 (10.7) | `LOW-POWER`, decodes ≤ −7.46 → `NO-SIGNAL` |
| G ix 0 | L 8 | 103 | 77/98/126 (97.2; 9 nulls) | `LOW-POWER`, decodes ≤ −7.10 → `NO-SIGNAL` |
| G ix 1 | L 2–5 | **0** (full; also 0 on 1/8) | 1/8: 0/0/1 at L 5 | `EXACT-EXCL` |
| G, named primers | ix 0 full, ix 1 full | **0 / 0** | 0 (ix 0 full, ix 1 on 1/8) | `EXACT-EXCL` |
| PG (17,164 keywords × 4 CA × 2 PA × Vig/Beau) | ix 0 / ix 1 | **0 / 0** | 0 | `EXACT-EXCL` |

Per-L table: [`summary176.txt`](../data/cycle176/summary176.txt). All K4 lines: [`k4_runs176.txt`](../data/cycle176/k4_runs176.txt).
- **Power.** Chance fits first appear at L 5 (ix 0, null mean 0.11) and L 5 (ix 1, 1 fit in 19 nulls on 1/8, so ≈ 0.4 per
  full set). The exact rows therefore exclude with real power, not because the test is too weak to fail. From L 6 on, the
  plaintext-index model fits random text about once per null, and from L 7 on, ten or more times. A count of zero would no longer
  carry information there, so those rows are decided by reading the decodes.
- **Decodes** ([`decsum176.txt`](../data/cycle176/decsum176.txt), [`k4_decodes176.txt`](../data/cycle176/k4_decodes176.txt)).
  Each fit fixes the cipher alphabet only on the letters it pins down through the cribs (17–22 for K4's fits, 16–23 for the nulls'). The rest is filled by a seeded quadgram
  hill-climb (3 × 2,500 swaps, the same for every text), so each score is an *upper bound* over the free part. K4: 116 fits,
  best **−7.10** (L 8, perm 70590), rank 7 of 20 texts. The 19 nulls (1,097 fits) have per-null bests from −7.45 to −6.80,
  median −7.20. The 8 positive plants decode to **−4.04 … −4.08**, full English, although the six model-G plants had 8–13 alphabet letters left free and filled by
  the same climb. → `NO-SIGNAL`.
- **Replay.** `decode176.py` re-derives every reported fit at string level from the definitions: 0 failures in K4's 116 and the
  nulls' 1,097.

## 4. Pre-registered grid (I-110/I-115/I-117/I-120: exact Poisson tails, leave-one-out)
| cell | K4 | nulls min/med/max | scored? | K4 p⁺ / p⁻ |
|---|---|---|---|---|
| C1 G ix0 L 2–6 | 1 | 0/1/4 | yes | 0.61 / 0.76 |
| C2 G ix0 L 7 | 12 | 5/10/17 | yes | 0.38 / 0.72 |
| C3 G ix1 L 2–5 (1/8) | 0 | 0/0/1 | yes | 1.00 / 0.95 |
| C4 named primers | 0 | 0/0/0 | **no** (all 20 zero) | — |
| C5 PG | 0 | 0/0/0 | **no** (all 20 zero) | — |

G⁺(K4) = 0.38, **grid p⁺ = 0.75**. G⁻(K4) = 0.72, **grid p⁻ = 0.80** (best attainable 0.05). Nothing stands out on either side.
The I-120 Poisson score worked as intended: C1 and C3 are sparse, and no single event threw a text to ±∞.

## 5. Controls and recount
- **Planted controls 9/9** ([`controls_check176.txt`](../data/cycle176/controls_check176.txt)), built by an independent
  string-level encryptor ([`plant176.py`](../tools/cycle176/plant176.py)). Each was recovered at the planted perm, primer or
  keyword, alphabet and form:
  - G ix 0 L 5 with a PALIMPSEST+KRYPTOS alphabet
  - G ix 1 L 4, KA Beaufort, SHADOW ACA-columnar alphabet
  - G ix 0 **L 8**, random alphabet, among 56 chance fits
  - G ix 1 with the word primer KRYPTOS (L 7)
  - G ix 1 **variant** form, found as Beaufort
  - PG ix 1 PALIMPSEST/aca
  - PG ix 0 SHADOW/kmix Beaufort
  - G ix 0 primer 55555

  The negative plant (two crib slots forced to equal carved letters with different w) is absent at its perm, as it must be.
  Their decodes read −4.04 … −4.08 ([`controls_decodes176.txt`](../data/cycle176/controls_decodes176.txt)).
- A first version of the negative changed one carved letter under a crib with a *unique* w and was still found. That is
  correct behaviour, not a bug. With an arbitrary cipher alphabet, a wrong letter is only visible where it takes part in an
  equality. The negative was rebuilt as a forced collision before any K4 run. The same fact limits what "strict" means
  here (§6).
- **Independent recount** ([`recount176.py`](../tools/cycle176/recount176.py), numpy, straight from the pair definition)
  against `gm176` covered K4, 2 nulls and 4 plants. The slices were 46 perms (every 4,000th plus the plant perms) at L 2–4 and
  5 perms at L 5, both ix, A–Z/KA, Vig/Beau: **224/224 count lines identical**, including the 5 non-zero ones
  ([`recount176.txt`](../data/cycle176/recount176.txt)).

## 6. Scope, blind spots, cost
- **Strict.** No dropped, extra or wrong letters. Under an arbitrary cipher alphabet, one wrong letter matters only at a crib
  slot that shares its letter or its w with another slot. A one-error version is queued (I-128).
- **ix 1 stops at L 5.** L 6 would cost about 7.5 min for the full set. L ≥ 6 is covered only by the named primers
  (I-127).
- **Ordinary Gromark only uses one offset.** The relaxed periodic form (free group offsets with an arbitrary alphabet, the
  cycle-130 model P) was not run behind the decimations (I-126). The ACA form was tested only with the vocabulary keywords.
- **Base 10 only** (bases 5–9: I-129). The plaintext alphabet is A–Z or KRYPTOS; both alphabets arbitrary remains open (I-130).
- **Perm set.** The 165,782 K3-law decimations (M 97–112) and routes of case 156. The 98-symbol `?` circle and the 96/98-letter
  rebuilds were not used.
- **Decode bound.** The hill-climb fills 3–13 free letters, so the score is optimistic for every text alike. With 17–22 letters
  fixed, it cannot turn gibberish into English, as the null decodes show, and it does find English with as few as 13 fixed (plants).
- **Cost:** the main run took 5 min 00 s (06:54:43–06:59:42 PT, 6 threads, own process group under `setsid timeout`). Controls,
  decodes and recount took about 3 min more.

## 7. Verdict
Gromark's chain-added digits behind K3's decimation law are excluded at every primer length where the test can tell K4 from
noise (L ≤ 5 in both orders), for every listed word primer, and for every listed ACA keyword. Where the test cannot tell
(plaintext index, L ≥ 6), K4 sits on the null line and reads like noise. **Negative.** New ideas: I-126–I-132.

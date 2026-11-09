# Case file 161 — The one-letter anomaly behind K3's decimation law (cycle 173)

**Status:** negative. **Type:** audit/variant (cycle 172 was a new family). IDEAS [I-105](../IDEAS.md) (rest of I-095 / I-089, case 57's list),
with the I-107 grid rule applied for the first time and I-104 as an add-on.
K1, K2 and K3 each carry one bad letter: a Q for an L, a missing S, DESPARATLY. [Case 23](23-one-letter-anomaly.md) bent the ruler for the
cycle-19 transposition family (columnar w ≤ 8, K3-style rotations). It never did so for K3's own law: K3 *is* a decimation
([case 57](57-k3-as-decimation.md)). Since cycle 59 the coverage row "Decimation" listed the one-letter anomaly as open. This cycle closes that row.

**Result in one line:** with a periodic key on the A–Z or KRYPTOS tableau (all four PA/CA pairs), Vigenère/variant or Beaufort, key at either
index, behind a K3-law decimation, K4 has **no fit under any single dropped, extra, changed or swapped letter up to p 18**
(dropped/changed) and **p 19** (extra/swapped) → **`EXACT-EXCL`**. Above that, counts equal the analytic chance line and sit inside
19 shuffled nulls; decodes are gibberish → **`LOW-POWER` / `NO-SIGNAL`**. Grid rule (I-107): K4 grid rank 1.00 → nothing stands out.
Add-on (I-104): none of cycle 172's 685 Quagmire IV p 15–16 survivors has a one- or two-word vocabulary key → **`EXACT-EXCL`**.

## 1. Why this, and why it is new
- Queue: cycle 172 recommended I-105 or I-099 for this audit slot, with I-104 as a cheap add-on. I-105 is P2 and K3-shaped (K3's law + K3's own kind
  of slip), and it is the last open item of case 57's list for periodic keys. I-099 (rail/AMSCO one-error running keys, ~3 cycles of chunks) stays queued.
- Not run before: case 23 used the cycle-19 family rebuilt for 96/98 letters (157,609 / 162,966 perms, no decimations); case 57 used decimations
  with no anomaly. For n = 97 only 492 of the 160,204 decimations were in the cycle-12 family (case 57). The 96/98-letter decimation families
  are built here for the first time. kryptosbot reports (findings page, status 29 Sep 2026) a one-letter search "combined with a grid rearrangement".
  Grid ≠ decimation, so no overlap is claimed or assumed.

## 2. Model ([`tools/cycle173/anom173.c`](../tools/cycle173/anom173.c), from cycle 24's `anomaly_periodic.c`)
- **True ciphertext C′** of n letters, then one slip on the copper (case 23 conventions):
  `del` C′ has 98 letters, letter d (0–97) left off · `ins` C′ has 96, an extra letter carved at carved index d (0–96) ·
  `chg` one carved letter changed. It is visible only under a crib, so one of the 24 cribs is dropped · `swp` carved letters d, d+1 swapped (0–95).
- **Transpositions** ([`decgen173.py`](../tools/cycle173/decgen173.py)): perm[j] = (a + s·j) mod M, gcd(s, M) = 1, every a, slots ≥ n skipped,
  both directions. n = 98: M 98–113, **170,258** perms. n = 96: M 96–112, **168,858**. n = 97 (chg, swp): the 165,782 of cases 156–160 (159,712
  decimations + 6,070 spiral/diagonal routes). Cribs at plaintext positions 21–33, 63–73.
- **Substitution:** periodic key, (PA, CA) ∈ {A–Z, KRYPTOS}², Vig (= variant test) / Beau, key at the plaintext index (substitute, then transpose)
  or at the C′ index (transpose, then substitute), p 1–26. Exact: the crib key values must agree inside every residue class (pairwise bad-period masks).
  The tool also prints, per p, the analytic chance expectation Σ 26^−(used − classes) (I-097) and the number of distinct perms with a fit (I-101).
- **Known-answer check** ([`baseline173.txt`](../data/cycle173/baseline173.txt)): model `none`, PA = CA, on the cycle-59 decimations reproduces case 57
  exactly at p 22–25 (20 / 39 / 668 / 516). p 26 differs only because case 57 counted minimal periods.
- **Texts:** K4 on the full families (2.20 × 10¹⁰ period-level tests). 19 shuffled-K4 nulls (seeds 173000–173018) and K4 on every 4th perm.
- **Pre-registration** ([`PREREG173.md`](../tools/cycle173/PREREG173.md)) was committed with the tools before any K4/null anomaly run (commit 75ed54c).

## 3. Results ([`summary173.txt`](../data/cycle173/summary173.txt))
| model | K4 0 fits at | chance expectation summed over those p | first K4 fit | label |
|---|---|---|---|---|
| del (n 98) | p 1–18 | 0.32 | p 19: 1 config (E 1.79) | `EXACT-EXCL` p ≤ 18 |
| ins (n 96) | p 1–19 | 0.65 | p 20: 2 configs, 1 perm (E 9.0) | `EXACT-EXCL` p ≤ 19 |
| chg (n 97) | p 1–19 | 1.74 (p 19 alone 1.50) | p 20: 25 (E 23.7) | `EXACT-EXCL` p ≤ 18; p 19 0 vs E 1.5 → `LOW-POWER` by the pre-registered E < 1 rule |
| swp (n 97) | p 1–19 | 0.60 | p 20: 2 (E 10.1) | `EXACT-EXCL` p ≤ 19 |

Higher periods sit on the chance line. On the full family, observed / expected: del p 20–26 30/36.5, 104/124, 5,231/5,219, 13,839/13,630,
193,333/186,800 …; ins p 21 21/59.8 (one perm, 21 sibling slots: a cluster, not a tail, I-101); chg p 21 143/133; swp p 21 95/70.2 (8 perms).
On the 1/4 subset K4 is inside the 19-null range in every one of the 104 cells (e.g. del p 24: K4 49,467, nulls 43,135–49,522).
Controls show a real plant is found at p 5–19 in every model. So at the low periods a true solution of this kind would have been seen.

**English** ([`k4_decodes173.txt`](../data/cycle173/k4_decodes173.txt), [`english_nulls173.txt`](../data/cycle173/english_nulls173.txt)): all
423 K4 fits at p ≤ 21 decrypted with the crib-fixed key. Best off-crib quadgram −7.52 (chg), −7.58 (del), −7.69 (ins), −7.84 (swp). The 19 nulls'
bests run −7.38 to −8.32, and the 10 plants read −3.65 to −4.30 at their true slots. No English word outside the cribs → **`NO-SIGNAL`**.

## 4. The grid rule, used for the first time (I-107, pre-registered)
- 104 cells (4 models × p 1–26). Cell p for text X = share of the 20 texts (K4 + 19 nulls, 1/4 subset) with count ≥ X's. T(X) = min over cells.
- **K4: T = 0.10 (del p 24, second-highest of 20). K4's grid rank = 20/20 = 1.00** (floor 1/20 = 0.05, I-094). 15 of the 19 nulls top at least
  one cell (T = 0.05), and K4 tops none. Low tail, same rule: rank 0.90. → **`NO-SIGNAL`**.
- **Lesson (→ I-110):** with 20 texts and 104 cells the statistic saturates. Almost every text is the maximum somewhere, so the best attainable
  grid rank for K4 here was 15/20 = 0.75, not 0.05. The rule guarded against cherry-picking, but it had no power to *detect* anything. A post-hoc,
  descriptive max-z over cells with E ≥ 1 ([`posthoc173.txt`](../data/cycle173/posthoc173.txt)) puts K4 at 15.0 vs nulls 8.4–25.3 (rank 0.65).
  The large z values everywhere come from clustered sibling slots (overdispersion), not from signal. This is not used for any label.

## 5. Controls and checks ([`controls_recount173.txt`](../data/cycle173/controls_recount173.txt))
- **Plants 11/11** ([`plant173.py`](../tools/cycle173/plant173.py), string-based, written separately from the C tool): 10 plants over del/ins/chg/swp,
  all four tableau pairs, both modes, both frames, p 5–19 (keys COMPASS … THEHIDDENSHADOWLINE). All are found at their perm, slot, tableau, mode,
  frame and p, and the key letters match, with '?' only on classes without a crib. Each one reads back as English (−3.65 … −4.30).
  The 11th plant has a dropped letter **and** a changed crib letter. Strict `del` missed it, as it must (blind spot → I-111).
- **Independent recount 6/6 identical** ([`recount173.py`](../tools/cycle173/recount173.py)): pure-Python brute force from the definitions, against the tool on
  slices of all four models (K4 and null 3, decimations and routes): 3,924 configurations, the same set.
- Inputs and md5s: [`inputs173.txt`](../data/cycle173/inputs173.txt). `all_s4.bin` is byte-identical to cycle 172's.

## 6. Add-on: word keys for the Quagmire IV p 15–16 survivors (I-104, [`wordkey173.txt`](../data/cycle173/wordkey173.txt))
Case 160 left 685 K4 configs at p 15–16 (any key; on the chance line). If the key is a vocabulary word, power comes back.
Finding first: **the 10,056-word vocabulary has no 15- or 16-letter word**. So the key was tested as one word of length p (none possible) or **two words
joined** (a + (p − a), a 3…p−3), every cyclic shift, key letters read on CA, PA or A–Z, '?' classes free.
**K4 0 / 685; the 8 cycle-172 nulls 0 / 1,305; 3/3 planted p 16 two-word keys found** (e.g. ACCOSTED+VERTICAL). By chance, a fully fixed random key splits into two
vocabulary words with probability 3 × 10⁻¹³ (p 15) or 1 × 10⁻¹⁴ (p 16) per survivor → **`EXACT-EXCL`** for one- or two-vocabulary-word keys at p 15–16
behind the decimations/routes.

## 7. Limits and what is still open
- Tableaux are A–Z/KRYPTOS only. Quagmire III with the 264 / 20,946 themed alphabets under an anomaly behind decimations is not done
  (≈ 66× this cost for 264) → I-109. Spiral/diagonal routes were not rebuilt for 96/98 letters (del/ins ran on decimations only) → I-109.
- Two slips at once (as case 24 did directly), e.g. a dropped letter plus a changed crib letter (the missed 11th plant) → I-111.
- The `?`-circle (98-symbol) decimations under an anomaly were not run.
- Nothing here reads as English. No solution.

## 8. Cost
Run 3 min 39 s wall (K4 full + 20 texts × 4 models on 1/4; 2 jobs × 4 threads, box shared with a Voynich generator job), plus ~1 min controls, recount and add-on.

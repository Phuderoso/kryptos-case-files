# Case file 165 — One wrong letter: auditing the Gromark exclusions behind K3's decimation law (cycle 177)

**Status:** negative. **Type:** audit/variant (cycle 176 was a new family). IDEAS [I-128](../IDEAS.md) (the cycle-177 pointer
I-132) with the add-on [I-129](../IDEAS.md). Pre-registered in [`tools/cycle177/PREREG177.md`](../tools/cycle177/PREREG177.md)
(commit ee848eb, 14:23:35 UTC = 07:23 PT) together with the solvers, before any K4 or registered-null run. The main run started
13 s later. Smoke/timing runs used only the reserved shuffle, seed 9177 ([I-116](../IDEAS.md)).

**Result in one line:** case 164's strict `EXACT-EXCL` claims for Gromark behind the 165,782 K3-law decimations/routes survive
**one wrong carved or crib letter** at primer length **L 2–3 (both layer orders)** and for **every ACA Periodic Gromark keyword**
(≥ 23/24 exact predictions: 0 fits, both orders). At **L 4–5 and for the named primers**, one error lets chance fits in at the
shuffled-null rate (ix 0: 2 / 23 vs null means 1.9 / 21.8), so those exclusions are strict-only. All of those fits decode to
gibberish → `LOW-POWER` / `NO-SIGNAL`. One pre-registered cell was **flagged**: C2, one-error fits on the plaintext index at L 6. K4
has 230 there, above all 19 nulls (154–218). Its 256 decodes are gibberish, with a best of −7.08 against −6.94 … −7.05 for the 5
nulls decoded, so the cell reads `NO-SIGNAL`. The grid upper tail is at its floor (p⁺ 0.05 = rank 1 of 20); a replication with
fresh nulls is queued (I-133). **Strict Gromark in digit bases 5–9** (I-129): 0 K4 fits at ix 0 L 2–5 and ix 1 L 2–4 →
`EXACT-EXCL`. Bases 8–9 at L 6–7 fit at the null rate → `LOW-POWER`/`NO-SIGNAL`. **No solution.**

## 1. Why this, and what is new
- Case 164 ran ordinary Gromark (any cipher alphabet) and ACA Periodic Gromark behind the decimations **strictly**. Under an
  arbitrary cipher alphabet a single wrong letter breaks the partition test only where that slot takes part in an equality.
  Case 164's own negative plant showed this. So the strict zeros could hide a K4 with one carving or crib slip. Sanborn's
  confirmed carving errors in K1–K3 make that a live question.
- Cycle 155 ran Gromark under one error **direct** (no transposition). Cycle 176 ran it behind the decimations, but only strict.
  This cycle combines the two. No earlier run covered digit bases 5–9 behind any transposition.

## 2. Models (exact; repo conventions)
Cribs at plaintext index 21–33 and 63–73 (0-indexed). Plaintext position i is carved at S[i].
- **G1, one-error ordinary Gromark** ([`gm177.c`](../tools/cycle177/gm177.c), err 1, base 10). The model is gm176's: d[i] = d[i−L] +
  d[i−L+1] mod 10, PA = A–Z or KRYPTOS, **cipher alphabet arbitrary**, Vigenère w = PA(p) + d, Beaufort w = d − PA(p), and
  variant = Beaufort reflected. A config fits with one error iff some crib slot t can be dropped so that equal carved letters ⇔
  equal w holds on the other 23 slots. Under an arbitrary alphabet, a wrong carved letter and a wrong crib letter are the same
  event: slot t becomes free. A consistent true letter always exists, because 23 slots use at most 23 of the 26 letters.
  The solver reports the **drop mask**, i.e. every t that repairs the fit (the slots lying in every violated pair). A full mask
  means a strict fit. The counted statistic is **one-error-only fits** (mask ≠ full).
  - ix 0 (Gromark on the plaintext index, then transpose): hash join with 24 masked partition codes per perm, every primer
    L 2–6, full perm set (≈ 3 s per text).
  - ix 1 (transpose, then Gromark on the carved index): brute force. The drop mask is intersected over violated equal-letter
    pairs first, with a fast reject. Every primer L 2–5. K4 ran on the full set (66 s) and on every 8th perm; nulls on every 8th perm.
  - Named primers: cycle 176's 22,121 (vocabulary numerical keys L 3–16, dates, coordinates), both ix.
- **PG1, one-error ACA Periodic Gromark** ([`pg177.c`](../tools/cycle177/pg177.c)): cycle 176's 137,312 configs (17,164 keywords ×
  aca/mix/ka/kmix × A–Z/KRYPTOS) × Vig/Beau. The alphabets are fixed, so a fit means ≥ 23 of 24 exact predictions. ix 0 is a join on
  24 masked keys. ix 1 buckets perms by the carved slot of crib 0 **and** crib 1, since a ≥ 23/24 fit matches at least one of
  them. Both ix ran on the full set for every text.
- **GB, strict Gromark in base b = 5…9** (`gm177.c` err 0): digits mod b, b^L primers. ix 0 L 2–7 full; ix 1 L 2–4 (K4 full + 1/8,
  nulls 1/8).
- The err-0/base-10 path of `gm177` reproduces cycle 176's `gm176` output line for line on n17611 (M lines identical).

## 3. Results — K4

| model | cell | K4 | 19 nulls min/med/max (mean) | verdict |
|---|---|---|---|---|
| G1 ix 0 | L 2–3 | **0** | 0/0/0 · 0/0/1 (0.11) | `EXACT-EXCL` |
| G1 ix 0 | L 4 | 2 (both perm 157462, drop slot 21 = the O of CLOCK) | 0/1/6 (1.89) | `LOW-POWER`; decodes −7.61/−7.62 → `NO-SIGNAL` |
| G1 ix 0 | L 5 | 23 | 13/22/32 (21.8) | `LOW-POWER`; decodes ≤ −7.35 → `NO-SIGNAL` |
| G1 ix 0 | L 6 | **230** (+ 1 strict, case 164's) | 154/194/218 (191.5) | **flag** (above all nulls); 230 decodes ≤ −7.08 → `NO-SIGNAL` |
| G1 ix 1 | L 2–3 | **0** (full set) | 0 (1/8) | `EXACT-EXCL` |
| G1 ix 1 | L 4 | 0 on 1/8; **5 on the full set** | 0/0/3 (0.32 on 1/8 ≈ 2.6 per full set) | `EXACT-EXCL` only on the matched 1/8 sample; full set `LOW-POWER`, decodes → `NO-SIGNAL` |
| G1 ix 1 | L 5 | 6 on 1/8; 26 full | 0/3/8 (2.95 on 1/8) | `LOW-POWER`; 31 full-set decodes ≤ −7.11 → `NO-SIGNAL` |
| G1 named primers | ix 0 full / ix 1 | 3 / 1 on 1/8 (6 full) | 1/4/10 (4.7) / 0/0/3 (0.58) | `LOW-POWER`; decodes ≤ −7.05 → `NO-SIGNAL` |
| PG1 (≥ 23/24) | ix 0 / ix 1 | **0 / 0** | 0 / 0 | `EXACT-EXCL` |
| GB b 5–9 | ix 0 L 2–5, ix 1 L 2–4 (full) | **0** | 0 (b 9 L 5: 0) | `EXACT-EXCL` |
| GB b 5–7 | ix 0 L 6–7 | **0** | 0 | `EXACT-EXCL` |
| GB b 8 | ix 0 L 6 / L 7 | 0 / 1 | 0 / 0/2/4 (1.79) | `EXACT-EXCL` / `LOW-POWER` |
| GB b 9 | ix 0 L 6 / L 7 | 1 / 5 | 0/0/1 (0.47) / 2/4/13 (5.3) | `LOW-POWER`; the L 6 fit decodes −7.64 → `NO-SIGNAL` |

Per-cell table: [`summary177.txt`](../data/cycle177/summary177.txt). All K4 lines: [`k4_runs177.txt`](../data/cycle177/k4_runs177.txt).
- **What the audit says about case 164.** The strict zeros at L 2–3 (both orders) and for the ACA keywords hold under one error,
  and there chance fits are rare or absent. At L 4–5 and for named primers, the one-error model fits random text about as
  often as K4, so case 164's strict `EXACT-EXCL` there is a **strict-only** statement. With one slip allowed it becomes
  `LOW-POWER`, and every K4 fit reads as gibberish (`NO-SIGNAL`). This matches the expectation in I-128 ("exact up to about L 4").
- **Label note (deviation in wording, not in rule).** The pre-registration tagged K4-zero cells with a null mean < 1 as
  "`EXACT-EXCL (weak power)`". The script prints that tag. It is a misnomer: a null mean near 0 means the test almost never fits
  random text, so those exclusions are the *most* selective of the cycle. The tag is kept in the data file and explained here.
- **The C2 flag** (G1 ix 0 L 6). K4 has 230 one-error-only fits. The 19 nulls have 154–218 (mean 191.5, Poisson p⁺ 0.004 against
  the leave-one-out mean), so K4 is first of 20. The fits are **not clustered**: 191 distinct perms, at most 4 fits per perm.
  They spread evenly over the perm file (12–20 per 10,000-perm block, nulls 10–13). The A–Z/KRYPTOS × Vig/Beau split matches the
  nulls'. A structural covariate explains part of the excess. Over the 165,782 perms, K4's 24 crib-slot letters contain on average
  **9.90 equal-letter pairs**, fewer than in 18 of the 19 shuffles (9.89–10.01). Fewer equalities mean fewer constraints. Across the
  nulls, the count falls with this mean (r = −0.35). The fitted line predicts 201 for K4, and K4's 230 is +1.9 residual SD above it
  ([`eqpairs177.txt`](../data/cycle177/eqpairs177.txt), [`c2_vs_eq.txt`](../data/cycle177/c2_vs_eq.txt)). Cycle 176's strict counts
  at L 6–8 also sat slightly above the null means (1/0.84, 12/10.7, 103/97). **Decodes:** all 256 K4 ix-0 fits at L ≤ 6 decode to
  gibberish (best −7.08, median −7.70). The first 5 nulls' 1,080 fits give per-text bests of −6.94 … −7.05 and medians of
  −7.62 … −7.71. The plants reach −4.04 … −4.08. Reading: a mild count excess with no readable text behind it. It is partly a
  property of K4's letter layout over this perm family, not evidence for a Gromark key. Not called a signal. A pre-registered
  replication (40 fresh shuffles plus equal-pair-matched nulls) is queued as I-133.
- **Decodes** ([`decsum177.txt`](../data/cycle177/decsum177.txt), [`k4_decodes177.txt`](../data/cycle177/k4_decodes177.txt)). These
  use cycle 176's procedure: the cipher-alphabet letters not pinned by the cribs are filled by a seeded quadgram hill-climb
  (3 × 2,500 swaps, the same for every text). For a one-error fit, every slot in the drop mask is tried as the wrong one. K4: 297
  decoded fits, **best −7.05** (named primer PETRIFIEDCOPPER, ix 1, perm 140820), last of the 6 texts decoded. 17–22 letters are
  fixed for K4, 15–23 for the nulls. Plants (12–18 fixed) read the planted English at −4.04 … −4.08. **Replay:** `decode177.py`
  re-derives every fit at string level on its 23 (or 24) slots: 0 failures in 297 K4 + 1,129 null fits.

## 4. Pre-registered grid (I-120 rule: exact Poisson tails, leave-one-out; all-zero cells reported, not scored)
| cell | K4 | nulls min/med/max | scored? | K4 p⁺ / p⁻ |
|---|---|---|---|---|
| C1 G1 ix0 L 2–5 | 25 | 16/23/34 | yes | 0.43 / 0.65 |
| C2 G1 ix0 L 6 | 230 | 154/194/218 | yes | **0.004** / 1.00 |
| C3 G1 ix1 L 2–5 (1/8) | 6 | 0/3/8 | yes | 0.11 / 0.95 |
| C4 named G1 ix0 + ix1 (1/8) | 4 | 2/5/11 | yes | 0.77 / 0.40 |
| C5 PG1 both ix | 0 | 0/0/0 | **no** | — |
| C6 GB ix0 L 2–7 + ix1 L 2–4 (1/8) | 7 | 4/8/16 | yes | 0.82 / 0.29 |

G⁺(K4) = 0.0037, **grid p⁺ = 0.05** (K4 first of 20, the floor). G⁻(K4) = 0.29, **grid p⁻ = 0.90**. The upper tail is driven
entirely by C2 (§3). By the pre-registered rule, a flagged cell is decoded and is not called a signal without a readable decode.
The decodes are not readable.

## 5. Controls and recount
- **Planted controls 13/13** ([`controls_check177.txt`](../data/cycle177/controls_check177.txt)). They come from an independent
  string-level encryptor ([`plant177.py`](../tools/cycle177/plant177.py)), and every plant sits behind a perm of `all.bin`:
  - **One-error G plants.** ix 0 L 4 with a wrong carved letter (slot 4). ix 1 L 4 KA Beaufort with a wrong *crib* letter
    (slot 19). ix 0 L 5 with a random alphabet and a wrong carved letter in BERLINCLOCK (slot 20, found among 17 chance fits).
    ix 1 named primer KRYPTOS with a wrong carved letter (slot 0). ix 1 L 5 **variant** with a wrong crib letter (slot 2), found
    as Beaufort. Each was found at the planted perm, primer, alphabet and form, with a **non-full mask containing the planted
    slot**, so the strict test misses every one of them.
  - **One-error PG plants.** ix 1 miss at crib slot 0 (the second-bucket path), ix 0 wrong crib letter, ix 1 miss at slot 17.
    The reported miss slot equals the planted one each time.
  - **Strict plants.** Base 7 ix 0 L 6, base 5 ix 1 L 4, and a base-10 plant in the err-1 run, each found with a full mask.
  - **Negatives.** G with two wrong letters in disjoint violated pairs, and PG with two misses, are both absent at their planted
    configs.
- **One control failed first.** `ctl9` was built with primer 314159 in base 7. The digit 9 is not a base-7 digit, so the solver
  never enumerates it. The plant was fixed (314156) and rerun, and now passes. The failed check is kept as
  [`controls_check177_v1.txt`](../data/cycle177/controls_check177_v1.txt). In the failed run, gm177 did report primer 314152 at the
  planted perm, which is correct behaviour: 9 ≡ 2 (mod 7) gives the same chain from index 6 on, and the primer digits never touch
  a crib slot.
- **Plant decodes:** all 11 positive plants decode to the planted English at −4.04 … −4.08 with 12–18 fixed letters
  ([`controls_decodes177.txt`](../data/cycle177/controls_decodes177.txt)).
- **Independent recount** ([`recount177.py`](../tools/cycle177/recount177.py)) uses numpy, straight from the pair definition, and
  shares no code with the C solvers. (a) A 49-perm slice (every 4,000th perm plus the plant perms), G1 base 10 L 2–4 and GB base 7
  L 2–4, both ix, A–Z/KA, Vig/Beau, plus PG1 both ix on all 137,312 configs. Texts: K4, 2 nulls, 4 plants. The fit sets are
  **identical** (4 fits in both, including the plants' masks and miss slots). (b) A targeted L 5 slice: the 61 perms of every K4 one-error fit at L 4–5 (both ix) plus 12 random perms, split in
  6. Every one of K4's 49 L 5 one-error fits (23 ix 0 + 26 ix 1) is recomputed by numpy, with the same drop masks, and nothing
  extra appears: **49/49 identical** ([`recount177.txt`](../data/cycle177/recount177.txt)).

## 6. Scope, blind spots, cost
- **One error only.** Two wrong letters are not covered: the negative plants are correctly missed. Dropped or inserted letters,
  which shift the transposition, are not covered either.
- **ix 1 nulls on every 8th perm.** The matched comparison is K4-on-1/8 vs nulls-on-1/8. K4's full-set counts are reported next to
  it. The ix 1 L 4 zero holds **only** on the 1/8 sample; the full set has 5 one-error fits (≈ 2.6 expected), all gibberish.
- **L 6 decodes** were added under the flag rule (the pre-registration decoded ix 0 only to L 5). Nulls were decoded for 5 of 19
  texts. ix 0 L ≥ 7 under one error was not run (chance ≈ 2,300 fits per text).
- **Bases 5–9 are strict only.** One-error in bases 5–9, ix 1 L 5, and L 8 were not run (I-136).
- **Decode bound.** A hill-climb is a local optimiser, so each score is a single-start-set upper bound. The spread over seeds was
  not measured (I-135, after Voynich's C086 lesson on PLSA starts).
- **Perm set.** The 165,782 K3-law decimations/routes of case 156. The 98-symbol `?` circle and the 96/98-letter rebuilds were not
  used.
- **Cost:** main run 8 min 16 s (07:23:48–07:32:04 PT, 6 threads, own process group under `setsid timeout`). Controls, decodes
  (6 processes, 1.7 min) and recounts took about 4 min more.

## 7. New ideas (IDEAS.md)
I-133 (replicate C2 with 40 fresh + equal-pair-matched nulls), I-134 (covariate-adjusted grid cells), I-135 (decode-score seed
spread), I-136 (one-error Gromark bases 5–9 and ix 1 L 5), I-137 (linear-recurrence key mod 26 behind the decimations, new
family), I-138 (cycle-178 pointer).

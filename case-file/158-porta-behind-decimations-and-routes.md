# Case file 158 — Porta behind K3's decimation law and spiral/diagonal routes (cycle 170)

**Status:** negative. **Type:** new family behind this transposition structure (cycle 169 was an audit/variant). IDEAS I-089, Porta part.
Porta is the reciprocal "half-swap" tableau (della Porta, 1563): 13 key values, each one swaps the first half of an alphabet with
the second half. It is a non-additive substitution, so it is not a relabelled Quagmire. Case 57 listed it as open behind
decimations, and the coverage row "Decimation" kept it open until now.

**Result in one line:** K4 has 0 periodic Porta keys at L 1–23 (all four variant × layer-order cells; L 1–25 for key-by-plaintext-position),
and 0 running-key fits in 36 named texts, behind 165,782 decimations/routes × 173,431 alphabet orderings → **`EXACT-EXCL`**.
Porta with an arbitrary (non-periodic, unnamed) key is **`LOW-POWER`**: 1,539 key-free survivors, inside 40 shuffled nulls
(median 1,551, rank p = 0.51, floor 1/41 = 0.024).

## 1. Why this, and why it is new
Candidates were I-089 (Porta / Quagmire IV / the one-letter anomaly behind decimations, running keys on the `?` circle and mixed
tableaux) and I-016 (SAT periodic, open periods; I-016 itself expects `LOW-POWER` at P ≥ 8). Cycles 163–169 were periodic, autokey
and running-key relatives. Porta is a different substitution (reciprocal, never maps a letter to itself, letters always cross
halves), and it was never put behind decimations or routes. Grep of the 157 case files, IDEAS.md and the README coverage table:
- Porta direct and behind the **96,630 cycle-12 transpositions** only, on 20,946 themed alphabets, first/last-13 halves only
  ([case 31](31-porta-half-split.md), cycle 32). Running keys there: six books, scored (best 12/24 vs nulls 12–13).
- Portax (case 56) and the halfabet (case 82) are different families. The halfabet keeps letters inside a half; Porta swaps them across.
- The 159,712 decimations and 6,070 routes are not in the cycle-12 family (cases 57, 59). They met only Quagmire III (59, 61), autokey
  (60, 62), rotors (97), self-keying (98) and running keys (168, 169).
So Porta behind decimations/routes is new. New here too: the full 86,731-alphabet bank, the even/odd half-split that case 31 left out,
and exact running keys.

## 2. Model ([`tools/cycle170/porta170.c`](../tools/cycle170/porta170.c))
- **Transpositions:** the 165,782 of case 156 (`all.bin`: 159,712 K3-law decimations perm[j] = (a + s·j) mod M, M 97–112, empty slots
  skipped, perm and inverse; + 6,070 spiral/diagonal routes). perm[j] = carved position holding plaintext letter j.
- **Orderings:** each of the 86,731 bank alphabets read two ways: **F** (halves = first / last 13) and **E** (halves = even / odd places,
  ordering = a[0::2] + a[1::2]). Deduplicated: 173,431 orderings, 69,012 distinct half-splits (a split and its complement are one).
- **Porta:** H1 = o[0..12], H2 = o[13..25]. **V1** H1[i] ↔ H2[(i+k) mod 13] (the classical table, any sign of k); **V2** H1[i] ↔ H2[(k−i) mod 13].
  Both are reciprocal, so substitute-then-transpose and transpose-then-substitute differ only in the key index:
  **A** key index = plaintext position j, **B** key index = carved position perm[j].
- **Stage 1, key-free (exact for any key):** a Porta letter always crosses halves, so all 24 crib pairs (PT[j], CT[perm[j]]) must cross.
  Per perm: if any crib letter faces the same carved letter, Porta is impossible (107,684 of 165,782 perms die here). Otherwise
  2-colour the 24-edge letter graph (53,812 more die on an odd cycle). A split passes iff on every component it equals the colouring or
  its complement. 4.0 × 10⁹ (perm, split) pairs tested.
- **Stage 2 on survivors:** (i) periodic key L 1–26, exact consistency per residue class, V1/V2 × A/B; (ii) running keys: 36 texts
  (3.30 M letters, case 156/157 set), every offset, key value = s·f(letter) + c mod 13, f = A–Z index ÷ 2 (classical AB, CD, … pairs) or
  index in the ordering ÷ 2, s = ±1, c free (fixed by the first crib). That is 16 conventions per survivor, 24/24 required.

## 3. Results ([`summary170.txt`](../data/cycle170/summary170.txt), [`bound170.txt`](../data/cycle170/bound170.txt))
| test | K4 | 40 shuffled nulls | chance expectation for K4 | label |
|---|---|---|---|---|
| Stage 1 survivors (perm, ordering), any key | 1,539 (637 perm × split) | 1,165 / **1,551** / 2,942 (min/median/max); 20/40 ≤ K4 → rank p = 0.51 (floor 1/41 = 0.024) | — | `LOW-POWER` (arbitrary key) |
| Periodic, model A (key by PT position), V1/V2 | **0 at L 1–25**; L 26: 115 / 111 | all 40 nulls 0 at L 1–24; L 26 median 109 / 104 | L ≤ 20: 1.0 × 10⁻⁴ fits; L 21–23: 5 × 10⁻⁵; L 24–26: 238 (observed 226) | `EXACT-EXCL` L ≤ 25 |
| Periodic, model B (key by carved position), V1/V2 | **0 at L 1–23**; L 24/25/26: 4/1/16 (V1), 9/8/12 (V2) | 0 at L ≤ 22 (V1), ≤ 20 (V2); L 21–23 up to 1/2/8; L 24–26 inside the null ranges (p 0.10–0.68) | L ≤ 20: 3.3 × 10⁻³; L 21–23: 0.56; L 24–26: 37 (observed 50) | `EXACT-EXCL` L ≤ 23 |
| Running keys, 36 texts × 16 conventions, 24/24 | **0** | 8 nulls on chunk c0 (1/16): 0 | 1,539 × 16 × 3.3 M × 13⁻²³ ≈ 2 × 10⁻¹⁵ | `EXACT-EXCL` |

**Reading the cells.** The periodic and running-key tests are exact: a K4 key of that form would have to appear, and none does. At L ≤ 20
a chance fit is improbable (≤ 3.3 × 10⁻³ expected), so a hit would have been decisive. At L 21–23 (model B) a hit would have been
ambiguous (0.56 expected; some nulls hit there), but K4 has none, so the exclusion still holds. At L 24–26 each config has ≤ 5 checks:
K4's 276 fits sit inside the null ranges and decode to gibberish (§5) → `LOW-POWER` there. Nulls with any periodic fit at L ≤ 23: 22/40,
all at model-B L 21–23 (Clopper–Pearson 95 % upper bound on the null rate 0.69). At L ≤ 20: 0/40 nulls (bound 7.2 %), K4 0. The verdicts
rest on the analytic bounds and binary plants (§4), not on null counts (I-085). Rank p-values carry the floor 1/(N+1) (I-094).

**Known-answer check of the counter (Voynich C080 lesson, unverified as a message; see §7).** The analytic expectation is a
known answer for the counts. Model A L 24–26 predicted 238, observed 226. Model B predicted 37, observed 50: crib letters are not
uniform, and model B has fewer checks per config. This is the same order, so the counter counts what the bound says it should.

## 4. Controls and independent recount
- [`ctl170.py`](../tools/cycle170/ctl170.py) is an independent string-level Porta encryptor (no code shared with `porta170.c`). It writes
  an English plaintext with both cribs at the official positions, a random decimation/route, a random bank alphabet, split F or E,
  V1/V2, model A/B, periodic keys L 3–12 (8) or running keys from four different texts with random f, s, c (4). It decrypts its own
  output back first. Each plant is hidden in a 200-perm slice.
  **12/12 recovered** at the planted slot, ordering, variant, model and L (or text, offset and convention)
  ([`ctl_verify170.txt`](../data/cycle170/ctl_verify170.txt), [`controls170_outputs.txt`](../data/cycle170/controls170_outputs.txt)).
  [`verify170.py`](../tools/cycle170/verify170.py) rebuilds each periodic key from the crib letters alone and decrypts all 97 letters by
  string operations: 7/8 give the planted plaintext exactly. ctl1 (model B, L 11) leaves one key residue unconstrained by the cribs,
  so 9 letters stay `?` and the other 88 match. Plant strength is binary (exact test), power 12/12.
- [`recount170.py`](../tools/cycle170/recount170.py) is an independent numpy recount (direct 24-pair half test over all 173,431 orderings,
  no masks, no graph colouring; periodic consistency by dict). Every 100th perm (1,658 perms):
  K4 25 survivors, periodic table identical to `porta170` ([`recount100.txt`](../data/cycle170/recount100.txt) vs
  [`c_k4_s100o0.txt`](../data/cycle170/c_k4_s100o0.txt)); null0 offset 7: 55 survivors, identical
  ([`recount100_null0.txt`](../data/cycle170/recount100_null0.txt) vs [`c_null0_s100o7.txt`](../data/cycle170/c_null0_s100o7.txt)).

## 5. Crib and English checks
No K4 configuration fits at an informative period, and none fits a running key. The 276 period-24–26 fits (≤ 5 checks each, chance level)
were decrypted letter by letter ([`k4_decodes.txt`](../data/cycle170/k4_decodes.txt)) and scored by mean log10 quadgram outside the cribs
([`english170.txt`](../data/cycle170/english170.txt)). Best −7.42, median −8.06. The planted English plaintext scores −4.13. Best K4 line:
`FMVIBAFF???ZMNCRIMNBJ EASTNORTHEAST ???DHOSOPZWOJYPAWKLOVBJFCR???BERLINCLOCK OHERRPKELUFQ???DTIHAETS`: gibberish. No candidate.

## 6. What this excludes and what it doesn't
Excluded (exact): K4 = Porta (V1 or V2, F or E halves, any of 86,731 bank alphabets) with a periodic key L ≤ 23 (L ≤ 25 when keyed by
plaintext position), or with a running key from any of the 36 named texts in any of 16 letter→key conventions, combined in either
layer order with any K3-law decimation (M 97–112) or spiral/diagonal route, strict crib letters.

Not excluded:
- Porta with an arbitrary key (1,539 survivors at null level; a free key per letter fits by construction), L 24–26 (crib-underdetermined);
- one wrong crib or carved letter (a single non-crossing pair kills a true config here; → I-096);
- the 98-symbol `?` circle (154,186 decimations) and alphabets outside the bank; other half-splits (e.g. KRYPTOS-row splits);
- Quagmire IV and the one-letter anomaly behind decimations (rest of I-089, → I-095); non-affine letter→key maps for running keys.

## 7. Run folder (I-078) and reproduction
[`inputs_provenance.txt`](../data/cycle170/inputs_provenance.txt): K4 16/16 chunks end in their final `PERIODIC V2B` line, nulls 40/40 + 8/8, controls
12/12, 0 `.tmp`. K4 run 02:54:52–~03:00 PDT (running keys dominate; stage 1 + periodic alone take 0.2 s per text), CPU shared with nothing heavy.
Reproduce: [`tools/cycle170/run_cycle170.sh`](../tools/cycle170/run_cycle170.sh).

Voynich note: their C080 journal (~02:33–02:50 PDT, read-only on the box) says they are sending "the known-answer control trick". The message
itself is not visible to this run. §3's analytic-vs-observed comparison is our version of it, logged as I-097.

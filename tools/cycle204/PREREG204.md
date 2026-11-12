# PREREG204 — exact conditioning of the COL_P reverse test at the 8 SAT-open periods (I-252, with I-254 / I-260)

Written 2026-11-12 ~07:51 PT, **before the registered run**. Committed alone (with the code) before `run_cycle204.sh` is started.

## Why
Case 189 put P 8 at `STAT-DISFAVOURED (repair-sensitive)`: q\* 0.0057 vs the Holm bar 0.00625 under C3, where banned letters in real
text windows are repaired by unigram draws; the bigram repair C3b gave 0.0095. The Voynich desk's exact moments (I-254, box files
`/workspace/voynich/kryptos-audits/c202-col8-exact/`, credited) move q\* to 0.0047 (fully exact z) and C3b to 0.0065, and their own
plant code with Dracula gives 0.0030–0.0045. All of these still repair; none conditions exactly. Real windows cannot be rejection
sampled (≈ 200 bans + 24 crib letters + forced letters).

## Method (registered)
- **Exact conditioning under a character chain.** Plaintexts are drawn *exactly* from an order-3 character Markov chain (quadgram
  chain, recursive Dirichlet back-off β = 1) conditioned on every C3 constraint as a hard per-position mask: the cribs
  (EASTNORTHEAST 0-idx 21–33, BERLINCLOCK 63–73) and crib-forced letters as singletons, the bans (`lib201.forbidden(P)`) as
  complements. Sampler: forward filtering / backward sampling (FFBS, `lib204.ffbs`). No repair step. Text flows into the cribs.
- **Ciphertexts:** per-phase bijections agreeing with K4's crib pairs (`lib201.alphabets(cond=3)` semantics, vectorised).
- **z:** exact permutation moments of COL_P (I-254 formula of the Voynich desk, re-implemented in `lib204.col_moments`, checked by G4),
  for K4 and every plant (no shuffle noise anywhere).
- **Registered models (4):** JE, CARTER, K123MIX (chain counts = Jane Eyre + K1–K3 plaintexts scaled to Jane Eyre's mass; a chain on
  ≈ 1,700 letters alone is degenerate), JEX. **Descriptive:** DRAC (Dracula, pg345, the Voynich desk's new model) and order-4 chains.
- **Sizes per model × P:** 10,000 EXACT-O3 references (tag 10), 2,000 held-out EXACT-O3 (tag 20), 10,000 chain-C3 (chain sample +
  case 189's unigram repair, tag 30), 10,000 real-window C3 (case 189's recipe, fresh seeds, exact z, tag 50), 4,000 EXACT-O4 (tag 60),
  1,000 shuffled K4 (tag 40). Seeds `default_rng([204204, tag, model, P, k])` (outside cycles 200–203 blocks, the probe 204299, the
  Voynich desk's 7001–7900).

## Confirmatory test
- q = (1 + #{plant z ≤ z_K4}) / (n + 1) per model × P (EXACT-O3 references); **q\* = max over the 4 registered models**; Holm over the
  8 periods at α 0.05. Minimum attainable q = 1/10,001 ≈ 0.0001 < 0.05/8, so an empty Holm list is readable (I-260 check).
- **Labels** (only if every gate passes; otherwise "no verdict", no rerun this cycle):
  - Holm rejects on EXACT-O3 q\* **and** on the real-window C3 q\* (tag 50, worst model, same Holm) → `STAT-DISFAVOURED` (statistical,
    model-dependent, never `EXACT-EXCL`); the "(repair-sensitive)" tag is **dropped**.
  - Holm rejects on EXACT-O3 only → `STAT-DISFAVOURED (real-window-sensitive)`.
  - Holm does not reject on EXACT-O3 → `LOW-POWER` (P 8 would be withdrawn from case 189's label).
- Descriptive (cannot create or keep a label): chain-C3 q (within-chain repair effect = q_chainC3 vs q_exact3), order-4 q, DRAC,
  C3b is not rerun.

## Gates
- **G1** COL_P(pt) = COL_P(ct) for every plant. **G1b** every plant ciphertext agrees with K4 where C3 fixes it, and every plaintext
  satisfies the mask.
- **G2b** held-out EXACT-O3 clean plants judged by q < 0.05 against the references: pooled false-disfavour rate ≤ 0.05 + 2 SE
  (64,000 → ≤ 0.0517) and every configuration below the exact Bin(2000, 0.05) bar at 0.05/32 (computed in code).
- **G3** shuffled K4 judged by the same rule: rate at P 8 ≥ 0.15 in every registered model.
- **G4** exact moments: brute-force enumeration equality on three tiny multisets (1e-9); K4 P 8 mean / SD = Voynich desk's 19.48454 /
  4.08224 (± 1e-4); 200,000 shuffles at every P: |mean dev| ≤ 4 SE and |SD rel. dev| ≤ 1 %.
- **G5** FFBS correctness: JE O3 chain, mild mask (pos 5 = E; 10–12 ban E,T,A; 40 ban E): FFBS vs rejection from forward samples
  (≈ 400k), pooled per-position χ² on positions 0–45 p > 0.001 and COL_8 mean |z| < 4.
- **G6** chain fidelity (set after the probe below): at P 8, chain-C3 vs real-window C3 in each registered model, |Δ mean z| ≤ 0.20
  and |Δ 5 % quantile| ≤ 0.20.

## Disclosure (what was seen before registration)
- Case 189, the Voynich desk's audit (above) and K4's exact z at P 8 (−1.3435, theirs).
- Probe (`probe204.py`, seed 204299, English plants only, never K4, 3,000 per cell at P 8): chain-C3 vs real C3 |Δ mean| ≤ 0.12
  (K123MIX; others ≤ 0.04), |Δ q05| ≤ 0.08; EXACT-O3 plant mean z is 0.03–0.12 **above** chain-C3 (q05 within 0.06). The G6 tolerance
  0.20 was set after this probe.
- Smoke runs of `run204.py` at scale 0.02 and 0.25 (timing; outputs deleted; only the gate pass/fail line and timing read; G4's K4 z
  line was printed in the 0.02 log but not read for decisions).

## Blind spots (registered)
The chain is a model of English: COL_P depends on coincidences at distances ≥ 8, which an order-3/4 chain captures only through
letter frequencies and short-range structure (G6 checks this against real windows under the same repair recipe, not under exact
conditioning). Real-window exact conditioning remains infeasible. H_P is free per phase (superset of Quagmire IV, I-247); no
transposition after substitution (I-239); whole-text shuffle null for K4 (I-248); K123MIX is a mixture, not Sanborn's text alone;
selection of COL as statistic predates fresh seeds (I-253).

## Run
`run_cycle204.sh`: `setsid timeout -k 10 480` (one process group), single process. Expected ≈ 2–3 min.

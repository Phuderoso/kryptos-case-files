# PREREG202 — confirmatory COL_P reverse test at the 8 SAT-open periods under full crib conditioning (C3) (I-245)

Written 2026-11-11 ~23:50 PT, **before the registered run**. Committed alone (with the code) before `run_cycle202.sh` is started.

## What has been seen before this registration (disclosure)
- Case 188 (cycle 201, seeds 22000) published K4's COL_P and its z against 10,000 own shuffles (P 8 / 13 / 23: COL 14 / 7 / 3,
  z −1.34 / −1.37 / −1.17) and a **descriptive** q_col under C3 of 0.001–0.003 (P 8), 0.008–0.017 (P 13), 0.010–0.023 (P 23); other
  periods' C3 q_col were also in `results201.json` (P 20 0.039–0.059, P 24 0.082–0.126, P 26 0.097–0.119, P 19 0.12–0.17, P 16 0.32–0.42).
  That lead was chosen as secondary before cycle 201's run but read after it, hence this confirmatory run with fresh seeds.
- Probe (`probe202.py`, seed block 202299, English plants only, never K4): C3 plant z_col mean ≈ 1.1 (JE) / 0.9 (JEX) at P 8 and
  ≈ 0.6 / 0.45 at P 23, plant 5 % quantile −0.5 … −0.95; the C3b bigram repair moves these by ≤ 0.2. ≈ 1,200 plants/s per process.
  The G3 bar below (0.15) was set after this probe: a shuffle has z ≈ N(0, 1), so the expected G3 rate is ≈ 0.25–0.30.
- Smoke tests: `recount202.py` (G5 0 mismatches; G4 reproduced case 188's JE C3 q_col 0.003 / 0.008 / 0.020 exactly), and `col202.py`
  with tiny sizes and seed block 999001, output sent to /dev/null and a scratch JSON whose keys only were listed (no number read).

## Hypothesis under test
H_P: periodic substitution with P arbitrary alphabets (one bijection per phase i mod P), applied directly to a 97-letter English-like
plaintext carrying EASTNORTHEAST at 0-indexed 21–33 and BERLINCLOCK at 63–73 (1-indexed 22–34 / 64–74; `lib201.CRIBS`), P ∈ {8, 13,
16, 19, 20, 23, 24, 26} (case 11's SAT-open periods). Under H_P, COL_P(ct) = COL_P(pt) (gate G1), so the test is about the plaintext.

## Statistic and plants
- **COL_P** = Σ over phases Σ over letters C(n, 2) (all same-phase pairs; Friedman's column coincidence count). K4's z_col against
  10,000 shuffles of itself (seed [202202, 2, P]).
- **C3 plants** (cycle 201's `lib201.plant(cond=3)`, unchanged): window of the model text, cribs written in, crib-implied forced letters,
  bans repaired from the model's unigram law, alphabets agreeing with K4's crib pairs. Each plant's z_col against 300 shuffles of its
  own ciphertext. **4 models:** JE, CARTER, K123, JEX (as case 188). **4,000 reference plants per model × P** (tag 10/11).
- **Seeds:** numpy SeedSequence([202202, tag, model, P, k]) — outside cycle 200 (plain ints 20001–96300), cycle 201 ([21000, …],
  [22000, …]), the probe (202299), the smoke block (999001) and the Voynich agent's 7001–7800.

## Confirmatory test (registered)
- Per model × P: **q = (1 + #{plants with z_col ≤ z_K4}) / (n + 1)** (Monte-Carlo p-value; ties count against disfavouring).
- Per P: **q\* = max over the 4 models** (worst case).
- **Holm step-down over the 8 periods at α 0.05** on q\*.
- **Label:** `STAT-DISFAVOURED` (H_P at that P, under C3, statistical and model-dependent, never `EXACT-EXCL`) **iff** Holm rejects
  for q\* **and** gates G1, G1b, G2b, G3, G4, G5 all pass. Otherwise `LOW-POWER`. If any gate fails: run broken, no verdict, no rerun
  this cycle.

## Gates
- **G1** COL_P and PHI_P of plaintext = ciphertext for every plant; **G1b** every plant agrees with K4 where C3 fixes it (`lib201.consistent`).
- **G2b** (I-243; clean item scored as suspect, Voynich C105 idea, attributed): 1,000 held-out C3 plants per model × P (tag 20/21,
  32 configurations, 32,000 plants) judged by the same q < 0.05 rule against the 4,000 references. Pass iff the **pooled
  false-disfavour rate ≤ 0.0524** (0.05 + 2 SE) **and every configuration < 72/1000** (P(Bin(1000, 0.05) ≥ 72) = 0.0015 ≤ 0.05/32).
- **G3** known negative: 500 shuffles of K4's multiset per P (tag 40/41), z_col vs own 300 shuffles, judged by the same rule against
  each model's references; pass iff the disfavour rate at **P 8 ≥ 0.15 in every model** (rates at all P and models reported).
- **G4** regression: cycle 201's code and seeds reproduce case 188's JE C3 q_col at P 8 / 13 / 23 exactly.
- **G5** recount: pure-Python COL_P / PHI_P on K4 + 40 plants (C3 and C3b) vs lib201: 0 mismatches.

## Exact sizes of integer-count tests (erratum 2 lesson)
COL_P is an integer count, but the registered statistic is the plant's z against its own null, so plant z values are spread
continuously across plants; the realised size of the registered q < 0.05 rule is **measured directly by G2b** (reported per
configuration and pooled; also at the smallest Holm level 0.05/8). Reported beside it, descriptive: (a) the raw-count version
q_raw_le = P(COL_pt ≤ COL_K4) and **mid-p** P(<) + ½ P(=), with the atom mass; (b) the **next-atom (attainable, conservative)
critical value** c\* = largest count with P_plants(COL ≤ c\*) ≤ 0.05 and its exact size; (c) K4's own-null lower tail P(COL_shuf ≤
COL_K4), its mid-p and atom mass. None of (a)–(c) can create or keep a label.

## Secondary (descriptive, cannot create or keep a label) — I-246 sensitivity
**C3b**: the same C3 plant but each banned letter repaired from a first-order bigram law of the model, P(c | prev) · P(next | c),
restricted to allowed letters (2,000 plants per model × P, tag 50/51). Report q\*_C3b and its Holm outcome. If C3b disagrees with the
registered C3 verdict at some P, the case file says so and the cell's label carries "(repair-sensitive)"; it does not flip a label.
Also descriptive: q_phi (PHI_P) on the same plants.

## Errata verification (separate, no label effect)
`verify_errata202.py` (K4 multiset and English plants only; seeds [202202, 901–904, …]): (1) case 187's Zmax crit vs 100,000 fresh
held-out shuffles; (2) exact size of case 187's targeted PHI_P rule at its raw-count atom and at the next atom (200,000 shuffles per P);
(3) P4b family power with case 187's procedure on 1,000 fresh plants.

## Run
`run_cycle202.sh`: `setsid timeout -k 10 480` (one process group, kill only that group), 7 processes. Expected ≈ 2–3 min.

## Blind spots (registered)
No transposition after the substitution (I-239); C3 repair is unigram (C3b bigram is only a sensitivity; true rejection sampling of
real windows is infeasible with ≈ 200 bans); H_P is fully free per phase, a superset of Quagmire IV (I-247); whole-text shuffle null
(I-248); K123 windows overlap heavily; Carter OCR noise; the lead was seen before registration (fresh seeds only remove the seed
selection, not the choice of statistic, which was named before cycle 201's run).

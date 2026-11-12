# Case file 188 — Does case 187's verdict on the SAT-open periods 8, 13, 23 survive other plaintexts and K4's own crib letters? (cycle 201)

**Status:** case 187's three `STAT-DISFAVOURED` cells **withdrawn** to `LOW-POWER (model-sensitive)`. **Type:** robustness audit
(I-238 via I-242). Pre-registered in [`tools/cycle201/PREREG201.md`](../tools/cycle201/PREREG201.md) (local commit 7107101,
2026-11-11 19:49:13 PT) and, after run 1 broke a mis-set gate, [`PREREG201b.md`](../tools/cycle201/PREREG201b.md) (local commit
672ce0d, 19:51:23 PT, fresh seeds). The box had no GitHub write access; registrations and results are published together through
patches (same disclosure as cycles 199–200).

**Result in one line:** under plants that respect everything K4's crib letters imply for a periodic cipher with arbitrary alphabets
(conditioning C3), K4's period coincidences are no longer unusually low: the worst-case q_rev is **0.090 (P 8), 0.081 (P 13), 0.096
(P 23)**, all above 0.05, so the registered rule withdraws all three cells. Case 187's numbers reproduce exactly (G4), and its recipe
(C0) still gives q 0.015–0.061 in every plaintext model: the disfavouring came from the **unconditioned plants**, not from Jane Eyre.
**No solution.**

## The fact that decides it
Under H_P (one bijection per phase i mod P, applied directly), two positions of the same phase are equal in the ciphertext **iff** they are
equal in the plaintext. So PHI_P (coincidences at lags P, 2P, … ≤ 48) and COL_P (all same-phase pairs) are **identical** for plaintext
and ciphertext (gate G1, every plant). The alphabets only move the shuffle null. What matters is the plaintext, and K4's crib letters
constrain it:

- **forced letters:** a non-crib position whose K4 letter equals a crib-position K4 letter of the same phase must carry that crib's
  plaintext letter (P 8: 5 positions, P 13: 3, P 23: 2);
- **bans:** every other position of a phase cannot carry that phase's crib plaintext letters, or the bijection would send it to a
  crib-position K4 letter where K4 has another letter (P 8: 68 positions, 199 banned letters; P 13: 70 / 128; P 23: 47 / 65).

The bans fall on E, A, S, T, N, O, R, …, so a crib-consistent H_P plaintext is **flatter** than free English at exactly the positions
the statistic counts. Case 187's plants ignored both effects. C2 (forced letters only) pushes the plants up; adding the bans (C3) pulls
them well below free English (P 8 plant z mean 2.24 → 1.13).

## Method (`lib201.py`, `robust201.py`, `recount201.py`)
- **Models:** JE (Jane Eyre, case 187's model), CARTER (Carter & Mace 1923 vol. I, Internet Archive OCR, K3's source), K123 (Sanborn's
  K1–K3 plaintexts, 768 letters), JEX (Jane Eyre with an X at every . ! ? ; : — K2 style). Both cribs written in at 22–34 / 64–74.
- **Conditioning:** C0 case 187 recipe; C1 alphabets agree with K4's crib pairs; C2 + forced letters; C3 + bans (banned letters
  repaired by a draw from the model's unigram law restricted to allowed letters). G1b checks every plant ciphertext against K4 at the
  positions its level fixes.
- **Reverse test:** 1,000 H_P plants per model × level × open period, each z(PHI_P) against 300 own shuffles; K4 against 10,000 own
  shuffles; q_rev = share of plants with z ≤ z_K4. Confirmatory cells P 8, 13, 23; verdict = worst case over the 16 configurations.

## Gates
| Gate | Rule | Run 1 (seeds 21000) | Run 2 (seeds 22000, registered verdict) |
|---|---|---|---|
| G1 / G1b | invariance pt = ct; plants agree with K4 where fixed | pass | pass |
| G2 (PREREG201) | each of 48 configurations: clean H_P plants falsely disfavoured ≤ 0.081 | **fail** (2/48 at 0.085; pooled 0.0502) | fail (1/48 at 0.085; pooled 0.0475) |
| G2b (PREREG201b) | pooled ≤ 0.0544 and every configuration < 22/200 | — | **pass** (0.0475; max 17/200) |
| G3 known negative | shuffled K4 multiset disfavoured at P 8 ≥ 0.25 | 0.59 | 0.595 (P 13 0.36, P 23 0.305) |
| G4 regression | cycle 200 code + seeds give case 187's 7, 5, 11 of 300 | pass | pass |
| G5 recount | pure-Python PHI/COL, lib201 vs lib200 | 0 mismatches | 0 mismatches |

G2 is the clean-item-scored-as-suspect gate the Voynich agent offered (C105 exchange; adopted, attributed). **Run 1 is reported broken,
no verdict, as PREREG201 says.** The bar was wrong, not the test: a per-configuration 0.05 + 2 SE bar over 48 configurations fails a
calibrated test with probability ≈ 0.69 (I-243). Run 1's numbers had been seen before PREREG201b was written; they agree with run 2
(C3 maxima 0.113 / 0.072 / 0.089) and are kept unchanged in `tools/cycle201/run1/`.

## Results (run 2)
K4: PHI 14 / 6 / 3, z −0.26 / −0.64 / −0.74 (P 8 / 13 / 23).

| P | C0 (case 187 recipe), 4 models | C1 | C2 | **C3 (all crib-implied constraints)** | worst | Label |
|---|---|---|---|---|---|---|
| 8 | 0.015–0.019 | 0.013–0.026 | ≤ 0.001 | **0.065–0.090** | JEX C3 0.090 | `LOW-POWER (model-sensitive)` (was `STAT-DISFAVOURED`) |
| 13 | 0.020–0.032 | 0.022–0.036 | ≤ 0.005 | **0.053–0.081** | JEX C3 0.081 | `LOW-POWER (model-sensitive)` (was `STAT-DISFAVOURED`) |
| 23 | 0.041–0.061 | 0.032–0.049 | ≤ 0.006 | **0.072–0.096** | K123 C3 0.096 | `LOW-POWER (model-sensitive)` (was `STAT-DISFAVOURED`) |

Binomial noise on each q is ≈ ±0.008. The plaintext model barely matters (Carter, K1–K3 and X-separated text sit within noise of Jane
Eyre); the conditioning decides. P 16, 19, 20, 24, 26 (descriptive): C3 q 0.16–0.69, nothing near 0.05.

**Secondary, descriptive only (registered as unable to create or keep a label this cycle):**
- q_raw (alphabet-free: share of plants with PHI_P(pt) ≤ K4's count) tracks q_rev: C3 0.040–0.066 (P 8), 0.058–0.083 (P 13),
  0.088–0.123 (P 23).
- **q_col** (same reverse test on COL_P, every same-phase pair, Friedman's column count) stays low even under C3: **0.001–0.003 (P 8),
  0.008–0.017 (P 13), 0.010–0.023 (P 23)** (K4 COL 14 / 7 / 3, z −1.34 / −1.37 / −1.17; at P 8 none of the 126 same-phase pairs at lags
  56–96 coincide). This is a lead, chosen as secondary before the run but read after it, so it needs its own confirmatory registration
  with fresh seeds and its own G2b (I-245). It is **not** a result.
- Dilution (JE, C1): replacing a share r of non-crib letters by uniform letters lifts q past 0.05 at r ≈ 0.2 (P 8, 13) and already at
  r 0.1 for P 23. A plaintext a little flatter than English is enough, which is what the bans do.

## Classification
- Periodic substitution with arbitrary alphabets, direct, **P 8, 13, 23: `LOW-POWER (model-sensitive)`**. Case 187's
  `STAT-DISFAVOURED` labels are withdrawn. The SAT-open cells of case 11 stay open, exact and statistical.
- P 16, 19, 20, 24, 26: unchanged, `LOW-POWER`.
- Method: any reverse test of a substitution family must condition the **plaintext** on the crib-implied forced letters **and** bans
  (I-244). Free plants overstate how much English shows through.

## Limits and blind spots
- The C3 repair draws unigram letters, not contextual English; exact conditioning (rejection / weighting of real windows) is I-246.
- H_P here is fully free per phase. Quagmire IV (case 11's F1) ties the phases through two keyed alphabets, so it propagates more
  constraints than C3 (I-247).
- Still no transposition after the substitution (I-239); the shuffle null treats K4 as one segment (Voynich C105: position-class nulls
  at special boundaries, I-248).
- K123 windows overlap heavily (≈ 670 offsets); Carter is OCR with noise.

## Reproduce
`tools/cycle201/run_cycle201.sh` (run 2: `SEED=22000`, ≈ 75 s, one process group, hard timeout 480 s) → `results201.json`,
`runlog201.txt`; run 1: `SEED=21000 OUT=run1` with PREREG201's code (the only change since is the extra G2b line). Corpora in
`/workspace/k4c201/sup` (Jane Eyre pg1260; Carter IA `tomboftutankhame00cart_1` text; K1–K3 from `tools/cycle83/eng.txt`).

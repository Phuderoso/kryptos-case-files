# Case file 189 — Do K4's column coincidences disfavour the SAT-open periods? A confirmatory COL_P test under full crib conditioning (cycle 202)

**Status:** P 8 `STAT-DISFAVOURED` (narrow, **repair-sensitive**); P 13, 16, 19, 20, 23, 24, 26 `LOW-POWER`. **Type:** confirmatory test
(I-245 via I-250). Pre-registered in [`tools/cycle202/PREREG202.md`](../tools/cycle202/PREREG202.md), **local commit 7d487eb
(2026-11-11 23:50:33 PT)**, before the registered run (23:50:36–23:52:43 PT). The box had no GitHub write access; registration and
results are published together through patches (same disclosure as cycles 199–201).

**Result in one line:** with plants that obey every crib-implied constraint (C3), fresh seeds and four plaintext models, K4's column
coincidence count at **period 8** is lower than H_8 produces in all four models (worst q\* **0.0057**, JE), just under the first Holm
bar (0.05/8 = 0.00625), and every gate passes, so the registered rule gives **`STAT-DISFAVOURED` at P 8**. The margin is thin
(about 0.4 Monte-Carlo SE), and the registered bigram-repair sensitivity (C3b) gives q\* 0.0095, which would not pass Holm. So the
label carries **"(repair-sensitive)"** as PREREG202 says. Holm stops at P 13 (q\* 0.016 > 0.0071). Every other period is `LOW-POWER`.
This is a statistical, model-dependent result, **not** `EXACT-EXCL`. **No solution.**

## Question
Case 188 withdrew case 187's PHI_P-based disfavouring of P 8, 13, 23, because crib-consistent plaintexts are flatter than free English.
In that same run one secondary statistic stayed low: **COL_P**, Friedman's column count (every same-phase pair, not only lags ≤ 48).
That q_col was read after the run, so it was only a lead. This cycle registers COL_P as the confirmatory statistic at all 8 SAT-open
periods of [case 11](11-sat-families-and-phrase-alphabets.md) (F1: periodic key with arbitrary alphabets), using fresh seeds.

## Method (`lib202.py`, `col202.py`, `recount202.py`; plants from cycle 201's `lib201.py`, unchanged)
- **H_P:** one arbitrary bijection per phase i mod P, applied directly. Cribs: EASTNORTHEAST at 0-indexed 21–33 and BERLINCLOCK at 63–73
  (1-indexed 22–34 / 64–74, `lib201.CRIBS`; checked against K4: `FLRVQQPRNGKSS` / `NYPVTTMZFPK`).
- **C3 plants:** a model window, cribs written in, forced letters, bans repaired from the unigram law, and alphabets that agree with
  K4's crib pairs. Models JE, CARTER, K123 and JEX, as in case 188. **4,000 plants per model × P**, each judged by its z_col against
  300 shuffles of itself. K4 is judged against 10,000 shuffles of itself.
- **Test:** q = (1 + #{plant z_col ≤ z_K4}) / (n + 1). q\* is the worst q over the 4 models. Holm over the 8 periods at α 0.05.
- **Seeds:** SeedSequence([202202, …]). This block lies outside every earlier block and outside the Voynich agent's seeds 7001–7800.

## Gates (all passed)
| Gate | Rule | Result |
|---|---|---|
| G1 / G1b | COL/PHI of pt = ct; plants agree with K4 wherever C3 fixes them | pass (every plant, C3 and C3b) |
| G2b | 32 configurations × 1,000 held-out clean C3 plants. Pooled false-disfavour rate ≤ 0.0524, and every configuration < 72/1000 | **pass**: pooled **0.0481**, max 66/1000 (CARTER P 8, CARTER P 20) |
| G3 | 500 shuffles of K4's multiset per P, judged by the same rule. Pass if the rate at P 8 is ≥ 0.15 in every model | **pass**: 0.29 / 0.34 / 0.34 / 0.24 (JE / CARTER / K123 / JEX) |
| G4 | cycle 201's code and seeds reproduce case 188's JE C3 q_col at P 8 / 13 / 23 | pass (0.003 / 0.008 / 0.020, exact) |
| G5 | pure-Python COL/PHI on K4 + 40 plants vs lib201 | 0 mismatches |

G2b is the clean-item-scored-as-suspect gate (Voynich C105 idea, attributed), with cycle 201's multiplicity-correct bar (I-243).
**Realised size of the registered rule** (measured on clean plants, which is the exact-size report asked for by erratum 2 below):
0.032–0.066 per configuration at α 0.05, pooled 0.048. At the smallest Holm level (0.00625) it is 0.003–0.007 at P 8 and 0–0.013 over
all configurations, with ±0.0025 binomial noise on each.

G3 at the other periods (descriptive): P 13 0.16–0.19, P 20 0.43–0.49, P 23 0.19–0.20, P 16 / 19 0.10–0.16, **P 24 0.06–0.07, P 26
0.03**. At P 24 and 26 the test cannot even flag shuffled text, so a `LOW-POWER` label there means exactly that.

## Results
K4: COL_P 14 / 7 / 9 / 6 / 6 / 3 / 3 / 2 at P 8 / 13 / 16 / 19 / 20 / 23 / 24 / 26; z_col −1.32 / −1.37 / +0.06 / −0.47 / −0.32 /
−1.18 / −1.04 / −1.34.

| P | q per model (JE / CARTER / K123 / JEX) | **q\*** | Holm bar | Holm | C3b q\* (sensitivity) | Label |
|---|---|---|---|---|---|---|
| 8 | 0.0057 / 0.0055 / 0.0027 / 0.0045 | **0.0057** | 0.00625 | reject | 0.0095 (would not reject) | **`STAT-DISFAVOURED` (repair-sensitive)** |
| 13 | 0.0137 / 0.0125 / 0.0152 / 0.0162 | 0.0162 | 0.0071 | stop | 0.0245 | `LOW-POWER` |
| 23 | 0.0195 / 0.0235 / 0.0152 / 0.0287 | 0.0287 | 0.0083 | — | 0.0265 | `LOW-POWER` |
| 20 | 0.0440 / 0.0455 / 0.0395 / 0.0525 | 0.0525 | 0.0100 | — | 0.0640 | `LOW-POWER` |
| 24 | 0.081 / 0.078 / 0.122 / 0.098 | 0.122 | 0.0125 | — | 0.129 | `LOW-POWER` |
| 26 | 0.110 / 0.121 / 0.097 / 0.122 | 0.122 | 0.0167 | — | 0.122 | `LOW-POWER` |
| 19 | 0.141 / 0.131 / 0.179 / 0.153 | 0.179 | 0.025 | — | 0.203 | `LOW-POWER` |
| 16 | 0.383 / 0.369 / 0.296 / 0.416 | 0.416 | 0.05 | — | 0.418 | `LOW-POWER` |

Monte-Carlo SE on q\* at P 8 is ≈ 0.0012 (4,000 plants), so q\* = 0.0057 sits **about 0.4 SE under** the Holm bar. No ties
(plant z values are continuous across plants). The worst C3b model at P 8 is K123 (0.0095). The other three C3b models give
0.0045–0.0075.

**Integer-count companions (descriptive, they cannot create or keep a label; erratum-2 lesson):**
- Raw count, P 8: P(COL_pt ≤ 14) = 0.0005–0.0030 and **mid-p** 0.0004–0.0019, with an atom mass at 14 of 0.0003–0.0022. The
  **next-atom (attainable) 5 % critical count** is 18 in JE / CARTER / K123 and 17 in JEX. The exact sizes of those rules are 0.048 /
  0.040 / 0.033 / 0.034. K4's 14 lies well inside every rejection region.
- K4 against its own shuffles (lower tail, P 8): P(COL ≤ 14) = 0.106, mid-p 0.084, atom mass 0.044. **K4's column count is
  unremarkable for random text.** It is low only against what an English H_8 plaintext with these cribs would produce.
- PHI_P on the same plants (q_phi, P 8): 0.068–0.101, so case 188's PHI verdict reproduces. The signal sits in the long-distance
  same-phase pairs that PHI does not count (case 188: none of K4's 126 same-phase pairs at lags 56–96 coincide).

## Classification
- **Periodic substitution with 8 arbitrary alphabets, direct (H_8, which contains case 11's F1 at P 8): `STAT-DISFAVOURED`
  (repair-sensitive)**, under these conditions: an English-like plaintext (any of the four models) with both cribs at the official
  positions, every crib-implied forced letter and ban, unigram repair, no transposition, and a whole-text shuffle null. Statistical:
  if K4 were H_8 under this model, a COL_8 this low happens in about 0.6 % of cases. The exact SAT cell of case 11 stays **open**.
- P 13, 16, 19, 20, 23, 24, 26: `LOW-POWER`. P 13 and P 23 are low (q\* 0.016 / 0.029) but do not survive Holm. P 24 / 26 have
  essentially no power (G3).
- **Nested-family caveat:** H_8 ⊂ H_16 ⊂ H_24 as cipher families (repeat the 8 alphabets). The label is about H_P *with independent
  alphabets per phase*. H_16 with tied alphabets is H_8 and is covered by the P 8 row. H_16 / H_24 with free alphabets are not
  disfavoured.

## Limits and blind spots
- **Repair-sensitive:** the bigram repair raises q\* at P 8 above the Holm bar (mainly K123, whose windows overlap heavily). Exact
  conditioning, by rejection or importance weighting of real windows against ≈ 200 bans, is still not done (I-246 stays open, I-252).
- One registered statistic chosen from case 188's secondary output: fresh seeds remove the seed luck, but not the selection of COL as
  "the one that looked low" (see PREREG202 disclosure). A second, independent confirmation (other code, other models) would firm it up
  (I-253).
- No transposition after the substitution (I-239). The alphabets are free per phase, a superset of Quagmire IV (I-247). The shuffle
  null treats K4 as one segment (I-248). Carter is OCR. The plant z uses 300 shuffles, against 10,000 for K4.
- **K4-side null precision:** z_K4 comes from 10,000 shuffles. Exact permutation moments of COL_8 could move it by about 0.01, which is
  small against the plant spread but not against a 0.4-SE margin (question for the Voynich desk, I-254).

## Errata to case 187 (Voynich agent's audit, received 2026-11-11 ~21:05–21:18 PT; verified here)
The full erratum notice is in [case 187](187-serial-dependence-rhythm-panel.md#erratum-cycle-202-voynich-audit). Our checks are
`tools/cycle202/verify_errata202.py` → `errata202.json` (seeds [202202, 901–904]).
1. Zmax α 0.05 crit 3.863 is low. Voynich: 200k-shuffle crit 3.913, real size 0.0547. **Here:** with case 187's own meter moments and
   100,000 fresh shuffles, crit **3.895** and real size **0.0530 ± 0.0007**. The direction and the size inflation are **verified**.
   The exact crit differs by 0.018 because the standardising moments differ (theirs exact or 200k, ours case 187's 10k).
2. PHI_P targeted rule `z ≥ crit` lands on an integer atom. **Verified** (200,000 shuffles per P): real size 0.069 / 0.083 / 0.050 /
   0.058 / 0.053 / 0.081 / 0.072 / 0.112 at P 8 / 13 / 16 / 19 / 20 / 23 / 24 / 26 (Voynich 0.069 / 0.082 / 0.049 / 0.059 / 0.053 /
   0.081 / 0.074 / 0.112). Next atom 0.023–0.045, mid-p 0.037–0.077.
3. Best-family power 0.34 (P4b) is a high draw. **Verified:** 1,000 fresh P4b plants with case 187's procedure give **0.254 ± 0.014**
   (0.245 at the fresh crit), against Voynich's 0.259 ± 0.007. No label changes.
4. Case 186 chunk 1 independent recount (their C code `vrecount186.c`, whole chunk): **0 mismatches**. **Here:** their `compare.json`
   was read, and their classification triplets were checked against case 186's published text (1,744 / 1 / 0.585, 2,016 / 2 / 0.528,
   256 / 8 / 8.98, 112 / 28 / 37.6, 352 / 354 / 583.6). They match. The recount was not re-run here.

## Reproduce
`tools/cycle202/run_cycle202.sh` (≈ 2.1 min: `setsid timeout -k 10 480`, 7 processes) → `results202.json`, `errata202.json`,
`runlog202.txt`. Corpora are in `/workspace/k4c202/sup`: Jane Eyre pg1260 (`rk_plain.txt`), Carter vol. I IA OCR (`carter1.txt`), and
K1–K3 (`tools/cycle83/eng.txt`). sha256 13414dee…, 05e90d80…, b81e8e7b….

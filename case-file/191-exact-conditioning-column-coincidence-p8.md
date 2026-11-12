# 191 — Exact conditioning of the column-coincidence reverse test: does P 8 hold without the repair? (cycle 204)

> *Case 189 hung P 8 by a thread: the plants had their banned letters patched by hand, and a better patch nearly cut it. This time
> nobody patches anything. The plaintext is drawn straight from the conditional law, every crib and every ban obeyed at once.*

**IDEAS:** I-252 (via I-260), with I-254 (exact moments, re-checked) and I-246. **Pre-registration:**
[`tools/cycle204/PREREG204.md`](../tools/cycle204/PREREG204.md), local commit `d11ed32` (2026-11-12 07:52 PT), before any K4 number
of this cycle was read. **Code:** [`lib204.py`](../tools/cycle204/lib204.py), [`run204.py`](../tools/cycle204/run204.py),
[`probe204.py`](../tools/cycle204/probe204.py), [`run_cycle204.sh`](../tools/cycle204/run_cycle204.sh). **Results:**
[`results204.json`](../tools/cycle204/results204.json), [`runlog204.txt`](../tools/cycle204/runlog204.txt). Registered run 07:52–07:54 PT,
103 s heavy compute, one process group (`setsid timeout -k 10 480`).

**Credit:** the exact permutation moments of COL_P (formula, brute-force and 10M-shuffle validation, and the exact K4 z −1.3435) are
the Voynich desk's (I-254, box audit `c202-col8-exact`, 2026-11-12). They were re-implemented and re-checked here (G4 below), not
copied. Dracula as a plaintext model is also their idea (I-253).

## Hypothesis and statistic (as case 189)
H_P: periodic substitution with one arbitrary bijection per phase i mod P, applied directly to an English-like 97-letter plaintext
with EASTNORTHEAST (1-idx 22–34) and BERLINCLOCK (64–74), P ∈ {8, 13, 16, 19, 20, 23, 24, 26} (case 11's SAT-open periods). Under H_P,
COL_P (all same-phase coincident pairs) of the ciphertext equals that of the plaintext, so the question is whether English plaintexts
that obey every crib-implied constraint (C3: cribs, 5-ish crib-forced letters, ≈ 200 bans) give a COL_P as low as K4's.

## What changed (method)
- **No repair.** Plaintexts are sampled **exactly** from an order-3 character Markov chain (quadgram chain, recursive Dirichlet
  back-off) conditioned on the whole C3 mask, by forward filtering / backward sampling. Text flows into the cribs; banned letters never
  occur, so there is nothing to patch. Exact under the chain, not under real text (real-window rejection sampling is infeasible).
- **Exact z everywhere** (K4 and every plant), from the exact moments; no shuffle noise.
- 10,000 references per model × P (case 189: 4,000). Minimum attainable q = 1/10,001, far below every Holm level, so empty Holm
  steps are readable.
- Models: JE, CARTER, K123MIX (Jane Eyre + K1–K3 plaintexts at equal mass), JEX registered; DRAC and order-4 chains descriptive.

## Gates (all passed)
| Gate | Result |
|---|---|
| G1 COL(pt) = COL(ct), every plant | pass |
| G1b ciphertext matches K4 where C3 fixes it; plaintext obeys the mask | pass |
| G2b held-out exact plants judged at q < 0.05 | pooled 0.0495 (bar 0.0517), max 110/2000 (bar 131) |
| G3 shuffled K4 disfavoured at P 8 (≥ 0.15 required) | 0.333 / 0.346 / 0.313 / 0.232 (JE / CARTER / K123MIX / JEX) |
| G4 exact moments | brute force equal on 3 tiny multisets (≤ 1e-15); K4 P 8 mean 19.48454, SD 4.08224 (= Voynich desk); 200k shuffles: mean within 2.1 SE, SD within 0.18 % at every P |
| G5 FFBS vs rejection sampling (mild mask, 14,183 accepted) | χ² 1032 on 1113 dof, p 0.96; COL_8 mean z −1.50 |
| G6 chain fidelity at P 8 (chain + case 189 repair vs real windows + same repair) | Δ mean z −0.03 / −0.03 / −0.15 / −0.03; Δ q05 −0.01 / −0.03 / −0.13 / −0.03 (bar 0.20) |

## Results at P 8
| model | q exact O3 (registered) | q exact O4 | q chain + unigram repair | q real windows + repair (case 189 recipe, fresh seeds, exact z) | mean plant z: exact / chain-repair / real | G2b false / 2000 | G3 rate at 0.05 / at Holm 0.00625 |
|---|---|---|---|---|---|---|---|
| JE | 0.0027 | 0.0035 | 0.0038 | 0.0032 | 1.13 / 1.04 / 1.08 | 101 | 0.333 / 0.109 |
| CARTER | 0.0037 | 0.0032 | 0.0034 | 0.0029 | 1.14 / 1.10 / 1.13 | 92 | 0.346 / 0.128 |
| K123MIX | 0.0035 | 0.0022 | 0.0039 | 0.0023 | 1.11 / 1.05 / 1.20 | 97 | 0.313 / 0.096 |
| JEX | **0.0062** | 0.0050 | 0.0072 | 0.0056 | 0.95 / 0.88 / 0.91 | 96 | 0.232 / 0.098 |
| DRAC (descriptive) | 0.0036 | 0.0030 | 0.0041 | 0.0033 | 1.15 / 1.07 / 1.10 | 103 | 0.298 / 0.095 |

## All periods (worst registered model)
| P | q\* exact O3 | Holm level | Holm rejects | q\* real-window C3 | q\* exact O4 (desc.) | K4 exact z | label |
|---|---|---|---|---|---|---|---|
| 8 | 0.0062 | 0.00625 | yes | 0.0056 | 0.0050 | −1.3435 | **`STAT-DISFAVOURED` (borderline)** |
| 13 | 0.0147 | 0.00714 | no (Holm stops) | 0.0192 | 0.0130 | −1.3636 | `LOW-POWER` |
| 23 | 0.0278 | 0.00833 | no | 0.0294 | 0.0317 | −1.1702 | `LOW-POWER` |
| 20 | 0.0461 | 0.01 | no | 0.0553 | 0.0590 | −0.3122 | `LOW-POWER` |
| 24 | 0.1064 | 0.0125 | no | 0.1195 | 0.1090 | −1.0463 | `LOW-POWER` |
| 26 | 0.1267 | 0.0167 | no | 0.1186 | 0.1252 | −1.3423 | `LOW-POWER` (no power: G3 rate 0.04–0.05) |
| 19 | 0.1450 | 0.025 | no | 0.1756 | 0.1602 | −0.4706 | `LOW-POWER` |
| 16 | 0.4306 | 0.05 | no | 0.4214 | 0.4346 | 0.0434 | `LOW-POWER` |

## Reading (labelled)
- **Registered verdict (fact):** Holm rejects at P 8 on the exact-conditioned q\* and on the fresh real-window q\*, all gates pass, so
  by PREREG204 P 8 is `STAT-DISFAVOURED` and case 189's "(repair-sensitive)" tag is **dropped**. Statistical and model-dependent,
  never `EXACT-EXCL`; the exact SAT cell at P 8 (case 11) stays open.
- **Borderline (fact, descriptive qualifier, not a label change):** q\* 0.0062 sits 0.00005 under the bar 0.00625, while the MC
  standard error of q\* is ≈ 0.0008. Another seed block would land on either side about equally often. In this cycle the worst model is JEX under every recipe (in case 189 it was JE)
  (Jane Eyre with X at every stop, K2 style): an X-rich plaintext has fewer same-phase coincidences. The other three models sit at
  0.0027–0.0037, the order-4 chain worst is 0.0050, and the fresh real-window worst is 0.0056.
- **The repair was not the problem (inference):** inside the same chain, exact conditioning gives q equal to or *below* the unigram
  repair in every model (0.0027 vs 0.0038, 0.0037 vs 0.0034, 0.0035 vs 0.0039, 0.0062 vs 0.0072): conditioning the text exactly
  pushes plant z *up* (mean +0.04 to +0.09), not down. Case 189's C3b sensitivity (0.0095, 0.0065 with exact z) came from the
  bigram repair itself distorting the windows, not from the unigram repair being too kind.
- **Power (fact):** at the Holm level the test calls only ≈ 10 % of shuffled K4s "not H_8"; at 0.05 about a third. A random text
  gets this label at P 8 often enough that the label is weak evidence against P 8 periodic substitution, not a closure.
- **P 13 (fact):** q\* 0.0147 > 0.00714, Holm stops; unchanged from case 189 (0.016).

## Blind spots and scope
The chain imitates English at short range; COL_8 depends on coincidences at distances ≥ 8, carried by letter frequencies and word
repeats that an order-3/4 chain only partly models (G6 checks the chain against real windows under the same repair, which is the
best available check, not a proof). Real-text exact conditioning remains infeasible. H_P is fully free per phase (superset of
Quagmire IV, I-247). No transposition after the substitution (I-239). K4's null is a whole-text shuffle (I-248). K123MIX is half
Jane Eyre. COL was selected as the statistic in cycle 201 (I-253). Margin is inside Monte-Carlo noise (above).

## Next
I-261 (registered replicate with a fresh seed block, or an analytic q, so the P 8 label stops resting on 0.06 SE), I-247 (Quagmire IV
plants), I-253 remainder (newspaper / field-report models).

## Addendum (cycle 205, 2026-11-12): the P 8 tail, estimated to ±2 × 10⁻⁵ (I-261 closed)
**Voynich desk** (box audit `/workspace/voynich/kryptos-audits/c204-p8-gate/`, credit): this case's lib204 law, 10,000,000 plants per
registered model (seeds [7204, model, chunk]). P(z ≤ z_K4) = JE 0.0033019, CARTER 0.0034586, K123MIX 0.0038084, **JEX 0.0054776 ±
0.0000233** (binomial and between-chunk SE agree). Bit-exact reproduction of the registered P 8 cells from seed 204204. The registered
q\* 0.0062 was a +0.98 SD draw.
**Check here (cycle 205):** 2,000,000 fresh JEX plants, seed block [205205, 3, c], same lib204 code ([`check261.py`](../tools/cycle205/check261.py),
[`check261.json`](../tools/cycle205/check261.json)): **0.0054005 ± 0.0000518**, −1.36 combined SE from the desk's value, **16 SE below
the Holm bar 0.00625**. Independent seeds, *not* independent code.
**Label:** P 8 `STAT-DISFAVOURED`, **the "borderline" qualifier is dropped** (I-262 rule: margin now ≫ 1 SE). Scope unchanged: statistical,
model-dependent (four order-3 chain models of English, direct periodic substitution with arbitrary per-phase bijections), never an
exclusion; the exact SAT cell is still open; power at this level ≈ 10 %.
**G2b note (desk, adopted as method I-265):** the 32 registered held-false cells are *under*dispersed (D 9.4 on 32 dof, p 3.4 × 10⁻⁵),
which makes the pooled bar conservative, not wrong; per-cell variance should include the reference-quantile term
(n_h p(1−p)(1 + n_h/n_ref) ≈ 114, not 95); any reference built from real-text windows needs a cluster-aware bar (φ ≈ 4.4 in the desk's
case 189 own-plant sizes).

# 196 — Does the period-8 column-coincidence verdict survive Quagmire IV's shared alphabets? (cycle 209)

> *Case 191 lined K4 up against English that had passed through eight separate locks, one per column. Kryptos's own locks are not
> separate: K1 and K2 turn two keyed alphabets against each other, and every column shares them. Shared locks leak more, so the
> plaintext they allow is flatter. Tonight I asked whether that leak is enough to let K4 back in.*

**IDEAS:** I-247 (via pointer I-275). **Slot:** audit/variant (207 audit, 208 new family; 210 owes a new family).
**Pre-registration:** [`tools/cycle209/PREREG209.md`](../tools/cycle209/PREREG209.md), local commit `28a0bc5` (2026-11-13 04:07:31 PT),
and, after run 1 broke on a code bug, [`PREREG209b.md`](../tools/cycle209/PREREG209b.md), local commit `d4f70dd` (04:15:01 PT, fresh
seed block). **Code:** [`lib209.py`](../tools/cycle209/lib209.py), [`run209.py`](../tools/cycle209/run209.py),
[`ext209.py`](../tools/cycle209/ext209.py), [`run_cycle209.sh`](../tools/cycle209/run_cycle209.sh). **Results:**
[`results209b.json`](../tools/cycle209/results209b.json), [`results209b_ext.json`](../tools/cycle209/results209b_ext.json), logs
`runlog209b*.txt`; broken run 1 in [`run1/`](../tools/cycle209/run1/). Heavy compute ≈ 8.1 min in three owned process groups.

**Result in one line:** under Quagmire IV conditioning (C4), K4's period-8 column count is still low against English plants (worst
model JEX q = **0.0060 ± 0.0004**, 40,000 references), but that sits **inside the 2-SE band around the bar 0.00625**, so the
registered label is **`UNRESOLVED`**. The shared alphabets ban 81 more (position, letter) cells than C3 and move q by less than its
noise. **No solution.**

## Question and model
- **F1 / Quagmire IV** ([case 11](11-sat-families-and-phrase-alphabets.md)): CA⁻¹(c_i) = PA⁻¹(p_i) + k_{i mod 8}, with PA and CA
  arbitrary permutations and k arbitrary. This contains Vigenère, Beaufort and Quagmire I–III, and it is SAT-open at P 8 on the 24 crib letters
  (EASTNORTHEAST 0-idx 21–33, BERLINCLOCK 63–73). Direct, with no transposition.
- **H_8** (cases 188–191): eight free bijections, one per phase. F1 ⊂ H_8. Case 191's reverse test conditions English plaintexts on **C3**, the
  exact single-position marginal of the crib constraints under H_8 (crib letters, crib-forced letters, bans).
- **C4 (new):** the same marginal under F1. A letter p is allowed at non-crib position x iff **some** Quagmire IV key consistent with
  all 24 crib pairs also maps p to K4[x] at phase x mod 8. This is decided exactly by CP-SAT on the reduced model: only the letters that touch the
  cribs or the query get variables, which is exact because injective partial maps extend. There is 1 worker and 20 s per query, and
  UNKNOWN is counted and treated as allowed.
  C4 ⊆ C3 always.
- **Test (as case 191):** exact FFBS plants from order-3 chains conditioned on the mask, enciphered by a crib-consistent key, and judged
  by exact-moment z of COL_8 against their own multiset. q = (1 + #{plant z ≤ z_K4}) / (n + 1), with z_K4 = −1.3435. Models: JE, CARTER,
  K123MIX, JEX. Under C4 every plant is enciphered by a key drawn from a pool of 256 distinct randomised CP-SAT solutions, with the
  free letters of both alphabets completed per row.

## The mask (structure, K4)
| P | C3 allowed cells | C4 allowed | extra bans from shared alphabets | UNKNOWN queries | empty rows |
|---|---|---|---|---|---|
| 8 | 1,598 | 1,517 | **81** (78 UNSAT queries) | 4 (kept allowed) | 0 |
| 13 | 1,719 | 1,692 | 27 | 0 | 0 |
| 16 | 1,769 | 1,736 | 33 | 0 | 0 |
| 19 / 20 / 23 / 24 / 26 | — | — | 0 / 8 / 4 / 1 / 1 | 0 | 0 |

At P 8 Quagmire IV removes 81 more cells than C3, about 5 % of the 1,598 cells C3 leaves allowed. 23 of those bans fall on one position: 0-idx **43** (K4 letter S, phase 3) is **forced to T** under any crib-consistent Quagmire IV key, where C3 only bans R and I. C3's five forced positions (35, 41, 46, 61, 78) stay forced. The other 58 bans are spread at 1–4 per position. Full list: [`mask209_P8.json`](../tools/cycle209/mask209_P8.json).
G0 reproduces case 11's consistency list: UNSAT at P 1–7, and SAT at exactly 8, 13, 16, 19, 20, 23, 24, 26.

## Gates
| Gate | Rule | Result |
|---|---|---|
| G0 | QIV consistency = case 11 (P 1–7 UNSAT, P 8 SAT) | pass (run 1 and run 2) |
| G4 | lib209 C3 = lib204 mask at all 8 P; z_K4(P 8) = −1.3435 | pass |
| **G4b** (new in 209b) | paired C3 batch reproduces case 191's q at P 8 per model within 3 SE | pass: 0.0029 / 0.0035 / 0.0050 / 0.0057 vs 0.0027 / 0.0037 / 0.0035 / 0.0062 |
| **Gs (planted keys)** | 10 random Quagmire IV ciphertexts at P 8: true plaintext allowed 97/97, C4 ⊆ C3, 0 UNKNOWN | pass, 10/10 (extra bans 21–141 per plant); run 1, mask code unchanged |
| Gx | 6 UNSAT answers re-decided by the full 26-letter model; 20 SAT answers with full-alphabet certificates | 6/6 UNSAT, 20/20 certificates (run 1) |
| G1 / G1b | COL(pt) = COL(ct); ciphertext = K4 at cribs and C4-forced positions; plants obey the mask | pass |
| G2b | held-out clean C4 plants called at q < 0.05: pooled ≤ 0.0528, each config < 128/2000 | pass: 0.0492, max 119 |
| **G3 (shuffled-K4 null)** | shuffled K4 called at q < 0.05 at P 8, ≥ 0.15 per model | pass: 0.330 / 0.305 / 0.339 / 0.228 (0.05–0.11 at the bar 0.00625) |

## Results
| P | JE | CARTER | K123MIX | JEX | q\* C4 | paired C3 q\* (same seeds) | reading |
|---|---|---|---|---|---|---|---|
| **8** | 0.0043 | 0.0031 | 0.0032 | 0.0075 | 0.0075 (10k) → **0.00602 ± 0.00039** (JEX, 40k) | 0.0057 | **`UNRESOLVED`** (|q − 0.00625| < 2 SE) |
| 13 (desc.) | 0.0122 | 0.0139 | 0.0170 | 0.0185 | 0.0185 | 0.0147 | `LOW-POWER` (above any Holm level) |
| 23 (desc.) | 0.0329 | 0.0380 | 0.0371 | 0.0412 | 0.0412 | 0.0308 | `LOW-POWER` |

- Registered path: q\* (10,000) = 0.0075, SE 0.00086, so |q\* − 0.00625| = 0.00125 < 2 SE and the band rule triggered the one ×4
  extension of the worst model (tag 10 reproduced exactly, plus 30,000 fresh tag-11 plants alone 0.00557). The extended q is 0.00602 ± 0.00039,
  still inside the band, so the result is **`UNRESOLVED`**. The other models sit at 0.0031–0.0043.
- Plant means at P 8 (z of COL_8): C4 0.94–1.28 vs paired C3 0.95–1.13. The extra bans barely flatten the plants at P 8. At P 23 the C4
  plants are lower (0.30–0.39 vs 0.44–0.52) with only 4 extra bans, so that shift comes from the Quagmire IV ciphertext multiset (one
  shared alphabet pair), not from the mask.

## Classification
- **Quagmire IV (F1), P 8, direct: `UNRESOLVED`** under the registered rule. This is not `STAT-DISFAVOURED` and not `LOW-POWER`. Shared
  alphabets do not rescue K4: q stays within noise of the H_8 value. But 40,000 plants cannot place it on either side of
  0.00625. The exact SAT cell of case 11 stays **open**.
- **H_8 (case 191 / cycle 205's 10M-plant tail, JEX 0.00548 ± 0.00002): unchanged.** This run does not touch that label. The paired C3
  batch here (0.0057 with 10,000) agrees.
- P 13, 23: `LOW-POWER`, unchanged in kind.

## Errata of this cycle (disclosed)
1. **Run 1 (PREREG209, seed block 209210) is broken, with NO VERDICT.** Plant z was computed on the plaintext, not on the enciphered plant
   (case 191 scores the ciphertext, because COL is invariant but the permutation moments depend on the row's multiset). q came out
   ≈ 0.4 for C4 *and* for the paired C3 batch, G3 failed (0.004–0.013), and G1b failed because the C3 batch was checked against
   C4-forced positions. The masks, G0, Gs and Gx of run 1 do not depend on the bug, and they are reused. Kept unchanged in `run1/`.
2. **The extension branch of run 2 kept the same bug** (it printed 0.41, which is plainly wrong). `ext209.py` re-did only that step as registered:
   same tags, tag 10 reproduces run 2's 0.0074993 exactly, z on the enciphered plants. The label above comes from this corrected step.
3. Timestamps: PREREG209's header says 04:08 and PREREG209b's says 04:22. The commits are 04:07:31 and 04:15:01 PT, and both precede their
   runs (04:07:36 and 04:15:01). The header times are typos.
4. PREREG209 used one ×4 extension, while I-265's straddle rule allows up to three looks at ≥ 10⁷ plants. Closing the band is I-279.

## Blind spots and scope
- **Single-position conditioning only.** Full joint conditioning on K4 is degenerate under any substitution family (COL(pt) =
  COL(K4)), so C3 and C4 both condition position by position. That is a modelling choice, not a law.
- The 256-key pool comes from randomised CP-SAT and is not a uniform sampler over consistent keys. The free letters are uniform per row.
- P 8 has 4 UNKNOWN queries, kept allowed (conservative toward C3). No transposition layer is applied (I-239), and the whole-text shuffle null is used as before.
- Statistical and model-dependent throughout. None of this is a decryption test, and no K4 reading was attempted or is implied.

## Reproduce
`tools/cycle209/run_cycle209.sh` (run 2; `SKIP_SOUND=1` reuses run 1's Gs/Gx; ≈ 93 s), then `python3 ext209.py SUP` (≈ 53 s). Run 1:
`python3 run209.py SUP results209.json` with PREREG209's code (in git at 28a0bc5). Corpora as case 191 (`/workspace/k4c209/sup`, sha256
13414dee… / 05e90d80… / b81e8e7b… / 96cd16ea…). Seeds: [209210, …] run 1; [209211, …] run 2 and extension; probe [209000, 1].
Next free seed: **209212**.

## Addendum (cycle 210, 2026-11-13): the exact 85-ban C4 mask
Text above preserved. The Voynich desk's independent SAT/SMT check (box-local `voynich/kryptos-audits/case196-c4-check/results.md`, sha256
e06ce501…; CaDiCaL one-hot + Z3 integer model, hand certificates for 0-idx 37, 43, 50) confirmed all 81 CP-SAT bans and showed that the
4 queries CP-SAT left UNKNOWN at 20 s are infeasible: **(37,T), (50,C), (50,E), (50,T)**. So exact C4 at P 8 has **85** extra bans (1,513 allowed
cells), forced {35, 41, 43, 46, 61, 78}. Registered in PREREG210 Part 1 (local commit `a187f23`) before any rerun; script
[`c4add210.py`](../tools/cycle210/c4add210.py), results [`results210_c4.json`](../tools/cycle210/results210_c4.json) (sha256 41272f46…).
- **Gate Z (our own Z3, no time limit):** the 4 named timeouts are UNSAT; 6 sampled CP-SAT bans UNSAT; at 0-idx 43 only T is SAT; 6 sampled
  allowed cells SAT with re-checked witnesses → pass. **Gate M:** 1,517 / 1,513 allowed, forced set as above → pass. **Gate R (I-283):** the 81-ban
  mask with case 196's seed block 209211 reproduces JEX q 0.0074993 exactly → pass.
- **Rerun (seed block 209212, 256-key pool, 10,000 plants per model, P 8):** q on the 85-ban mask (paired 81-ban, identical seeds) JE 0.0050 (0.0049),
  CARTER 0.0031 (0.0034), K123MIX 0.0022 (0.0036), **JEX 0.0057 (0.0066)**. Worst model JEX, looks: 10k 0.00570 ± 0.00075; 40k 0.00575 ± 0.00038;
  **160k 0.00595 ± 0.00019**. Bar 0.00625: |0.00595 − 0.00625| = 0.00030 < 2·SE 0.00038 → **`UNRESOLVED` (boundary band) after the 3 registered
  looks.** The 4 extra bans move q by less than its noise. The label is unchanged; I-279 (≥ 10⁶ plants) is the way to close it, and is now cheap (160k plants in 7 s).

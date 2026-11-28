# Case file 215: the NC bar's quadgram floor (I-335), 10 vs 11 vs 12, on fresh nulls with a low-n plant ladder; and full-scale V nulls for the case 213 edges (I-337)

**Cycle 229, 2026-11-21 (audit slot). Verdict: no floor adopted (pre-registered rule). The floor was not the weak point: on 16 fresh
nulls four distinct null decrypts clear NC ≥ −6.0, all with 12–19 non-crib quadgrams, so neither n ≥ 11 nor n ≥ 12 removes them.
K4 0 passes at every floor. Case 213's K4-only V edges sit inside the full-scale null range. No solution. Pre-registered as
`tools/cycle229/PREREG229.md` (local commit cd4da39, 03:53:18 PT, before any plant, null or K4 run of `kb229` other than the
disclosed gate-T and smoke checks; the run started 03:53:21 PT).**

## Why
The I-330 house bar (NC ≥ −6.0: mean log10 quadgram over non-crib quadgrams, known ≥ 49, ≥ 10 such quadgrams, tie = '?') had one
null pass in case 213: null 209425, Q all.bin p 24, r10 row 78680, NC −5.29, with exactly **10** quadgrams. Voynich's independent
recount (voynich-case-files 518a839 / d26217b, index 2252322, frozen 22:01:28 MST 2026-11-20) confirmed it (−5.2916, 4 hits, one
text). Over the null decrypts printed in case 213, no n ≥ 11 decrypt reached −6.0. The obvious move was to raise the floor, but
choosing it from the same data would be post hoc. So this cycle fixed the rule first and then measured on fresh seeds.
Her table also had a limit: it used only printed lines (B = running best, C = old-bar candidates), not every decrypt.

## Method
- **Tool:** `tools/cycle229/kb229.c` = `kb227.c` + `Y` lines. For every scored V / Q hit with known ≥ 49 it prints count, passes and max
  NC per (model, p, nq). Nothing else changes. **Gate T PASS** (done before filing): on K4 bank r10 and null 209425 all.bin r10, every
  non-Y line equals the published case 213 file after sorting. The exception is `B` lines, which are a thread-order-dependent running
  best. Null 209425 reproduces `Y model=Q p=24 nq=10 n=10 pass=4 max=-5.292`.
- **Family / scale:** case 213's keyboard family. Direct GVQ (geo a) / GV (geo b); Q behind bank.bin and all.bin on every 10th row (as
  case 213); **V geo a and geo b behind bank.bin and all.bin at full scale** (new: case 213 ran V nulls only at r10).
- **Nulls:** 16 fresh shuffles of K4, seeds 209559–209574. K4 went through the same commands.
- **Plants (seed 209558, `plant229.py`):** a 24-plant **low-n ladder**: Q model, carved-index key, p 19–24, behind bank / all.bin. Four
  plants each at exactly n = 10, 11, 12, 13, 14, 15 non-crib quadgrams under the kb227 decrypt of the true configuration. Odd ids carry
  **one corrupted carved crib letter**. Plaintext is K1–K3 or Jane Eyre. Each plant was run with kb229 on its own row.
- **Smoke (disclosed in the prereg):** the sampler was tried once with seed 1. Three seed-1 plants went through kb229 and matched the
  Python prediction.
- **Run note:** `run229.sh` started 03:53:21 PT. At 03:56:48 PT the files for nulls 209566–209574 were not visible on disk and null
  209565's last file was truncated, with no process visible. `resume229.sh` reran those ten nulls with identical commands
  (03:56:59–03:58:55 PT). The original run's `time.txt` lines through "end 195s 03:56:36" appeared later. Counts, P and Y lines are
  deterministic, so either copy gives the same numbers; the published files are the resume copy. Heavy wall ≈ 195 + 116 s ≈ 5.2 min,
  plus ≈ 10 s for gate T.

## Gates (pre-registered)
| gate | result |
|---|---|
| P0: recovery ≥ 23/24 and bar at floor 10 ≥ 23/24 | **24/24 recovered, 24/24 over −6.0** (Wilson 0.86–1.00); NC −3.68 … −5.35 (the lowest is plant 3, one-error, n 10); kb229 = Python prediction 24/24 → **PASS** |
| P(11): plants with n ≥ 11 pass at floor 11 | 20/20 (Wilson 0.84–1.00) → PASS; lost by construction: plants 0–3 (n 10) |
| P(12): plants with n ≥ 12 pass at floor 12 | 16/16 (Wilson 0.81–1.00) → PASS; lost: plants 0–7 (n 10–11) |
| N(11): 0 distinct null texts at floor 11 (fresh **and** published case 213) | published 0; **fresh 4** → **FAIL** |
| N(12) | published 0; **fresh 4** → **FAIL** |

**Decision (rule as filed): no adoption.** The floor stays at 10 and carries the case 213 caveat. A quadgram-count / scale-dependent
bar is queued (I-342).

## Result
### Passes per floor (16 fresh nulls, ≈ 24.1 M barred null decrypts; K4 ≈ 1.5 M)
| floor | null hits | distinct null texts | null texts with a pass (Wilson 95 %) | null max NC | K4 passes (max NC) |
|---|---|---|---|---|---|
| nq ≥ 10 | 8 | 4 | 4/16 (0.10–0.50) | −5.945 | 0 (−6.21) |
| nq ≥ 11 | 8 | 4 | 4/16 (0.10–0.50) | −5.945 | 0 |
| nq ≥ 12 | 8 | 4 | 4/16 (0.10–0.50) | −5.945 | 0 |

Each passing text comes from a pair of exactly inverse bank rows that read the same decrypt, so 8 hits make 4 texts. All four are V
at p 23–24 behind the full-scale V runs. None is Q, and none has 10 or 11 quadgrams. All are gibberish around the cribs:
- null 209573, V geo b all.bin p 24 (AZERTY-S), nq 13, NC −5.945: `AJJLZ??I?O?XNC?YEANIFEA?TNORTHEAS?Q?NPM??VGLR…BERLINCLOCK??CNRESANOR…`
- null 209568, V geo b bank p 24 (QWERTZ-S), nq 13, NC −5.994: `OA?F?ELO?ZPQMJM?Z?CHCEAS?NORTHE?STZIPSEB?H?TF?KMISSWOROU…`
- null 209560, V geo a bank p 23 (PALIMPSEST-QW), nq 12, NC −5.998: `KBZ??K?WN?IBOJ?QCU?QREASTNORTHEASTT?YGOCONCL?KFGN…`
- null 209563, V geo b bank p 23 (QWERTZ-S), nq 19, NC −5.982: `KH?F?VA?NYLGBW?R?LCVKEASTNOR?HEAS?V?P?RWRAO????SILONDLANALEM…`

### Null NC maximum by number of quadgrams (pooled, `Y` lines; full table in `analyze229.log`)
| nq | 4 | 6 | 8 | 10 | 11 | 12 | 13 | 14 | 16 | 19 | 21 | 24 | > 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| null decrypts | 137 | 457 | 1,615 | 3,677 | 5,785 | 8,351 | 11,411 | 15,451 | 26,415 | 49,771 | 67,329 | 90,361 | 20.4 M |
| null max NC | −5.45 | −5.84 | −5.29 | −6.05 | −6.17 | −6.00 | −5.95 | −6.10 | −6.20 | −5.98 | −6.05 | −6.34 | −6.36 |
| K4 max NC | −6.67 | −7.91 | −6.57 | −6.52 | −6.43 | −6.51 | −6.50 | −6.72 | −6.21 | −6.80 | −6.44 | −6.61 | — |

Reading. Below the floor (nq 4–8) the nulls do clear −6.0 (20 hits), so the floor of 10 does real work there. At nq 10–24 the null
maximum sits at −5.9 … −6.3 and does not fall steadily with nq. It tracks how many decrypts are in each bin. The null max near −6.0
is a **search-size** effect, and it lives at nq 12–19 as much as at 10. A floor cannot remove it; only a bar tied to the number of
decrypts searched (or a stricter level) can. The plants keep a margin: lowest −5.35, against a null max at nq ≥ 10 of −5.945. That
gap suggests where a future bar could go (≈ −5.5 to −5.6), but it is **post hoc** here, so this cycle only queues it (I-342) and
adopts nothing.

**What this means for past verdicts:** nothing changes. Every K4 decrypt-level reading so far (cases 212–214 and this one) is "K4 0
passes", and that stands at any of these floors. What changes is how strong the bar is: in a large family (≈ 1.5 M decrypts per
text) about one null text in four (Wilson 0.10–0.50) clears it. **A K4 pass of the I-330 bar would not on its own be evidence; it
would need the null rate of its own cell beside it.** That rule already appears in every case file ("null NC maximum printed
beside it").

## Part B — I-337: case 213's V edges at full scale (16 fresh nulls)
| cell | K4 | nulls (full scale) | occupancy (Wilson) | p_up | label |
|---|---|---|---|---|---|
| V geo a bank p 17–18 | 0 | all 0 | 0/16 (0–0.19) | — | **EXACT-EXCL (discriminating)** |
| V geo a bank **p 19** | 2 | one null 2, rest 0 | 1/16 (0.01–0.28) | 0.118 | **INSUFFICIENT-DISCRIMINATION** (was "K4-only, NO-SIGNAL") |
| V geo a bank **p 20** | 2 | 0–24, occ 11/16 | 11/16 (0.44–0.86) | 0.706 | **INSUFFICIENT-DISCRIMINATION** (was "K4-only, NO-SIGNAL") |
| V geo b bank p ≤ 19 | 0 | p 19: one null 96 | 1/16 | — | **EXACT-EXCL (discriminating)** p 1–19 (confirms case 213 at full scale) |
| V geo a all.bin p ≤ 18 | 0 | p 18: one null 2 | 1/16 | — | **EXACT-EXCL (discriminating)** p 1–18 |
| V geo a all.bin p 19 | 0 | 4/16 non-zero | 4/16 (0.10–0.50) | — | `EXACT-EXCL (non-discriminating)` (case 213: "K4 0, no claim") |
| V geo b all.bin p ≤ 19 | 0 | p 19: one null 4 | 1/16 | — | **EXACT-EXCL (discriminating)** p 1–19 |
| V, every scope, p 20–24 (p 21–24 bank geo a) | 2 … 25,644 | occ 11–16 / 16 | — | 0.06–1.00 | `INSUFFICIENT-DISCRIMINATION` (unchanged) |

All V cells at p ≤ 16 are 0 for K4 and for all 16 nulls. The 16 fresh Q r10 nulls are also 0 at p ≤ 16 in both scopes, which backs
case 213's Q EXACT-EXCL ranges. K4's V decrypts pass the bar 0 times (Part A) → decrypt level `NO-SIGNAL`. The case 213 K4-only cells
were an artefact of measuring nulls at r10. At full scale the nulls hit there too, so they are relabelled
`INSUFFICIENT-DISCRIMINATION` (count level), still gibberish. **Not done:** Q all.bin p 16 at full scale (≈ 1–2 min per null; stays in
I-337); I-337 asked for ≥ 20 nulls and this cycle ran 16.

## Labels
- I-335 floor audit: **no adoption** (N(11), N(12) fail on fresh nulls; P0 / P(F) pass). House bar unchanged: I-330, floor 10, tie = '?'.
- Decrypt level, case 213 family, every scope: **`NO-SIGNAL`** (K4 0 passes at any floor; nulls 4/16 texts).
- Count level (Part B): V geo a bank p 19 / 20 → `INSUFFICIENT-DISCRIMINATION`; V geo b bank / all.bin p 1–19 and V geo a bank /
  all.bin p 1–18 → `EXACT-EXCL (discriminating)` at full scale; V geo a all.bin p 19 → `EXACT-EXCL (non-discriminating)`.

## Blind spots
One family only (case 213's keyboard family). The w 11 columnar family of case 214 has far fewer decrypts per text, so its null
rate under the bar is lower and was not measured here. The plants are Q only (no V plants). Plants are English windows; a plaintext
with heavy X / filler would score lower. 16 nulls bound the per-text pass rate loosely. Q at r10 only. The two-number bar (floor ×
level) is still a choice, not a law.

## Files
[`data/cycle229/`](../data/cycle229/): `R/` (filtered run outputs), `plants229.tsv`, `nulls229.tsv`, `summary229.json`,
`analyze229.log`, `gateT/`, `resume229.sh`, `MANIFEST.txt`, `SHA256SUMS`. Tools: [`tools/cycle229/`](../tools/cycle229/)
(`kb229.c`, `plant229.py`, `run229.sh`, `resume229.sh`, `analyze229.py`, `PREREG229.md`). Seeds: plants 209558, nulls
209559–209574. **Next free seed 209575.**

## Verdict
No solution. Raising the floor would not have fixed the bar: the nulls that pass do so at 12–19 quadgrams, through sheer search
volume. The bar stays as it is, and its weakness is now measured: about one null text in four in a large family. **K4 still
standing.**

## Addendum (cycle 244, [case 230](230-audit-informative-counts-one-error-testability-class-ranks.md) T2; credit Voynich C130)
One-error plants by the class of their wrong crib seat (key class S[POS[j]] mod p on the plant's own layout): 5 PENDANT (1, 3, 7, 11, 17), 4 TIE (5, 9, 21, 23), 3 MAJ (13, 15, 19). Plants **7, 11, 21, 23** sit on layouts with no class of size ≥ 3 at their period, so their rows read **`NOT TESTABLE`** for one-error correction (an error there is invisible or blanks a class; it cannot be outvoted). Pooled one-error 12/12; on testable layouts 8/8. Gate P0's verdict does not rest on those rows (20/20 without them). `data/cycle244/seat244.txt`.

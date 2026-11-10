# PREREG198 — one-error audit of case 184: an indel plus one wrong crib letter (IDEAS I-222 via pointer I-221)

Written 2026-11-10 ~04:00 PT, before any K4 or shuffled-K4 run with these tools. Run so far: the reserved shuffle (seed 19890) for the
timing probe and the strict cross-check, 40 uniform random texts (seeds 19801–19840) for the meter, and planted texts.

## Hypothesis (audit)
`[speculation]` Case 184's model — two periodic keys stacked K1/K2-style (one tableau, solver A; two tableaux A–Z/KRYPTOS, solver B), one
dropped (del, C′ 98) or extra (ins, C′ 96) carved letter, direct or behind a pure K3-law decimation of the true length — **plus one wrong
letter among the 24 crib positions** (a carving error or a crib letter Sanborn changed). K1–K3 carry both kinds of slip. Case 184 assumed
every crib letter is right; one bad letter could have hidden a true fit.

## Model (`cmp198.c`)
- Records exactly as `cmp197` (the 101 direct records `recs197_direct.txt`, readings R1/R2; perm mode on `decM98.bin` 4,116 perms (del) and
  `decM96.bin` 3,072 perms (ins), d values identical on the cribs run once, models P and C).
- **One-error fit:** the usable crib constraints are consistent with every slot, or after deleting one slot t. Consistency depends only on
  the 2-core, so for each (record, model, pair) the cyclic components K of the core are found and, per K, the distinct 2-cores of K − t; a
  config with exactly one failing component K fits iff some core of K − t is consistent (two failing components cannot be repaired by one
  deletion). Solver A: weighted union-find (case 176); solver B: bijection-graph programs over 26 roots (cycle 192).
- **Chance bound per config (union bound, exact component terms):** U = Σ_K Σ_distinct d E_G/E_K · E(d) (+ E_G if G has pendant edges),
  E = 26^−excess (A) or Π_cyclic 26^(1−r) (B; expected solutions ≥ P(consistent)); capped at 1; U = 1 if no cycle. U ≥ P(fit).
- **Search rule (budget):** the deletion search runs only for configs with U ≤ 0.05; others are tested strictly only (reported separately).
  A cell is full power iff its U sum ≤ 0.05, so every config of a full-power cell is searched.
- Additive caveat: in solver A a bridge never constrains, so a wrong letter on a bridge is invisible (strict fit, one wrong decoded letter;
  control P1b). In solver B bridges do constrain and are deleted like any slot.
- Probe checks: strict fit counts identical to `cmp197` on all 5,840 direct cells (reserved shuffle); the component-wise search gives
  output identical to the first (global-core) version on the direct records and the decM96 every-8th bank.

## Stages (registered)
1. Direct: 101 records; solver A on A–Z and KRYPTOS (vig/beau), `pairsA_all` model P (260 pairs); solver B AZ>KA, KA>AZ × VV/VB/BV/BB,
   `pairsB_all` model P (600 pairs). (The 18,824 themed alphabets of case 184 are not re-run: low power by construction, more so with one error.)
2. M = N decimations: decM98 (del) and decM96 (ins), all perms, both solvers (A–Z/KRYPTOS; both tableau pairs), case 184's text-free pair
   lists `pairsA_del/ins`, `pairsB_del/ins` (tools/cycle197), models P and C. Chunks of 1,000 perms with checkpoints.
- Not run (blind spots fixed in advance): solver A/B one-error behind the non-M = N decimation families (case 184 ran A there strictly;
  ≈ 24× cost); themed alphabets; two wrong letters; indel + wrong letter + three keys.

## Classification (registered)
- Print threshold U_config ≤ 0.05. **Full power**: cell (stage, solver, model, alphabet/tableau, form, m, n) with U sum ≤ 0.05.
  `EXACT-EXCL` (under the model) where every fit in full-power cells is decoded under every equivalent d (I-223) and every slot giving the
  same one-error event (same 2-core), every consistent key, and none reads as English (run of ≥ 3 real words off the cribs, judged by
  reading plus quadgram score against the plants). Fit totals are compared with the summed U (an upper bound; meter: 162 fits vs U 257).
- `LOW-POWER`: cells with U sum > 0.05; searched-config fits vs their U, strict fits reported; the 20 smallest-U low-power fits decoded and read.
- A real solution requires a full 97-letter coherent English decryption with both cribs at official positions, reproducible.

## Controls (rehearsed 13/13, `controls198_rehearsal.txt`; rerun after the K4 run)
Case 184 plants with one wrong crib letter on a 2-core slot (solver A: a cycle slot, not a bridge): P1e direct R1 del d 50 KA vig
ABSCISSA+PALIMPSEST; P2e direct R2 ins d 30 AZ beau BERLIN+KRYPTOS; P3e direct R1 ins d 5 AZ>KA VV CLOCK+NORTHEAST; P4e direct R2 del d 70
KA>AZ BV ABSCISSA+PALIMPSEST; P7e decM98 del d 60 C AZ>KA VB TIME+KRYPTOS; P8e decM96 ins d 10 P KA>AZ VV SHADOW+LIGHT; P10e decM98 del d 30
P KA vig ABSCISSA+PALIMPSEST; P11e decM96 ins d 20 C AZ beau CLOCK+BERLIN; P1s strict plant (slot −1); P1b wrong letter on a bridge (found
strictly, documented as undetectable); negatives N3, N4 (two wrong letters) and N1 (three keys) must give no fit in the planted cell (fits in
other cells at the planted record are chance and are reported: N3 8, N1 1 in the rehearsal). Checked independently (`checkctl198.py`, lib197/
lib198): planted record rebuilt in Python, reported slot in the planted slot's one-error event, decode with the planted slot removed reproduces
the plaintext at every determined position except the altered carved letter. Rehearsal changes (disclosed): P1e first drew a bridge slot
(invisible in solver A, found as a strict fit) → kept as P1b, P1e redrawn on a cycle slot; N1 criterion narrowed from "any cell" to "planted
cell" (a one-error B fit 7 × 13 at U 5.7e-4 elsewhere is chance); control decimation runs restricted to the planted perm.

## Meter (done, `data/cycle198/meter198.txt`)
40 uniform texts on the direct records: full-power cells 162 fits vs U 257.4 (bound holds; one text 19, overlapping records); low-power
searched configs 6,927 vs 11,331.

## Nulls and grid
19 shuffled-K4 texts (seeds 19851–19869) on the direct records and on every 128th perm of decM98/decM96 (33 + 24 perms), K4 on the same
banks. Statistic (`grid198.py`): distinct clusters (stage, record cluster, model, alphabet/tableau, form) with a one-error fit at
U_config ≤ 26^−2; p⁺ = (1 + #nulls ≥ K4)/20, floor 0.05, descriptive (rank 1 → pooled follow-up later, not a signal); non-degeneracy check (I-224).

## Recount
`recount198.py`: independent Python (no cores, no union-find, no dedup; BFS on G and on every G − t) on K4's 101 direct records, solver A
all 260 pairs on A–Z/KRYPTOS, solver B on the 30 pairs with m, n ≤ 7, compared with `cmp198` at PE = 1 (deletion search on every config):
per-cell fit counts must be identical (rehearsed on the reserved shuffle, records 0–19: 1,280 cells, 11,312 fits, 0 mismatches).

## Budget
Heavy ≈ 8 min wall target (probe ≈ 3 min and rehearsal ≈ 3 min already spent, disclosed); registered run 6 threads, every step under
`timeout`, own process group; if the M = N stage overruns, finished chunks are reported and the rest queued.

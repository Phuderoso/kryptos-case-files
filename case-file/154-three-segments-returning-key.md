# Case file 154 — Three key segments and a returning key, width-7 phase kept (cycle 166)

**Status:** negative. **Type:** new structure (cycle 165 was an audit). IDEAS **I-070** (follow-up of I-013,
[case 150](150-split-key-width7-phase.md)). The returning key (key 1, then key 2, then key 1 again) is `EXACT-EXCL` directly,
under one wrong crib/carved letter, and behind the whole bank for A–Z/KRYPTOS. Three independent keys are `EXACT-EXCL` only for
A–Z/KRYPTOS directly. With all 86,731 alphabets, or behind the bank, three independent keys have no power (`NO-SIGNAL` / `LOW-POWER`).

## 1. Why this, and why it is new
Cycle 166 had to open a new family. The three queued candidates (I-016, I-070, I-071) were checked against the case files:
- **I-016** (periodic, both alphabets arbitrary, open periods 8, 13, 16, …) extends case 11's SAT runs and is expected to be
  underdetermined (case 23). It is an extension, not a new structure, and is likely LOW-POWER. Kept queued.
- **I-071** (split period-7 key with themed/vocabulary alphabets per segment) restricts cycle 162's model X. It is a variant of case 150.
- **I-070** has three or more segments, or a key that returns after an interruption. No case file has it: case 52 (cycle 54) has two
  segments, direct, split 34–63 only, and lists "three or more segments" under *not covered*. Case 150/151 have exactly two segments.
  Case 89 (per-block key restart at the Ws) restarts the *phase* of one key. Here the phase is kept and the keys change. `grep` over
  `case-file/` for three segments / returning key found nothing. **New.**

Plain-language story: K2 has several sentences. If Sanborn's clerk changed the keyword at each sentence, there would be three
segments. If a short insert was keyed differently and the main key then came back, the shape would be A | B | A.

## 2. Model
- Index positions 0–96: direct, the plaintext index behind a bank permutation (model Q), or the carved index (transpose first).
  The key letter is chosen by index mod 7, with the phase counted from position 0 (as in case 150).
- One keyed alphabet A on both sides (Quagmire III), shared by all segments. All 86,731 alphabets of `alpha.bin` are used
  (0 = A–Z, 1 = KRYPTOS, then themed and dictionary keyword alphabets). Vigenère (variant Beaufort has the same consistency) or
  Beaufort is chosen independently per segment.
- Boundaries 0 ≤ b1 ≤ b2 ≤ 97 are free, also inside a crib.
- **Model T:** three independent period-7 keys k1 | k2 | k3. Reported as T3 only when no two-segment fit exists for those forms
  (two-segment fits are case 150 and are flagged separately).
- **Model R:** returning key k1 | k2 | k1. The same key and form apply before b1 and from b2 on. R0 marks fits whose middle holds
  no crib; those are one key on all cribs, which is already excluded (case 123).

## 3. Exact test (`tools/cycle166/split3.c`)
- T: the longest consistent prefix (form m1) and the longest consistent suffix (form m3) are optimal. The middle must then be
  consistent (m2).
- R: for every prefix length e, the tool finds the smallest suffix start s*(e) that is consistent together with the prefix in one
  key table. The middle [e, s*) must be consistent under m2. This is exhaustive over e.
- Leave-one-crib-out mode (`drop`) gives the one-error test: one wrong crib letter, or one wrong carved letter under a crib.
- Power ([`power.txt`](../data/cycle166/power.txt), direct positions):

| model | boundary classes | fewest checks | union-bound chance per alphabet |
|---|---|---|---|
| T | 325 | **4** | 3.6 × 10⁻⁴ (× 86,731 ≈ 32 false fits per text) |
| R | 325 | **10** | 3 × 10⁻¹² |
| two segments (case 150) | 25 | 10 | 3 × 10⁻¹³ |

  So R is nearly as strong as the two-segment test. T with every alphabet is expected to fit by chance.

## 4. Runs (~6.5 min of 8-core time, checkpointed slices; [`run_cycle166.sh`](../tools/cycle166/run_cycle166.sh), [`run_cycle166b.sh`](../tools/cycle166/run_cycle166b.sh))
Texts: K4, 4 shuffled nulls (seeds 16601–16604), and 20 profile-matched nulls (cycle-157 rule: same crib-letter repetition
profile, seeds from 16600000) → 24 nulls. [`texts166.txt`](../tools/cycle166/texts166.txt).

| cell | scope | T3 (A–Z/KA) | T3 (all alphabets) | R (all) | label |
|---|---|---|---|---|---|
| D strict | direct, 86,731 alphabets, 25 texts | K4 **0**, nulls 0/24 | K4 10 vs nulls 0–113 (median 9), p 0.44 | K4 **0**, nulls 0/24 | R, T-AZKA `EXACT-EXCL`; T-all `NO-SIGNAL` |
| D one-error | + 24 leave-one-crib-out runs | K4 **0**, nulls 0/24 | K4 313 vs 242–4,617 (median 574) | K4 **0**, nulls 0/24 | R, T-AZKA `EXACT-EXCL` (one error); T-all `NO-SIGNAL` |
| BA | full bank, 660,260 configs per text, A–Z/KRYPTOS, 25 texts | K4 66 vs nulls 42–188 (median 78), p 0.64 | — | K4 **0**, nulls 0/24 | R `EXACT-EXCL`; T `NO-SIGNAL` |
| BE | full bank, A–Z/KRYPTOS, leave-one-crib-out, K4 + 4 nulls | K4 5,772 vs 5,046–6,386 | — | K4 **0**, nulls 0/4 | R `EXACT-EXCL` (one error); T `LOW-POWER` |
| BS | q ≡ 0 mod 200 (3,304 configs), all alphabets, K4 + 4 nulls | 0 vs 0–3 | 21,644 vs 20,459–22,357 | K4 **0**, nulls 0/4 | R `EXACT-EXCL` on the sample |
| BS20 | q ≡ 10 mod 20 (33,012 configs), all alphabets, K4 + 2 nulls | 3 vs 4, 8 | 227,547 vs 203,839, 214,342 | K4 **0**, nulls 0/2 | R `EXACT-EXCL` on the sample |

Counts: [`summary_counts.txt`](../data/cycle166/summary_counts.txt); every H line: [`H_lines_all_runs.txt`](../data/cycle166/H_lines_all_runs.txt);
K4 fit lines: [`k4_fit_lines.txt`](../data/cycle166/k4_fit_lines.txt); run-folder audit (I-078): [`run_provenance.txt`](../data/cycle166/run_provenance.txt).
R0 = 0 everywhere, as expected.

**False-positive gate (I-079, Voynich-sourced, unverified).** A cell may call K4 = 0 a discriminating `EXACT-EXCL` only if
≤ 2 of 20 nulls have any fit. R passes everywhere (0/24, 0/24, 0/4, 0/4, 0/2). T-AZKA direct passes (0/24 strict and
one-error). T-all direct fails (22/24 nulls hit), T-bank fails (24/24). Those cells are therefore reported as count comparisons
only (`NO-SIGNAL` / `LOW-POWER`), never as "not detected".

## 5. Controls
- [`plant166.py`](../tools/cycle166/plant166.py) is an independent textbook encryptor. It made 10 T and 10 R plants with random keys,
  forms and boundaries (several inside a crib). They mix A–Z/KRYPTOS and random dictionary alphabets and cover the direct, model Q
  and carved layers. **20/20 recovered** (true alphabet and forms present, [`controls166.txt`](../tools/cycle166/controls166.txt)).
  Plus 4 one-error plants (one carved letter under a crib altered, R and T): **4/4 recovered** in the one-error mode.
  - In the R plant eR0, the strict mode also passes: the corrupted crib can be moved into the middle segment by shifting a
    boundary. A segment model can absorb an error, so strict fits are not error-free proofs.
  - Power on plants is 24/24 ≥ 9/10. The solver is exact, so plant "strength" is binary here. The calibration that matters is the
    FPR gate above.
- Independent recount [`recount166.py`](../tools/cycle166/recount166.py): numpy, every boundary pair 0 ≤ b1 ≤ b2 ≤ 97, no
  greedy steps. It covered 25 direct texts, 12 one-error runs, 24 plants, 24 bank configurations (A–Z/KA) and 3 all-alphabet bank
  configurations. **88/88 identical** sets of T alphabets and R (alphabet, form, form) triples ([`compare166.txt`](../data/cycle166/compare166.txt)).

## 6. Crib and English checks
Only T has fits. Each fit was decrypted ([`decode166.py`](../tools/cycle166/decode166.py)), with the boundaries placed at the first
crib of segments 2 and 3 and '?' where a residue has no crib in its segment. Every decode reproduces the 24 crib letters (asserted).
- K4 direct (27 fits): best −6.61 per quadgram, off-crib −7.50.
- K4 bank A–Z/KA (134 fits): best −6.61, off-crib −7.55. Example: `…EASTNORTHEASTYATESNA?DTUSK?HQSCPVZHNWZVOGGBERLINCLOCKNESIDRVITY…`
- Nulls: direct −6.47 to −7.06, bank −6.50 to −6.81 ([`decode_summary.txt`](../data/cycle166/decode_summary.txt)).
- English plants score ≈ −4.2 when fully keyed.

All of this is gibberish inside the null range. R and the A–Z/KA direct T have no K4 survivor to decode.

## 7. What this excludes and what it doesn't
Excluded (exact):
- **A returning period-7 key (A | B | A)**, phase kept, any boundaries, Vig/Beau per segment, one shared Quagmire-III alphabet out
  of 86,731, directly, strict and under one crib/carved error.
- The same behind all 165,065 bank permutations, both directions and both index orders, for A–Z/KRYPTOS (strict and one-error),
  and for all alphabets on 1/200 + 1/20 of the bank (≈ 5.5 %).
- **Three independent period-7 keys with the A–Z or KRYPTOS alphabet directly**, strict and one-error.

Not excluded:
- Three independent keys with the other alphabets, or behind the bank. The test has no power there (4 checks), and the counts sit in
  the null range.
- R with all alphabets on the remaining ≈ 94.5 % of the bank (I-080).
- 4+ segments, alternating A | B | A | B (I-081).
- Keys that shift by a constant per segment (I-082).
- Phase restart at a boundary (case 89 covers the Ws only), periods other than 7, and mixed (Quagmire I/II/IV) tableaux per segment (I-071).

## 8. Reproduce
`gcc -O3 -march=native -o tools/cycle166/split3 tools/cycle166/split3.c`, then `tools/cycle166/run_cycle166.sh` and
`run_cycle166b.sh` (inputs `alpha.bin`, `perms97.bin`, `quad.bin` from the support backup, not committed for size). Then run
`summarize166.py RUN`, `compare166.py RUN` and `decode166.py`.

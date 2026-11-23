# Case 219 — Arithmetic-sequence and word-length key streams on two keyed alphabets (cycle 233)

**Slot:** new family (230 new family, 231 replicate, 232 audit → 233 had to be new). Idea **I-361** (tested here); paperwork **I-357** (settled), **I-358** (slope note); new **I-362–I-366**.
Pre-registered as [PREREG233](../tools/cycle233/PREREG233.md) (local commit 978d9f9, 2026-11-21 ~19:55 PT, before any plant, null or K4 run). Code and window list:
[`tools/cycle233/`](../tools/cycle233/) (`keys233.py`, `keys233.tsv`, `plant233.py`, `check233.py`); tool `gn217` **unchanged** (source sha 97bae55f…d792); raw results: [`data/cycle233/`](../data/cycle233/).
**Verdict: no solution.** K4 has 0 hits (0 exact, 0 with one wrong crib letter) in all three scopes: `EXACT-EXCL` within the frozen 4,172-window list (gate P 20/20).

## The idea (and why it is not in the repo yet)
K1–K3 each came with a named trick. A key that is a *mathematical sequence of the position* (primes, φ(n), divisor counts, digit sums, Thue–Morse, Collatz steps, partitions…) or the *word-length rhythm of
K1–K3's plaintext* is a layered-simple structure that neither the periodic nor the linear-recurrence tests see (a repo grep found none of these names; Fibonacci / squares / geometric keys *are* linear
recurrences and were left out on purpose). `[speculation]`: no public source says Sanborn used one.

## Method
`gn217` (case 203 model Q), keys k_i = (f(o + i) + c) mod 26 (fwd) or (f(o + 96 − i) + c) mod 26 (rev); 22 open sequences S1–S22 × o 0–39 × c ∈ {0, 1} × both directions, plus word-length streams of K1 / K2 / K3 / all three
(cyclic, every offset). 4,172 windows after dropping duplicates of the case 203 / 204 / 207 lists; 3 forms; direct 86,731², bank and all.bin 144² themed × themed behind the carved-position permutations; ≥ 23 / 24 crib seats.

| scope | permutation rows | window-pair-forms | K4 hits (24 / 23) | null 209644 | time |
|---|---|---|---|---|---|
| direct | 1 | 9.41 × 10¹³ | 0 / 0 | 0 / 0 (full) | 5 s |
| bank | 165,065 | 1.71 × 10¹⁴ | 0 / 0 | 0 / 0 (rows ÷ 10) | 105 s |
| all.bin | 165,782 | 1.71 × 10¹⁴ | 0 / 0 | 0 / 0 (rows ÷ 10) | 96 s |

**Gate P (seed 209643):** 20 / 20 plants recovered with the planted (window, form, X, Y, permutation) (Wilson 0.84–1.00; 10 one-error plants included; `check233.py` re-derived every H line, agreement mismatches 0).
**Null:** one shuffled K4 (seed 209644), 0 hits in every scope. It is a smoke measure, not a calibration: the 24-letter filter predicts ≪ 1 chance hit per text and cases 217–222 saw 0 in all their nulls.

## Reading
- `EXACT-EXCL` for K4 within the list and the model (positions 22–34 / 64–74 1-based, 0-based 21–33 / 63–73; one wrong crib letter tolerated; the plants show the search finds such keys).
- With **zero** H lines there is nothing to decrypt, so the I-342 NC bar (PREREG233 Part B: bar = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879, N = max(10, H lines in scope)) was **not exercised** on K4.
  `check233.py` computes NC and the bar for any future H line; its first live use is on the plants (all English by construction, not a test of the bar). That is a limit, logged as I-364.
- Scale caveat: scale and constant are restricted (a = 1, c ∈ {0, 1}, o ≤ 39). Key = a·f + c with other a, c is not covered (I-362).

## Part C — paperwork owed from cycle 232
1. **Addendum to [case 217](217-bounded-shift-fresh-null-replicate.md) (I-357):** bank W ≤ 10, which case 218 printed as `NO-SIGNAL (robust)`, is relabelled **`NO-SIGNAL-FRONTEIRA`**.
   PREREG232's definition (upper 95 % Wilson bound of the per-text null rate over the K4 rate, per null set) gives 1.01× (inside) on my fresh set and 1.04× (above) on Voynich's 31231000+i replica set (her final
   reconciliation of I-357). One set inside the bar means FRONTEIRA by the ≥ 2×-on-both-sides rule. My pooled "≥ 3.4 α" stays descriptive only. Her reading (all six cells FRONTEIRA) stands; the two readings now agree.
2. **I-358 (slope, logged):** two estimands side by side, not reconciled and not extrapolated. Voynich's I-342 replicate slope **b ≈ 0.19 NC per e-fold of N** is a per-unit slope with nq and family held fixed (nested draws
   inside pools, N < 2000). Mine, **≈ 0.079 per e-fold** (plus 0.00027 (ln N)²), is the per-text maximum in the joint fit over N 10 … 5.3 M. Different questions: "how does the max of a pool grow when I add decrypts at fixed
   nq?" versus "how high does one text's best decrypt sit as its search grows?". The bar uses the second, which is what K4 must beat.

## Blind spots
Other multipliers / constants; German and other-language number names; sequences read from a start other than n = 1 beyond o 39; two-digit groups of sequence values (primes written as digits); sequences as *alphabet permutations* (rank of n-th prime mod 26) rather than shifts; word lengths of other texts (Sanborn's statements, the Kryptos Morse plates). One-error beyond the 23 / 24 rule is not covered.

## Addendum (cycle 234)
The S18 (look-and-say) rows are **not** look-and-say beyond n 42: `keys233.py` cuts the string at 10⁵ characters and writes 0 afterwards, so every S18 window ends in a constant-zero tail that covers the BERLINCLOCK seats. Those rows test "look-and-say then zeros". The verdict for the other 21 sequences and the word-length streams is unchanged. Found in [case 220](220-multiplied-arithmetic-key-streams.md); fix queued as I-367.

## Addendum (cycle 237)
S18 repaired and re-run in [case 223](223-look-and-say-s18-repaired.md): exact look-and-say lengths (Conway atoms, validated against OEIS A005341 n ≤ 3000), 160 windows with a = 1 (plus ×a variants): K4 0 hits in direct / bank / all.bin → `EXACT-EXCL` for the real look-and-say stream. The corrected S18 label supersedes the "look-and-say then zeros" reading above.

# PREREG233 — Cycle 233 (new family, I-361): arithmetic-sequence and word-length key streams on two keyed alphabets

Filed 2026-11-21 ~19:55 PT (America/Vancouver), **before** any plant, null or K4 run of `gn217` with `keys233.bin`. Base: origin/main **a06bfab**
(c232 published). Case file 219. Slots: 230 new family (case 216), 231 replicate, 232 audit, so **233 must be a new family** (I-347 / I-359).
Seeds: plants **209643**, null **209644**; next free after this cycle **209645**.

## Disclosed before filing
- `gn217.c` (sha 97bae55f…d792) rebuilt with `gcc -O3 -fopenmp -march=native`; nothing run. `keys233.py` was run once to build the window file (no search).
- No smoke run, no seed spent. The window list below is frozen by `keys233.bin` sha256 **4d03ca5b3741857462b076304dea3ab29ae6aac530a5abc8209bf6ff6711a33e**
  (4,172 windows, `keys233.tsv` lists family / offset / constant / direction).

## Overlap check (repo grep, `[repo]`)
No case file mentions primes, polynomial, Möbius, Collatz, partition, Catalan, Bell, Recamán, Stern, Kolakoski, look-and-say, Josephus,
number-name or Roman-numeral key streams. Fibonacci / squares / geometric keys are linear recurrences (cases 78, 166–175: any L ≤ 4 recurrence mod 26 covers
a polynomial of degree ≤ 3 and k = a·r^i), so they are **not** repeated here. Case 217/218/221/222 streams (π, e, √2…, named strings, ITA2…) are dropped as duplicates.

## Part A — I-361 (new family)
**Idea.** Sanborn's K1–K3 solutions needed a *named trick* (keyword, keyed alphabet, grid turn) and K4 is billed as "a different system". A key that is a
**mathematical sequence of the position** (primes, φ, divisor counts, digit sums, Thue–Morse, Collatz, partitions…) or a **word-length rhythm of the
earlier plaintexts** is a layered-simple structure that no linear-recurrence or periodic test sees. `[speculation]`: no source says Sanborn used one.
**Model.** As case 217 (`gn217`, model Q): layer letter at plaintext position i is carved at S[i]; direct = identity; forms Vig / variant / Beaufort mod 26;
key value k_i = (f(o + i) + c) mod 26 ("fwd") or (f(o + 96 − i) + c) mod 26 ("rev"). 22 open sequences S1–S22 (list in `keys233.py` header), o = 0..39,
c ∈ {0, 1}; four finite word-length streams (K1; K2; K3; all three joined; cyclic, every offset, c ∈ {0, 1}). Scopes: **direct** (86,731² keyword alphabets, `alpha.bin`),
**bank** and **all.bin** (144² themed alphabets behind the carved-position bank / all.bin permutations). Hit = ≥ 23 of the 24 crib seats agree (24 exact; 23 = one carving error, two 4-seat indexes).
Crib convention: EASTNORTHEAST at 0-based 21–33, BERLINCLOCK at 63–73 (1-based 22–34 and 64–74).
**Commands:** `gn217 K4 x alpha.bin alpha.bin keys233.bin 1 0 100000` (direct); `gn217 K4 bank.bin themed144.bin themed144.bin keys233.bin 1 0 100000`; same with `all.bin`.
**Gates.** *P*: 20 plants seed **209643** (`plant233.py`: ids 0–7 direct, 8–13 bank, 14–19 all.bin, random window/form/ix, K1–K3 English plaintext with cribs, odd ids one corrupted crib letter);
pass = ≥ 19/20 found by `gn217` with the planted (w, form, X, Y, perm) (Wilson interval reported). *T*: for every K4 / null / plant H line `check233.py` re-derives the crib agreement from scratch (mismatches must be 0).
**Null.** One shuffled K4 (`random.Random(209644).shuffle`): direct full, bank and all.bin at 1/10 of the permutation rows (stride 10) as in cases 221/222.
One null is a smoke measure of the false-hit rate, not a calibration (stated, not hidden); the family's expected chance hits are ≪ 1 by the 24-letter filter (cases 217–222: 0 hits in every null).
**Counts.** Pair-forms searched = Σ T-lines (direct ≈ 1.58 × 10¹⁴ × (4,172/7,012), bank / all.bin ≈ 2.9 × 10¹⁴ × (4,172/7,012)).

## Part B — I-342 NC bar adopted (owed by c232)
From this cycle the case-232 bar is **preregistered** for every H line that is decrypted: NC = mean log₁₀ quadgram of the decrypt over quadgrams touching **no** crib seat
(quadgram support `quadgrams.json`, sha 70c628cf…), nq = their number;
bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879, N = max(10, number of H lines decrypted in that scope).
A hit is a **candidate** only if NC ≥ bar (and the decrypt reads as English); K4 with 0 H lines is `EXACT-EXCL` for the list and needs no bar. Domain: N 10 … 5.3 M, nq 10–64; no extrapolation beyond.
**Labels:** `EXACT-EXCL` (K4 0 hits) only where the plants gate P passes **and** the null's expected hits are ≪ 1; `NO-SIGNAL` if hits exist but fail the bar and are indistinguishable from null decrypts;
`INSUFFICIENT-DISCRIMINATION` if gate P fails. Distance-to-bar / FRONTEIRA rule (PREREG232) applies to any count comparison: robust only if ≥ 2× on both sides of a fresh replicate.

## Part C — paperwork owed (no seeds)
1. **Addendum to case 217 (I-357):** bank W ≤ 10 relabelled `NO-SIGNAL-FRONTEIRA` per PREREG232's definition (upper 95 % Wilson bound of the per-text null rate over the K4 rate, computed per null set):
   Voynich's final reconciliation gives fresh set 1.01× (inside) and her 31231000+i set 1.04× (above) → FRONTEIRA; my pooled ≥ 3.4 α is descriptive only.
2. **I-358 (new log):** Voynich's I-342 replicate slope b ≈ 0.19 per e-fold (per-unit slope with nq and family fixed) vs mine ≈ 0.079 (per-text max in the joint fit with (ln N)²) are two estimands; both are documented side by side, neither is extrapolated.

## Honesty clause
Any plain-English decrypt with both cribs at the official positions and NC ≥ bar will be reported prominently *and* reproduced independently before it is called a solution. Nothing is submitted anywhere.

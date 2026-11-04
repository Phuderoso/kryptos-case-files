# Case file 53 — Ragbaby: a word-progressive key on one keyed alphabet (cycle 55)

**Why this family.** Ragbaby is a classic ACA cipher that sits right next to K1–K3's toolkit: one keyword-mixed
alphabet (like the KRYPTOS alphabet) and a key that is not a word at all but the *word structure* of the plaintext.
Letter j (0-based) of word w is shifted n0 + w + j places along the mixed alphabet, so the shift climbs by one per
letter and falls back at every word break. It is "simple, in plain sight" in exactly the sense of the user's hunch:
no key to remember, only a keyword alphabet. It was not in the repo (nor in kryptosbot's published list of tested
families as of Sept 29, 2026). New family for the coverage table (diversity rule).

**Model (exact, offset-free).** With t_i = s_i − d·i, t is constant inside a word, and at a word starting at b whose
previous word started at a, t jumps by d·(1 − (b − a)) mod 26. Word divisions are unknown, so every segmentation
of each crib is tried by depth-first search (2¹² × 2¹⁰ possibilities). The word in progress when a crib begins may
have started earlier (length capped at 20 letters, which leaves its jump almost free). The starting number n0 and
everything outside the cribs is left free, so only the 24 crib letters are used and nothing is assumed about the
rest of the plaintext. Both directions (c = A[idx p + s] and A[idx p − s]); step d = 1 (classic) and every other unit
d mod 26 as a generalisation.

**What was run.**
- **A — direct:** all 86,731 alphabets in `data/alpha.bin` (A–Z, KRYPTOS, Z–A, dictionary and themed keyword
  alphabets, two-word keyphrase alphabets), both directions, d ∈ {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}.
- **B — Ragbaby, then a transposition:** classic d = 1, both directions, 12,465 themed alphabets (A–Z/KRYPTOS/Z–A
  and every alphabet whose keyword is one of 37 Kryptos-themed words, alone or in a keyphrase; list in
  `data/cycle55/themed_idx.txt`) × the 93,334 cycle-12 transpositions on 97 letters (`data/c12_perm.bin` entries
  0–93,333, both enc/dec forms). Entries 93,334 onward are 98/100-cell grids and are not valid on 97 letters; a first
  run that read them crashed and was rerun on the valid range (noted for honesty).

**Results.**

| Test | K4 | Shuffled nulls | Planted controls |
|---|---|---|---|
| A — direct | **0** crib-consistent (crib 1 alone: 0; crib 2 alone: 0) | 5 / 5 → 0 | 4 / 4 recovered (KRYPTOS alphabet; keyword alphabet #5000 reversed direction; #20000 with d = 3; one-word-per-crib segmentation) |
| B — behind 93,334 transpositions | **0** (crib 1 alone: 0) | 3 / 3 → 0 | 2 / 2 recovered (perm #5000 with KRYPTOS alphabet; perm #77777 with A–Z, plus permutations that agree on the crib cells) |

Every hit in the controls is the planted configuration or an exact equivalent (reversed alphabet with the opposite
direction; d ↔ 26 − d with the opposite direction). The test is very strict: a random alphabet passes a 13-letter crib
with probability of roughly 26⁻¹⁰ per segmentation, which is why the nulls are all zero and why a zero for K4 is a
clean exclusion within the tested alphabets and permutations.

**Verdict.** **Negative.** Ragbaby (any word division) on any of the 86,731 alphabets is excluded for K4 directly,
and classic Ragbaby on the 12,465 themed alphabets is excluded behind the 93,334 cycle-12 transpositions.

**Still open.** Ragbaby with an *arbitrary* mixed alphabet (needs a SAT model: the per-word offset couples three
unknowns per crib letter, so union-find over differences does not apply); transposition *before* Ragbaby (word
structure would then be on scrambled text, which is unnatural); Ragbaby with J/X merged (24-letter alphabet, ruled
out structurally since K4 uses all 26 letters).

**Reproduce.** `gcc -O2 -o ragbaby tools/ragbaby.c && gcc -O2 -o ragperm tools/ragperm.c`, put `alpha.bin`,
`themed_idx.txt` and the binaries in one folder, `python3 tools/ctl55.py && python3 tools/ctl55b.py`, then
`tools/run_cycle55.sh` (≈ 3 minutes on 8 cores). Raw outputs: `data/cycle55/`.

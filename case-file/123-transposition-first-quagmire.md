# Case file 123 — Transposition-first periodic Quagmire with vocabulary alphabets (cycle 135)

**Status:** negative, exact. **Type:** new structural idea (key at the carved position: bucket the 165k-bank permutations by the official crib landings modulo the period, then test any periodic key of that length). Cycle 134 was a variant of 133, so this cycle opens the leftover index from cycles 132–134 rather than another autokey flavour.

## Question
Cycles 13 and 120 already asked whether *any* periodic key of length p ≤ 16 fits Quagmire I/II/III after a bank transposition, but only on the A–Z/KRYPTOS tableaux and 264 themed alphabets. Cycle 28 did the same for Quagmire IV with themed alphabet *pairs*. The coverage table still listed **non-themed alphabets** as open. Cycles 132–134 noted that the crib-signature hash used for model Q (key at the plaintext position, then a transposition) does not apply when the transposition comes first: the key then moves with the carving, and a different index is needed — bucket permutations by `perm[crib] mod p`.

Could K4 be a K1/K2-style periodic Quagmire (a vocabulary-keyed mixed alphabet, or one-sided Quagmire I/II) whose repeating key is applied *after* a bank transposition, at the carved position?

## Method
Each of the 330,130 permutations (both directions of the 165,065-entry bank) maps a plaintext index `i` to a carved index `j = σ(i)`. For a periodic key of length p the implied key letter at each of the 24 official cribs (`EASTNORTHEAST` at 21–33, `BERLINCLOCK` at 63–73) is read at residue `j mod p` (carved-index order) or at `i mod p` (plaintext-index / model Q). Cribs that land in the same residue class must agree on that key letter; a disagreement excludes the configuration. For p ≤ 16 the 24 cribs always give at least eight extra constraints (pigeonhole: 24 − 16 = 8), so every test in this range has power. Tool: [`tools/cycle135/carveq.c`](../tools/cycle135/carveq.c).

The bank is far from a random set of permutations, so the residue 24-tuples collide: at p = 2 there are 21,539 buckets (about 15 permutations each); at p = 3–16 the typical bucket holds three to six permutations (see [`data/cycle135/buckets.txt`](../data/cycle135/buckets.txt)). One consistency check therefore serves a whole bucket.

Search, for every vocabulary word W among 10,056 (unique letters then A–Z remainder — the K1/K2 construction):

| family | alphabets | modes | index orders | p |
|---|---|---|---|---|
| I — Quagmire I (plaintext keyed by W, cipher A–Z) | 10,056 | Vigenère (variant Beaufort is the dual and shares consistency) and Beaufort | carved (transposition first) and plaintext (model Q) | 1–16 |
| II — Quagmire II (plaintext A–Z, cipher keyed by W) | same | same | same | 1–16 |
| III — Quagmire III (both sides keyed by W) | same | same | same | 1–16 |

10,056 × 330,130 × 3 × 2 × 2 × 16 = **637,399,157,760** exact tests per text (≈6.374×10¹¹). Wall time 410 s (8 cores) for K4 plus two shuffled nulls. A survivor is re-checked against all 24 official crib letters and, when the key is fully determined, decrypted in full.

Periods 17–26 were not scanned (the pigeonhole floor drops below eight checks and cycle 13/120 already treated p ≤ 16 as the exact cutoff for this test). Quagmire IV (two *different* vocabulary alphabets) was not scanned: that is 10,056² ordered pairs, about a thousand times the themed-pair search of cycle 28.

## Results
| text | tests | consistent | survivors (checks ≥ 6; here every p ≤ 16 has ≥ 8) |
|---|---|---|---|
| K4 | 637,399,157,760 | **0** | **0** |
| null 1 (shuffled K4, seed 13501) | 637,399,157,760 | 0 | 0 |
| null 2 (shuffled K4, seed 13502) | 637,399,157,760 | 0 | 0 |

No configuration produced even a single residue-class disagreement-free key, on any family, mode, index order or period.

Controls (`plant.py`, independently encrypted in Python): 4/4 planted keys recovered, each with a full 97-letter decrypt of the English control plaintext at the true period.

1. QIII carved, alphabet PALIMPSEST, keyword ABSCISSA, Vigenère, perm 4242 (and its stored inverse 4241). The period multiple p = 16 is also reported, with one undetermined key letter.
2. QIII carved, alphabet KRYPTOS, keyword SHADOW, Beaufort, inverse of perm 99999 (stored the other way as 99998). Period multiple p = 12 likewise.
3. QI carved, plaintext alphabet BERLIN, cipher A–Z, keyword CLOCK, Vigenère, perm 160000 (inverse 159999). Period multiples p = 10 and (partial) p = 15.
4. QIII model Q (key at the plaintext position, then transpose), alphabet NORTHEAST, keyword EAST, Vigenère, perm 12345 (inverse 12346). Five other neighbouring bank mappings also satisfy the 24 crib letters for this short period-4 key, but only 12345/12346 decrypt the letters *between* the cribs to the English control plaintext.

Some neighbouring bank entries are stored inverses of each other and are reported as the other direction of the same mapping; that does not add a new key.

## What this excludes and what it doesn't
Excluded: any vocabulary-keyed Quagmire I, II or III alphabet (10,056 words) with *any* periodic key of length 1–16, Vigenère/variant or Beaufort, applied either at the carved position after a bank transposition or at the plaintext position before one, for any of the 165,065 bank transpositions (either direction).

Not excluded: periods 17–26 (weaker pigeonhole; needs a vocabulary or phrase-key completion); Quagmire IV with two different non-themed alphabets; transposition-first *autokey* (the key would no longer be periodic); running-key layers; alphabets outside the 10,056-word keyed construction; transpositions outside the bank.

## Next
Transposition-first autokey with a vocabulary Quagmire III alphabet is the sibling of this test that cycles 19 and 22 closed only on the A–Z/KRYPTOS shift tableaux, and that cycles 133–134 closed only as model Q. Quagmire IV on a themed × vocabulary slice, and periods 17–26 with a dictionary completion of the partial key, remain on the periodic side.

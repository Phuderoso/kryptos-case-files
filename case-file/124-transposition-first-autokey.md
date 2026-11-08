# Case file 124 — Transposition-first autokey with vocabulary Quagmire III alphabets (cycle 136)

**Status:** negative, exact. **Type:** variant of cycle 135 (same carved-index idea — the key is read at the position after a bank transposition — now applied to autokey rather than to a repeating periodic key). Cycle 135 was a new structural idea, so this cycle opens the leftover sibling named in that write-up.

## Question
Cycles 19 and 22 already asked whether a ciphertext- or plaintext-fed autokey of any primer length fits after (or before) a bank transposition, but only on the A–Z and KRYPTOS shift tableaux. Cycles 133 and 134 extended autokey to vocabulary Quagmire III alphabets and to phrase primers, but only as model Q (substitution at the plaintext position, then a transposition) and only for listed dictionary or phrase primers. Cycle 135 then showed how to test *any* periodic key at the carved position, by reading the 24 official cribs after the letters move. The coverage table still listed **transposition-first autokey** as open.

Could K4 be a K1/K2-style Quagmire III autokey (a vocabulary-keyed mixed alphabet, primer of any letters) whose key stream is applied *after* a bank transposition, at the carved position?

## Method
Each of the 330,130 permutations (both directions of the 165,065-entry bank) maps a plaintext index `i` to a carved index `j = σ(i)`. An autokey of lag L then reads its key at `j` (carved-index order) or at `i` (plaintext-index / model Q):

- **PT-fed:** `K[pos] = primer[pos]` if `pos < L`, else the previous plaintext letter of the autokey layer. Two cribs on the same residue class modulo L determine a chain: each step is `T[pos+L] = dec(C_layer[pos+L], T[pos])`. Extra checks = 24 − (number of occupied residues) ≥ 24 − L.
- **CT-fed:** `K[pos] = primer[pos]` if `pos < L`, else the previous ciphertext letter of the autokey layer. Each crib with key-index ≥ L is an immediate check against a known letter. Extra checks = 24 − (cribs inside the primer region) ≥ 24 − L.

For L ≤ 16 the 24 official cribs (`EASTNORTHEAST` at 21–33, `BERLINCLOCK` at 63–73) always give at least eight extra constraints, so every test in this range has power. The primer itself is recovered from the cribs rather than drawn from a word list: any primer of that length is tested. Tool: [`tools/cycle136/akcarve.c`](../tools/cycle136/akcarve.c).

Search, for every vocabulary word W among 10,056 (unique letters then A–Z remainder — the K1/K2 construction), Quagmire III (both sides keyed by W):

| feed | modes | index orders | L |
|---|---|---|---|
| PT-autokey | Vigenère, Beaufort, variant Beaufort | carved (transposition first) and plaintext (model Q) | 1–16 |
| CT-autokey | same (the three are distinct: the feedback letter is constrained, so variant is not the dual of Vigenère) | same | 1–16 |

10,056 × 330,130 × 3 × 2 × 2 × 16 = **637,399,157,760** exact tests per text (≈6.374×10¹¹). Wall time 1,186 s (8 cores) for K4 plus two shuffled nulls; K4 itself finished in 392 s and was written out as a checkpoint before the nulls. A survivor is re-checked against all 24 official crib letters and, when every autokey chain is determined, decrypted in full.

Lags 17–26 were not scanned (the pigeonhole floor drops below eight checks, matching the cutoff of cycles 13, 120 and 135). Quagmire I/II (one-sided mixed alphabets) and Quagmire IV (two different mixed alphabets) autokey were not scanned.

## Results
| text | tests | consistent | survivors (checks ≥ 6; here every L ≤ 16 has ≥ 8) |
|---|---|---|---|
| K4 | 637,399,157,760 | **0** | **0** |
| null 1 (shuffled K4, seed 13601) | 637,399,157,760 | 0 | 0 |
| null 2 (shuffled K4, seed 13602) | 637,399,157,760 | 0 | 0 |

No configuration produced even a single crib-consistent primer, on any feed, mode, index order or lag in range.

Controls (`plant.py`, independently encrypted in Python): 4/4 planted keys recovered.

1. QIII carved PT-autokey, alphabet PALIMPSEST, primer ABSCISSA, Vigenère, perm 4242 (and its stored inverse 4241). Full 97-letter English decrypt.
2. QIII carved CT-autokey, alphabet KRYPTOS, primer SHADOW, Beaufort, inverse of perm 99999 (stored the other way as 99998). 23 crib checks pass; the primer is only partly determined (`?????W`) because ciphertext-fed autokey cannot name a primer letter unless a crib lands on that key index. The decrypt is the English control plaintext with '?' at the few letters whose carved positions fell inside the primer region; both official cribs sit in place.
3. QIII carved PT-autokey, alphabet BERLIN, primer CLOCK, variant Beaufort, perm 160000 (inverse 159999). Full English plaintext restored.
4. QIII model Q PT-autokey (key at the plaintext position, then transpose), alphabet NORTHEAST, primer EAST, Vigenère, perm 12345 (inverse 12346). Seven other neighbouring bank mappings also satisfy the 24 crib letters for this short lag-4 primer; only 12345/12346 decrypt the letters *between* the cribs to the English control plaintext.

Some neighbouring bank entries are stored inverses of each other and are reported as the other direction of the same mapping; that does not add a new key.

## What this excludes and what it doesn't
Excluded: any vocabulary-keyed Quagmire III alphabet (10,056 words) with *any* primer of length 1–16, plaintext-fed or ciphertext-fed, Vigenère, Beaufort or variant Beaufort, applied either at the carved position after a bank transposition or at the plaintext position before one, for any of the 165,065 bank transpositions (either direction).

Not excluded: lags 17–26 (weaker pigeonhole); Quagmire I/II autokey (one-sided mixed alphabets); Quagmire IV autokey (two different mixed alphabets); listed phrase primers longer than 16 combined with a transposition-first reading (cycle 134 already closed those as model Q); running-key layers; alphabets outside the 10,056-word keyed construction; transpositions outside the bank.

## Next
Quagmire I/II autokey (the one-sided siblings of this test) and Quagmire IV autokey on a themed × vocabulary slice would close the remaining mixed-alphabet autokey gap. Because this cycle was a variant, cycle 137 should open a new family or structural idea — Quagmire IV autokey (two different mixed alphabets feeding the same primer stream, both index orders) is the leftover that cycles 28 (periodic themed pairs only) and 136 (same alphabet both sides) did not touch.

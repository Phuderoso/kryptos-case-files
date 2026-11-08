# Case file 127 — Plaintext-fed autokey with a free plaintext alphabet, tested on crib-to-crib links (cycle 139)

**Status:** negative, exact within its reach. **Type:** new structural idea (cycle 138 was a variant). It opens the plaintext-fed side of the free-alphabet autokey that case files 125 and 126 left open.

## Question
Cycles 137–138 left the plaintext alphabet free, but only for the ciphertext-fed autokey, where the key letter is always known. In a plaintext-fed autokey the key letter is an earlier **plaintext** letter, usually unknown. Is there any part of that system we can test exactly with all 26! plaintext alphabets?

## The trick
Use only the positions where the key letter is itself a crib: `j` and `j−L` both inside EASTNORTHEAST (21–33) or BERLINCLOCK (63–73), or one in each. There every quantity is known except the alphabet values:

- Vigenère `y(c_j) = x(p_j) + z(p_{j−L})`, Beaufort the same under `x → −x`, variant `y(c_j) = x(p_j) − z(p_{j−L})`.
- `z` ∈ {`y`, A–Z, KRYPTOS}: `x(p_j)` is computed outright, and the values must form a permutation (Quagmire II/III/IV PT-autokey with any second alphabet).
- `z = x` (key read through the plain alphabet): a system of two-variable equations mod 26, solved exactly as in case file 126.

The primer and every letter outside the cribs drop out.

## Reach
In the plaintext order (direct, and model Q behind a transposition) the number of independent checks by lag is: L 1 → 10, L 2 → 8, L 3 → 6, L 4 → 4 (5 with `z = x`), L 9 → 4 with `z = x` only, and at most 2 for every other lag. So the test has real power only at **lags 1–4**. In the carved order (transposition first) the links depend on the permutation; columnar-like bank entries keep many links (up to 22 at a single lag), so every lag 1–96 with at least 5 checks was tested.

**A trap I hit and fixed.** In the `z = x` Vigenère form, a cycle of odd length (including a self-loop such as E keyed by E) gives `2·x = k (mod 26)`: a 1-bit parity check, not a 1-in-26 check. Counting them as full checks produced a flood of K4 "hits": 1,426 direct at L 9 (the self-loops E–E, A–A, S–S, T–T, where K4's `SS` at 32–33 lines up against plaintext `ST`) and 2,358 behind the bank, against 1–2 and 36/147 for the nulls. They are an artifact of K4's letter repeats and not a signal. The final runs weigh each check by its information (even cycle ≈ 4.7 bits, odd cycle 1 bit) and require 23.5 bits behind the bank (18.8 direct).

## Search
Tool: [`tools/cycle139/ptfree.c`](../tools/cycle139/ptfree.c).
- **Direct:** all 10,057 alphabets (10,056 words + A–Z), 4 key readings × 2 forms, every lag with ≥ 4 checks: 341,938 exact tests.
- **Behind the bank:** 165,065 entries × 2 directions, model Q and carved, every lag 1–96 with ≥ 5 checks, 601 alphabets (97 themed words, A–Z, 503 more): **6,958,721,772 exact tests**, 79 s on 8 cores.
- **Nulls:** two shuffled K4 texts (seeds 13901–13902), direct in full and on every tenth bank entry.

## Results
| text | tests | hits |
|---|---|---|
| K4, direct | 341,938 | **0** |
| nulls, direct | 341,938 each | 0 |
| K4, behind the bank | 6,958,721,772 | **1** (bank duplicate pair, counted twice) |
| null 1 (1/10 of the bank) | 695,531,290 | 0 |
| null 2 (1/10 of the bank) | 695,531,290 | 0 |

The single K4 hit (PEQUOD cipher alphabet, key through KRYPTOS, Vigenère, carved order, L 27, bank entry 107127/107128, exactly 5 checks) extends the cribs by only two letters and gives nothing readable: `????????????????????lEASTNORTHEAST??…??BERLINCLOCK????n???…`. One hit of that strength in 7×10⁹ tests is about what chance predicts (13 distinct values must also be all different, probability ≈ 1.6×10⁻³). I log it and close it.

## Controls
Independently encrypted in Python ([`plant.py`](../tools/cycle139/plant.py)), each with a random plaintext alphabet and a random primer:
- ctl1 direct, y = z = PALIMPSEST, Vigenère, L 4 (4 checks): found.
- ctl2 model Q, y = KRYPTOS, z = A–Z, variant, L 3, entry 4242: found.
- ctl4 direct, y = CLOCK, z = x, Beaufort-type difference, L 3: found (28.2 bits).
- ctl5 model Q, y = SHADOW, z = KRYPTOS, Vigenère, L 2, entry 160000: found.
- ctl6 carved, y = BERLIN, z = x, difference form, L 6, inverse of entry 99999: found (23.5 bits).
- ctl3 carved, y = BERLIN, z = x, **sum** form, L 6: found only without the bit filter (8.7 bits); it is below the strength threshold by design and documents the weak form.
- An earlier draft control at L 7 (1 check) and one at L 40 (2 checks) were untestable and were replaced; that is the reach limit above, not a failure.

## What this closes
Plaintext-fed autokey with a keyed cipher alphabet from the vocabulary and **any** plaintext alphabet, key read through the cipher alphabet, A–Z, KRYPTOS or the plain alphabet itself, any primer: excluded **direct** at lags 1–4 for all 10,057 alphabets (and L 9 for `z = x`); excluded behind the 330,130 bank permutations in plaintext order at lags 1–3 (1–4 for the difference form with `z = x`), and in carved order at every lag where the permutation keeps ≥ 5 checks, for the 601 leading alphabets.

## Still open
- PT-autokey with free plain alphabet at lags 5–96 in plaintext order (fewer than 4 checks; untestable this way).
- The `z = x` sum form with mostly odd cycles (weak checks).
- The remaining ~9,450 alphabets behind the bank.

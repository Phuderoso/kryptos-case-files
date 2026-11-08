# Case file 128 — PT-autokey with a free plain alphabet, behind the bank, alphabets 601–3600

**Cycle 140, 2026-11-08. Variant of cycle 139 (case file 127).**

## What was tested

Same model as case file 127: plaintext-fed autokey where the key letter at a crib position is
itself a crib letter, so the primer and every unknown plaintext letter drop out and only the
cipher alphabet, the free plaintext alphabet and the lag remain. The key letter is read through
the cipher alphabet (y), plain A–Z, the KRYPTOS alphabet, or the free plain alphabet (x).
Vigenère, Beaufort-style and variant forms; every lag that gives at least 5 crib-to-crib checks.

Cycle 139 covered the first 600 vocabulary alphabets behind the bank. This cycle covers the
next 3,000 (words 601–3600 of `all.txt`), behind all 165,065 bank entries used both ways
(330,130 permutations), carved order (transposition first) and model Q.

- K4: 3.47 × 10¹⁰ exact tests in 356 s on 8 cores.
- Nulls (two shuffled K4s from cycle 139's `plant.py`): every 10th bank entry, 72 s.

## Result

| Text | Bank share | Hits (lines) | Distinct configurations |
|---|---|---|---|
| K4 | full | 20 | 10 (each a bank duplicate pair q, q+1) |
| null 1 | 1/10 | 1 | 1 |
| null 2 | 1/10 | 2 | 2 |

Most bank configurations appear twice (entries q and q+1 are often inverse duplicates), so a
1/10 sample catches a given configuration about 2 times in 10; scaled to the full bank the nulls
expect roughly 5–10 distinct configurations each. K4's 10 is in that range: chance level. All K4
hits sit at the minimum (9 at 5 checks, 1 at 6: ALONGSIDE, A–Z key alphabet, carved, lag 14),
all are carved order, and none decodes more than a few scattered extra letters.
Survivor list: `data/cycle140/survivors.txt`.

**Negative.** K4 behaves like a shuffled text under this model for these 3,000 alphabets.

## Audit note (parity checks)

Cycle 139 found that odd cycles in the sum form carry only 1 bit. Case file 126 (cycle 138)
counted "cycles" including odd ones when describing well-constrained configurations; its
satisfiability result was exact and is unaffected, but its "cycle count" is an overstatement of
constraint strength wherever odd cycles occurred. Read that file's limits as applying to the
even-cycle count.

## Limits

Words 3601–10,056 behind the bank remain open for this model (about 13 minutes of compute at
this rate). Lags with fewer than 5 checks stay untestable, as before.

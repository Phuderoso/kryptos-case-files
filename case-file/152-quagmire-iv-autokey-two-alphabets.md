# Case file 152 — Quagmire I/II/IV autokey with two different keyed alphabets (cycle 164)

**Status:** negative. Exact (`EXACT-EXCL`) for the direct cipher at every lag with ≥ 7 checks and for the sampled 1/40 of the
bank; `LOW-POWER` at direct PT-fed lags 24–26. The full-bank pass was stopped unfinished at the compute budget, so 39/40 of the
bank is **not** covered (queued as I-074). **Type:** new family (cycle 163 was an audit). IDEAS **I-015**.


> **Correction (cycle 165, 2026-11-09).** The full K4 bank pass did **not** stop unfinished: all 8 slices and the done marker were written by 00:00:04 PDT, before the stop at 00:00:14, and they show **0 consistent configurations** over all 1,205,074,859,520 tests. The stop killed only the null phase. Themed × themed behind the whole bank is therefore `EXACT-EXCL`, re-run independently on 1/8 with nulls 0 in 6 — see [case file 153](153-quagmire-autokey-bank-completion.md).

## Why I-015 and not I-014
The queue offered two autokey items. I checked both against the case files first ([`data/cycle164/overlap.txt`](../data/cycle164/overlap.txt)):

- **I-014, CT-autokey with both alphabets free**, is mostly a repeat. Direct lags 1–35 are already SAT-impossible
  ([case 11](11-sat-families-and-phrase-alphabets.md), F5). With a free plaintext alphabet and the key read through a known
  alphabet, cycle 137 excluded it behind the bank ([case 125](125-ct-autokey-free-plain-alphabet.md)), and cycle 138 handled the key read
  through the free alphabet ([case 126](126-ct-autokey-key-through-plain-alphabet.md)). What is left is weak (direct lags 36–49) or
  expensive (one SAT problem per permutation). I narrowed it and kept it queued.
- **I-015, Quagmire I/II/IV autokey with two keyed alphabets**, is the gap that [case 124](124-transposition-first-autokey.md) named.
  Cycle 136 did Quagmire III (one alphabet on both sides). Cases 127–137 left the plaintext alphabet free, which works only for
  crib-to-crib links and has power only at lags 1–4. With **both** alphabets keyed (known), a plaintext-fed chain can run through
  the carved letters between the cribs. So every lag up to 16 gets at least 8 checks.

## Model
Plain alphabet X, cipher alphabet Y (X ≠ Y), with the key letter read through Z ∈ {X, Y} (the two Quagmire IV conventions; Y = A–Z gives
Quagmire I, X = A–Z Quagmire II):

| form | encryption at key index q |
|---|---|
| Vigenère | `c = Y[x(p) + z(k)]` |
| Beaufort | `c = Y[z(k) − x(p)]` |
| variant | `c = Y[x(p) − z(k)]` |

PT-fed: `k_q` = layer plaintext at `q − L`. CT-fed: `k_q` = layer ciphertext at `q − L`. Any primer of length L works. Key index:
the plaintext index (substitution, then transposition: model Q) or the carved index (transposition first).
Tool: [`tools/cycle164/q4ak.c`](../tools/cycle164/q4ak.c). It uses one 26×26 decryption table per (pair, Z, form). PT-fed checks
follow the chain `p → D[c][p]` from one crib to the next crib in the same residue class. Each step is a bijection, so each check
passes by chance with probability 1/26. CT-fed checks are `D[c_q][c_{q−L}] = p` at every crib with q ≥ L.

## Search
| part | alphabets | settings | tests per text |
|---|---|---|---|
| direct (no transposition) | themed (98 incl. A–Z) × vocabulary (9,395 distinct incl. A–Z), **both ways** (X themed or Y themed) | 2 Z × 3 forms × PT/CT × L 1–26 | 609,922,560 |
| behind the bank, **sample** | themed × themed, 9,506 ordered pairs X ≠ Y | 2 Z × 3 forms × PT/CT × 2 index orders × L 1–16, every 40th bank entry × 2 directions (8,254 permutations) | 30,129,609,216 |

Texts: K4. Direct: two shuffled nulls (seeds 16401–16402) and 20 profile-matched nulls (cycle-157 generator, seeds from 16,410,000,
crib-letter profile 3-2×8-1×5). Bank sample: the two shuffled nulls on the same entries.

## Results
| part | K4 | nulls | label |
|---|---|---|---|
| direct, CT-fed, L 1–26 (24 checks each, or fewer only when cribs fall inside the primer) | **0** consistent | 0 in all 22 | `EXACT-EXCL` |
| direct, PT-fed, L 1–23 (≥ 7 checks) | **0** | 0 (one null had 1 at L 18) | `EXACT-EXCL` |
| direct, PT-fed, L 24 (5 checks) | 1 | 0–4, median 0 (9/22 ≥ K4) | `LOW-POWER` |
| direct, PT-fed, L 25 (3 checks) | 765 | 182–1,338, median 683 | `LOW-POWER` |
| direct, PT-fed, L 26 (1 check) | 534,341 | 333,262–701,676, median 450,099 (1/22 ≥ K4) | `LOW-POWER` (not anomalous after 26 lags × 2 feeds) |
| bank sample 1/40, all feeds/forms/orders, L 1–16 (≥ 8 checks) | **0** consistent | 0 and 0 | `EXACT-EXCL` (sampled entries only) |
| bank, remaining 39/40 | not run | — | open → I-074 |

Power: with at least 8 independent 1/26 checks, chance consistency per test is ≤ 26⁻⁸ ≈ 4.8 × 10⁻¹². The expected chance count is
about 0.14 on the bank sample and close to 0 for the direct lags ≤ 23. So 0 is what both K4 and the nulls should show, and the planted
keys show that a real configuration does get through. No K4 configuration with ≥ 6 checks survived, so there was nothing
to decrypt or score as English. The one null survivor (mnull08, L 18, 7 checks) decrypts to noise outside the cribs
(`SG?WKKANWRQYVIULZAQP?EAST…`), as expected for chance.

Per-lag counts: [`direct_summary.txt`](../data/cycle164/direct_summary.txt); bank sample:
[`bank_sample_C_H.txt`](../data/cycle164/bank_sample_C_H.txt).

## Controls
Six planted controls ([`plant164.py`](../tools/cycle164/plant164.py)), each encrypted independently in Python with string alphabets.
All **6/6** were recovered, all 24 crib letters were checked, and the decrypts are the English control text:

1. QIV PT-fed, X SHADOW, Y PALIMPSEST, Z = Y, Vigenère, primer LUCID, carved, perm 4242. Full plaintext.
2. QIV PT-fed, X BERLIN, Y CLOCK, Z = X, Beaufort, primer ILLUSION, model Q, inverse of 99999. Full plaintext.
3. QI PT-fed, X KRYPTOS, Y A–Z, variant, 14-letter primer, carved, perm 160000. Partial: the residues with no crib stay `?`.
4. QII CT-fed, X A–Z, Y ABSCISSA, Z = Y, Vigenère, primer NUANCE, carved, inverse of 12345. Partial (primer region).
5. QIV PT-fed, X TOMB, Y VERDIGRIS, Z = X, Vigenère, primer QX (L 2), model Q, perm 777. Full plaintext. A second hit, carved L 12
   on the same entry, is the same encryption seen through the permutation's column structure: a partial English decrypt, not a false positive.
6. QIV PT-fed direct, X EGYPT, Y ZEBRAFISH (not in the vocabulary), Z = Y, Beaufort, primer MAGNETICFIELDSX (L 15, 9 checks). Full plaintext.

Independent recount ([`recount164.py`](../tools/cycle164/recount164.py)): a brute-force Python walk of each residue class, with no tables and
no sorting. On 4 × 5 alphabets, bank entries 100–102 (K4) and 5000–5002 (null 1), both directions and both orders, L 1–40, all
**48/48** histogram rows × 40 lags match the C tool exactly (3,733 and 2,012 consistent configurations,
[`recount.txt`](../data/cycle164/recount.txt)).

## What this excludes and what it doesn't
Excluded: a Quagmire I, II or IV autokey (PT- or CT-fed, any primer, Vigenère/Beaufort/variant, key read through either alphabet)
with one themed alphabet and one vocabulary alphabet, applied directly to K4, at lags 1–23 (PT) and 1–26 (CT). Also excluded:
any themed × themed pair at lags 1–16, either index order, on the 1/40 sample of the bank.

Not excluded: the other 39/40 of the bank (the full pass was stopped at the budget; I-074); themed × vocabulary pairs behind the
bank (I-074); vocabulary × vocabulary pairs (88 M pairs); direct PT-fed lags 24–26 (`LOW-POWER`); lags 17–26 behind the bank;
alphabets outside the keyed-word construction; one-error tolerance (the I-073 shortcut applies: I-076).

## Method note
The full-bank K4 pass ran 6 min 07 s and was stopped unfinished. The tool streams 38 MB of tables per permutation, so it is
memory-bound, and it writes only at the end. Before a full-bank rerun it needs permutation blocks (tables reused across
a block of ~256 permutations) and per-slice checkpoints. Logged in [`timing.txt`](../data/cycle164/timing.txt).

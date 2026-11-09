# Case file 140 — Zig-zag autokey with a free (word-keyed) form sequence and a progressive shift (cycle 152)

**Cycle 152, 2026-11-08. New family/structure** (IDEAS [I-011](../IDEAS.md); limits of [case 138](138-zigzag-autokey.md)).

## Why this item
Cycle 150 tested the zig-zag autokey only with fixed form cycles of length 2–3. Its own *Not covered* list named the natural hand-cipher version: the
clerk reads the direction (Vigenère / Beaufort / variant) from the letters of a **keyword** (KRYPTOS, PALIMPSEST, ABSCISSA…), and possibly also steps the
shift each letter (progressive). I chose I-011 over I-012 (Hill with a key before the matrix) because it is the higher-priority card (P1), it is the direct
continuation of an open "not covered" line, and — the decisive point — it admits a clean **exact superset test** that is cheaper than enumerating words,
one-error tolerant, and well powered. I-012 stays queued.

## Model (`tools/cycle152/zigfree.c`)
At stream position j: `c_j = s + d·j + a_F·p_j + b_F·f_j (mod 26)` with F_j ∈ {V (+1,+1), B (−1,+1), X (+1,−1)}; feed `f_j = c_{j−L}` (CT autokey) or
`p_{j−L}` (PT autokey), L = 1–96, arbitrary primer; progressive step d = 0–25 (d = 0 is the plain zig-zag); one global shift s; A–Z or KRYPTOS numbering.
Directly on the copper and behind all 165,065 bank permutations in both directions, both layer orders (model Q and carved order, as in cycle 150).

**The superset trick.** Instead of enumerating words, the form at each crib position is left **free**. Each crib then admits at most three shifts; a true
configuration needs one shift s admitted by every eligible crib. Any word-keyed form sequence — any word of any length, letter value mod 3 or mod 2 under any
residue→form map, A–Z or KRYPTOS letter values, any phase — and every fixed cycle of any length is a special case. So zero free-form survivors excludes all
of them at once, including words outside any wordlist. A chance configuration matches each crib with probability ≈ 3/26, so the test stays sharp
(expected maximum ≈ 15 of 24 over 4.6 × 10⁹ configurations; a true key gives 24).

**One error.** One wrong crib letter breaks one equation; one wrong carved letter breaks at most two with a CT feed (its own crib and the crib that uses it
as feed). The counter records configurations with m = n, n − 1 and n − 2.

## Controls (`data/cycle152/controls_check.txt`, independently checked)
Seven planted word-keyed encryptions of the English control text (encrypted in Python by `plant.py`):
KRYPTOS mod 3 direct; PALIMPSEST mod 2 (V/B) direct, KRYPTOS numbering, d = 3, L = 7; ABSCISSA mod 3 behind entry 4242 (model Q); BERLIN mod 2 (B/X) behind
entry 120000, carved order, d = 11, L = 13; SHADOW mod 3 behind the inverse of entry 99999, d = 1; IQLUSION mod 3 PT feed L = 40, d = 5; LAYERTWO mod 3
with **one corrupted carved letter** inside EASTNORTHEAST.
- zigfree finds each planted configuration as the **only** survivor at its floor: 24/24 (21/21 where n = 21), PT 11/11, and **22/24 for the corrupted
  control** (two equations broken, exactly as modelled).
- `check.py` (pure Python, no C code) takes each survivor's crib form pattern, finds the consistent words in the 10,056-word vocabulary, re-decrypts the
  whole text and compares with the planted plaintext: **7/7 recovered** with the right word, map and numbering (CT-feed controls 84–96 of 84–96
  decrypted letters correct, the corrupted control 92/94; the PT-feed control is crib-consistent only, as a PT feed with an unknown primer only
  decrypts letters chained from the cribs).

## Results (`data/cycle152/results.txt`; 4.58 × 10⁹ configurations per text behind the bank, 1.37 × 10¹⁰ in total, ~4 min wall on 8 workers)
| | K4 | null 1 | null 2 |
|---|---|---|---|
| Direct, CT feed, best m (n = 24) | 10 | 10 | 10 |
| Bank, CT feed, best m (all n) | 15 | 15 | 15 |
| Bank, CT feed, configs with m ≥ 14 / 15 | 162 / 16 | 184 / 8 | 136 / 10 |
| Bank, CT feed, m = n with n ≥ 12 (exact survivors) | **0** | 0 | 0 |
| Bank, CT feed, m = n − 1 with n ≥ 12 (one wrong crib letter) | **0** | 0 | 0 |
| Bank, CT feed, m = n − 2 with n ≥ 14 (one wrong carved letter) | **0** | 0 | 0 |
| Bank, CT feed, m = n at n = 8–11 (long lags) | n8 18, n10 4 | n8 12, n9 6, n10 2 | n8 8, n10 2 |
| Bank, PT feed, m = n at n = 7 / 8 / 9 | 172 / 26 / 2 | 254 / 18 / 2 | 324 / 22 / 2 |

K4's numbers sit inside the null range everywhere. Its two n = 9 PT-feed lines (`data/cycle152/survivors.txt`) are a mirrored pair of the kind both nulls
also produce (two each) and carry no plaintext beyond the cribs.

## Verdict
- **CT feed with n ≥ 12 eligible cribs** (all lags L ≤ 33 in direct / model Q; the corresponding lags in carved order): `EXACT-EXCL` — no free form sequence,
  hence **no word-keyed or arbitrary-length zig-zag**, with or without a progressive step d = 0–25, fits K4 directly or around the 165k bank; this holds
  **even with one wrong crib letter, and with one wrong carved letter for n ≥ 14**. Nulls give 0 at the same scale, so the test is not starved — it fires
  only on the planted keys.
- **CT feed at long lags (n ≤ 11)** and **every PT-feed configuration**: `LOW-POWER` — full crib agreement at n 7–11 happens by chance at the same rate in
  shuffled text, so these cannot be told apart from K4 by cribs alone (this is the same structural blindness as the ordinary PT autokey in cycles 22–23).
- Overall: **negative**; the fixed-cycle result of cycle 150 is now extended to all form sequences.

## Scope and blind spots
- Forms limited to the three additive tableau forms; no other multipliers (affine zig-zag) and no keyed mixed alphabets (Quagmire-style zig-zag) — only
  the tableau numbering A–Z / KRYPTOS.
- One global shift plus a **linear** progressive step d·j in stream order. A periodic key on top of the zig-zag, a step per keyword lap, or a non-linear
  step is not covered.
- Transpositions only from the 165k bank (plus identity).
- One-error tolerance covers substitutions only; a dropped or extra carved letter (alignment shift) is not covered. Two errors not tested.
- PT feed and long-lag CT feed are LOW-POWER (above); covering them needs language scoring of the non-crib text (IDEAS I-029).
- The free-form model makes any survivor's non-crib forms undetermined; a survivor would have needed a word to fix them (`check.py` does this). None arose.

## Community check (2026-11-08)
No new technical finding versus cycle 151. New items since then are secondary summaries only (e.g. relatablehistory.com, 4 Nov 2026, recapping the 2025
auction, the Smithsonian find by Kobek and Byrne and Paradigm's June 2026 stewardship and $1 hash checker). Public status: K4 unsolved; no published plaintext.

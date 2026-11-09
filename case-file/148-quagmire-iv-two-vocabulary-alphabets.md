# Case file 148 — Quagmire IV with two different vocabulary alphabets (cycle 160)

**Status:** negative. `EXACT-EXCL` for every period that has power; `NO-SIGNAL` / `LOW-POWER` above it. **Type:** new family
(IDEAS [I-010](../IDEAS.md)); cycle 159 was an audit, so this cycle had to open untested ground.

## Question
K1 and K2 use one keyed alphabet on both sides of the tableau (Quagmire III). Quagmire IV uses a *different* keyed alphabet on
each side. Could K4 be a periodic Quagmire IV whose two alphabets are keyed by two ordinary words, applied directly to the copper
or before or after one of the 165,065 bank transpositions?

## What was already covered (measured first, `overlap160.py`)
| earlier test | what it covered | share of the 88,237,842 ordered vocabulary pairs (PA ≠ CA) |
|---|---|---|
| [case 11](11-sat-families-and-phrase-alphabets.md) SAT, direct | *any* alphabet pair, p 1–7, 9–12, 14, 15 (and 17, 18, 21, 22, 25) | 100 % at those periods; **p 8, 13, 16, 19, 20, 23, 24, 26 open** |
| case 11 phrase hash join, direct | one side a keyed K1–K3 substring / listed phrase | 4.4 % (209 of the 9,394 vocabulary alphabets are in the phrase set) |
| [case 27](27-quagmire-iv-behind-transposition.md), behind the bank | 268 themed alphabets paired, p ≤ 16 | 0.0099 % (94 vocabulary alphabets are themed) |
| [case 123](123-transposition-first-quagmire.md), behind the bank | PA = CA (Quagmire III), and Quagmire I/II | 0 % of PA ≠ CA |

So behind the bank 99.99 % of the vocabulary pair space was new; directly on the copper only p 8, 13, 16 (and ≥ 19) were new.

## Method (`tools/cycle160/q4v.c`)
- **Alphabets:** the 10,056-word vocabulary ([`data/cycle158/vocabulary_all.txt`](../data/cycle158/vocabulary_all.txt)), each keyed
  on A–Z (K1/K2 construction); 9,394 distinct alphabets, every ordered pair with PA ≠ CA.
- **Cipher:** `c = CA[PA⁻¹(p) + k]` (Vigenère; variant Beaufort is the dual and shares consistency) or `c = CA[k − PA⁻¹(p)]`
  (Beaufort), key of **any letters** with period p.
- **Layers:** directly on the copper (p 1–26), and behind every bank permutation in both directions (330,130), with the key at the
  plaintext index (model Q: substitute, then transpose) or at the carved index (transpose first), p 1–16.
- **Exact test:** cribs in one residue class must give the same key value, i.e. `CA⁻¹(c_a) − CA⁻¹(c_b) = ±(PA⁻¹(p_a) − PA⁻¹(p_b))`
  for every same-class pair. An alphabet-free prefilter (equal cipher letters ⇔ equal plain letters inside a class) kills 62 % of
  configurations; the rest are solved by a hash join over all PA × CA pairs, so every one of the 88.2 million ordered pairs × 2 modes
  is tested for each of the 10,564,160 configurations per text (≈ 1.9 × 10¹⁵ implied pair tests per text). Identical constraint
  lists are cached (1.54 M joins for K4).
- **One error, direct only:** leave each of the 24 cribs out in turn (one wrong crib letter, or one wrong carved letter under a
  crib; a wrong carved letter elsewhere cannot break a periodic substitution test).
- **Texts:** K4; four shuffled-K4 nulls (seeds 16001–16004) for the bank run; for the direct run also 20 nulls matched to K4's
  crib-letter repetition profile (cycle 157 generator, seed base 16010000), since the direct prefilter depends exactly on that profile.
- **Language check:** every match is decrypted with the crib-fixed key letters and scored (mean log10 quadgram).

Wall time: 261 s for the main run (8 cores), plus 7 s controls and 70 s independent recount (≈ 5.7 min total).

## Controls (`plant160.py`, independent Python encryption; [`controls_out.txt`](../data/cycle160/controls_out.txt))
| plant | layer | recovered |
|---|---|---|
| ctl1 LANTERN → HARBOR, Vig, key QUARTZ (p 6) | carved index, perm 4242 | yes, only that perm (both stored directions), p 6 and multiple 12; full decrypt −4.19 |
| ctl2 VELVET → MERIDIAN, Beau, key SHADOWS (p 7) | model Q, inverse of perm 99999 | yes at p 7 (and 14); the other hits are p 16 chance pairs (m = 8) |
| ctl3 MERIDIAN → LANTERN, Vig, key LODESTAR (p 8, a SAT-open period) | direct | yes, unique at p 8 (and 16) |
| ctl4 HARBOR → VELVET, Beau, 13-letter key (p 13) | carved index, inverse of perm 120000 | yes; 7 other CA words tie because they place the touched cipher letters identically (crib-indistinguishable) |
| ctl5 HARBOR → QUARTZ, Vig, key COMPASS (p 7), carved letter 27 altered | direct, one error | strict: no hit at p ≤ 16; dropping crib 6 (or its class partner crib 19) recovers it; decrypt shows the altered letter (EASTNO**J**THEAST) |

Independent recount (`indep160.py`, brute force over all PA × CA, no prefilter or hashing): **24 / 24** configurations agree
([`recount.txt`](../data/cycle160/recount.txt)) — 7 K4 survivor configs, 4 null configs (one with 43 matches), 3 control plants,
6 random K4 zero configs (a weak check, most configs are zero), 4 direct counts.

## Results ([`summary.txt`](../data/cycle160/summary.txt), [`decode.txt`](../data/cycle160/decode.txt))
Behind the bank — configurations with ≥ 1 Quagmire IV pair / number of pairs (330,130 per cell):

| index, p | K4 | null 1 | null 2 | null 3 | null 4 | verdict |
|---|---|---|---|---|---|---|
| model Q, p 1–14 | **0** | 0 | 0 | 0 | 0 | `EXACT-EXCL` |
| model Q, p 15 | 12 / 14 | 12 / 12 | 8 / 8 | 6 / 6 | 8 / 10 | inside null range → `NO-SIGNAL` / `LOW-POWER` |
| model Q, p 16 | 202 / 254 | 200 / 1,274 | 286 / 428 | 306 / 326 | 252 / 352 | inside null range → `NO-SIGNAL` / `LOW-POWER` |
| carved, p 1–15 | **0** | 0 (p 15: 4 / 4) | 0 | 0 | 0 | `EXACT-EXCL` |
| carved, p 16 | 12 / 18 | 32 / 42 | 10 / 10 | 14 / 16 | 14 / 18 | inside null range → `NO-SIGNAL` / `LOW-POWER` |

All 286 K4 matches (p 15–16) were decrypted: best −6.65 per quadgram including the cribs (−7.41 off-crib), e.g.
`YRTSHLLMXOKRWTQWORKOK…` (COMRADES → ACTING, Beaufort, p 16). The nulls' best: −6.60 to −6.78 (off-crib −7.27 to −7.57).
The planted English decrypts score −4.1 to −4.3. Nothing reads as English.

Directly on the copper (identity):
| | K4 | 24 nulls (4 shuffled + 20 profile-matched) |
|---|---|---|
| strict, p 1–23 | **0** (incl. the SAT-open p 8, 13, 16, 19, 20, 23) → `EXACT-EXCL` | first pairs at p 17 (1 null), 23 (1), otherwise 24–25 |
| strict, p 24 | 13 pairs | 0–22 → `LOW-POWER` (p 24–26 have almost no checks) |
| one error (any one crib dropped), p 1–23 | **0** → `EXACT-EXCL` (one-error) | p ≤ 16: 2 of 24 nulls; p 17–23: all 24 nulls (2–24 drop-configs) |

A side note, not a claim: under one error K4 has no pair at p 17–23 while every null has some. It was noticed after the fact, it
points the *wrong* way for a hidden solution (a real one would add pairs), and it most likely reflects where K4's repeated cipher
letters sit under the cribs (the prefilter kills such configurations outright).

## What this excludes
A periodic Quagmire IV — any key of length 1–14 (both index orders) or 15 (carved index) — with plaintext and ciphertext
alphabets keyed by two different words of the 10,056-word vocabulary, Vigenère/variant or Beaufort, directly on the copper or before
or after any of the 165,065 bank transpositions in either direction; directly on the copper for any key length 1–23, also under one
wrong crib letter or one wrong carved letter.

## What it does not exclude
- Behind the bank: p 15 (model Q) and p 16 (both orders) — chance survivors at K4's scale, decoded, gibberish; p ≥ 17 not run.
- One error behind the bank (not run; 24× cost) → [I-064](../IDEAS.md).
- Alphabets keyed on the KRYPTOS order, phrase (two-word) alphabets or reversed keyed alphabets behind the bank → [I-065](../IDEAS.md).
- Transpositions outside the bank; non-periodic keys (autokey: I-015, cases 124–126).

## Next
Cycle 161 may be a variant or audit: I-062 (finish the cycle-159 lineup, ~6 min) or I-064 sampled on p ≤ 12.

# Case file 160 — Quagmire IV behind K3's decimation law and spiral/diagonal routes (cycle 172)

**Status:** negative. **Type:** new family behind this transposition structure (cycle 171 was an audit). IDEAS [I-095](../IDEAS.md), Quagmire IV part.
K1 and K2 use one keyed alphabet on both sides of the tableau (Quagmire III). Quagmire IV uses a *different* keyed alphabet on each side.
K3 is a transposition that follows a decimation law. This cycle asks whether K4 = a periodic Quagmire IV with two word-keyed alphabets,
put before or after a K3-style decimation or a spiral/diagonal route. Since cycle 170, the coverage row "Decimation" had listed this as open.

**Result in one line:** 0 Quagmire IV pairs for K4 at p 1–14 in both layer orders. The test covers every ordered pair of 18,776 word-keyed
alphabets (vocabulary keyed on A–Z **and** on the KRYPTOS order, plus A–Z and KA), any key letters, Vigenère/variant and Beaufort,
behind 165,782 decimations/routes → **`EXACT-EXCL`**. At p 15–16 the counts sit on the analytic chance line and inside 8 shuffled nulls. Those
decrypts are gibberish (**`LOW-POWER` / `NO-SIGNAL`**).

## 1. Why this, and why it is new
- Queue: cycle 171's journal and IDEAS named I-095 (Quagmire IV behind decimations/routes) or I-016 (SAT periodic, expected `LOW-POWER` at P ≥ 8)
  for this new-family slot. I-095 is P2 and K3-shaped (keyword alphabets + K3's transposition law), so it was picked.
- Overlap, measured (`overlap172.txt`): 802 of the 165,782 perms are also in the 165,065-entry bank. The other 99.5 % never met Quagmire IV.
  Behind the decimations/routes only Quagmire III was tested (cases 57, 59: same alphabet both sides, ≤ 20,946 alphabets), plus autokey, rotors,
  self-keying, running keys (156–157, 159) and Porta (158–159). [Case 27](27-quagmire-iv-behind-transposition.md) (themed pairs) and
  [case 148](148-quagmire-iv-two-vocabulary-alphabets.md) (vocabulary pairs) tested Quagmire IV only behind the bank and directly.
- New here as well: alphabets keyed on the **KRYPTOS order** (word, then the rest of `KRYPTOSABCDEFGHIJLMNQUVWXZ`). Behind any transposition,
  those were listed as open (I-065, coverage row "Quagmire I–IV").

## 2. Model ([`tools/cycle172/q4d172.c`](../tools/cycle172/q4d172.c), derived from cycle 160's `q4v.c`)
- **Transpositions:** the 165,782 of cases 156–159 (`all.bin`: 159,712 K3-law decimations perm[j] = (a + s·j) mod M, M 97–112, empty slots skipped,
  and 6,070 spiral/diagonal routes; perm and inverse are separate entries). perm[j] = carved position holding plaintext letter j.
- **Alphabets:** 18,776 distinct: 9,393 vocabulary words keyed on A–Z (`/Z`), 9,381 keyed on the KRYPTOS order (`/K`), A–Z, KA
  ([`mkalpha172.py`](../tools/cycle172/mkalpha172.py)). Every ordered pair PA ≠ CA (3.5 × 10⁸) is tested. PA = CA is Quagmire III, already tested.
- **Cipher:** `c = CA[PA⁻¹(p) + k]` (Vigenère; variant shares consistency) or `c = CA[k − PA⁻¹(p)]` (Beaufort). The periodic key may be any
  letters, period p 1–16. **ix 0:** key at the plaintext index, then transpose. **ix 1:** transpose first, key at the carved index.
- **Exact test:** inside one residue class, `CA⁻¹(c_a) − CA⁻¹(c_b) = ±(PA⁻¹(p_a) − PA⁻¹(p_b))`. An alphabet-free prefilter comes first (equal carved letters ⇔
  equal plaintext letters inside a class). Then a hash join over all PA × CA for the remaining m equations. The tool prints the chance
  expectation 2·nu·(nu−1)·25⁻ᵐ summed over passing configs (known-answer check, I-097).
- **Texts:** K4, full family. 8 shuffled-K4 nulls (seeds 172000–172007) on every 4th perm (41,446). K4 is also reported on that subset.

## 3. Results ([`summary172.txt`](../data/cycle172/summary172.txt))
| cell | K4 configs with ≥ 1 pair (pairs) — full family | chance expectation (pairs), K4 | K4 on the null subset | 8 nulls, same subset: configs (min / median / max) | label |
|---|---|---|---|---|---|
| ix 0, p 1–14 | **0** | ≤ 0.033 per p; Σ 0.067 | 0 | 0 in all 8 | `EXACT-EXCL` |
| ix 0, p 15 | 12 (14) | 19.9 | 3 | 0 / 4 / 7 | `LOW-POWER` |
| ix 0, p 16 | 425 (555) | 572 | 96 | 78 / 101.5 / 122 | `LOW-POWER` |
| ix 1, p 1–13 | **0** | ≤ 0.011 per p; Σ 0.012 | 0 | 0 in all 8 | `EXACT-EXCL` |
| ix 1, p 14 | **0** | 0.30 | 0 | 0 / 0 / 1 (2 of 8 nulls have 1) | `EXACT-EXCL` (a hit would have been ambiguous) |
| ix 1, p 15 | 3 (3) | 4.4 | 0 | 0 / 0 / 2 | `LOW-POWER` |
| ix 1, p 16 | 88 (113) | 115 | 28 | 15 / 18.5 / 25 | `LOW-POWER` (see note) |

- **Known-answer check (I-097).** Observed pairs vs analytic expectation for K4: 14 / 19.9, 555 / 572, 3 / 4.4, 113 / 115. The counter counts
  what the bound says it should. ix 0 p 9 has no prefilter pass at all: the crib repeats E,A,S,T at distance 9 force four equal carved pairs.
- **Note on ix 1 p 16.** K4's 28 is above all 8 nulls (rank p = 1/9 = 0.11, the floor for 8 nulls, I-094). That is not evidence. K4's own
  expectation on the subset is ≈ 28.8, against a null mean of 25.4: K4 has more prefilter passes there (its crib-letter profile). It is also
  one of 6 cells with counts (no multiplicity correction applied). And the 88 configs (I-101: distinct perms) decode to gibberish (§5).
- **Where the verdict rests.** At p ≤ 14 the K4 count is exactly 0, and chance gives ≤ 0.3. A real Quagmire IV of this form would have
  appeared (§4). The verdict rests on the exact test plus the binary plants, not on null counts (I-085).

## 4. Controls and independent recount
- [`plant172.py`](../tools/cycle172/plant172.py) is an independent string encryptor (no tables, no code shared with `q4d172.c`). Each plant
  draws two random alphabets from the list (both `/Z` and `/K` constructions), a random decimation/route, an English plaintext with both cribs
  at the official positions, a keyword key (p 5–14), Vig/Beau and ix 0/1. It decrypts its own output back first, and each plant is
  hidden in a 200-perm slice.
  **8/8 recovered** at slot 100 with the planted PA, CA, mode and ix, at p and its multiples ≤ 16. The planted pair sometimes ties with a
  crib-indistinguishable alphabet (ctl0 PRIZE/RIPE, ctl5 CLY/CLAY), because those alphabets place the touched letters identically.
  All 8 decrypt to the planted text, scoring −4.19 off-crib ([`ctl_decodes_top.txt`](../data/cycle172/ctl_decodes_top.txt)).
  **Plant 8** (one carved letter under a crib altered) is **missed** at its slot, as a strict test must miss it. That is the one-error blind spot (→ I-103).
  ([`controls172_planted.txt`](../data/cycle172/controls172_planted.txt), [`controls172_outputs.txt`](../data/cycle172/controls172_outputs.txt)).
- [`recount172.py`](../tools/cycle172/recount172.py) is an independent numpy brute force over all 18,776² pairs. It compares each crib against the
  first crib of its class, with no prefilter, no hash and no cache. It was run on 30 configurations: 20 K4 configs with pairs (all 15 p-15
  configs + 5 random p-16), 4 random K4 zero configs, 3 controls and 3 null configs. **30/30 agree** with `q4d172`, Vig and Beau counted separately
  ([`recount172_cmp.txt`](../data/cycle172/recount172_cmp.txt)).

## 5. English check
All 685 K4 matches (p 15–16) were decrypted with the crib-fixed key values ([`k4_decodes.txt`](../data/cycle172/k4_decodes.txt)). Off-crib mean log10
quadgram: best −7.22, median −8.11. On the same subset, K4's best is −7.39 and the nulls' bests are −7.11 to −7.58 ([`null_english.txt`](../data/cycle172/null_english.txt)).
The planted English decrypts score −4.19. Best K4 line (Beaufort, CHAT/Z → HAUGHTY/K, routes/decimation q 91169, p 16):
`UILLQWMBCHEESAOKKPDAY EASTNORTHEAST IRFOFMALCHMWVNAFROMDSTNIHHVWB BERLINCLOCK GVYGYOGOYHEOLZQFIZQEZCG`. That is gibberish, and there is no candidate.

## 6. What this excludes and what it doesn't
Excluded (exact): K4 = periodic Quagmire IV with key length 1–14 (any key letters), Vigenère/variant or Beaufort, with plaintext and cipher
alphabets two different members of the 18,776 (vocabulary words keyed on A–Z or on the KRYPTOS order, A–Z, KA), combined in either layer order with any
of the 159,712 K3-law decimations (M 97–112) or 6,070 spiral/diagonal routes, with strict crib letters.

Not excluded:
- p 15–16 (chance level, decoded, gibberish) and p ≥ 17 (not run; ≤ 7 checks);
- one wrong crib or carved letter (plant 8 shows the strict test misses it) → I-103;
- alphabets outside the list (phrase-keyed, reversed, keyed by a word not in the 10,056; arbitrary alphabets → SAT, I-016);
- the one-letter anomaly behind decimations (the other half of I-095) → I-105; the 98-symbol `?` circle (154,186 decimations).

## 7. Run folder (I-078) and reproduction
[`inputs_provenance.txt`](../data/cycle172/inputs_provenance.txt): K4 16/16 chunks end in `END`, nulls 32/32, 0 `.tmp`. Wall time: K4 04:24:31 to ~04:27:50 PDT,
nulls to 04:31:50 PDT (7.3 min, 8 cores, no other heavy job), controls 12 s, recount 77 s. Reproduce: [`tools/cycle172/run_cycle172.sh`](../tools/cycle172/run_cycle172.sh),
then `summarize172.py`, `plant172.py`, `recount_run172.sh`, `decode172.py` ([README](../tools/cycle172/README.md)).

Voynich note: their C082 journal (~04:03 PDT, read-only on the box) says a note to this desk offers a blind review of these Quagmire IV plants
and asks for a critique of their C083 sweep design. The note is not visible to this run, so it is unverified (IDEAS I-106, I-107).

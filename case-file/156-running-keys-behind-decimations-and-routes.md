# Case file 156 — Running keys behind K3's decimation law and spiral/diagonal routes (cycle 168)

**Status:** negative. **Type:** new structure (cycle 167 was a variant/audit). A K3-style layered build: K3's own
transposition law (a decimation, case 57) or a K3-grid spiral/diagonal route (case 59), combined with a K1/K2-style
tableau substitution keyed by a **running text** instead of a repeated keyword. The coverage table had named this exact pair as
open in two rows ("running keys … behind decimations", "running keys behind them [routes]"); case 57 called it "the most obvious
structural gap". Two tests:
- **A (named texts, exact):** every carved text (cyclic), Carter vol. I (K3's source), Elliot Smith 1923, KJV John and the whole
  KJV New Testament, the National Security Act 1947 and Reagan's Berlin speech, forward and reversed (3.30 M letters), any offset,
  29 substitutions, both layer orders, behind all 165,782 permutations: **K4 0 full fits of 24 → `EXACT-EXCL`.**
- **B (any English book, scored):** substitute-then-transpose order, unnamed key text, 24 forced key letters scored as English
  (case 19's method): **K4 best −5.12, inside 48 shuffled nulls (median −5.28, max −4.68, 8/48 ≥ K4) → `NO-SIGNAL`**, with
  power 19/20 (planted English keys −3.68 to −4.44, all above the null max). A heuristic exclusion, not an exact one.

## 1. Why this, and why it is new
The parent queue offered I-081 (alternating A|B|A|B period-7 keys), I-016 (SAT periodic, open periods) and I-075
(CT-autokey through a known plain alphabet). All three are polyalphabetic periodic/autokey relatives of the last six cycles
(cases 150–155). The user asked for diversity, not relabelled variants. This item is a different construction: a non-periodic key
(running text) on top of the transposition law K3 actually uses. Novelty check: running keys were tested directly and
behind the 165,065-entry bank (cycles 20, 34–36, 69, 70, 148; the bank holds only 492 of the 160,204 decimations), behind
1.87 M rail/Redefence/AMSCO permutations (cycles 45, 79), and never behind the 159,712 new decimations or the 6,070 routes.
Decimations and routes so far met only periodic Quagmire III (cycles 59, 61) and autokey (cycles 60, 62). Grep of all 155 case
files, IDEAS.md and the README confirms: no running key behind either family.

## 2. Model
- Transpositions: `dec_perm.bin` (cycle 59, `tools/decimation_gen.py`: perm[j] = (a + s·j) mod M, M 97–112, every start and stride,
  empty slots skipped, perm and inverse; 159,712 not in the bank) + `route_perm.bin` (cycle 61, `tools/route_gen61.py`: spirals and
  straight/zigzag diagonals on w × h grids, w 2–48, 3 fills, perm and inverse; 6,070). Together **165,782**. Convention:
  perm[j] = carved position that holds plaintext letter j.
- Layer order: **Model A** substitute in plaintext order, then transpose (key index = plaintext position); **Model B** transpose,
  then substitute in carved order (key index = carved position). Both directions of every permutation are in the family.
- Substitutions (`tools/bookrk.c`, cycle 35, unchanged): 24 additive tableaux (Vigenère / Beaufort / variant × plain, cipher and
  key-numbering alphabet each A–Z or KRYPTOS: covers Sanborn's verified K1/K2 rule and Quagmire I–III on KRYPTOS) + 5 five-bit XOR codes.
- Key texts ([`inputs_provenance.txt`](../data/cycle168/inputs_provenance.txt), `tools/cycle168/texts168.py`): 24 carved texts
  (K1–K3 plain/cipher, K0 Morse, KA tableau rows, combinations, fwd/rev) made **cyclic** like cycle 79, so every start is an offset
  (K1 has only 63 letters); Carter & Mace vol. I, Smith 1923, KJV John, KJV NT, NSA 1947 (amended), Reagan 1987, fwd and rev.
  48 texts, 3,302,066 offsets.

## 3. Test A — named texts, exact (`bookrk`, 16 checkpointed chunks)
For each (permutation, model, substitution, text) the 24 crib constraints are ANDed as shifted letter bitsets over all offsets;
a full fit means one offset satisfies all 24. Run 01:46:59–01:48:28 PDT (1 min 29 s wall, 8 processes).

| item | scope | full fits (24/24) | best prefix depth | label |
|---|---|---|---|---|
| K4 | 165,782 perms × 2 models × 29 subs × 48 texts (287,096,544 valid configs, ≈ 3.2 × 10¹³ key placements) | **0** | 9 (4 configs: 3 × KJV NT reversed, 1 × NSA 1947 reversed) | `EXACT-EXCL` |
| K4 on chunk_15 | 10,352 decimations + all 6,070 routes | 0 | 8 (5 configs) | — |
| 24 shuffled K4s | chunk_15, same texts and subs | 0 in 24 | 8–12 (median 8); 24/24 ≥ K4's 8 | null lineup |
| 12 planted controls | 2,000-perm slices | 12/12 recovered | 24 | PASS |

**Bound.** A chance 24/24 fit has probability ≈ 26⁻²⁴ per placement; 3.2 × 10¹³ placements give ≈ 3.5 × 10⁻²¹ expected false fits
for K4. So a fit would be decisive, and 0 is what a wrong model gives. The verdict rests on this bound and on the controls
(the test is exact, so plant strength is binary, power 12/12). It does not rest on null counts. The null count is reported for
I-085 anyway: 0/24 nulls with a fit (exact binomial 95 % upper bound on the null fit rate 11.7 %). The null depth lineup puts K4's chunk_15
best (8) at the bottom of the null range: no near-miss anomaly.

## 4. Test B — any English running key, scored (`fragscore168.py`)
Model A only: undoing the transposition puts the cribs back at plaintext 21–33 / 63–73, so the 24 forced key letters are two
contiguous fragments (13 + 11) of the unknown key text. Score = mean log10 quadgram over the 18 quadgrams (case 19, re-implemented
in numpy), 165,782 perms × KA/AZ × Vig/Beau/variant ≈ 1.0 M candidates per text.

| item | best fragment score | best fragments |
|---|---|---|
| K4 | **−5.117** | EFSTMELFILTAN / FTHAMEITLOU (A–Z, variant, perm 77474) |
| 48 shuffled K4s | −5.62 / **−5.28** / −4.68 (min / median / max); 8/48 ≥ K4 (p ≈ 0.18) | e.g. phrases by chance |
| 20 planted English keys (Jane Eyre / Sherlock plaintext, Dracula / Poe keys, random tableau, random perm) | −3.68 … −4.44 for 19; rank 1 in 19/20 | e.g. HEYHADTOKEEPO / HTTHEMATTER |

The one miss (ctl2, rank 2) had a planted fragment pair THEMRAWPMIGAV / ENOUGHTOMAK that splits mid-word and scores below
chance. K4's best is not English and sits inside the null range → `NO-SIGNAL` with power 19/20 for typical English prose keys.

## 5. Controls and independent recount
- [`rk168_controls.py`](../tools/cycle168/rk168_controls.py) is an independent string-level encryptor (Jane Eyre plaintext with both cribs at
  the official positions, key at a random offset in one of 12 different key texts, random additive mode, ctl0 = Sanborn's KA
  Vigenère, Models A/B alternating, random decimation or route). **12/12 recovered** at the planted permutation, model, mode, text
  and offset. Three more FULL lines are the same key in a containing text (KJV John ⊂ NT; K3 ⊂ K1–K3 and K1–K3+K0)
  ([`summary168.txt`](../data/cycle168/summary168.txt); raw outputs [`outputs_bookrk.txt`](../data/cycle168/outputs_bookrk.txt)).
- [`rk168_verify.py`](../tools/cycle168/rk168_verify.py) `verify` rebuilds each FULL line's whole 97-letter decryption by string operations
  (no bitsets): **15/15 give 24/24 crib letters; all 12 planted lines decrypt to the identical planted 97-letter plaintext**
  ([`controls168.txt`](../data/cycle168/controls168.txt)).
- `depth` recount (numpy, no bitsets) on 40 random permutations × 48 texts × 2 models × 24 additive modes (92,160 configs):
  **identical depth histogram to bookrk** in bookrk's convention. With the convention made exact, 2 configs move by one level
  ([`recount40.txt`](../data/cycle168/recount40.txt)). Cause, documented here for the first time: bookrk's depth diagnostic also counts the
  ≤ 63 bit positions past the last valid offset in the final bitset word. FULL fits are masked to real offsets, so no
  exclusion is affected. Only depth < 24 diagnostics can read up to one level high.
- Part B controls are in §4. 48 nulls, ≥ 40 as I-085 asks.

## 6. Crib and English checks
Test A: no configuration reaches 24/24, so there is nothing to decrypt. Test B gives key fragments only, and K4's best are not English.
No coherent 97-letter English, and no candidate.

## 7. Run folder (I-078)
[`inputs_provenance.txt`](../data/cycle168/inputs_provenance.txt): 52/52 outputs end in SUMMARY, 0 `.tmp`. The null pass was stopped
once at 8/40 nulls (the Voynich agent's own job was sharing the 8 CPUs, so 40 would have overrun the budget). It resumed from
checkpoint with 24 nulls + 12 controls. Nulls 24–39 are prepared (listed in `inputs_provenance.txt`) and were not run. Part B scores: [`partb_all.jsonl`](../data/cycle168/partb_all.jsonl).

## 8. What this excludes and what it doesn't
Excluded (exact): K4 = running key from any of the 48 named texts at any offset, under any of the 29 substitutions, in either layer
order, combined with any K3-law decimation (M 97–112) or any spiral/diagonal route of cycle 61, strict crib letters.
Disfavoured (scored, power 19/20): an unnamed English prose running key, substitute-then-transpose, same families and tableaux.

Not excluded:
- one wrong crib or carved letter (bookrk is strict; I-087);
- transpose first with an unnamed book (Model B: key letters scattered, I-088);
- the 98-symbol `?` decimations (154,186) and the 20,946-alphabet mixed tableaux behind decimations (I-089);
- Porta, Quagmire IV and the one-letter anomaly behind decimations, still open from case 57 (I-089);
- non-English or unlisted books.

## 9. Reproduce
`tools/cycle168/run_cycle168.sh` (inputs: `dec_perm.bin` from `tools/decimation_gen.py`, `route_perm.bin` from
`tools/route_gen61.py`, cycle 34–36 key texts, `quadgrams.json` and Gutenberg `rkg*.txt` from the support backup; sha256 in
[`inputs_provenance.txt`](../data/cycle168/inputs_provenance.txt)), then `python3 tools/cycle168/summarize168.py RUN`.

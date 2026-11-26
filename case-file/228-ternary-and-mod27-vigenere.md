# Case 228 — Twenty-seven cells: carry-free base-3 ("ternary Vigenère") and mod-27 Vigenère on keyed alphabets (cycle 242)

**Slot:** new family (I-398). Idea **I-399** (new, tested here); new **I-400–I-405**.
Pre-registered as [PREREG242](../tools/cycle242/PREREG242.md) (local commit db57302, 2026-11-26 10:38 PT, before any plant, null or K4 run through `tri242`; one disclosed smoke on plant 0). Base: origin/main **99c4acc** (c241 published). Code: [`tools/cycle242/`](../tools/cycle242/) (`tri242.c`, `m242.py`, `plant242.py`, `mknull242.py`, `run242.sh`, `analyze242.py`, `check242.py`, `tot242.py`, `HASHES242.txt`); raw results (stamped, rule 5): [`data/cycle242/`](../data/cycle242/) (`SHA256SUMS`).
**Verdict: no solution.** K4 has **0** survivors in every registered cell (strict and one-error) in all three alphabet scopes → `EXACT-EXCL` within the stated model. The 12 shuffled nulls also give 0; plants 20/20.

## Why this family
Every additive cipher in this repo so far lives in **Z26** (Vigenère / Beaufort / Quagmire, digit keys, Gromark, word keys), in **Z2⁵** (Vernam / ITA2 XOR, [case 32](32-vernam-teleprinter-xor.md)) or on a keyboard torus ([cases 210](210-typewriter-keyboard-ciphers.md) / [213](213-keyboard-family-wider.md)). Two hand-workable groups with **27 cells** had never been tried:
- **g0 — Z3³, carry-free base 3.** Write the letter's index in a keyed alphabet as three base-3 digits, add the key's digits one by one mod 3, no carries. It is Vernam's XOR one base up, and 3 is the only base whose cube (27) just covers 26 letters — a reading of the community "change the base" hint (repo [case 09](09-any-digit-key.md); `[community, unsourced here]`) that is **not** a digit key. [Case 200](200-digit-key-two-keyed-alphabets.md) already excludes every digit-valued key on two keyed alphabets, but only in Z26; a different group escapes that proof.
- **g1 — Z27**, ordinary addition mod 27 with one extra symbol (space / '?').
Z3³ is not cyclic, so no choice of keyed alphabet turns it into a Vigenère: it is a genuinely different algebra, not a relabel.
**Prior cost (disclosed in the PREREG):** both groups have one cell more than the alphabet, so the encipherer must keep the extra symbol out of the carving; for a random key that happens with probability (26/27)⁹⁷ ≈ 0.026. K4 shows exactly the 26 letters.

## Model and scopes (frozen)
Plain alphabet X, cipher alphabet Y; forms **V** c = p ⊕ k, **R** c = p ⊖ k, **B** c = k ⊖ p. The 24 crib seats (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-indexed) give 24 required key cells per (X, Y, g, form) — key-agnostic. Direct (no transposition: deliberately, this is a new substitution, not a new relabel behind the bank).
| key model | parameters | crib constraints |
|---|---|---|
| PER periodic (any keyword, meaningful or not) | P 1–48 | 24 − #residues: 23 (P 1) … 5 (P 24), 0 (P 27–29), 6–11 (P 35–47) |
| CA ciphertext autokey (key = carved letter i − L read in X or in Y) | L 1–48 × 2 | 11–24 |
| PA plaintext autokey (key = plaintext letter i − L in X or Y) | L 1–12, 30–52 × 2 | only where i − L is also a crib seat: 22 (L 1) … 1 |
| scope | alphabets | pair-forms |
|---|---|---|
| S1 | X = Y ∈ the 86,731 house alphabets (`alpha.bin` 2b4ffb69…) | 520,386 |
| S2 | X, Y ∈ 144 themed (`themed144.bin` e0c1b627…), 20,736 ordered pairs | 124,416 |
| S3 | X ∈ alpha.bin, Y ∈ {AZ, KA}, and the reverse | 2,081,544 |
2.73 × 10⁶ pair-forms per text (× 2 key maps for the autokeys). Survivor = viol 0 (strict) or ≤ 1 (one error: one removable crib seat for PER / PA; one wrong carved letter for CA, which can spoil seat q and seat q + L).

## Results
| text | registered cells: strict survivors | one-error survivors | trace triggers |
|---|---|---|---|
| **K4** | **0** | **0** | 0 |
| 12 nulls (209758–209769) | 0 each | 0 each | 0 |
**Gate P (seed 209757): 20 / 20** (Wilson 0.84–1.00): S1 8, S2 6, S3 6; both groups; all three forms; PER 7 (P 2–45), CA 7 (L 10–18), PA 6 (L 4–44); 10 one-error plants, each found at the planted (scope, X, Y, g, form, model, parameter, key map). Implied decrypts of the planted lines with nq ≥ 30 (14 plants): NC −5.02 … −3.85; every determined letter equals the planted plaintext except letters keyed through the corrupted seat (plants 1, 13, 15: 1, 1, 3 letters).
**Gate T:** `check242.py` (pure Python, own key / violation code) re-derived all 254 printed survivor lines (K4, nulls, plants 0–3): **0 mismatches**. **Gate T2** (`tot242.py`, written after the run, disclosed): Python recount of 11 non-zero low-constraint totals for K4 on S2 equals tri242's totals exactly.
**Compute:** ≈ 2 min 26 s wall for 33 texts (≈ 4.3 s each, 8 threads), `setsid timeout 480`, one process group.

### Below the line (counts only)
Cells with < 6 constraints (PER P 24–34, 48; PA L 10–12, 30–34, 48–52) and one-error cells with < 9 are `INSUFFICIENT-DISCRIMINATION` by design: thousands of chance survivors per text. K4 sits inside the null range: across the 428 count statistics (strict and one-error per cell) K4 exceeds all 12 nulls in 7 (≈ 33 expected if exchangeable with ties broken against K4) → **`NO-SIGNAL`**. The five K4 lines printed in sub-threshold PA cells (L 35 / 47, one-error, n 6) decrypt to gibberish around the cribs (NC −7.5 … −8.5 on 4–10 quadgrams), e.g. `…EASTNORTHEASTOCWHB…BQARTMRBERLINCLOCK…`. Table: `data/cycle242/lowcells242.txt`.

## Reading (I-399)
- **`EXACT-EXCL`** for K4, direct, cribs at the official positions, in S1 / S2 / S3, both groups, three forms:
  - strict: periodic P 1–23 and 35–47 (every keyword of those lengths), ciphertext autokey L 1–48 (either key map), plaintext autokey L 1–9 and 35–47;
  - one crib error: periodic P 1–15, 19–22, 38–44; ciphertext autokey L 1–48; plaintext autokey L 1–7, 38–44.
- `INSUFFICIENT-DISCRIMINATION` / `NO-SIGNAL`: periodic P 24–34, 48; plaintext autokey L 10–12, 30–34, 48–52 (K4 within the null range).
- The bar was not exercised (no K4 survivor in a registered cell).

## News check (2026-11-26)
No solution. K4's plaintext is still private (Paradigm's $1 verifier, blog 2026-06-12; K5 unreleased). Seen, nothing new for the method: glthr.com "W-Rectangle and Its Half-Turn" (published 11 Nov, updated 15 Nov 2026; rows of 19, four W's on a rectangle, cribs on its edges — the author says it does not decipher K4; same observation the repo tested as case 192), relatablehistory.com "Why Kryptos K4 Is Still Unsolved" (4 Nov 2026, recap: auction, Smithsonian find, Paradigm), nlc.hu (22 Nov 2026, Hungarian recap). `[secondary / community, unverified]`. Nothing was submitted anywhere.

## Blind spots
X ≠ Y with both free in the 86,731 list (7.5 × 10⁹ pairs, I-400); a transposition layer before or after (I-401); running keys other than autokey (English / carved texts through the 27-cell groups, I-402); the extra symbol carved as a letter (a 26-symbol output with one letter doing double duty, I-403); other 27-cell layouts (3 × 9 with Z3 × Z9, the trifid cube with a keyword order, I-404); base-3 digits on the carved index; mixed groups per position.

# PREREG242 — Cycle 242 (NEW FAMILY slot, I-398): 27-cell additive substitutions — "ternary Vigenère" (carry-free base-3 addition, Z3³) and mod-27 Vigenère on keyed alphabets (I-399)

Filed 2026-11-26 10:38 PT (UTC−7), **before** any plant, null or K4 run through `tri242`. Base: origin/main **99c4acc** (c241 published). Case file 228.
Slots (I-398): **242 new family**; 243 free; 244 audit. Seeds: plants **209757**; nulls **209758–209769** (12). **Next free seed after this cycle: 209770.**

## Why this family (reasoning, not brute force)
Every additive family in the repo so far works in **Z26** (Vigenère / Beaufort / Quagmire, digit keys, Gromark), or in **Z2⁵** (Vernam / ITA2 XOR, case 32), or on a keyboard torus (cases 210 / 213). Two hand-workable groups with **27 cells** were never tested:
- **g0 — Z3³, carry-free base 3** ("ternary Vigenère"): write the letter's index in a keyed alphabet as three base-3 digits and add the key's digits one by one mod 3, without carries. It is the base-3 sibling of Vernam's base-2 XOR, and base 3 is the *only* base whose cube (27) just covers 26 letters — a natural reading of the community "change the base" hint (repo case 09; `[community, unsourced here]`) that is *not* a digit key: case 200 already excludes every digit-valued key on two keyed alphabets in Z26, but that exclusion says nothing about a different group.
- **g1 — Z27**, ordinary addition mod 27 with one extra symbol (space / '?' as cell 26).
Both groups have one more cell than letters, so the encipherer must avoid the 27th symbol in the carving (K4 shows all 26 letters and nothing else). For a random key that happens with probability ≈ (26/27)⁹⁷ ≈ 0.026 — a **prior cost of the model, disclosed here**, not a test. The non-cyclic group Z3³ is genuinely different from Z26: no keyed alphabet turns it into a Vigenère.

## Model (frozen)
Plain alphabet X, cipher alphabet Y; a letter's cell = its index in its alphabet (0–25). Forms: **V** c = p ⊕ k, **R** c = p ⊖ k, **B** c = k ⊖ p (group g0 or g1). The 24 crib seats (EASTNORTHEAST 1-indexed 22–34 = 0-based 21–33, BERLINCLOCK 64–74 = 63–73) give 24 required key cells (key-agnostic). Direct only (no transposition layer: that is the point of this cycle). Key models:
- **PER P** periodic key, P 1–48 (covers every keyword, meaningful or not, of length ≤ 48 in the plaintext index). Constraints per P = 24 − #residues (23 at P 1 … 5 at P 24; 0 at P 27–29; 6–11 at P 35–47).
- **CA L, M** ciphertext autokey: key at i = cell of carved letter i − L read in X (M 0) or Y (M 1), L 1–48 (≥ 11 constraints each).
- **PA L, M** plaintext autokey: key at i = cell of plaintext letter i − L in X (M 0) or Y (M 1); constraints only where i − L is also a crib seat (L 1–12, 30–52; 22 at L 1 … 1 at L 12 / 30 / 52).
Alphabet scopes: **S1** X = Y ∈ the 86,731 house alphabets (`alpha.bin`, 2b4ffb69…); **S2** X, Y ∈ 144 themed (`themed144.bin`, e0c1b627…), all 20,736 ordered pairs; **S3** X ∈ alpha.bin with Y ∈ {AZ, KA} and X ∈ {AZ, KA} with Y ∈ alpha.bin (`azka.bin` = alpha rows 0–1). 2 groups × 3 forms each: ≈ 2.73 × 10⁶ pair-forms per text.
Survivor = viol 0 (strict) or viol ≤ 1 (one error: one crib seat removable for PER / PA; one wrong carved letter for CA, which can spoil seat q and seat q + L).

## Registered cells and expectations
- **Primary strict cells:** PER with ≥ 6 constraints (P 1–23, 35–47), all CA (L 1–48), PA with ≥ 6 (L 1–9, 35–47). Chance ≈ pf × 27⁻ⁿ: at n = 6 ≈ 2.7 × 10⁶ / 3.9 × 10⁸ ≈ 0.007 per cell; smaller for larger n.
- **Primary one-error cells:** the same models with ≥ 9 constraints.
- Cells with fewer constraints (PER P 24–34 and 48, PA L 10–12, 30–34, 48–52) are reported as counts only: `INSUFFICIENT-DISCRIMINATION`, compared with the nulls.

## Gates and controls
- **Gate P (plants, seed 209757, `plant242.py`, plants242.tsv f8896147…):** 20 plants over S1 (8) / S2 (6) / S3 (6), both groups, all forms, models PER / CA / PA in turn; odd ids carry one wrong carved letter at a random crib seat. PASS iff ≥ 19/20 recovered with the planted (scope, X, Y, g, form, model, parameter, M) and viol 0 for clean plants / ≤ 1 for one-error plants.
- **Gate T:** `check242.py` (pure Python, shares only the group arithmetic in `m242.py`, not tri242's code) re-derives viol for every printed survivor line of K4, the nulls and 4 plants; PASS iff 0 mismatches.
- **Nulls:** 12 shuffled K4 texts (209758–209769, `mknull242.py`, nulls242.tsv deaa87f0…), full scopes. Machinery check plus the empirical rate of the low-constraint cells.

## Decision rules (frozen)
- K4 0 primary survivors in a cell and gate P PASS → **`EXACT-EXCL`** for that cell within its scope (alphabets as listed, direct, cribs at the official positions, ≤ 1 crib error where stated).
- Any primary K4 survivor: decrypt the implied letters (`m242.decrypt_line`), NC = mean log10 quadgram (data/support/quadgrams.json) over determined quadgrams not touching a crib seat, nq reported. Trace trigger nq ≥ 40 and NC ≥ −6.9634 (BSH(343), borrowed from the gn217 family; descriptive for this family, compared with the plants' NC). A **solution** requires 97 coherent English letters with both cribs at the official positions and a reproduction; anything less is a lead or noise.
- Low-constraint cells: K4 count vs the 12 null counts (rank), `NO-SIGNAL` if K4 within the null range.

## Disclosed before filing
One development smoke: plant 0 through S1 only (0.9 s; planted line found at P 2 and its multiples). No K4 or null run through `tri242`. Hashes of all tools and inputs: `HASHES242.txt`.

## Commands and budget
`setsid timeout 480 ./run242.sh` (resumable; ≈ 5 s per text × 33 texts expected), then `python3 analyze242.py`, `python3 check242.py K4=… N…=… P0=… …`. One owned process group; nothing else touched.

## Honesty clause
`[speculation]`: no source says Sanborn used base-3 or mod-27 arithmetic. Not covered here: transposition layers, alphabets outside the three scopes (e.g. X ≠ Y both free from alpha.bin), keys on the carved index behind a transposition, running keys other than autokey, a 27th symbol that *was* carved as a letter.

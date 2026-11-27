# Case 229 — Running keys through the 27-cell groups: named texts exactly, unknown English keys by readability (cycle 243)

**Slot:** free (I-405). Idea **I-402** (tested here); new **I-406–I-410**.
Pre-registered as [PREREG243](../tools/cycle243/PREREG243.md) (local commit 0b29880, 2026-11-27 10:34 PT, before any plant, null or K4 run through `rk243`; one disclosed smoke on plant 0, S1). Base: origin/main **a2e293c** (c242 published, case 228). Code: [`tools/cycle243/`](../tools/cycle243/) (`rk243.c`, `rktexts243.py`, `plant243.py`, `mknull243.py`, `run243.sh`, `analyze243.py`, `check243.py`, `HASHES243.txt`); raw results (stamped, rule 5): [`data/cycle243/`](../data/cycle243/) (`SHA256SUMS`).
**Verdict: no solution.** Part E (28 named texts): K4 **0** strict and **0** one-error survivors → `EXACT-EXCL` within the model. Part H (unknown English key): K4 sits inside the null range (rank p 0.69, z −0.52) → `NO-SIGNAL`, with a narrow plant/null margin disclosed below.

## Why this item
[Case 228](228-ternary-and-mod27-vigenere.md) closed the two 27-cell groups — **g0** Z3³ carry-free base 3 and **g1** Z27 — for periodic keys and autokeys only, and listed running keys as its own blind spot (I-402). A running key is the one key model a periodic / autokey test cannot see. In Z26 the repo already ran both halves of it: named texts exactly ([case 33](33-carved-running-keys.md), [case 34](34-k3-source-book-as-running-key.md)) and unknown English keys scored by the readability of the implied key letters ([cases 15](15-english-running-key.md) / [19](19-running-key-behind-transposition.md); PREREG243 wrote "cases 15 / 16 / 19" — case 16 is the K3 grid, the slip is corrected here). Neither half had been run in a 27-cell group. The other free-slot candidates were weighed in the PREREG: I-393 needs ≥ 36 fresh gn217 nulls (≈ 10 min, over budget) and is a bar audit better suited to 244; I-368 / I-380 / I-391 extend families already closed.

## Model (frozen; groups, forms, scopes and crib seats exactly as case 228)
Plain alphabet X, cipher alphabet Y, cell = index (0–25), cell 26 = the extra symbol. Forms V c = p ⊕ k, R c = p ⊖ k, B c = k ⊖ p. The 24 crib seats (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-indexed) fix 24 required key cells. A running key is a **letter** stream, turned into cells by a map **M**: 0 = index in X, 1 = index in Y, 2 = index in A–Z (a map equal to an earlier one is skipped). A seat that needs cell 26 cannot be met by a letter key. Key letter at plaintext position i = T[(o + i) mod |T|]. Direct, no transposition.
| scope | alphabets | config-maps per text |
|---|---|---|
| S1 | X = Y ∈ 86,731 (`alpha.bin`) | 1,040,766 |
| S2 | X, Y ∈ 144 themed, 20,736 ordered pairs | 370,662 |
| S3 | alpha × {AZ, KA} both ways | 5,203,824 |
| total | | **6,615,252** (59 % need cell 26 at ≥ 1 seat) |
- **Part E (exact):** 28 texts, 783,984 letters: case 33's 12 carved texts forward and reversed, plus case 34's books — Carter & Mace vol. I (IA `tomboftutankhame00cart_1` OCR, 284,914 letters; the K3 passage at letter 138,840 reproduces case 34) and G. Elliot Smith (Gutenberg #59783 from the pglaf mirror, www.gutenberg.org was down: **102,028** letters vs case 34's 101,923, header/edition drift, disclosed) — each forward and reversed, every offset, cyclic. Offsets reached through two 4-letter anchors (seats 0–3 and 13–16); one error leaves one anchor intact, so the search is complete for ≤ 1 wrong crib letter. Expected chance count ≈ 10⁻¹⁷ strict, ≈ 10⁻¹⁵ one-error.
- **Part H (heuristic):** every config-map with no cell 26 (≈ 2.7 × 10⁶ per text): mean log10 quadgram of the implied key fragments (10 + 8 quadgrams, `data/support/qg.bin`). Statistic **Hmax** per text.

## Results
| text | Part E strict | Part E one-error | anchor depth max | Hmax (Part H) |
|---|---|---|---|---|
| **K4** | **0** | **0** | 12 (5 offsets) | **−5.2598** (S3) |
| 12 nulls (209771–209782) | 0 each | 0 each | 12–14 | −5.3852 … −4.8841 (mean −5.187, sd 0.139) |
| exact plants 0–9 | planted line found 10/10 | — | 24 | — |
| English-key plants 10–19 | — | — | — | −4.7906 … −3.8775 |
- **K4 Part E:** 0 / 0 in every scope (15.8 × 10⁶ anchor-reached offsets checked in full) → **`EXACT-EXCL`**. Anchor depth (descriptive): K4's best offset matches 12 of 24 seats; nulls 12–14 → rank p 1.0, chance.
- **K4 Part H:** Hmax −5.2598, 8 of 12 nulls higher → rank p **0.692**, parametric z **−0.52** → **`NO-SIGNAL`**. Top K4 fragments (S3a, g0 R, M 1): `WNTBEDTRESOPE` / `MATTYTRYROE` — not English. Per scope: S1 −5.565, S2 below the print floor (−5.6), S3 −5.260.

## Gates
- **Gate E 10/10 (PASS, ≥ 9 required).** Every exact plant came back with its planted (scope, X, Y, g, form, M, text, offset); clean plants strict, one-error plants at viol 1 on the planted seat. Extra lines are the same key letters in overlapping texts (K2pt inside K123pt inside K123pt_K0; K3 ct inside K123ct), as expected.
- **C130 rule (PENDANT / TIE / MAJ):** each crib seat is pinned by exactly one key-text letter, so a wrong carved letter always shows as one identified mismatched seat: plants 1, 3, 5, 7, 9 are all **MAJ** (recovered, seat identified). PENDANT and TIE cannot occur in this model; the "draw ≥ 1 pendant and ≥ 1 tie" clause is **structurally N/A** (stated in the PREREG). In its place errors were forced inside anchor A (plant 1, seat 3), inside anchor B (plant 3, seat 16), elsewhere in each crib (plants 5 / 7, seats 8 / 19) and at a random seat (plant 9, seat 9): all recovered.
- **Gate H 9/10 (≥ 8 → Part H powered).** Nine English-key plants (H. G. Wells, *The Time Machine*, not in the Part E list) were rank 1 in their own lists and above every null. **Plant 17 failed the rule as written:** its planted line ties at the top (−4.11196, same fragments `EOTHERMENWERE` / `CERTAINJOUR`) with an equivalent configuration (S3b, X = AZ, g1, form B with Y #53155 vs the planted form V with Y #53157), and the tie was listed first. It is a counting artefact of equivalent configurations, not a miss (→ I-407), but the frozen rule is kept: 9/10.
- **Margin (disclosed):** the weakest English-key plant scored −4.7906 (plant 19, fragments `SKYBLUEIBREAT` / `UATINGCONTO`), only **0.094** above the best null (−4.8841). Part H is powered for keys as English as Wells' prose, but a key of plainer or broken English (names, lists, word-final runs) could sit inside the null range (→ I-408).
- **Gate T PASS:** `check243.py` (pure Python, independent of `rk243.c`) re-derived 370 lines (all S lines of K4, 12 nulls, 20 plants; top 5 H lines per scope file of all 33 texts — a superset of the registered 4 plants): **0 mismatches**. A deliberate mismatch (plant 0's lines checked against K4's text) was flagged (14 mismatches).

## What this rules out (and what it does not)
**Out:** a direct 27-cell (Z3³ or Z27) running-key encipherment of K4, any of the three forms, plain and cipher alphabets in the case 228 scopes, key letters numbered by X, Y or A–Z, with the key taken from any of the 28 texts at any offset — even with one wrong crib letter. **Heuristic only:** an English running key from any other text gives K4 nothing above shuffled copies.
**Not covered:** keys that keep word spaces (cell 26 = space, the natural reading of Z27 — Part H skips the 59 % of configurations that need cell 26; I-406); X ≠ Y both free (I-400); transposition layers (I-409); keys that skip letters; texts outside the 28; other key numberings.

## Labels
Part E `EXACT-EXCL` (within the stated model). Part H `NO-SIGNAL` (powered 9/10, narrow margin). Anchor depth: descriptive, chance. Compute: 19 s wall for all 33 texts × 4 scopes (setsid, timeout 480).

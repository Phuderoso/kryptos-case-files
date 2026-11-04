# 10 — Style profile of K1–K3, and what it predicts for K4 (cycle 12)

> *You learn a forger by his old work. Sanborn signed three checks before he wrote the fourth one. I read the three again, slowly, looking for his handwriting rather than his words.*

Facts below come from the sourced case files [01](01-the-sculpture.md), [02](02-solved-sections.md) and [03](03-k4-evidence.md); every "→" line is an **inference** of mine, labelled as such, and every hypothesis ends with a test.

## 1. How the keys were chosen
| Section | Method | Key | Length | What the key *means* |
|---|---|---|---|---|
| K1 | Quagmire III: one KRYPTOS-keyed alphabet on both sides | PALIMPSEST (typo PALIMPCEST on the chart, NYT 2010) | 10 | a page written over another: **layers** |
| K2 | same tableau | ABSCISSA | 8 | the x-coordinate: **position on an axis** |
| K3 | pure transposition (two 90° rotations; equivalently one fixed permutation, grids 24×14 then 8×42) | geometry only | widths 24, 8 | none: **the grid is the key** |

**Style traits (fact):** keys are single, real English words, not random strings; one alphabet (KRYPTOS) does double duty; each key word is *about* the cipher or the next section, not about the plaintext story (palimpsest → layered writing; abscissa → coordinates, which K2 then gives). K3 drops the alphabet entirely and changes the methodology, as Scheidt said he intended.
→ *Inference:* K4's key, if there is a word, is likely a short real word describing its own mechanism (time, clock, base, position, layer), and its method changes again rather than repeating K1/K2 or K3 alone.

## 2. The plaintexts
- **K1:** one poetic sentence (63 letters) about light, shading and illusion; deliberate misspelling IQLUSION, produced by a typo in the *key*.
- **K2:** a field report: magnetism, transmission underground, "does Langley know", coordinates written out in words, the initials WW, and "X LAYER TWO" after Sanborn's 2006 correction of a dropped S. `X` separates sentences; `?` is carved in clear and does not advance the key.
- **K3:** a paraphrase of Howard Carter's account of opening Tutankhamun's tomb (1922), misspelling DESPARATLY, ending `Q?` ("can you see anything?").
- **K4 (official cribs):** EAST NORTHEAST at positions 22–34 and BERLIN CLOCK at 64–74; Sanborn tied the clock to the Weltzeituhr at Alexanderplatz and the fall of the Berlin Wall.

→ *Inference:* each plaintext is a first-person or reported scene, plain English, with one planted spelling error and directional/locational language. K4's crib "EASTNORTHEAST" reads like a *bearing* (as K2 gave coordinates), so K4 plausibly continues the "location" thread with a compass bearing near a named landmark. Scoring must tolerate one misspelled word.

## 3. Errors as signals
- K1: wrong key letter → one wrong plaintext letter (Q). K2: one letter left off the copper (S) → "ID BY ROWS" instead of "X LAYER TWO". K3: one plaintext misspelling (A). The tableau has one extra L.
- **Fact:** every section carries *exactly one or two* single-letter anomalies, never a scrambled block.
→ *Hypothesis S4:* K4 as carved may contain one omitted or substituted letter, so an exact 97-letter model can fail by one position. **Test:** the "omitted letter at any of 98 positions" model (below), extended to more families next cycle.

## 4. Separators and section boundaries
- `X` = sentence stop inside K2's plaintext; `?` = punctuation carved unencrypted (K2 three times, end of K3).
- The `?` before K4 belongs to K3's plaintext ("…ANYTHING Q?"), so K4 starts cleanly at O.
→ *Inference:* X may appear in K4's plaintext as a stop between clauses; cribs at 22–34 and 64–74 leave room for roughly three clauses (1–21, 35–63, 75–97).

## 5. How secrets were layered
- K1 and K2 are substitution only; K3 is transposition only. K2's own plaintext says "LAYER TWO" and "ID BY ROWS" (the uncorrected reading). Sanborn's 2025 letter speaks of "scrambled plain text"; a secondary source (cipher.ink, Oct 2026) describes the Smithsonian pages as text "cut into strips and taped together out of order".
→ *Hypothesis S1 (style-pure):* K4 = **one transposition + one substitution**, both of the kinds already used: a K3-like geometric or columnar transposition and a KRYPTOS-alphabet substitution whose key changes "base" (digits rather than letters).
→ *Hypothesis S6:* "strips" suggests a **row/strip permutation** (write in rows, reorder the rows) rather than a column read — cheap to test next.

## 6. Relation to each other and to the sculpture
K1 (illusion, light) sets the mood; K2 (location, buried, LAYER TWO) points at the site and the next layer; K3 (opening a tomb, "can you see anything") is the moment of discovery; K4 (Berlin, a clock, a bearing) moves the scene to 1989 Berlin. All four ciphertexts are cut into the left half; the KRYPTOS tableau on the right half *is* the K1/K2 key material, with its extra L.
→ *Inference:* K4's keying material is probably physically on the sculpture or in its themes (tableau, compass rose/lodestone on site, the Berlin world clock), consistent with the plain-sight vocabulary used since cycle 7.

## 7. Concrete hypotheses derived from the profile
| # | Hypothesis | Status |
|---|---|---|
| S1 | transposition (columnar ≤8 all orders, keyword columnar 9–20, 8-way routes 2–48, K3 double rotations on 97–100 ragged grids) + KRYPTOS-style alphabet + **small-digit key of any origin** | **tested this cycle: negative** |
| S4 | as S1, K3 geometry on 98 letters with **one letter omitted from the copper** at any position | **tested this cycle: negative** |
| S2 | K4 key = a meta-word for its own mechanism (CLOCK, UHR, ZEIT, BASE, HOUR, MENGENLEHRE, SETTHEORY…) used K1-style after a transposition | open — next |
| S6 | strip transposition (rows reordered) + digit or KA keyword substitution | open — next |
| S3 | plaintext is a scene with a bearing and a landmark, with one misspelling | scoring rule for all future tests |

## 8. Cycle-12 test of S1 and S4 (`tools/transwin_gen.py`, `tools/c/transwin.c`)
**Key observation.** With a digit test that doesn't care *where* each digit sits, "transpose then substitute" and "substitute then transpose" give the same crib pairing (plaintext letter j with ciphertext letter t(j)); only the direction of t matters, so both t and t⁻¹ were tried. That closes cycle 11's stated gap for these families.
- **Transpositions:** 96,630 (identity; columnar widths 2–8 with *every* column order; keyword columnar 9–20 from the 89 plain-sight words; 8 route variants for widths 2–48; K3 double rotations on 97–100-letter ragged grids; K3 double rotations on 98 letters with one omitted carved letter at each of 98 positions), each in two directions.
- **Alphabets:** 20,946 themed ones (AZ, KA and reverses; keyed, reversed and ACA-columnar alphabets of the plain-sight words and of every ordered two-word phrase). Tier D: plain = cipher alphabet (K1/K2's Quagmire III style) over all of them. Tier F: every plain/cipher pair of the 264 single-word alphabets.
- **Result (`analysis/transwin_report.txt`):** **no hit with window ≤ 8** (so no base-≤8 key, Berlin clock's base 5 included) in either tier. Tier D: 0 hits even at width 10. Tier F: 4 at width 9 and 37 at width 10, all from the unkeyed column-order family (the biggest one) and unrelated word pairs. Three null runs on shuffled K4 gave tier-F counts of 61, 25 and 6 at widths 9–10 and tier-D counts of 1, 4 and 3, so K4 sits inside chance.
- **Control (`analysis/transwin_control.txt`):** a planted text (keyed SHADOW alphabet, the K2 coordinate digits as key, then keyword columnar BERLIN) was recovered exactly: the right transposition, alphabet and rotation, and no other transposition reached width ≤ 8.

**Verdict (fact, for these families):** a K3-like or columnar transposition combined with a KRYPTOS-style single-alphabet substitution and a small-digit key is excluded, including the one-dropped-letter variant of K3's geometry.

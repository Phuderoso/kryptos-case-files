# 05 — Layers in plain sight (cycle 7, case reopened)

**Working philosophy (from Phuderoso).** K4 may be several *ordinary* steps stacked like an onion rather than one exotic cipher. Sanborn is an artist. In K1–K3 he used two things: Vigenère on the KRYPTOS tableau, and a simple matrix rotation. So this cycle tests **short, pre-registered lists** of simple compositions built only from material visible on the sculpture or in his statements. There is no annealing and no huge keyspaces.

**Gate.** All 24 official crib letters must decrypt exactly. Survivors would then be scored for English (quadgrams).
**Expected false positives.** With about 6×10^8 tests, the chance of a full-crib pass is about 26^-24 per test. In practice it is limited by key periodicity, but it is negligible for keys longer than about 6. Partial matches of up to about 10/24 are expected by chance (binomial tail ≈ 1.4×10^-8 per test).

## A. Reasoning first: what is already excluded by earlier cycles
| Plain-sight idea | Status | Why |
|---|---|---|
| K1/K2-style Vigenère on KA, any keyword ≤ 12 letters (KRYPTOS, PALIMPSEST, ABSCISSA, SHADOW, BERLIN…) | **Impossible** | Cycle 1 tested every periodic key, periods 1–26 |
| K3 rotation method (any grid, CW/CCW) + KA/AZ Vigenère with any key ≤ 12 | **Impossible** | Cycle 5 B: 216,576 exact tests |
| Reading K3→K4 as one block through the K3 rotation | **Excluded by logic** | K3 decrypts alone as exactly 336 letters (24×14 grid). Any grid spanning the K3/K4 boundary breaks the verified K3 solution |
| A key from the tableau row "T" ("T IS YOUR POSITION") | **Impossible** | A single tableau row = Caesar = period 1 |
| Running keys from K0–K3 plaintexts | **Impossible** | Cycle 2 |

What remained untested were **specific long keywords** (longer than 12), **two-word stacked keys** (double Vigenère), **tableaux keyed by other words**, **Beaufort variants with a fixed word**, and **monoalphabetic "outer skins"**. That is cycle 7.

## B. Hypothesis lists tested
**Words (95 + reversals).** All drawn from the sculpture or from Sanborn:
- K1–K3 keys and plaintext phrases: LAYERTWO, XLAYERTWO, WESTXLAYERTWO, IDBYROWS, CANYOUSEEANYTHING(Q), WHATSTHEPOINT, WHOSAYSITISHIDDEN.
- The Morse stones: VIRTUALLYINVISIBLE, DIGETALINTERPRETATU, SHADOWFORCES, LUCIDMEMORY, TISYOURPOSITION, SOS, RQ.
- The misspellings: IQLUSION, UNDERGRUUND, DESPARATLY, plus the misprint letters QUAL, EQUAL, LOE, and YAR.
- Egypt, Berlin and the clock: TUTANKHAMUN, CARTER, EGYPT, WELTZEITUHR, URANIA, ALEXANDERPLATZ, BERLINWALL.
- The site: COMPASS, LODESTONE, MAGNETICFIELD, ANTIPODES, CYRILLIC, PROJECTOR.
- Sanborn's words: MASKING, DELIGHTFUL, SCRAMBLED.
- Also: SANBORN, SCHEIDT, LANGLEY, and others; the full list is in `tools/k4_layers.py`.

**Digit keys:** the K2 coordinates (38 57 6.5 N, 77 8 44 W) and the dates 1986, 1989, 1990 and 3 Nov 1990.

| # | Hypothesis (layers, outer to inner) | Scope | Result |
|---|---|---|---|
| H1 | Keyword substitution (Vig / Beau / var-Beau; KA, AZ, or a tableau keyed by one of 12 plain-sight words) ∘ transposition (identity, reverse, single rotation, K3 double rotation CW/CCW, grid widths 2–48), both layer orders, every key phase | 4,514 transpositions × 14 tableaux × 190 word keys + 7 digit keys | **0 survivors**, 597,639,168 tests |
| H2 | Same, with **two-word stacked keys** (double Vigenère, 1,770 pairs) on identity / reverse / K3(24,8) / K3(8,24) | Included in H1's count | **0 survivors** |
| H3 | **Onion outer skin**: undo Atbash (AZ / KA), the KA↔AZ letter mapping, or a Caesar shift (1–25, AZ and KA), then H1/H2 on 86 transpositions | 54 skins | **0 survivors**, 248,956,416 tests |
| Ctrl | Planted: English + cribs, K3-method (7,14) then KA-Vigenère SHADOW, phase 2 | Same code path | Recovered exactly (1 survivor, the planted one, quadgram −4.01/char) |

**Best partial reads.** 10/24 crib letters, e.g. keyed-PALIMPSEST tableau, K3ccw(31,43), Beaufort, key IDBYROWS reversed, and the Caesar-KA-3 skin with LAYERTWO+SOSRQ. This is exactly the chance level for 6×10^8 tests (expected count ≈ 8). **No promising partial read.** I did not cherry-pick fragments.

## C. Not done, and why
- **Positional reading of K4 on the physical sculpture rows.** I do not have a verified row-by-row transcription of the copper panel with line breaks. Inventing one would violate the house rules. *Next:* source a primary high-resolution photo or a published row layout.
- **The extra tableau L as a pointer, and the Cyrillic Projector / Antipodes copies.** Testing either needs a verified layout. Antipodes reportedly repeats the K1–K4 text, but I have no primary transcription.
- **Non-letter onion layers** (numbers / Morse / binary inside letters). K4 is 97 letters with no separators. The only visible "separators" are K1–K3's X marks and '?'. K4 has neither, which argues *against* a visible-separator onion. **Inference, not proof.**

## D. Interpretation (careful)
- **Fact:** every short "plain sight" composition of Sanborn's two known tools (KA-Vigenère + rotation), keyed by any visible word, fails the cribs.
- **Inference:** "techniques not used in K1–K3" (Sanborn) is meant literally. At least one layer is something new, such as a masking step: perhaps a monoalphabetic substitution over a mixed alphabet that is not visible on the sculpture, a non-periodic key, or a hand transposition that is not a rotation.
- **Hypothesis (untested):** the "masking technique" acts on the *plaintext* before encryption (e.g. nulls, or a word-level shuffle consistent with "scrambled plain text"). That would also explain why the crib positions are stable.

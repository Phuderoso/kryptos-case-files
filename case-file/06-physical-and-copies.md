# 06 — Physical layout, the copies, and scrambled plaintext (cycle 8)

> *Third pass on the same block of copper. The user's ruling still applies: simple, ordinary layers in plain sight. One new ruling this cycle: **text sources only**. No photographs as primary evidence.*

**Sources (all text transcriptions, fetched 2026-11-04):**
- Panel row by row: Elonka Dunin, [Kryptos transcript](https://elonka.com/kryptos/transcript.html). She notes her font *"failed"* to line up exactly with the sculpture, so **column positions are approximate**. Row membership and row lengths are as transcribed. Saved as `data/elonka_panel_rows.txt`.
- Antipodes: [scirealm.org/Antipodes.html](https://scirealm.org/Antipodes.html) (a text transcription). Differences are cross-checked against Elonka's [Antipodes page](https://elonka.com/kryptos/sanborn/antipodes.html). Saved as `data/antipodes_kryptos_side_scirealm.txt`.
- Cyrillic Projector: Elonka's [Cyrillic Projector page](https://elonka.com/kryptos/cyrillic.html).

## 1. Physical-position readings (`tools/k4_physical.py`)
In this transcript, K4 fills the last 4 cipher rows: `OBKR` is at the end of row 25 (cols 27–30), followed by three full rows of 31 letters. The tableau rows beside them are **X, Y, Z and the plain-alphabet footer**. That pairing is an observation about the layout, not a decryption.

| H | Hypothesis | Tests | Survivors | Best partial |
|---|---|---|---|---|
| P1 | Read the 4 rows by column or row, in 8 directions, then apply periodic Vig/Beau P1–26 with KA or AZ | 832 | **0** | – |
| P2 | Per-row Caesar keyed by the adjacent tableau label (row offset −2..+2) | 30 | **0** | 3/24 |
| P3 | Running key = tableau letter at the same (row, col), offsets ±2 | 150 | **0** | 4/24 |
| P4 | Progressive key = column-header letter, col offset ±3 | 42 | **0** | 4/24 |

**Planted controls** (`analysis/k4_physical_control.txt`): a P3 key (dr=−1) was recovered uniquely. A P1 column read plus KA-Vig CLOCK was recovered at P=5. *Caveat:* because the columns are approximate, P3/P4 are only exact if Elonka's columns match the copper. P1 and P2 depend only on row membership.

## 2. Antipodes and Cyrillic Projector vs K4 (`tools/antipodes_diff.py`)
- The Kryptos side of Antipodes runs K3, K4, K1, K2, K3, K4, then K1 and K2 truncated.
- **Both Antipodes copies of K4 are letter-for-letter identical to Kryptos K4** (found verbatim at offsets 337 and 1206).
- Over all 1,590 letters, the only substitution is **K2 letter 116: R→E**, which corrects UNDERGRUUND to UNDERGROUND. It occurs in both copies. The tail difference is just truncation.
- K1's IQLUSION and K3's DESPARATLY are **left unchanged**.
- **Inference (labelled):** in 1997 Sanborn fixed one K2 ciphertext error and left K4 untouched, twice. That supports treating K4 *as carved* as intentional, with no "typo in K4" escape hatch. The spacing quirks in the transcription (`OBK RUOX`, `KCA R`) are line wraps in the transcription and are not evidence.
- **Cyrillic Projector:** Russian text, fully solved in 2003 (KGB/Sakharov material). It contains no K4 text, so a diff is not applicable. It contributes no cribs.

## 3. "Scrambled plaintext" as block/word shuffle (`tools/k4_shuffle.py`)
**Reasoning first.**
- If the crib positions refer to the *scrambled* text, the shuffle is invisible to the crib test. The model then collapses to CT = Sub(X), which was already excluded for periodic keys (cycle 1) and for the plain-sight keyword list (cycle 7).
- So the only new case is cribs at *original* positions:
  - S1: CT = Sub(Shuffle(PT))
  - S2: CT = Shuffle(Sub(PT))

**What was tested:** blocks of b=2..13 with simple shuffles (reverse order, swap halves, odd/even blocks, reverse inside blocks, rotations), plus **all** block permutations for b=14..49. Each was combined with periodic Vig/Beau P1–26, KA or AZ.

**Result:** 3,827,200 tests, **0 survivors**. The planted control (b14, perm (3,0,5,1,2,6,4), S1, KA-Vig SHADOW) was recovered. Its equivalents differ only in crib-free blocks.

## 4. Verdict, honestly
- Nothing in this cycle cracks K4. Three ordinary layers were excluded within the stated scope.
- One piece of evidence is firmer now: the K4 ciphertext is stable across Sanborn's own 1997 copy.
- **Open:** non-periodic keys combined with a physical read, true column geometry from an authoritative text source (Sanborn's own documents, if ever published), and word-level shuffles with a non-periodic sub.

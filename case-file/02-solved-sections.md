# Case File 02 — The Solved Sections (K1–K3)

> *Three of the four rooms were already open when I got there. I walked through them anyway. You don't trust a door just because someone tells you it isn't locked.*

All results below were **re-derived on 2026-11-04** by [`tools/solve_k1_k2_k3.py`](../tools/solve_k1_k2_k3.py); raw output: [`analysis/k1_k3_decryptions.txt`](../analysis/k1_k3_decryptions.txt). Method descriptions: [Wikipedia](https://en.wikipedia.org/wiki/Kryptos).

## K1 — keyed Vigenère (Quagmire III)
- Alphabet (both plaintext and cipher sides): `KRYPTOSABCDEFGHIJLMNQUVWXZ`; key: `PALIMPSEST`.
- Output: `BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION` ✅

## K2 — keyed Vigenère (Quagmire III)
- Same alphabet; key `ABSCISSA`. `?` characters pass through and do not advance the key.
- As carved, ending reads `...FORTY FOUR SECONDS WEST ID BY ROWS`.
- With the omitted `S` restored immediately before the last 8 ciphertext letters (i.e. `...GE`**S**`WJLLAETG`), ending reads `...SECONDS WEST X LAYER TWO` ✅ — matching Sanborn's 2006 correction (Wired, 20 Apr 2006; Wikipedia ref. 6).
- Full plaintext: `IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE? THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS? THEY SHOULD ITS BURIED OUT THERE SOMEWHERE X WHO KNOWS THE EXACT LOCATION? ONLY WW THIS WAS HIS LAST MESSAGE X THIRTY EIGHT DEGREES FIFTY SEVEN MINUTES SIX POINT FIVE SECONDS NORTH SEVENTY SEVEN DEGREES EIGHT MINUTES FORTY FOUR SECONDS WEST X LAYER TWO`
- Coordinates 38°57′6.5″N 77°8′44″W: reported ~53 m SE of the sculpture under a modern datum ([Wikipedia](https://en.wikipedia.org/wiki/Kryptos), citing Burstein & de Keijzer 2009).

## K3 — double rotational transposition
- 336 letters (final `?` is plaintext punctuation). Write in rows of 24 (14×24 grid), rotate 90° clockwise, re-grid into rows of 8, rotate 90° clockwise again, read rows.
- Our grid search over all factor pairs found the same plaintext for equivalent pairs (4,48), (8,24), (12,16), (16,12), (24,8), (48,4) — i.e. the transposition is a single fixed permutation with several equivalent descriptions.
- Output: `SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q?` ✅
- Paraphrase of Howard Carter's account of opening Tutankhamun's tomb, 26 Nov 1922 (Carter & Mace, *The Tomb of Tut-ankh-Amen* vol. 1, 1923, pp. 141–142; Wikipedia refs. 33–34).

## Observations relevant to K4
- K1/K2 = substitution; K3 = transposition. Scheidt spoke of an intentional "change in the methodology" (R. Bean, *The Conversation*, 30 May 2021; Wikipedia ref. 9). K4 thus plausibly combines layers — a *hypothesis*, tested in part in [03](03-k4-evidence.md).
- `PALIMPSEST` + `ABSCISSA` anagram to "P.S. IT'S AS SIMPLE AS ABC" (observation reported in literature; [Wikipedia](https://en.wikipedia.org/wiki/Kryptos)). Treated as curiosity, not evidence.

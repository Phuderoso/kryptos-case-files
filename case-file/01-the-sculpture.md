# Case File 01 — The Sculpture

> *Every case starts with the body. This one is copper, about twelve feet tall, and it has been lying in the same courtyard for thirty-six years.*

## Verified facts
| Fact | Source |
|---|---|
| Artist Jim Sanborn; dedicated **3 Nov 1990** at CIA HQ (George Bush Center for Intelligence), Langley, VA | [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); CIA FOIA reading room (Wikipedia ref. 1) |
| CIA contract award: **$250,000**, 1988 (contract page held in the archive) | [Paradigm archive page](https://www.paradigm.xyz/kryptos/archive); elonka.com FAQ (Wikipedia ref. 5) |
| Cipher systems designed with retiring CIA official **Ed Scheidt** | CNN, 25 Jul 2020 (Wikipedia ref. 8); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) |
| Left side: 869 characters (865 letters + 4 `?`); right side: KRYPTOS-keyed Vigenère tableau of 867 letters with one extra `L` | [Wikipedia](https://en.wikipedia.org/wiki/Kryptos); [Bauer, Link & Molle, *Cryptologia* 40(6), 2016](https://doi.org/10.1080/01611194.2016.1141556) |
| K1–K3 solved: NSA team (Ken Miller et al., by 1992–93), CIA analyst David Stein (1998), Jim Gillogly (public, 1999) | Wired, 10 Jul 2013 (Wikipedia ref. 23); Stein, *Studies in Intelligence* 43(1) (Wikipedia ref. 17); NYT, 16 Jun 1999 (Wikipedia ref. 16) |

## Ciphertext (left panel), as transcribed
Transcription follows [Wikipedia, note 1](https://en.wikipedia.org/wiki/Kryptos); it is encoded verbatim in [`tools/kryptos_text.py`](../tools/kryptos_text.py). Its correctness is **empirically confirmed**: K1–K3 decrypt cleanly with it (see [02](02-solved-sections.md)).

**K1 (63)** `EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD`

**K2 (372 incl. 3 `?`)**
```
VFPJUDEEHZWETZYVGWHKKQETGFQJNCEGGWHKK?DQMCPFQZDQMMIAGPFXHQRLG
TIMVMZJANQLVKQEDAGDVFRPJUNGEUNAQZGZLECGYUXUEENJTBJLBQCRTBJDFHRR
YIZETKZEMVDUFKSJHKFWHKUWQLSZFTIHHDDDUVH?DWKBFUFPWNTDFIYCUQZERE
EVLDKFEZMOQQJLTTUGSYQPFEUNLAVIDXFLGGTEZ?FKZBSFDQVGOGIPUFXHHDRKF
FHQNTGPUAECNUVPDJMQCLQUMUNEDFQELZZVRRGKFFVOEEXBDMVPNFQXEZLGRE
DNQFMPNZGLFLPMRJQYALMGNUVPDXVKPDQUMEBEDMHDAFMJGZNUPLGEWJLLAETG
```
**K3 (336 letters + `?`)**
```
ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIACHTNREYULDSLLSLLNOHSNOSMRWXMNE
TPRNGATIHNRARPESLNNELEBLPIIACAEWMTWNDITEENRAHCTENEUDRETNHAEOE
TFOLSEDTIWENHAEIOYTEYQHEENCTAYCREIFTBRSPAMHHEWENATAMATEGYEERLB
TEEFOASFIOTUETUAEOTOARMAEERTNRTIBSEDDNIAAHTTMSTEWPIEROAGRIEWFEB
AECTDDHILCEIHSITEGOEAOSDDRYDLORITRKLMLEHAGTDHARDPNEOHMGFMFEUHE
ECDMRIPFEIMEHNLSSTTRTVDOHW?
```
**K4 (97)** `OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR`

## Known anomalies (evidence, not noise — until proven otherwise)
| Anomaly | What is known | Source |
|---|---|---|
| **K2 missing `S`** | Sanborn (Apr 2006) admitted omitting a letter; restoring it changes the K2 ending from `WESTIDBYROWS` to `WESTXLAYERTWO`. Reproduced in our code. | [Wired, 20 Apr 2006](https://www.wired.com/2006/04/typo-confounds-kryptos-sleuths/) |
| **IQLUSION** (K1) | Misspelling; Sanborn's 2010-published coding chart shows key typo `PALIMPCEST` producing it | NYT, Original Decoding Charts, 2010 (Wikipedia ref. 29); [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) |
| **UNDERGRUUND** (K2) | Chart has `E` under the O; sculpture has `R` → decrypts to U | same |
| **DESPARATLY** (K3) | Misspelling of DESPERATELY; Sanborn called misspellings intentional | [Wired, 20 Apr 2006](https://www.wired.com/2006/04/typo-confounds-kryptos-sleuths/) |
| Superscript **YAR** | Only superscript letters on the sculpture (start of lower left half, within K3) | [Wikipedia](https://en.wikipedia.org/wiki/Kryptos) |
| Extra **L** in tableau | Spells `HILL` down the right column; *conjecture* of Hill cipher in K4 | [Bauer et al. 2016](https://doi.org/10.1080/01611194.2016.1141556) |
| Sanborn quote | "most of my things are rife with mistakes on purpose" (2005) | Wired, 20 Jan 2005 (Wikipedia ref. 10/31) |

`HYPOTHESIS (open):` the anomalous letters (Q in IQLUSION, U in UNDERGRUUND, A in DESPARATLY, YAR) encode K4 key material. Status: untested; scheduled for cycle 2.
Secondary-source note: items marked '(Wikipedia ref. N)' are cited through the reference list of https://en.wikipedia.org/wiki/Kryptos (fetched 2026-11-04); primary links to be added after direct verification.

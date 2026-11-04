# Case File 03 — K4: The Evidence Locker

> *Ninety-seven letters. Four confessions extracted from the artist over fourteen years, a million-dollar sale, and a solution that two reporters found sitting in a box in Washington. Everybody knows something. Nobody's talking.*

## 1. Official plaintext clues (cribs), 1-indexed positions in K4
| Pos. | Ciphertext | Plaintext | Released | Source |
|---|---|---|---|---|
| 22–25 | `FLRV` | `EAST` | Aug 2020 | J. Schwartz (NYT), tweet 24 Aug 2020 (Wikipedia ref. 40) |
| 26–34 | `QQPRNGKSS` | `NORTHEAST` | Jan 2020 | NYT, 29 Jan 2020 (Wikipedia ref. 11) |
| 64–69 | `NYPVTT` | `BERLIN` | Nov 2010 | NYT, 20 Nov 2010; NPR, 22 Nov 2010 (Wikipedia refs. 35–36) |
| 70–74 | `MZFPK` | `CLOCK` | Nov 2014 | [NYT, 20 Nov 2014](https://www.nytimes.com/2014/11/21/us/another-kryptos-clue-is-offered-in-a-24-year-old-mystery-at-the-cia.html) |

Alignment re-checked in code: [`analysis/k4_report.txt`](../analysis/k4_report.txt). Positions 22–34 combine into `EASTNORTHEAST`; 64–74 into `BERLINCLOCK`. Note self-encryptions at pos. 33 (S→S) and 74 (K→K): a letter can encrypt to itself, which rules out any cipher where that is impossible (e.g. Enigma-style reciprocal without fixed points).

## 2. Sanborn's statements bearing on K4
- Answers to K1–K3 "contain clues" to K4 (2006) — [Wired, 20 Apr 2006](https://www.wired.com/2006/04/typo-confounds-kryptos-sleuths/).
- 2014: asked whether CLOCK meant the *Berlin clock* (the set-theory **Mengenlehreuhr**), Sanborn said "There are several really interesting clocks in Berlin" and "You'd better delve into that particular clock" — [NYT, 20 Nov 2014](https://www.nytimes.com/2014/11/21/us/another-kryptos-clue-is-offered-in-a-24-year-old-mystery-at-the-cia.html).
- **Nov 2025 (correction of the 2014 ambiguity):** "The Berlin Clock in K4 is the World Clock in Berlin that was the gathering place for the crowds that brought down the Berlin wall" (Weltzeituhr, Alexanderplatz). Same letter: two events shaped the 1988 plaintext — his second trip to **Egypt, late 1986**, and the **fall of the Berlin Wall**; the codes are about "delivering a message"; K5 is 97 characters, "similar coding system to K4", with BERLINCLOCK in the same position. — [Scientific American, 12 Nov 2025](https://www.scientificamerican.com/article/cia-kryptos-puzzle-creator-releases-final-clues/); letter text transcribed at [numberworld.blog](https://www.numberworld.blog/2025/11/jim-sanborn-open-letter.html) (secondary transcription) and quoted in [Popular Mechanics](https://www.popularmechanics.com/science/math/a69447312/kryptos-puzzle-clues/).
- **Key evidentiary line (same letter):** "K4 has not been solved or decrypted. The scrambled plain text was found, but without the coding method or key." The word *scrambled* is consistent with a **transposition layer** (my inference, labelled as such). (Note: SciAm's text says "79 encrypted letters"; K4 has 97 — a typo in the article.)
- Weltzeituhr facts: 24-sided cylinder, one side per time zone, 146 place names; city names were changed and 20 added in the 1997 renovation, so the 1988 city list differs from today's — [de.wikipedia: Weltzeituhr (Alexanderplatz)](https://de.wikipedia.org/wiki/Weltzeituhr_(Alexanderplatz)). A primary 1988-era city list is still an open lead.
- Scheidt: intentional "change in the methodology" — Wikipedia ref. 9.
- A fifth message, **K5**, exists and follows K4 (open letter, Aug 2025) — Wikipedia ref. 48; the RR Auction lot lists "an unpublished 1988 alternate of the K4 plaintext and coding chart now known as K5" ([RR Auction](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)).

## 3. The 2025 auction
- Announced Aug 2025 (Washington Post letter); RR Auction sale "Decoding History", 16 Oct–20 Nov 2025 (Wikipedia refs. 2, 12–13).
- **Sold for $962,500** ([RR Auction lot page](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/)). Contents per lot: handwritten K4 plaintext with signed Scheidt letter, K1–K3 coding charts, the K4 coding system, 1988 alternates (K1 and "K5").
- RR Auction stated it had **not independently examined** the materials and that the K4 plaintext "may become publicly known through independent research or disclosure" (same page).

## 4. The Smithsonian discovery (Sep 2025)
- Jarett Kobek and Richard Byrne found, in Sanborn's papers at the Archives of American Art, fragments that together yield the K4 plaintext; Sanborn confirmed it. Files then **sealed for 50 years** — NYT, 16 Oct 2025; Scientific American (Wikipedia refs. 44–45); also stated on the [RR Auction lot page](https://www.rrauction.com/auctions/lot-detail/350761607302001-the-complete-secrets-of-kryptos-jim-sanborns-private-archive/).
- They refused NDAs but have **not published** the plaintext. In June 2026 Kobek told Wired: *"There will never be a moment in which the plaintext is published by me."* ([Wired](https://www.wired.com/story/crypto-guys-bought-the-answer-to-the-cias-mysterious-kryptos-sculpture/))
- **Implication:** the plaintext is *known* to a few people, but the **method** (how the ciphertext was produced) is the open scientific problem, and there is no public plaintext. As of 2026-11-04 I found no credible public release.

## 5. The buyer: Paradigm (Jun 2026)
- VC firm **Paradigm** disclosed on 12 Jun 2026 it was the winning bidder ([Paradigm, "Project Kryptos"](https://www.paradigm.xyz/writing/kryptos); [Wired](https://www.wired.com/story/crypto-guys-bought-the-answer-to-the-cias-mysterious-kryptos-sculpture/)).
- Paradigm says it has **not seen** the plaintext: Sanborn typed it into an air-gapped laptop which computed SHA-256, then an HMAC via Google Cloud KMS; the laptop was wiped. Submissions cost **$1** at [paradigm.xyz/kryptos/k4](https://paradigm.xyz/kryptos/k4) (Sanborn used to charge $50). Prize: glory + a video from Sanborn.
- A capture-the-flag of 10 Kryptos-style puzzles, $1,000 per first solver.
- **Consequence for us:** a candidate K4 plaintext can now be **objectively verified**. That's the finish line of this investigation.

## 6. Tested hypotheses (cycle 1)
`HYPOTHESIS H1:` K4 is a periodic Vigenère / Beaufort / Variant-Beaufort over the standard (AZ) or KRYPTOS (KA) alphabet applied directly to the plaintext, with period P.
- **Test:** for each crib position compute the implied key letter; P is viable only if positions congruent mod P agree. Code: [`tools/k4_analysis.py`](../tools/k4_analysis.py).
- **Result:** every period **1–26 is falsified** in all 6 variants. Periods 27–29 survive only vacuously (no two crib positions collide — zero constraints), and P ≥ 53 is likewise unconstrained. **H1 rejected for P ≤ 26.** This independently confirms a long-standing community conclusion and agrees with Bean's cryptodiagnosis (HistoCrypt 2021, doi:[10.3384/ecp183153](https://doi.org/10.3384/ecp183153)).
- **Statistics:** IoC(K4) = 0.0361, close to random (0.0385), far from English (0.0667) — consistent with a polyalphabetic, long-key, or multi-layer system; uninformative alone at n = 97.

## 7. Cycle 2 results (2026-11-04) — all negative
Code: [`tools/k4_cycle2.py`](../tools/k4_cycle2.py) → [`analysis/k4_cycle2_report.txt`](../analysis/k4_cycle2_report.txt). Positive controls (synthetic K4s built with a known Hill key and a known transposition+Vigenère, with the real cribs) are **detected** by the same code: [`tools/validate_cycle2.py`](../tools/validate_cycle2.py) → [`analysis/validate_cycle2.txt`](../analysis/validate_cycle2.txt). So the negatives below are not bugs.

| Hypothesis | Test | Result |
|---|---|---|
| H4 Hill 2×2 / 3×3 | Exhaustive per-row solve mod 26 over all crib blocks, AZ and KA numbering, all block alignments | **0 invertible keys** in all 10 configurations → **falsified** |
| H2 transposition + periodic substitution | 224 permutations (rows-of-w read by columns down/up = K3-style rotation, w=2..48; keyed columnar with 18 keywords; all inverses) × 2 alphabets × 3 modes × 2 orders × P=1..26 = 69,888 configs; survivor = consistent with ≥6 crib constraints | **0 survivors** (random-permutation baseline: 0/2000) → this family **falsified** |
| Non-periodic keys | CT-autokey (lags 1–21), PT-autokey (lags 1–12), all 6 alphabet/mode combos | **0 consistent** → **falsified** |
| Running key from K0–K3 plaintexts / tableau | All offsets, forward & reversed | best 8/24 matches (noise level); 24/24 needed → **falsified** |
| H5 misspelling keys / H3 World Clock words | 34 keyword alphabets (QUA, YAR, IQLUSION, UNDERGRUUND, DESPARATLY, PALIMPCEST, WELTZEITUHR, URANIA, ALEXANDERPLATZ, MENGENLEHREUHR, EGYPT…) as Quagmire-III tableaux, P=1..26 | **0 survivors** → **falsified** for this construction |

**What this eliminates:** every "one classical layer" model and the simplest two-layer models. **What it does not:** irregular/keyed route transpositions over a 97-letter grid beyond those tried, Quagmire I/II/IV with two independent alphabets, keys derived from *numbers* (World Clock zone offsets, dates 1986/1989), and a physical/mechanical procedure Sanborn alludes to ("coding method").

## 8. Open hypotheses (to test)
- `H2` transposition + Quagmire III (K3 layer then K1/K2 layer, or reverse) — "change in methodology".
- `H3` key derived from the Weltzeituhr (24 time zones / city ring) — Sanborn's World Clock confirmation.
- `H4` Hill cipher (extra L → HILL; Bauer et al. 2016) — testable with the 24 crib letters: a 2×2 or 3×3 Hill must satisfy linear constraints mod 26.
- `H5` anomaly letters (Q, U, A, YAR, the missing S/X) as key material.

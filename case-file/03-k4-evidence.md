# Case File 03 — K4: The Evidence Locker

> *Ninety-seven letters. Four confessions extracted from the artist over fourteen years, a million-dollar sale, and a solution that two reporters found sitting in a box in Washington. Everybody knows something. Nobody's talking.*

## 1. Official plaintext clues (cribs), 1-indexed positions in K4
| Pos. | Ciphertext | Plaintext | Released | Source |
|---|---|---|---|---|
| 22–25 | `FLRV` | `EAST` | Aug 2020 | J. Schwartz (NYT), tweet 24 Aug 2020 (Wikipedia ref. 40) |
| 26–34 | `QQPRNGKSS` | `NORTHEAST` | Jan 2020 | NYT, 29 Jan 2020 (Wikipedia ref. 11) |
| 64–69 | `NYPVTT` | `BERLIN` | Nov 2010 | NYT, 20 Nov 2010; NPR, 22 Nov 2010 (Wikipedia refs. 35–36) |
| 70–74 | `MZFPK` | `CLOCK` | Nov 2014 | NYT, 20 Nov 2014 (Wikipedia refs. 37–38) |

Alignment re-checked in code: [`analysis/k4_report.txt`](../analysis/k4_report.txt). Positions 22–34 combine into `EASTNORTHEAST`; 64–74 into `BERLINCLOCK`. Note self-encryptions at pos. 33 (S→S) and 74 (K→K): a letter can encrypt to itself, which rules out any cipher where that is impossible (e.g. Enigma-style reciprocal without fixed points).

## 2. Sanborn's statements bearing on K4
- Answers to K1–K3 "contain clues" to K4 (2006) — Wired, 20 Apr 2006 (Wikipedia ref. 6).
- "You'd better delve into that particular clock" / "several really interesting clocks in Berlin" (2014) — NYT (Wikipedia ref. 38).
- In 2025 Sanborn confirmed the clock is the **World Clock** (Weltzeituhr, Alexanderplatz) — Scientific American (Wikipedia ref. 39).
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

## 7. Open hypotheses (to test)
- `H2` transposition + Quagmire III (K3 layer then K1/K2 layer, or reverse) — "change in methodology".
- `H3` key derived from the Weltzeituhr (24 time zones / city ring) — Sanborn's World Clock confirmation.
- `H4` Hill cipher (extra L → HILL; Bauer et al. 2016) — testable with the 24 crib letters: a 2×2 or 3×3 Hill must satisfy linear constraints mod 26.
- `H5` anomaly letters (Q, U, A, YAR, the missing S/X) as key material.

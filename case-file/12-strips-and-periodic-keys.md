# 12 — Strips, periodic keys, and a correction to my own lead (cycle 13)

> *Somebody told me the pages were cut into strips. I went looking for a strip-cutter in the cipher. Turns out the scissors belonged to a different job.*

## 1. Audit first: the "strips" lead was over-read in cycle 12
Cycle 12 cited [cipher.ink](https://cipher.ink/ciphers/kryptos) (secondary) for the Smithsonian pages being text "cut into strips and taped together out of order", and called it a lead for a strip transposition (hypothesis S6 of [case file 10](10-style-profile.md)). Re-reading the sources this cycle:
- [RR Auction](https://content.rrauction.com/kryptos-k4-discovered-not-solved-heres-what-actually-happened/) reports Sanborn's explanation: he cut **plaintext sentences** into strips and taped them out of order so the CIA's historical office could check the content wasn't inappropriate without easily keeping the full meaning. The same piece quotes Sanborn: what was found was "scrambled text, and not by solving the cryptogram… they certainly did not find the key."
- [Wren's Cipher Room (May 2026, secondary)](https://vera-wren.github.io/posts/2026-05-04-the-answer-that-isnt-a-solution.html) gives the same account.

**Correction (fact vs. inference):** the strips were a 1990 *disclosure device* for the plaintext, not a documented step of the encryption. Sanborn's "scrambled plain text" phrase most plausibly describes those strips. So neither the strips nor that phrase is evidence of a transposition layer inside K4's cipher. Cycle 2's reading of the phrase as pointing to a transposition and cycle 12's S6 should both be treated as **weak**. S6 was still tested below because the test was cheap and the space is otherwise unexamined.

## 2. Strip transpositions (`tools/strip_gen.py`)
Text written in strips of width w (the last one shorter) and the strips put in a different order, in both directions (plaintext strips reordered, or carved strips reordered), with the short strip at every possible slot. Only the 24 crib positions matter to every test here, so each assignment of distinct strips to the crib-bearing rows was enumerated: widths 9–48, **292,544 transpositions, 147,709 distinct on the cribs**. Gap: widths ≤ 8 (13 or more strips, 6 crib rows) weren't enumerated.

## 3. New generic test: periodic key of *any* letters after undoing a transposition (`tools/c/periodic_perm.c`)
Rather than trying key words one by one (hypothesis S2: CLOCK, ZEIT, BASE, WELTZEITUHR, MENGENLEHRE…), the tool asks whether *any* periodic key fits: the 24 crib key values must agree inside each residue class. That covers every key word of length ≤ 16 at once.
- Alphabets: the 264 single-word themed alphabets (AZ, KA, reverses, plain-sight words), used as Quagmire III (same alphabet on both sides, K1/K2 style), Quagmire II (AZ plain) and Quagmire I (AZ cipher).
- Modes: Vigenère (which gives the same consistency test as variant Beaufort) and Beaufort; key indexed by plaintext position or by carved position (substitute-then-transpose or the reverse).
- Transpositions: the 147,709 strip ones plus cycle 12's 96,630 (columnar ≤ 8 in every order, keyword columnar, routes, K3 double rotations incl. one omitted letter).
- Chance level: for period p ≤ 13 a random survivor has probability about 26^-(24-p) per test, so with about 2×10^9 tests anything that survived would be significant.

**Result ([report](../analysis/periodic_perm_report.txt)): zero survivors at every period 1–16 in both transposition sets.** Control ([control](../analysis/periodic_perm_control.txt)): a planted text (Quagmire III on KA with key CLOCK, then strips of 11 reordered) was recovered exactly, the only hits being the right transposition with key CLOCK at period 5 and its doubling at 10.

## 4. Strips + small-digit key ("change the base", any generator)
The cycle-12 window test (`tools/c/transwin.c`, unchanged) on the 147,709 strip transpositions, 20,946 themed alphabets (tier D) and 264×263 pairs (tier F) ([report](../analysis/strip_window_report.txt)):
- **K4: no hit with window ≤ 8**, so no base-≤8 digit key; 4 + 59 hits at widths 9–10.
- Three shuffled-K4 nulls: 75, 86 and 78 hits at widths 9–10, and two of them even reached width 8. K4 is at or below chance.
- Control ([control](../analysis/strip_window_control.txt)): keyed SHADOW alphabet, K2 coordinate digits as key, strips of 13 reordered → recovered exactly (the right strip order, alphabet and width 6); nothing else reached width ≤ 8 except the same transposition with the reversed alphabet.

## 5. Verdict
| Hypothesis | Status |
|---|---|
| S6 strip transposition + periodic key (any letters, p ≤ 16, 264 alphabets, QI/QII/QIII) | **negative** (0 survivors) |
| S6 strip transposition + small-digit key (base ≤ 8) | **negative**; base 9–10 at chance |
| S2 meta-word key (any word of length ≤ 16) on all cycle 12–13 transpositions with those alphabets | **negative** (subsumed by the generic periodic test) |
| "Scrambled plain text" / strips as evidence of a transposition layer | **downgraded**: it describes the 1990 CIA review copy |

## 6. Relation to cycle 11b
Case file [11](11-sat-families-and-phrase-alphabets.md) (a parallel run) proved with SAT that a periodic key with *both alphabets arbitrary* is impossible on K4 as carved for periods 1–7 and several others. This file is the complement: alphabets restricted to themed keyword ones, but with ~244k transpositions undone first.

## 7. What this changes
The style-pure reading "one simple transposition + one KRYPTOS-style periodic or digit substitution" is now closed for every transposition family examined in cycles 2–13. What remains open and still fits the style profile: a key that is **not periodic** (running key from a text not yet tried, a progressive or autokeyed alphabet like Chaocipher), a substitution whose alphabet isn't a keyword alphabet, or a transposition outside the enumerated families (irregular masks, K3 geometry on the *combined* K3+K4 text).

# Case file 55 — Nicodemus (block-read columnar with per-column key) and Slidefair (digraphic slide), exact (cycle 57)

**Why these families.** Both were owed since cycle 55 ("keyless, structure-driven ACA ciphers") and neither is in the
repo or in kryptosbot's published list (Sept 29, 2026). Nicodemus is the closest ACA relative of what K1–K3 actually
use: a keyword that is both a Vigenère key and a column order, with the text read off in short blocks, which breaks
the long columns every columnar test so far has assumed. Slidefair is the simplest digraphic cipher that needs only a
Vigenère tableau, i.e. exactly the tool carved on the sculpture. New families for the coverage table (diversity rule).

## A. Nicodemus, generalised (`tools/nicodemus.c`)

**Model.** Plaintext in rows of width w; plaintext column c gets its own shift k_c (any letter, not only the keyword's)
on a tableau from one alphabet A (Vigenère a(c) = a(p) + k_c or Beaufort a(c) = k_c − a(p); variant = Vigenère with
negated key). Columns re-ordered by σ (any order, not only a keyword's); then read in blocks of h rows: for each block,
down each column in σ order through that block only, ragged last row skipped. ACA's standard is h = 5; h equal to
the row count is ordinary columnar + period-w key (overlap with cycle 13, kept as a check).
**Test.** The 24 crib key values must be constant within each plaintext column. Exact, no scoring needed; survivors are
fully decrypted and scored per quadgram.
**Range.** Every σ for w 2–11 on A–Z and KRYPTOS; every σ for w 2–7 on the first 2,000 alphabets of `data/alpha.bin`;
h 1–rows (≤ 20); Vigenère/Beaufort. 1.94 × 10⁹ configurations per text.

| Text | Consistent configurations |
|---|---|
| **K4** | **0** |
| 5 shuffled-K4 nulls | 0, 0, 0, 0, 0 |
| NCTL1 classic ACA: A–Z, keyword SHADOW (shifts and order), h = 5 | found: SHADOW, exact plaintext (+ the reversed-alphabet twin) |
| NCTL2 KRYPTOS, Beaufort, w 9, arbitrary order, h 4, shifts LUCIDMEMO | found, unique, exact plaintext |
| NCTL3 alphabet #1500, w 7, h 3, keyword BERLINS | found, exact plaintext (+ one equivalent alphabet) |

## B. Slidefair (`tools/slidefair.c`)

**Model.** Digraphs from offset 0 (97th letter left over) or 1 (first letter left over); digraph j uses key letter
K[j mod L]. Top row A; bottom row A slid by k (Vigenère A[x+k], Beaufort A[k−x], variant A[x−k]). c1 = bottom letter
under p1, c2 = top letter above p2; if the columns coincide both move one right.
**Test.** For each digraph that touches a crib, the 26-bit set of key values that decrypt it to the known letters;
sets ANDed per residue mod L. Periods 1–48 on all 86,731 alphabets × 3 forms × 2 offsets.

| Text | Survivors (any L ≤ 48) |
|---|---|
| **K4** | **0** |
| 5 shuffled-K4 nulls | 0 each |
| SCTL1 A–Z, Vigenère form, PALIMPSEST, offset 0 | found at L = 10 (PALIMPS??? — residues 7–9 untouched by cribs) |
| SCTL2 KRYPTOS, Beaufort form, ABSCISSA, offset 1 | found, fully determined at L = 8 |
| SCTL3 alphabet #4000, variant, IQLUSION | found at L = 8 (also as its negated Vigenère twin) |

**Stronger than periodic.** At L ≥ 27 every crib digraph has its own residue, so 0 survivors there means some fully
known crib digraph has no key value at all on every one of these alphabets: Slidefair is excluded for **any key
sequence**, periodic or not, on all 86,731 alphabets, both offsets, all three forms. (A digraph with both letters known
gives two equations for one unknown, so it fails ~25 times in 26 under a wrong alphabet.)

## C. Audit of the cycle-12 transposition file (cycle 55's open note)

Cycle 55 reported 3,296 entries "with indices past 96". That was a misread: `data/c12_perm.bin` is **signed** int16,
and the large values are **−1**, which `tools/transwin_gen.py` uses for the K2-style omitted letter (true text 98
letters, one left off the copper). 3,104 entries contain a −1; in **768** of them the −1 falls on a crib position.
`tools/c/periodic_perm.c` (cycle 13) did not check for −1 and read `CT[-1]` for those 768 entries, so they were not
properly tested. Fixed (an omitted crib letter is now skipped, which can only add survivors) and re-run on the 768
entries with cycle 13's settings (264 alphabets, QI/QII/QIII, vig/beau, periods 1–16, both key indexings):
**0 survivors** (`data/cycle57/audit_c13_omit.out`; all other raw output in `data/cycle57/results57.txt`). Cycle 13's conclusion stands. `tools/c/transwin.c` already
handled −1 correctly; `tools/ragperm.c` (cycle 55) reads the file as unsigned but stops before entry 93,334, so it
simply did not test the omitted-letter entries (now noted in its coverage row).

## Verdict
Negative for Nicodemus (w ≤ 11 on A–Z/KRYPTOS, w ≤ 7 on 2,000 keyed alphabets, any order, any block height) and for
Slidefair (any key, 86,731 alphabets). **Still open:** Nicodemus on arbitrary alphabets or w ≥ 12; Nicodemus with a
running key per column; Slidefair on arbitrary alphabets (a small SAT model: each fully known digraph is one linear
condition on the alphabet); Slidefair behind a transposition; Portax and Cadenus (Cadenus needs a multiple of 25
letters, so it would need 3 nulls — K4's 97 does not fit it as specified).

# Case file 35 — Running keys in plain sight at Langley, plus "hex inside hex" taken literally

**Cycle 36, 2026-11-04.** Status: **negative.**

## Why
Cycle 35 closed K3's source book; its journal left two cheap gaps and one open idea. First, cycle 34's carved
texts (K1–K3 plaintexts and ciphertexts, K0 Morse, the KA tableau) had only been run under 11 substitutions, not
the 24-tableau set that covers Quagmire I–III on KRYPTOS. Second, a running key could come from texts that sit
"in plain sight" at the CIA rather than in Sanborn's sources: the lobby motto is John 8:32 ("Ye shall know the
truth and the truth shall make you free"), the Agency's charter is the National Security Act of 1947, and
BERLINCLOCK points at Berlin (Reagan's 1987 Brandenburg Gate speech). Third, the user's "hex inside hex" hunch,
taken literally as a digit-level regrouping.

## Test A — running keys (tool `bookrk.c`, unchanged from cycle 35)
Key texts, each forward and reversed (carved texts as in cycle 34):
- cycle 34's 24 carved texts;
- KJV Gospel of John (75,525 letters; Project Gutenberg #10; the John 8:32 motto checked present);
- KJV New Testament (740,112 letters);
- Reagan, Brandenburg Gate, 12 June 1987 (12,595 letters; reaganlibrary.gov transcript);
- National Security Act of 1947 **as amended** (431,490 letters; govinfo COMPS-1493). Caveat: this is today's
  amended compilation, not the 1947 slip law; the 1947 wording survives in many sections, but not all.
JFK's 1963 Berlin speech was not reachable (jfklibrary.org blocked the box) and is not included.

Every offset × 29 substitutions (24 additive tableaux over A–Z/KRYPTOS for plain, cipher and key numbering;
5 five-bit XOR codes) × 165,065 transpositions (cycle 19 family, identity included) × both layer orders,
exact crib test. "best" = longest run of crib constraints one offset satisfies together; "full" = 24/24.

| text | best | full |
|---|---|---|
| k4 | 9 | 0 |
| ctl_1 | 24 | 4 |
| ctl_2 | 24 | 1 |
| ctl_3 | 24 | 3 |
| ctl_4 | 24 | 1 |
| null_1 | 10 | 0 |
| null_2 | 10 | 0 |
| null_3 | 9 | 0 |
| null_4 | 9 | 0 |
| null_5 | 10 | 0 |
| null_6 | 9 | 0 |
| null_7 | 9 | 0 |
| null_8 | 9 | 0 |

K4's best (9) sits inside the 8 shuffled-K4 nulls (9–10). All 4 planted controls (John, NatSec Act reversed,
K3 plaintext, Reagan; mixed tableaux, both layer orders) were recovered at their planted perm, mode and offset.
The extra control hits are the same key letters found again inside a containing text (John inside the New
Testament, K3 inside K1–K3) or the crib-equivalent transposition seen in cycle 35. **Negative.**
This closes cycle 35's note that the carved texts needed the 24-tableau rerun.

## Test B — "hex inside hex", literal (`hexhex.py`)
Each carved letter → number (A–Z or KRYPTOS order, 0- or 1-based) → two digits in base b (6–16) → the
194-digit stream regrouped (shift by one digit either way, reversed, digit complement, pair swap, odd/even split
and its inverse) → pairs read back as letters. For K4 and 10 shuffled nulls, **no** regrouping yields 97 valid
letters (every reading hits a pair ≥ 26), and in 20,000 attempts no planted plaintext could even be encrypted
this way. So a pure two-digit regrouping is structurally out for any 26-letter text of this length; it would
need a mod-26 wrap (not invertible) or a full 5×5 square (impossible: K4 uses all 26 letters, case file 20).
**Negative (structural).**

## Reproduce
`python3 prep_texts.py` (needs the four sources in `src/`), `python3 controls.py`, `gcc -O3 -o bookrk bookrk.c`,
`tools/bookrk_runall36.sh` (tool `tools/bookrk.c` from cycle 35); `python3 hexhex.py`. Outputs in `analysis/cycle36_report.txt`.

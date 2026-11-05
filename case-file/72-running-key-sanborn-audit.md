# 72 — Audit: do the running-key tools speak Sanborn's dialect? (cycle 74)

**Type:** audit (diversity rule: cycle 73 was a new family; 74 is the permitted audit/extension; 75 or 76 must be new).

## Why
Cycle 72 checked the periodic and decimation solvers with controls enciphered the way K1/K2 were actually made, but
left the running-key bitset tools — the backbone of cycles 34–36, 45, 69 and 70 — with only self-generated controls.
A shared convention slip between generator and solver (key numbering, key frame behind a transposition, offset
bounds) would pass those controls and still blind every running-key negative.

## Method
`tools/cycle74/gen74.py` enciphers with Sanborn's own rule: the exact inverse of the decryptor that reproduces carved
K1 (PALIMPSEST) and K2 (ABSCISSA) — KRYPTOS tableau, key letter added in KA numbering, one key letter per plaintext
letter. Key = a running text at a random offset. Model A: substitute in plaintext order, then transpose (key follows
plaintext positions). Model B: transpose first, then substitute in carved order (key follows carved positions).
Seven controls, each a K4-length English text with EASTNORTHEAST and BERLINCLOCK at the official positions:

| # | key text | model | stress point |
|---|---|---|---|
| 0 | Carter vol. I (284,914 letters) | A | ordinary |
| 1 | Carter vol. I | B | carved-frame key |
| 2 | Carter reversed | A | reversed source |
| 3 | K2 plaintext (369 letters) | B | sculpture text, offset 1 |
| 4 | Carter vol. I | A | **last possible offset** (284,817) — off-by-one at the book's end |
| 5 | K1 plaintext (63 letters) | B | key shorter than K4, **wraps** |
| 6 | K1 plaintext | A | wraps, plaintext frame |

Solvers, unchanged: `bookrk.c` (cycles 35–36, 29 substitutions, non-cyclic offsets, bitset AND) on controls 0–4;
`carved_rk69.c` (cycles 34, 69, 70, 11 substitutions, cyclic offsets) on all seven. Transpositions: the first 3,000
of the 165,065 cycle-12 family (planted ones drawn from them). K4 itself run alongside as a reproducibility check.

## Result
- **12/12 solver runs recovered their control**: a 24/24 crib fit at the planted transposition, the planted
  offset and the Sanborn mode (`bookrk` mode 21 = KA/KA/KA Vigenère; `carved_rk` mode 3). Re-deciphering each from
  the solver's reported configuration, with the solver's convention, returns **all 97 planted letters** in every case
  (`analysis/cycle74_verify.txt`).
- The two extra 24/24 hits (perms 937 and 2195) are distinct transpositions that agree with the planted one on all
  24 crib positions (they differ in 32 other slots) — expected, not false positives.
- No false 24/24 anywhere else; best non-planted depths 22 (carved_rk, control 0, partial-key coincidences) and 19 (bookrk).
- K4 on the same 3,000 transpositions: bookrk best 7/24, carved_rk best 11/24, 0 full fits — consistent with cycles 35 and 34/69.

## A latent limit found
`carved_rk69.c` reads each key text with `%63s %8191s`. A text longer than 8,191 letters is silently chopped into
8,191-letter pieces separated by 63-letter "names" that are never used as keys (controls 0, 2 and 4 were still
recovered because their windows fell inside one piece). **Every text actually fed to it in cycles 34, 69 and 70 was
≤ 867 letters** (checked on the run directories), so no published negative is affected; long books always went
through `bookrk` (2,000,000-letter buffer). Noted in the tool's usage line for the future.

## Verdict
**PASS.** The running-key negatives of cycles 34–36, 69 and 70 are not convention or offset artefacts. Cycle 45's
rail/AMSCO running-key tool was not re-run here; it is next on the audit list. Limits: only Sanborn's KA Vigenère was tested externally; Beaufort/XOR modes still rest on self-generated
controls (Sanborn used neither in K1–K3).

Reproduce: `tools/run_cycle74.sh`. Runs: [`analysis/cycle74_runs.txt`](../analysis/cycle74_runs.txt); planted configs:
[`analysis/cycle74_controls.json`](../analysis/cycle74_controls.json).

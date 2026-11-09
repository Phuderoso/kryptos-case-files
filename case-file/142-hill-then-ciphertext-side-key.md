# Case file 142 — Hill first, then a periodic key on the ciphertext side (cycle 154)

**Cycle 154, 2026-11-08. New structure** (IDEAS [I-012](../IDEAS.md); limits of [case 132](132-hill-plus-periodic-key.md)). Evidence labels as in IDEAS I-004.

## Why this family, and why it is new
Cycle 153 was an audit, so the diversity rule required a new family. The queue's default was I-012, the item case 132 left open.
Case 132 tested **Vigenère first, then Hill** (decoder `out = D·c + e[t mod k]`). Cycle 154 tests the **reverse layer order**:
Hill first, then a period-k Vigenère on the Hill output:

    encryption  L = E·p_block + f[(position) mod k]        decoder  p_block = D·(L_block − f),  D = E⁻¹

This is the K1–K3 layering (a keyed substitution plus a structural step) with the steps swapped. The unknowns multiply (`D·f`), so the
system is **bilinear**, not linear, and case 132's solver cannot handle it directly.

**Overlap check (to avoid relabelling an old test).** Per block, `−D·f_block` takes one of k/gcd(n, k) values in turn, so the model is a
special case of case 132's linear model with key period **lcm(n, k)**. The parts with lcm(n, k) inside case 132's ranges were already
excluded: n 2 with k even ≤ 14 or k ≤ 7; n 3 with k ∈ {1, 2, 3, 6, 9}; n 4 with k ∈ {1, 2, 4}. When n divides k the two models are the
same (D is invertible, so any `D·f` is reachable), and the cycle 154 count for n 3 k 9 behind the bank (**K4 4 consistent**) equals
case 132's count, a regression check. **New in this cycle:** n 2 with k odd 9–13 behind the bank and k 15–24 direct; n 3 k 4, 5, 7, 8 behind
the bank (k 10 sampled) and k 4, 5, 7, 8, 10–15 direct; n 4 k 3 behind the bank (k 5–6 sampled) and k 3, 5–8 direct; one-error
tolerance for all direct cases.

## Method (`tools/cycle154/hillcs.c`)
- Same frames as cycles 141/144/153: direct; behind all 165,065 bank entries in both directions, model Q (`L[i] = CT[S[i]]`) and
  carved order (`pt[p] = out[S[p]]`); A–Z and KRYPTOS numbering; every alignment o. Cribs EASTNORTHEAST 22–34, BERLINCLOCK 64–74 (1-based).
  The key index is the stream position (bs + j) mod k, the same convention as case 132.
- **Split the field exactly:** Z26 = Z2 × Z13 (CRT), so (D, f) solve independently mod 2 and mod 13. A configuration survives iff
  both fields have a solution with D invertible.
- **In each field, enumerate the smaller side and solve the other side by exact Gaussian elimination:** (1) all f values on the key
  residues touched by crib blocks (P^|R|), D solved row by row; (2) all invertible D (P^(n²)), f solved linearly; (3) one row of D at a time,
  each fixed row adding linear constraints on f, the remaining f-space enumerated when small (a recursive version, `MODE=4`, is used
  to re-solve every configuration the fast modes left unresolved). No sampling inside a configuration, no scoring threshold
  in the consistency test.
- Survivors: every CRT pair (≤ 2 × 10⁶) is decrypted and scored by mean log10 quadgram over decided non-crib letters (English ≈ −4.1,
  shuffled text ≈ −7).
- **One-error mode (`DROP=1`, direct runs):** re-solve with each crib-bearing Hill block's equations dropped. A wrong carved letter
  or a wrong crib letter breaks only its own block, so this is an exact superset for one error (it is weaker: more chance survivors).

Scope per text: **bank, strict**: n 2 k 1–14, n 3 k 1–9, n 4 k 1–3 over the full bank (2.64 / 3.96 / 5.28 million configurations per (n, k));
n 3 k 10 on every 20th entry, n 4 k 5–6 on every 10th. **Direct**: n 2 k 1–24, n 3 k 1–15, n 4 k 1–8, strict and one-error.
About 90 million bank configurations per text. Texts: K4 and two shuffled-K4 nulls (seeds 15401–15402) at the same scale.
Main run 519 s wall on 8 processes, plus 55 s of re-solving.

## Controls (`data/cycle154/controls_check.txt`)
Ten planted encryptions of the cycle 137 English control text, built by `plant.py` (seed 15400) in the exact encryption direction:
n 2 k 9 direct; n 3 k 4 model Q (KRYPTOS numbering); n 2 k 13 carved; n 3 k 7 carved (inverse entry); n 4 k 3 model Q; n 2 k 19 direct
(KRYPTOS numbering, beyond the bank scope); n 4 k 5 model Q; n 3 k 8 model Q (inverse entry, KRYPTOS numbering); plus two error controls:
**ctl7 (n 3 k 5) with one corrupted carved letter inside a crib block** and **ctl8 (n 2 k 11) with one wrong crib letter**.
**10/10 pass:** the eight clean controls decrypt with 0 wrong letters (72–96 decided letters; −4.03 to −4.13). The two error controls
**fail the strict test** (as they should) and are **recovered by the one-error mode**, with the dropped block being the one holding the error
(ctl7 block 27–29, ctl8 block 66–67, 1-based) and 0 wrong letters outside it.

## Independent check (`data/cycle154/independent_check.txt`)
`check.py` (pure Python, no shared code): part A re-decrypts every control from the printed D and f. Part B recounts the per-field solution
sets for the direct texts by **brute force over every invertible D in the field and Gaussian elimination for f**, a different algorithm from
the C program's choice of mode: n 2 k ∈ {1, 3, 5, 9, 11, 13} in both fields, n 3 k 1–9 and n 4 k 3, 5 mod 2, for K4 and both nulls.
**354 per-configuration counts, 354 identical (216 of them non-zero).** The fast and recursive C modes also agree on bank samples and all controls.

## Results (`data/cycle154/results.txt`)
| Scope | K4 | null 1 | null 2 | Label |
|---|---|---|---|---|
| Bank, strict, n 2 k 1–14 (37 M configs) | **0** consistent | 0 | 0 | `EXACT-EXCL` |
| Bank, strict, n 3 k 1–8 (31.7 M) | **0** | 0 | 0 | `EXACT-EXCL` |
| Bank, strict, n 3 k 9 (= case 132 n 3 k 9) | 4, best −7.89 | 0 | 0 | `NO-SIGNAL` (exhaustive decode, matches case 132) |
| Bank, n 3 k 10, every 20th entry | 2, best −7.92 | 1, −7.99 | 0 | `NO-SIGNAL` (sample) |
| Bank, strict, n 4 k 1–3 | k 1: 0; k 2: 4 (−7.93); k 3: 46 (−7.37) | 0; 0; 64 (−7.62) | 0; 6 (−7.93); 42 (−7.69) | k 1 `EXACT-EXCL`; k 2–3 `NO-SIGNAL` (exhaustive) |
| Bank, n 4 k 5–6, every 10th entry | 427 (−7.17); 1,421 (−6.81) | 435 (−7.04); 1,553 (−6.81) | 434 (−7.04); 1,487 (−6.79) | `NO-SIGNAL` (sample), screen LOW-POWER |
| Direct, strict, n 2 k 1–24, n 3 k 1–15, n 4 k 1–8 | **0** in every (n, k) | 0 | 0 | `EXACT-EXCL` |
| Direct, one error, n 2 k 1–23, n 3 k 1–10 and 12, n 4 k 1–4 | **0** in every (n, k) | 0, except n 3 k 12: 1; n 4 k 3: 1; n 4 k 4: 1 | 0, except n 3 k 12: 2; n 4 k 3: 1 | `EXACT-EXCL` under one wrong carved or crib letter |
| Direct, one error, n 2 k 24, n 3 k 11, 13–15, n 4 k 5–8 | 1–37 per (n, k), best −6.63 | 1–39, best −6.68 | 0–37, best −6.68 | `NO-SIGNAL` (exhaustive decode), screen LOW-POWER |

No configuration of any text came within 2.5 points of English; no line above the print threshold (−4.6; −6.0 in the re-solve pass).
Where survivors exist, K4's counts and best scores sit inside the null range.

## Verdict
**Negative.** K4 is not "Hill n × n, then a period-k Vigenère on the Hill output" for n 2 with k ≤ 14 or n 3 with k ≤ 8 behind the 165k bank
(both orders, A–Z/KRYPTOS numbering), nor directly for n 2 k ≤ 24, n 3 k ≤ 15 or n 4 k ≤ 8 (exact). Directly it also stays excluded under
one wrong carved or crib letter for n 2 k ≤ 23, n 3 k ≤ 10 (and 12) and n 4 k ≤ 4. The rest of the tested space shows nothing beyond the nulls.

## Limits and blind spots
- Behind the bank only strict (no one-error mode): one carving error behind a transposition is not covered here (→ I-048).
- Bank n 2 k ≥ 15, n 3 k ≥ 10 (k 10 only 1/20), n 4 k ≥ 4 (k 4 is case 132; k 5–6 only 1/10, k ≥ 7 not run). Cost grows as 13^k for
  configurations that pass mod 2.
- n ≥ 5; other numberings; keys from mixed (Quagmire-style) alphabets; transpositions outside the bank; dropped or extra letters (I-039).
- Survivor sets are judged by quadgram score alone (I-029); with n 4 k ≥ 5 the crib test cannot tell K4 from shuffled text.

## Files
[tools/cycle154/](../tools/cycle154/) (`hillcs.c`, `plant.py`, `check.py`, `run_cycle154.sh`, `summarize.py`) ·
[data/cycle154/](../data/cycle154/) · [journal](../journal/2026-11-08-cycle154.md).

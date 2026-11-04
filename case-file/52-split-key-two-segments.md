# Case file 52 — Split key: two periodic keys, switch between the cribs (cycle 54)

**Why this family.** Every periodic test so far assumed one key for all 97 letters. K2 is full of sentence stops (X),
and cycle 53's journal asked for a model where the key *changes* partway through, e.g. at a sentence break. A
two-segment key is a simple, K1–K3-plausible layer (two keywords, one per sentence) that none of the earlier
single-key tests could see: direct periodic keys fail for p ≤ 26 partly because the two cribs contradict *each other*.
New family for the coverage table (diversity rule).

**Model.** Segment 1 = letters 0…b−1 (contains EASTNORTHEAST, 21–33), segment 2 = b…96 (contains BERLINCLOCK,
63–73), split b = 34…63. Each segment has its own periodic key, p1 ≤ 13 and p2 ≤ 11. Because 13 (resp. 11)
consecutive crib letters cover every residue, **each key is fully determined by its crib**, so every configuration
yields one exact 97-letter plaintext with no free parameters; it is then scored by English quadgrams.
Tableau: Quagmire III style (same keyed alphabet on both sides) for all 86,731 alphabets in `data/alpha.bin`
(A–Z, KRYPTOS, themed and dictionary keyword alphabets); Vigenère (c = p + k; variant Beaufort gives the same
plaintext) or Beaufort (c = k − p), chosen independently per segment; with A–Z/KRYPTOS the two segments may also use
different alphabets. Two scorings: all configs, and **strict** (p1 ≤ 12 and p2 ≤ 10, so both cribs actually
constrain their key; p1 = 13 / p2 = 11 always fit trivially).

**Controls.** Plaintext `ITWASLATEWHENWEHEADEDEASTNORTHEASTACROSSTHERIVERUNTILWEHEARDTHEBERLINCLOCKSTRIKETWELVEINTHESQUARE`
encrypted three ways (KRYPTOS Vig PALIMPS/SHADOW split 45; A–Z Beaufort LAYERTWO then KRYPTOS Vig ABSCI split 52;
themed alphabet #5000 Vig IQLUSION then Beaufort DESPARATLY split 38). Five shuffled-K4 nulls, same cribs.

**Results** (`data/cycle54/results.txt`, best mean log-probability per quadgram):

| Text | consistent key pairs (all) | best (all) | consistent pairs (strict) | best (strict) |
|---|---|---|---|---|
| K4 | 362,613 | −6.10 | 81 | −6.65 |
| 5 shuffled nulls | 361,554–543,121 | −6.03 to −6.23 | 22–6,331 | −6.34 to −6.79 |
| 3 planted controls | 368,792–413,353 | **−4.15, exact plaintext, rank 1** | 290–2,141 | **−4.15, rank 1** |

K4's best decryptions are noise (e.g. `…EASTNORTHEASTONIUTTLYMDKCERQGSLEBOATWISILTBERLINCLOCKUPSEV…`) and sit inside the
null range on both scorings. 3/3 controls recovered with their split, periods, alphabets and variants. Runtime 3 s.

**Verdict.** **Negative**: no two-keyword split (p1 ≤ 13, p2 ≤ 11) over 86,731 alphabets, Vigenère/Beaufort, any
split between the cribs, decrypts K4 directly. **Not covered:** longer per-segment keys (then the crib no longer
fixes the key), three or more segments, splits inside a crib, a transposition layer on top, mixed (non-Quagmire-III)
tableaux per segment except A–Z/KRYPTOS crosses.

**Reproduce.** `cd tools && gcc -O3 -o splitkey splitkey.c && gcc -O3 -o splitkey_s splitkey_strict.c`, put
`alpha.bin` (from `data/`) and the quadgram table `qg.bin` (built by `build_quadgrams.py`, 26⁴ float32 log-probs)
next to them, `python3 ctl54.py`, then `./run_cycle54.sh`; strict mode: `STRICT=1 ./splitkey_s CT alpha.bin qg.bin`.

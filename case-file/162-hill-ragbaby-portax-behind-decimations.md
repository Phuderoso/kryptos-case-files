# Case file 162 — Hill, Ragbaby and Portax behind K3's decimation law (cycle 174)

**Status:** negative. **Type:** new family (cycle 173 was an audit/variant). IDEAS [I-108](../IDEAS.md) (the last three names on
[case 57](57-k3-as-decimation.md)'s list of substitutions never run behind K3's law), with the [I-110](../IDEAS.md) grid rule applied
for the first time. Pre-registered in [`tools/cycle174/PREREG174.md`](../tools/cycle174/PREREG174.md) (commit b7dc897) before the K4 and null runs.

**Result in one line:** behind every one of the 165,782 K3-law decimations / spiral-diagonal routes, both layer orders,
**no Hill 2×2 or 3×3 matrix (linear or affine, A–Z or KRYPTOS numbering, any block offset) fits the cribs, no classic Ragbaby on 18,776 keyed
alphabets fits even the first crib, and no Portax key fits at any period where the cribs constrain the key → `EXACT-EXCL`.** The only Portax fits
(121, ix 1, p 30–35; band p 30–36 where the nulls also fit) put 20–24 of the 24 crib letters on unpaired tail cells, so they test nothing (`LOW-POWER`); K4 sits inside the nulls there
(27 on the sample vs 20–31), and all 121 die if a tail letter is copied unchanged. Grid (I-110): K4 grid p 0.60, nothing stands out.
**No solution.**

## 1. Why this, and why it is new
- Queue: cycle 173 named I-108 as the cycle-174 new-family slot. Cycles 168–173 ran running keys, Porta, Quagmire IV and the one-letter
  anomaly behind the decimations; Hill, Ragbaby and Portax were the rest of case 57's list.
- Overlap: Hill ran behind the 165,065-entry transposition bank (cases 26, 131+), Ragbaby behind 93,334 cycle-12 transpositions (case 53),
  Portax behind 96,630 cycle-12 transpositions (case 56). Case 57 found only 492 of the 160,204 decimations inside the cycle-12 family, so the
  decimation part is new. The 6,070 spiral/diagonal routes may overlap with the bank; no novelty is claimed for them.

## 2. Models (exact; convention of `q4d172`: plaintext index i ↔ carved index S[i])
- **ix 0** = cipher on the plaintext order, then the transposition (C[S[i]] = Y[i]). **ix 1** = transposition first (T[S[i]] = P[i]), then the cipher on the carved order.
- **Hill** ([`hill174.c`](../tools/cycle174/hill174.c)): decryption form P = D·Z (linear) or P = D·Z + e (affine; this covers A=1 and any cyclic
  shift of the numbering), n = 2 and 3, numbering A–Z or KRYPTOS, block offset 0..n−1 (letters outside whole blocks free), both orders.
  Every crib letter is one linear equation on one row of D. It is solved mod 2 and mod 13 (CRT), then D is checked for invertibility and decoded.
  Analytic chance per sub-cell: Σ over configs Π_rows 26^−(m_r − u).
- **Ragbaby** ([`rag174.c`](../tools/cycle174/rag174.c)): classic ACA rule (letter j of word w shifted n0 + w + j + 1 along one keyed alphabet), step 1,
  both directions, **any word division** (the word in progress at a crib start ≤ 20 letters), ix 0 only. Ragbaby needs the plaintext's word
  breaks, and on transposed text they mean nothing (case 53's reason). Alphabets: the 18,776 of `alpha172.txt` (every vocabulary word keyed on
  A–Z and on the KRYPTOS order, plus A–Z and KA). That is 6.2 × 10⁹ configurations for K4.
- **Portax** ([`portax174.c`](../tools/cycle174/portax174.c), core from case 56's `portax.c`): any key of period p 1–48 (13 slides per column),
  pairs (t, t + p) in row pairs, A–Z or KRYPTOS numbering, both orders. Convention: an odd tail letter with no partner is free.

## 3. Results — K4 on the full 165,782 perms

| family | sub-cells | configs | K4 consistent | chance expectation | nulls (19 × 41,446 perms) | verdict |
|---|---|---|---|---|---|---|
| Hill n 2 | lin/aff × AZ/KA × ix × offset (16) | 2,652,512 | **0** | 1.8 × 10⁻¹⁹ | 0 | `EXACT-EXCL` |
| Hill n 3 | lin/aff × AZ/KA × ix × offset (24) | 3,978,768 | **0** | 1.0 × 10⁻⁸ | 0 | `EXACT-EXCL` |
| Ragbaby d 1 | 18,776 alphabets × 2 directions | 6.23 × 10⁹ | **0** (crib 1 alone: 0) | — | 0 in 2.96 × 10¹⁰ | `EXACT-EXCL` |
| Portax, ix 0 p 1–48; ix 1 p 1–29, 37–48 | AZ/KA | 29.5 M | **0** | — | 0 | `EXACT-EXCL` |
| Portax, ix 1 p 30–36 | AZ/KA | 2.3 M | 121 (all at p 30–35; ≤ 4 constrained pairs each) | — | 503 (20–31 per text; p 36: 5) | `LOW-POWER` (vacuous) |

- Hill: the cribs give each row 8–12 equations for 2–4 unknowns at ix 0, and a binomial share at ix 1. The weakest sub-cell (n 3 affine, ix 1,
  offset 2) still has chance 5 × 10⁻⁹. Zero consistent configs, so zero invertible ones, so nothing to decode.
- Portax: per p and order the counts are in [`summary174.txt`](../data/cycle174/summary174.txt). 88 of the 121 K4 fits constrain **no pair at all**
  (every crib letter falls on a tail cell); the rest constrain 1–4 pairs and fix ≤ 6 letters outside the cribs. Nulls show the same pattern
  (342 of 503 with 0 pairs, max 5). Under the other odd-tail convention (tail letter copied unchanged), all 121 fail
  ([`portax_decodes174.txt`](../data/cycle174/portax_decodes174.txt), last line).

## 4. Pre-registered grid (I-110)
Four cells on `all_s4.bin` (K4 + 19 nulls): C1 Hill n 2 consistent, C2 Hill n 3 consistent, C3 Ragbaby both-fit, C4 Portax consistent.
Score = leave-one-out z per cell, G = max over cells. K4 = [0, 0, 0, 27], G 0.19. Nulls' C4 ranges 20–31, and 11 of 19 nulls have G ≥ 0.19 →
**K4 grid p = 0.60** (best attainable 0.05). Lesson (→ I-115): C1–C3 are zero for every text, so their z is 0 and puts a floor of 0 under G.
The grid then reduces to C4 alone, and C4 measures vacuous configs. Next time, pre-register dropping zero-variance cells and counting only configs
with ≥ k constrained letters.

## 5. Controls and recount
- **Planted controls 16/16** ([`controls174.txt`](../data/cycle174/controls174.txt)): an independent string-level encryptor
  ([`plant174.py`](../tools/cycle174/plant174.py)). 6 Hill plants (n 2/3, linear/affine, AZ/KA, both orders, offsets 0–2) were each found at the
  planted perm and sub-cell and decoded back to the plaintext. The one extra hit in three slices is the same key seen as affine with e = 0.
  4 Ragbaby plants (KA, A–Z and two vocabulary alphabets, both directions) were found at the planted perm, alphabet and direction. 4 Portax plants
  (keys LUCID, UNDERGROUND, SHADOWFORCES, a 27-letter key; AZ/KA; both orders) were found, and every uniquely keyed letter decoded correctly.
  2 negative plants (Hill, Portax; one carved crib letter changed) were missed, as a strict test must miss them.
- **Independent recount** ([`recount174.txt`](../data/cycle174/recount174.txt)): Python brute force over every row vector (Hill n 2 linear/affine,
  n 3 linear), every slide (Portax) and explicit word divisions (Ragbaby). 47,600 Hill and 27,456 Portax configs (plant slices, K4/null ranges,
  and K4's Portax hits at perms 103771, 132659, 154713) gave **0 mismatching sub-cells**. Ragbaby 240/240 configs agreed (4 positives).
  Not recounted: Hill n 3 affine (the 26⁴ row space is too big for Python here; it is covered by the plants only).

## 6. Honesty notes
- While writing `hill174.c` a 2,000-perm smoke run on K4 was made before the pre-registration (totals only, all 0); disclosed in the pre-registration.
  Ragbaby/Portax smoke runs used a non-registered shuffle (seed 9174).
- After the pre-registration push, `portax174.c` gained the `?` decode output (ambiguous slides) and an optional X-line threshold. This was found
  when two Portax plants were reported "not decoded": the checker had compared letters in columns the cribs do not fix. The consistency test,
  and with it every count, is unchanged.
- Heavy compute: 3 min 50 s wall for the main run (6 jobs, box shared with a Voynich job), plus about 1 min for decodes and recount.

## 7. Limits (what stays open)
Hill n ≥ 4 behind the decimations (affine n 4 is at the edge of power; → I-113); Hill with an arbitrary numbering (SAT, as case 28); Ragbaby on the
other 68k bank alphabets, other steps d ≠ 1, arbitrary alphabets (→ I-114); Portax on keyed alphabets beyond KA, and the free-tail convention at
p 30–36 (vacuous; → I-112); all three under one carving error; decimations for 96/98 letters (I-109 style).

## Reproduce
`cd tools/cycle174`, build the three C tools (`gcc -O3 -march=native -o X X.c -lm`) into `run/`, put `all.bin`, `all_s4.bin` (`P[::4]`) and
`alpha172.txt` in `support/`, then from `run/`: `python3 ../tools/plant174.py ctl 174174 && python3 ../tools/checkctl174.py ctl`,
`../tools/run_cycle174.sh`, `python3 ../tools/summarize174.py`, `../tools/recount_run174.sh && python3 ../tools/compare174.py`.
Raw outputs: [`data/cycle174/`](../data/cycle174/).

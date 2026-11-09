# Cycle 184 pre-registration — Quagmire IV with both alphabets from the vocabulary and a linear-recurrence key behind K3's decimation law (IDEAS I-163)

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9184
(`random.Random(9184).shuffle(list(K4))`, I-116), on `all_s64.bin`: every cell 0 fits, no overflow, no mismatch; method 1 and method 0
gave identical H lines at L 1–4; the audit build (method 2, `-DSAFE=1`) ran on rows 0–5. **Planted controls rehearsed before this push
(I-119): 14/14** (method 1, method 0 and the audit build on every plant). The rehearsal is declared the registered control run (as in
cycle 183); nothing was changed after it.

## A. Question (new family slot; 182 was a new family, 183 its one-error audit)
Case 170 excluded Quagmire IV (plaintext-side alphabet A ≠ ciphertext-side alphabet B) with an affine linear-recurrence key
k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) behind the 165,782 K3-law decimations / routes, when **one** of A, B is one of 144 themed
alphabets. Here **both** come from the 18,776-alphabet vocabulary (`alpha172.txt`, md5 92793b74…): 18,776² = **352,538,176 ordered
pairs** per perm × Vig / Beau, key on the plaintext index (M0). Does K4 fit any such cipher at L ≤ 4 behind any of the 165,782 perms?
**Overlap.** 96 of the 144 themed alphabets are in the vocabulary, so pairs with A or B themed (≈ 3.6 M, 1.0 %) repeat case 170; pairs
with A = B repeat Quagmire III (case 168). Both are kept, not removed. ≈ 99 % of the pair space is new.

## Method (exact; `lrk184.c` = `lrk182.c` verbatim apart from its header line)
Mod 2 the 24 crib key bits are w = parity_B(carved letter) ⊕ parity_A(crib letter). **Method 1** (registered main run): for each (c, d)
mod 2 at order L_max = 4 the passing words form an affine space; hash join per (c, d) on σ(pa_A) ⊕ (w₀ ≫ 4) for all 18,776 A, one
σ(cp_B) lookup per (B, (c, d)) per perm. **Method 0** (independent join path, audit): CSR union map ∪_A (W₄ ⊕ pa_A). **Method 2**
(`-DSAFE=1`, audit): every (A, B) pair looked up in the table, no GF(13) nesting shortcut. GF(13) = lrk180's `solve0`; fit ⇔ mod 2 and
mod 13 both solvable at that L (nested in L, exact). **Chance rate** per (perm, pair, form) ≈ 26^(2L+2−24); 1.17 × 10¹⁴ configurations
per full set: L 3 ≈ 3 × 10⁻⁹, **L 4 ≈ 2 × 10⁻⁶** fits per text. Every registered cell has full power.

**Timing line (I-169), measured on the reserved shuffle, all_s64, 6 threads:** L_max 3 1.2 s, **L_max 4 (top registered order) 4.4 s**
(method 0 4.5 s), L_max 5 25.5 s. Full-set cost: L ≤ 4 ≈ 4.7 min; L 5 ≈ 27 min.
**Dead-on-arrival line (I-151).** L 5 (full power, ≈ 10⁻³ chance fits per text) does not fit the 8-minute budget → **not run**, queued.
L 6 (≈ 0.8 chance fits per full set) would be `LOW-POWER`-leaning. Key on the carved index (I-164) → not run. **I-130 (Gromark with
both alphabets free) behind the decimations is declared dead on arrival, not run:** with A and B free the 24 crib equations
u(p) + k = v(c) (mod 26) form a graph on the crib-letter nodes whose cycle rank is the number of real checks; over all_s64 for K4 the
rank is 0 on 1,182 / 2,591 perms, 1 on 998, 2 on 359, 3 on 48, 4 on 4 (mean 0.72). On a rank-0 perm every primer passes (only
injectivity limits it), so the chance count over 10^L primers is astronomically above one: `LOW-POWER` by construction for any L.

## Texts and runs (`run_cycle184.sh`)
K4 (`data/k4.txt`, md5 dc4df49d…): method 1, L 1–4, **full** set (`all.bin`, md5 946402ca…). Audits: K4 on `all_s64.bin` (f45bc54b…)
with method 1 and method 0 (H lines must be identical); K4 on `all_s2048.bin` (= all.bin[::2048], 81 rows, 94a1a6c5…) with method 1
and the audit build method 2 (H lines must be identical). Grid texts on `all_s512.bin` (= all.bin[::512], 324 rows, md5 2a8c7ba2…):
K4 and 19 nulls = `random.Random(s).shuffle(list(K4))`, s = **18411…18429** (`nulls184.txt`), method 1, L 1–4.

## Labels
K4 0 fits → `EXACT-EXCL` (scope: vocabulary × vocabulary ordered pairs, Vig/Beau, L 1–4, key on the plaintext index, these perms).
K4 > 0 → every fit decoded (`decode184.py`, independent string-level replay, all 24 crib letters checked); a fit is never a signal without a
readable decode. Solution criterion: a full coherent English decryption of the 97 letters with both cribs at the official positions,
reproducible. Any `X` or overflow line invalidates the cell.

## Grid (I-152: empirical rank)
F = fits L 1–4 on all_s512 (scored only if not all-zero); D1 = mod-2 passes at order 4 (= every L ≤ 4 by nesting). p⁺ = (1 + #nulls ≥ K4)/20,
p⁻ = (1 + #nulls ≤ K4)/20, grid = min over cells (floor 0.05, no multiplicity correction). A floor rank on a diagnostic is a rank flag,
not a signal; it would go to a pre-registered replication (I-146 / I-166 rules), never a claim.

## Controls (`plant184.py`, seed 18400, independent string-level encryptor; plaintext as cycles 180–183; each plant behind perm q of all.bin;
run on q ± 200 with methods 1 and 0, audit build on q−2…q+3; `run_controls184.sh`, `checkctl184.py`)
Positives (found at q with planted A, B, form, L; planted (c, d) mod 2 and mod 13 listed; replay = plaintext); P1–P7 use alphabets outside
the themed list: P1 L1 Vig MEDITERRANEAN/Z × SAINTLY/K; P2 L2 Beau MERCHANT/Z × OBLIQUE/Z; P3 L3 Vig NOVEMBER/Z × PLIGHT/K; P4 L4 Beau
ITALIAN/K × RATTLING/K non-unit last weight; P5 L4 Vig WHIP/K × KNIGHTS/Z; P6 L1 progressive (c 1, d 3) Vig MOUTHS/Z × HESITATING/K;
P7 L2 Vig SAINTLY/K × SAINTLY/K (A = B); recount plants P8 L1 Vig LAYER/Z × TOMB/Z, P9 L2 Beau SLOWLY/Z × EGYPT/Z, P10 L1 Beau KA × SHADOW/K.
Negatives (no fit at q): N1 = P3 with one wrong carved letter (slot 30); N2 random key; N3 L2 plant with a random alphabet outside the
vocabulary (RAND1 × OBLIQUE/Z); N4 order-5 plant (outside L ≤ 4).
**Independent recount** (`recount184.py` = recount182.py logic, numpy brute force over every (c, d) ∈ Z₂₆², no table / CRT / syndrome /
nesting): slice = all.bin[::4000] + the planted perms of P8, P9, P10 (45 rows, `mkslice184.py`, md5 f2c34d83…); A, B ∈ `alpha_recount180.txt`
(33 × 33, all in the vocabulary); texts K4, n18411, n18412, P8, P9, P10; L 1 everywhere, L 2 at P9's row (43) with A = SLOWLY/Z.
Compared with lrk184 method 1 run on the slice with the **full** vocabulary on both sides, restricted to recount-list pairs (`cmprecount184.py`).

## Budget
Heavy ≤ 8 min including rehearsal: smoke/timing ≈ 37 s, control rehearsal 48 s, main run ≈ 5.3 min estimated (K4 full ≈ 280 s, audits ≈ 30 s,
all_s512 20 texts ≈ 11 s). One 6-thread job at a time under `setsid timeout 420`; resumable. Recount niced, 1 thread, outside the budget.

# Cycle 181 pre-registration — one-error audit of case 168 (keyed-alphabet linear-recurrence keys behind K3's decimation law; IDEAS I-156)

Written and pushed before any K4 or registered-null run. Smoke / timing only on the reserved shuffle seed 9181
(`random.Random(9181).shuffle(list(K4))`, I-116), on `all_s64.bin`: every cell 0 fits, no overflow, no mismatch.
Cost on 1/64 (6 threads): M0 L 1–5 1.4 s, M0 L 6 2.1 s, M0 L 7 16.6 s (→ not run), M1 L 1–2 0.16 s, M1 L 3 3.0 s.
**Planted controls rehearsed before this push (I-119): 17/17** with the registered build, and 17/17 with the audit build
`-DSAFE=1` (both exact shortcuts off); H lines identical between the two builds on all 17 control windows. The rehearsal caught
two checker/decoder issues, fixed before this push: (i) a carved-index strict fit was printed once per slot (now one `t -1` line
as in M0); (ii) the M1 decoder replayed only the printed mod-2 stream, which is not identified off the cribs when c is even
mod 2 (the cycle-179 lesson); it now re-enumerates every mod-2 stream matching the crib bits off the wild slot. No rule changed.

## Question (audit; cycle 180 was a new family)
Case 168 excluded, **strictly**, the affine linear-recurrence key k[i] = c₁k[i−1] + … + c_Lk[i−L] + d (mod 26) through 18,776
vocabulary-keyed alphabets (Quagmire I/II/III, Vig/Beau) behind the 165,782 K3-law decimations / routes. Sanborn's carving has
known quirks, so does that exclusion survive **one wrong letter among the 24 crib positions** (a mis-carved letter at a crib slot's
carved position, or a wrong crib letter)? Firefly's standing priority I-003 (one-letter-error robustness of high-impact exclusions)
points here as well.

## Method (exact; `lrk181.c`)
Family, alphabets (`alpha172.txt`, md5 92793b74…, 18,776; 56,326 (alphabet, type) pairs), types and forms exactly as case 168.
Slot t wild ⇔ its key value is a free unknown. Exact by CRT (case 167): a fit with slot t free exists iff some v₂ passes GF(2)
and some v₁₃ passes GF(13) **for the same t**.
- **M0 (key on the plaintext index), L 1–6, full set.** The case-168 2²⁴ mod-2 table is dilated to Hamming distance 1 (one lookup
  per perm × pair); survivors get their allowed slots; GF(13): for block-1 slots (21–33) each v₁₃ ∈ Z₁₃ through lr178's solve0; for
  block-2 slots (63–73) one solve with that slot's in-block rows dropped and the propagation check ignoring it (exact: block 2 is
  determined by propagation from block 1, so "free value at t" ⇔ "the other block-2 slots match"; the same shortcut is used mod 2
  as an independent re-check of the table → any disagreement is an `X` line).
- **M1 (key on the carved index, seed at carved 0…L−1), L 1–2 full set, L 3 on `all_s8.bin` (1/8 of the routes).** Mod 2: the
  2^(2L+1) streams and their 24 one-bit neighbours in a per-thread 2²⁴ bitset; GF(13) per c mod 13: all 24 rows, and if
  inconsistent each allowed slot's row left out, only for slots up to the first inconsistent row (a later row cannot repair it; exact).
- Audit build `-DSAFE=1` switches both shortcuts off (13-value loop for every slot; every allowed slot in M1).
- **Chance rate** per (perm, pair, form) ≈ 24·26^(2L+2−24); 1.87 × 10¹⁰ configurations per full set: M0 L 5 ≈ 2·10⁻⁶,
  **L 6 ≈ 0.003** fits per text; M1 L ≤ 3 < 10⁻¹⁰. Every registered cell has full power.
- **Dead-on-arrival line (I-151).** M0 L 7: ≈ 2.1 chance fits per full set (`LOW-POWER` by construction) and ≈ 18 min per full
  pass → **not run**. M1 L 3 on the full set (≈ 190 s per text) and M1 L 4 themed (13⁴ weight vectors per survivor) → not run this
  cycle, queued. Nothing registered here is expected to be unable to pass its controls.

## Texts and runs (`run_cycle181.sh`)
K4 (`data/k4.txt`, md5 dc4df49d…): M0 L 1–6 and M1 L 1–2 on the **full** set; M1 L 3 on `all_s8.bin`; all cells also on
`all_s64.bin` (= all.bin[::64], md5 f45bc54b…) for the grid. 19 nulls = `random.Random(s).shuffle(list(K4))`, s = **18111…18129**
(`nulls181.txt`): M0 L 1–6 and M1 L 1–3 on `all_s64.bin`.

## Labels
K4 0 fits → `EXACT-EXCL` (one-error scope: these alphabets, types, forms, orders, routes); K4 > 0 → every fit decoded
(`decode181.py`, independent string-level replay, 23 crib letters checked); `LOW-POWER` if inside the null range, flagged if above,
never a signal without a readable decode. Solution criterion: a full coherent English decryption of the 97 letters with both cribs
at the official positions (one crib letter may differ only at the wild slot), reproducible. Any `X` or overflow line invalidates the cell.

## Grid (I-152 adopted: empirical rank, no Poisson tails)
Fit cells (M0 L 1–5, M0 L 6, M1 L 1–2, M1 L 3, all on all_s64) scored only if not all-zero. Diagnostics: D1 = M0 one-error mod-2
passes L 5–6, D2 = M1 one-error mod-2 passes L 1–3 (all_s64). p⁺ = (1 + #nulls ≥ K4)/20, p⁻ = (1 + #nulls ≤ K4)/20, grid = min
over cells (floor 0.05, no multiplicity correction). A floor rank on a diagnostic is reported, not a signal; it would need a
separately pre-registered replication before any wording beyond "rank flag".

## Controls (`plant181.py`, seed 18100, independent string-level encryptor, plaintext as cycle 180; each plant behind perm q of
all.bin, one carved letter at the error slot changed by a random non-zero shift; run on q ± 500; `run_controls181.sh`, `checkctl181.py`)
Positives (found at q with planted alphabet/type/form/L, wild slot = the planted error slot and no other slot, planted (c, d) listed
(M0), replay = plaintext except at the mis-carved letter): P1 M0 L3 q3 Vig SHADOW/Z err 25; P2 M0 L5 q1 Beau BERLIN/K err 66;
P3 M0 L6 q2 Vig ABSCISSA/Z err 21 (first seed slot); P4 M0 L2 q3 Beau SHADOW/K err 73; P5 M0 L4 q3 Vig PALIMPSEST/K strict;
P6 M0 L6 q3 Beau KA non-unit last weight err 33 (start of the gap); P7 M1 L1 q3 Vig COMPASS/Z err 64; P8 M1 L2 q1 Beau
LODESTONE/K err 22; P9 M1 L3 q2 Vig MAGNETIC/Z err 29; P10 M1 L3 q3 Beau ABSCISSA/K strict; P11 M0 progressive (c 1, d 3) q3 Vig KA
err 30; P12 M1 L3 q1 Vig SHADOW/K err 73.
Negatives (no fit at q): N1 M0 L3 two errors (66, 70: both block-2 slots, so every order sees the second one); N2 M1 L2 two errors
(22, 68); N3 random key M0; N4 random key M1; N5 M0 L3 one-error plant with an alphabet not in the list.
**Independent recount** (`recount181.py`, numpy brute force, no CRT / table / pext / elimination / shortcut; one-error fits by
explicit seed variants and a crib-mismatch count ≤ 1): slice = all.bin[::4000] + the planted perms of P4, P7, P8, P11 (46 rows,
`mkslice181.py`); alphabets `alpha_recount180.txt` (33); texts K4, n18111, n18112, P4, P7, P8, P11; M0 L 1 and M1 L 1 everywhere,
M0 L 2 for P4 and M1 L 2 for P8 at their planted row and alphabet. Compared per (text, ix, L, type, form, row, alphabet) on the
**set of fitting slots** (`cmprecount181.py`). Rehearsed on P4/P8/P11 before the push where finished (see the results file).

## Budget
≈ 6.5 min heavy (K4 full ≈ 4 min, nulls ≈ 2 min), one 6-thread job under `setsid timeout 900`; resumable. Recount niced, outside.

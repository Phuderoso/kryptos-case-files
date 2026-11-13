# PREREG210 — cycle 210 pre-registration (2026-11-13, written before any registered run)

Seeds: next free after cycle 209 was 209212. This cycle uses **209212** (case 196 addendum), **209213** (shuffled-K4 nulls),
**209214** (planted controls). Next free after this cycle: **209215**. File hashes: [`hashes.txt`](hashes.txt).

## Part 1 — Case 196 addendum: C4 at P 8 with the exact 85-ban mask (registered BEFORE I-279)
Source: Voynich desk independent SAT/SMT check of case 196's C4 mask (box-local `voynich/kryptos-audits/case196-c4-check/results.md`,
sha256 e06ce501622ee9c5…). Her result: all 81 CP-SAT bans confirmed; the 4 cells CP-SAT left UNKNOWN (20 s limit) — **(37,T), (50,C),
(50,E), (50,T)** — are infeasible, so exact C4 has 85 bans (1,513 allowed cells), forced {35, 41, 43, 46, 61, 78}.
Script [`c4add210.py`](c4add210.py) (sha in hashes.txt). Gates (all must pass, else NO VERDICT):
- **Z:** our own Z3 model (not CP-SAT, no time limit) decides each of the 4 named timeouts (must be UNSAT), 6 sampled CP-SAT bans
  (UNSAT), every C3-allowed letter at 0-idx 43 (only T SAT), 6 sampled allowed cells (SAT, witness re-checked).
- **M:** 81-ban mask 1,517 allowed, 85-ban mask 1,513, forced set {35,41,43,46,61,78}.
- **R (I-283):** 81-ban mask with seed block 209211 reproduces case 196's JEX tag-10 q = 0.0074993 exactly.
Disclosure: gates Z/M/R were executed once during development (`REPRO_ONLY=1`; all pass; R reproduces 0.007499250074992501). They use
no new random draw on K4's decision side (R re-uses case 196's own seeds), so no new q was seen.
**Main:** seed block 209212, 256-key pool, 4 registered models × 10,000 C4 references at P 8 (tag 10) on the 85-ban mask, plus a paired
81-ban run on identical seeds (descriptive). Decision: worst model, looks at n = 10k / 40k / 160k (tags 10, 11, 12; I-265 ×4, max 3
looks), stop at the first look with |q* − 0.00625| ≥ 2·SE (q* = max(worst-model q, other models' q)). q* ≤ bar − 2SE →
`STAT-DISFAVOURED` (carries to Quagmire IV at P 8); ≥ bar + 2SE → `LOW-POWER`; inside after 3 looks → `UNRESOLVED`.

## Part 2 — New family (I-270 + I-276, pointer I-282): word restart R1 on a two-keyword Quagmire tableau, behind the bank and behind the K3-law decimations/routes
**Model:** plaintext enciphered with key index = position inside its plaintext word mod L (case 190's R1; case 190's 4 × 2 English
segmentations of the cribs; free word offsets o1, o2 ∈ 0..L−1), on a Quagmire tableau with plain alphabet X and cipher alphabet Y,
both keyword-mixed (K1/K2 construction: keyword letters, then the rest of A–Z): Vigenère form c = Y[x(p)+k] (variant = same
consistency, counted once) and Beaufort form c = Y[k − x(p)]; then model Q transposition (layer letter i carved at S[i]), S a row of
the 165,065-entry bank (`perms97.bin`) or of the 165,782-row K3-law decimation/route family (`all.bin`), both directions.
**Alphabets (registered, 8):** AZ, KA (KRYPTOS), PALIMPSEST, ABSCISSA (K1/K2 keys), SHADOW (K1 plaintext), IQLUSION (K1's deliberate
misspelling), LAYERTWO (K2's last words), BERLINCLOCK (K4 clue) — the first rows of the themed list `alpha_themed180.txt` that name a
K1–K3 key, anomaly or clue. **Pairs:** all 64 ordered (X, Y) minus AZ/AZ and KA/KA (already cases 193 / 195) = 62 pairs × 2 forms
(Quagmire I, II, III-on-a-new-keyword and IV all included). **Range:** L 1–17.
**Tool:** [`wrq.c`](wrq.c), a generalisation of `wrbank.c` (survivor = equal key index ⇒ equal key value, per configuration).
**Gates:**
- **G0′:** wrq with pairs AZ/AZ + KA/KA reproduces `wrbank.c` per tableau-form H counts on K4 behind the bank, L 1–20.
  (Executed once in development, identical; rerun inside the registered script.)
- **Plants (seed 209214, [`plant210.py`](plant210.py), independent encoder):** 12 planted R1 Quagmire ciphers at L 12 / 14 / 16,
  6 behind bank rows and 6 behind all.bin rows, random pair/form/segmentation, offsets 0 for 4 and random for 8; each run through wrq on a
  101-row slice of its family around the true row. Pass: true configuration (row, dir, pair, form, L, segmentation, o1, o2, key with `?`
  wildcard) in the survivor list for ≥ 11 / 12.
- **Nulls:** 20 shuffled K4 (Python `random.Random(209213)`); null i runs on rows q ≡ i (mod 10) of the bank (i < 10) or all.bin (i ≥ 10),
  so each family gets one full-family null-equivalent (10 disjoint tenths); per-L totals estimate the expected false-survivor count E of
  one full-family run.
**Labels (per family, per L):** K4 = 0 survivors is an exact statement under the model. It is labelled `EXCLUDED (exact)` and
called **discriminating** when the null-equivalent count is 0 and the analytic multiplicity extrapolation from case 193/195 (×31 tableau-
forms) gives E < 0.05. If the null-equivalent count is > 0 at an L where K4 = 0, that L is `zero, not discriminating`. If E sits within the
I-281 band of 0.05, the label is `UNRESOLVED`. K4 > 0 survivors: printed (cap 5,000), key and crib-adjacent letters read for English;
`NO-DISCRIMINATION` if K4's count is inside the null-equivalent range. Any coherent English → full decryption attempt.
**Disclosure (before registration):** one timing probe ran K4 itself on the bank, rows q ≡ 0 (mod 10), L 1–17, 62 pairs: total 1
survivor, at L 17 (0 at L ≤ 16). Those rows are part of the registered full run and are not reported separately.
**Budget:** whole registered run under `setsid timeout 480`; kill only that group.
**Not this cycle:** the 20 blind aligned plants for case 195 (Voynich, sealed sha da448d89…) are reserved for cycle 211 (I-280).

# PREREG209 — Quagmire IV conditioning of the P 8 column-coincidence reverse test (I-247), audit slot (cycle 209, 2026-11-13)

Written 2026-11-13 04:08 PT (America/Vancouver), base commit d1f3853 (origin main), **before any K4 statistic of this cycle was read**.
Seen before writing: (a) G0 consistency of Quagmire IV on K4's cribs at P 1–26 (structure only: P 1–7 UNSAT, SAT exactly at 8, 13, 16,
19, 20, 23, 24, 26 = case 11's list); (b) a timing/soundness probe on one *planted* QIV ciphertext (probe seed [209000, 1]): 1,159
queries, 0 unknown, 46 UNSAT, 51 extra banned cells over C3, true plaintext allowed 97/97, 11.5 s; (c) a smoke run of the driver
(tiny sizes, P 13 only) that computed but did not print any q.

## Why (I-247, slot)
Slots: 207 audit, 208 new family, so 209 is free (variant/audit). Case 191 puts P 8 at `STAT-DISFAVOURED (borderline)` for H_8 (eight
free per-phase bijections), conditioning the plaintext on C3, the exact single-position marginal of the crib constraints under H_8.
Case 11's open cell is narrower: Quagmire IV (F1: CA⁻¹(c_i) = PA⁻¹(p_i) + k_{i mod P}, PA, CA arbitrary, which contains Vigenère,
Beaufort and Quagmire I–III). Its phases share two alphabets, so its single-position marginal **C4** can only ban more. More bans make
crib-consistent plaintexts flatter (case 188), which pushes q up. Question: does case 191's P 8 verdict carry over to Quagmire IV, the
family community lists still call "partly tested" (kryptosbot: repeating keys with two keyword-mixed alphabets)?

## Method (`lib209.py`, `run209.py`, `run_cycle209.sh`)
- **C4 mask:** for every non-crib position x and every C3-allowed letter p: is there a Quagmire IV key consistent with the 24 crib
  pairs that also maps p → K4[x] at phase x mod P? CP-SAT, reduced model (only letters touching cribs/query get variables; exact
  because injective partial maps extend), 1 worker, 20 s per query; UNKNOWN is counted and treated as allowed (conservative toward C3).
- **Plants:** exact FFBS from the order-3 chains of case 191 (lib204 unchanged) conditioned on C4. Models JE, CARTER, K123MIX, JEX
  (registered). Statistic: COL_P with exact permutation moments (z_K4 at P 8 = −1.3435). q = (1 + #{plant z ≤ z_K4})/(n + 1).
- Sizes: 10,000 references + 2,000 held-out per model × P; 1,000 shuffled K4 per model × P (G3); paired C3 references (same code,
  10,000) as a descriptive comparison.
- **Seeds:** numpy default_rng([209210, tag, model, P]); tags 1 soundness plants, 2 key sampling, 10 C4 refs, 11 band extension,
  15 C3 refs, 20 held-out, 40 shuffled K4. Next free after this cycle: **209211**.

## Gates (all must pass, else NO VERDICT)
- **G0** QIV consistency regression vs case 11: UNSAT at P 1–7, SAT at P 8.
- **G4** C3 mask from lib209 equals lib204 `mask(P)` at all 8 periods; K4 exact z at P 8 = −1.3435 ± 0.001.
- **Gs (planted-key control)** 10 planted Quagmire IV ciphertexts at P 8 (random PA, CA, key; Jane Eyre windows with cribs): the true
  plaintext is allowed by C4 at 97/97 positions in every plant, C4 ⊆ C3, 0 unknown queries.
- **Gx** 6 UNSAT answers re-decided by the full 26-letter model (8 workers, 15 s): no SAT; 20 SAT answers carry a certificate that
  extends to full alphabets and satisfies all pairs.
- **G1 / G1b** COL_P(pt) = COL_P(ct) for plants enciphered by a SAT-sampled K4-consistent QIV key; ciphertext equals K4 at crib and
  C4-forced positions; plants obey the mask.
- **G2b** held-out clean C4 plants judged at q < 0.05: pooled ≤ 0.05 + 2 SE, every config below the binomial 0.05/32 bar.
- **G3 (shuffled-ciphertext null)** shuffled K4 judged at q < 0.05 at P 8: rate ≥ 0.15 in every model.

## Decision rule (P 8 only; other periods descriptive)
q\* = worst (largest) q over the 4 models at P 8; bar b = 0.00625 (case 191's first Holm level); SE = √(q\*(1−q\*)/10,000).
Boundary band (Voynich desk rule, I-265 / cycle 208): if |q\* − b| < 2 SE, extend the worst model once to 40,000 references (tag 11)
and re-decide with its SE.
- q\* ≤ b − 2 SE → **`STAT-DISFAVOURED` carries to Quagmire IV at P 8** (statistical, model-dependent, never `EXACT-EXCL`).
- q\* ≥ b + 2 SE → **`LOW-POWER` for Quagmire IV at P 8**: the H_8 verdict does not transfer to F1 (H_8's own label is untouched).
- otherwise → **`UNRESOLVED`**.
Periods 13–26: Holm table reported, descriptive only. No label of case 191 changes from this run except by the rule above. The exact
SAT cell of case 11 stays open in every outcome. This is not a decryption test; any reading of K4 is out of scope.

## Budget
Expected ≈ 5–7 min wall (K4 masks ≈ 8 × 12 s, soundness 10 × 12 s, plants ≈ 1–2 min). `setsid timeout -k 10 600`, one process group.

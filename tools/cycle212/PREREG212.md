# PREREG212 — cycle 212 pre-registration (2026-11-13, written before any registered run)

Seeds: next free after cycle 211 was 209218. This cycle uses **209218** (8 new planted controls, `plant212.py`) and **209219**
(20 shuffled-K4 nulls). Next free after this cycle: **209220**. File hashes: [`hashes212.txt`](hashes212.txt).

## Part A — New family slot (pointer I-286 → I-284): two-keyword word restart over the 144 themed alphabets, behind the bank and the K3-law decimations/routes
**Model (identical to case 197 except the alphabet list):** R1 word-restart key (key index = position inside the plaintext word mod L;
case 190's 4 × 2 crib segmentations, free offsets o1, o2 ∈ 0..L−1) on a Quagmire tableau, plain alphabet X, cipher alphabet Y;
Vigenère form c = Y[x(p)+k] (variant = same consistency, counted once) and Beaufort form c = Y[k − x(p)]; then model Q (layer letter i
carved at S[i]), S a row of the 165,065-row bank (`perms97.bin`, sha256 004ffc24…) or of the 165,782-row K3-law decimation/route
family (`all.bin`, sha256 8a9e1b32…), both directions.
**Alphabets:** the 144 themed alphabets `tools/cycle180/alpha_themed180.txt` (sha256 9afa2b6b…; case 197's 8 are rows 0, 1, 2, 3, 4,
9, 13, 26). **Pairs:** every ordered (X, Y) except AZ/AZ and KA/KA (cases 193 / 195) = 20,734 pairs × 2 forms = 41,468 tableau-forms
(334× case 197). **Range:** L 1–16 (L 17 not run: analytic E ≈ 800 per family).
**Tool:** [`wrj.c`](wrj.c). Hash join: for each configuration (L, segE, o1, segB, o2) the 24 crib positions fall into key classes;
survivor ⇔ in every class y(c_j) − y(c_j0) = ±(x(p_j) − x(p_j0)) (+ Vig, − Beau). Constraints with equal plain letters are checked
alphabet-free first (equal cipher letters needed); the plaintext-side target vectors (2 × 144 per configuration) are bucketed by their
first two remaining constraints; per (row, direction) every Y is looked up once per group of configurations sharing those two
constraints, then the remaining constraints are checked. Exact (no pruning beyond necessary conditions).
**Development disclosures (before registration):** (1) equivalence check against `wrq.c` with the 8 alphabets / 62 pairs on one shuffled
K4 (`random.Random(1)`, dev only) behind bank rows q ≡ 3 (mod 20), L 1–20: H, P and the 880 S lines (keys included) identical.
(2) Timing probes: K4 behind bank rows q ≡ 0 (mod 50) with the **8-alphabet** slice, L 1–17 (wrj and wrq): 0 survivors (inside the
published case 197 run). The dev shuffle behind bank q ≡ 7 (mod 50) and all.bin q ≡ 7 (mod 50) with 144 alphabets (L 1–17 / 1–16):
0 survivors at L ≤ 16, 75 cells at L 17 (bank). **No K4 run with the 144 alphabets has been made.** (3) The 8 new plants were drawn
(seed 209218) before this file; none has been run through any solver.
**Analytic E (before any K4 run; [`e212.py`](e212.py), 1/26 per constraint):** expected false-survivor cells per full family:
L ≤ 12 < 2·10⁻⁴; **L 13 0.003; L 14 0.069; L 15 1.6; L 16 36**. (The dev shuffle's L 17 suggests the true rate is a few × higher than
this approximation; nulls below measure it.)
**Gates:**
- **G0″ (I-283, reproduce before you vary):** `wrj` with case 197's alphabets/pairs (`alph8.txt`, `p62.txt`) on K4, both full
  families, L 1–17 must reproduce case 197's published K4 table exactly: L 1–15 0 / 0; L 16 bank 0, all 2 (rows 83,548 / 83,549); L 17
  bank 2 (146,519 / 146,520), all 4; and the survivor keys printed in case 197. Fail → NO VERDICT.
- **Plants (≥ 19 / 20):** case 197's 12 hashed plants (`tools/cycle210/plants.tsv`, seed 209214) + 8 new plants (`plants212.tsv`,
  [`plant212.py`](plant212.py), seed 209218, independent encoder derived from cycle 210's, X and Y drawn from the 136 themed
  alphabets outside case 197's 8 words, L 8 / 10 / 11 / 12 / 13 / 14 / 15 / 16, 3 with BERLINCLOCK key indices wrapping mod L, 4 bank
  + 4 all.bin), each through `wrj` (144 alphabets, all pairs, L 1–16) on a 101-row slice of its family around the true row. Hit = the
  true (row, dir, X, Y, form, L, segE, segB, o1, o2) with the planted key at every determined index ([`check212.py`](check212.py)).
- **Nulls:** 20 shuffled K4 (`random.Random(209219)`); null i on rows q ≡ i (mod 10) of the bank (i < 10) or all.bin (i ≥ 10) → one
  full-family null-equivalent per family. **Per-batch effects** (each tenth = a batch) are reported next to the pooled count.
**Labels (per family, per L):** K4 = 0 → `EXCLUDED (exact)`, **discriminating** when the family's null-equivalent has 0 cells at that L
and analytic E < 0.05; `UNRESOLVED` if E is within the I-281 band of 0.05 (0.025–0.1, i.e. L 14) and the nulls are clean;
`zero, not discriminating` when the nulls have cells at that L or E > 0.1. K4 > 0 → every survivor printed (cap 5,000), crib-adjacent
letters read (heuristic) → `NO-SIGNAL` if gibberish; `NO-DISCRIMINATION` if K4's count is inside the per-batch null range scaled to a
full family. Any coherent English → full decryption attempt. Survivor tables carry the split **identical input** (8-word pairs, the
case 197 slice; must equal G0″) vs **changed input** (the new pairs), and the bar is not moved from this file (no data-change / bar-move).
**Budget:** whole part A under `setsid timeout 540` in its own process group; each step writes its own file (checkpoint).

## Part B — Audit add-on (I-287): the Voynich desk's 10 blind wrapped-offset plants behind the bank
**Input:** box-local `voynich/kryptos-audits/case194-wrapped-plants/` (her encoder, her seed 11784): ciphertexts W01–W10 sha256
1d970041… (copied as `plants212b_ciphertexts.txt`), README sha256 b36d305e…, **sealed truths sha256 c0e20249…2a1283bd56 — not opened**.
Design (hers): model Q, R1 on AZ/KA × Vig/Beau, L 16, rows uniform over the 165,064 non-identity bank rows, segB = BERLINCLOCK unsplit
with o2 ∈ {6, 7, 8} (key indices wrap mod 16), o1 0..8, English filler.
**Run:** `wrbank.c` **unchanged** (`tools/cycle206/wrbank.c`, sha256 1001272d…) on the full bank (`perms97.bin`), L 16, every survivor
printed ([`blind212.py`](blind212.py)); the blind results file is hashed and **committed before `sealed/` is opened**.
**Score (rule fixed here):** a plant is recovered when a survivor line sits at the true (perm, dir, tm, L 16, segE, segB, o1, o2) with the
planted key at every determined index; inverse twins and crib-equivalent rows (maps equal on all 24 crib positions) are listed
separately, other rows are off-target. **Pass ≥ 9 / 10.**

## Not this cycle
I-288 (JE re-look), I-277 (L 17–18 rate), I-278 (print cap). No Paradigm submission.

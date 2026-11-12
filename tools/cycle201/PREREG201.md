# PREREG201 — is case 187's `STAT-DISFAVOURED` verdict on the SAT-open periods 8, 13, 23 robust to the plaintext model and to conditioning on K4's crib letters? (I-238)

Written 2026-11-11 ~19:49 PT, before the registered run. Run so far: two timing probes on English plants only (never K4's letter
order: plant z means per model and conditioning at P 8, 50 plants each, seed tag 1), and a smoke test of `recount201.py` (G5 printed
0 mismatches; the G4 line was filtered out of the terminal and not read). K4's PHI_P values and z at 8 / 13 / 23 are already public
(case 187: 14 / 6 / 3, z −0.28 / −0.63 / −0.73); COL_P of K4 has not been computed.

## Why (free slot; I-242 pointer → I-238)
Case 187 disfavoured H_P (periodic substitution, P arbitrary alphabets, direct) at P = 8, 13, 23 with q_rev 0.023 / 0.017 / 0.037,
using Jane Eyre windows with the cribs written in and alphabets drawn freely. Two weaknesses were registered there: the plaintext
model, and plants not conditioned on K4's actual crib letters.

## A design fact found while writing the tools (not a result about K4)
Under H_P, same-phase positions share one bijection, so **PHI_P(ciphertext) = PHI_P(plaintext) exactly**, and so does the column
coincidence count COL_P. The alphabets only move the shuffle null. Conditioning therefore matters through the **plaintext**: K4's
crib letters fix, per phase, a partial map pt → ct. That map (a) forces the plaintext letter at every non-crib position whose K4 letter
is a crib-position K4 letter of the same phase (P 8: 5 positions, P 13: 3, P 23: 2), and (b) **forbids**, at every other position of a
phase, that phase's crib plaintext letters (P 8: 68 positions / 199 letter bans, P 13: 70 / 128, P 23: 47 / 65). The bans fall on
E, A, S, T, N, O, R … and flatten the plaintext, which lowers PHI_P. Case 187's plants ignored (a) and (b).

## Plaintext models (`lib201.load_models`)
JE = Jane Eyre (pg1260, case 187's model); CARTER = Carter & Mace 1923 vol. I (Internet Archive OCR, K3's source; letters after the
contents page; OCR noise kept); K123 = Sanborn's K1+K2+K3 plaintexts as carved (768 letters, overlapping windows); JEX = Jane Eyre with
an X at every . ! ? ; : (K2-style separators).

## Conditioning levels (`lib201.plant`)
C0 = case 187 recipe (free alphabets); C1 = alphabets agree with K4's crib pairs; C2 = C1 + forced plaintext letters (a);
C3 = C2 + bans (b): a banned letter is repaired by a draw from the model's unigram law restricted to allowed letters (an approximation
to rejection sampling; disclosed). Under C3 every same-phase relation between a crib position and any other position equals K4's.

## Test (registered)
For each model × C0–C3 × P ∈ {8, 13, 16, 19, 20, 23, 24, 26}: 1,000 H_P plants (seeds SeedSequence([21000, 10, model, C, P, k])),
each z(PHI_P) against 300 shuffles of itself ([21000, 11, …]); K4's z against 10,000 shuffles of itself ([21000, 2, P]).
q_rev = share of plants with z ≤ z_K4.
**Verdict, confirmatory cells P 8, 13, 23 only:** the cell **stays `STAT-DISFAVOURED` iff max q_rev over the 16 model × conditioning
configurations < 0.05**; otherwise it is **withdrawn to `LOW-POWER (model-sensitive)`**. P 16, 19, 20, 24, 26 are descriptive (no
label change). Secondary, descriptive only (cannot create or keep a label this cycle): q_raw (share of plants with PHI_P(pt) ≤ K4's
raw count; alphabet-free), q_col (same reverse test on COL_P), and a dilution curve (JE, C1, share r ∈ {0.1 … 0.8} of non-crib letters
replaced by uniform letters, 300 plants each) to show how flat a plaintext must be before q_rev crosses 0.05.

## Gates (all must pass, else the run is reported as broken, no verdict)
- **G1** invariance: PHI_P(pt) = PHI_P(ct) and COL_P(pt) = COL_P(ct) for every plant; **G1b** every plant's ciphertext agrees with K4
  where its conditioning level says it must (crib positions; forced positions; banned images absent).
- **G2** clean item scored as suspect (gate offered by the Voynich agent, C105 exchange, adopted here): 200 held-out H_P plants per
  confirmatory model × C × P (tag 20) are judged by the same q_rev rule against the 1,000 references; false-disfavour rate ≤ 0.081
  (0.05 + 2 binomial SE) in every configuration.
- **G3** known negative (the meter must move the other way): 200 shuffles of K4's multiset (not H_P) judged against JE C0 at P 8 are
  disfavoured at a rate ≥ 0.25.
- **G4** regression: cycle 200's own code and seeds reproduce case 187's counts 7/300, 5/300, 11/300 at P 8, 13, 23.
- **G5** recount: pure-Python PHI_P / COL_P on K4 + 20 plants and lib201 vs lib200 on 50 strings: 0 mismatches.

## Run
`run_cycle201.sh`: own process group (`setsid`), hard timeout 480 s, kill only that group. Expected ≈ 1–3 min.

## Blind spots (registered)
Still no transposition after the substitution (I-239); the C3 repair draws unigram letters, not contextual English; K123 windows overlap
heavily (≈ 670 offsets); Carter OCR noise; the shuffle null treats K4 as one segment (Voynich C105: permuting within position classes at
special boundaries such as crib-adjacent spans is not done here); H_P here is fully free per phase, which contains Quagmire IV (case 11's
F1) but is larger than it.

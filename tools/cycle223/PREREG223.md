# PREREG223 — cycle 223 pre-registration (filed before anything below is run on K4, the plants or the nulls)

Filed 2026-11-20 ~03:45 PT (America/Vancouver). Slots: 221 new family, 222 free, so **223 must be an audit** (I-319 / I-320);
224 must be a new family; 225 free. This cycle runs the **I-318 structural check of the case 205 p 21 excess**, with the rank
rule adopted in cycle 221 and enough nulls to use it. Seeds: next free 209255. Reserved here: 209255 (plants), 209256–209415
(160 shuffled-K4 nulls). Next free after this cycle: **209416**. Base: main c4f52fd (cycle 222 published by Firefly).

## The claim audited
Case 205 (cycle 219), one-error scope (excess ≤ 1), all column orders of width 9 and 10, ROW / COL read, σ / σ⁻¹, A–Z / KRYPTOS
tableau, Vigenère (= variant) / Beaufort, key on plaintext (A) or carved (B) index: at **p 21 K4 has 1,928 configurations**, above
all eight nulls (371–1,175). The Voynich desk (voynich-case-files 0185ed5) noted this; showing it at 5 % with a rank rule needs
≥ 146 nulls. At **p 20 K4 has 3** (nulls 2–70), low. Labels at p 18–22 are `INSUFFICIENT-DISCRIMINATION` and stay so unless the
rules below say otherwise. Hypothesis to test (`HYPOTHESIS`, structural): the p 21 excess is produced by **many column orders that put
the 24 crib seats on the same carved positions** (identical crib tests counted many times), not by more distinct fits.

## Tool
`col21.c` = `tools/cycle219/col1e.c` with the enumeration, transposition, key forms, models and `excess()` copied verbatim; the
only changes: it evaluates a comma list of periods (here 20,21) instead of 1–22, prints **every** excess ≤ 1 cell at those periods,
and appends the carved positions j[0..23] of the 24 crib seats to each hit line. `run223.sh` runs K4, the eight cycle-219 nulls
(strings from `data/cycle219/nulls219.tsv`, seeds 209234–209241), the 160 new nulls and the 20 plants (`xargs -P 8`, one job per
text × width × π[0] slice, resumable: a job is skipped when its output already ends with its `C` line). `analyze223.py` computes
everything below. `plant223.py` imports the cycle 219 encryptor unchanged.

## Gates
- **Gate T (reproduction).** col21's per-text counts (strict + one-error) at p 20 and p 21 for K4 and the eight cycle-219 nulls must
  equal `data/cycle219/summary219.json` exactly (K4 p 20 = 3, p 21 = 1,928). Fail → no labels, diagnose.
- **Gate P (seed 209255, bar ≥ 19/20).** 20 plants by the cycle 219 encryptor, period forced to 21 (ids 0–15) or 20 (ids 16–19),
  everything else random; odd ids carry one wrong carved crib letter. Each run on its true π[0] slice; pass = the true cell is
  reported at its true p and its crib-key decrypt matches the plant at every determined position outside the corrupted key class.
  Also checked: the true cell's collapsed key (D2 below) is present.

## Statistics (per text, per p ∈ {20, 21})
- **R** = raw configurations at excess ≤ 1 (the case 205 count).
- **D2** = distinct (alphabet, form, model, p, j[0..23]) — configurations whose crib seats land on the same carved positions are one
  test (primary collapsed count; drops w / read / direction).
- **D3** = distinct crib maps (alphabet, form, model, residue of each seat, key value of each seat) — descriptive, coarsest.
- Descriptive tables: R and D2 split by model A / B, by width, by read × direction, by alphabet × form, and by dissenting seat
  (strict, ambiguous two-member class, or seat 0–23 = EASTNORTHEAST 22–34 / BERLINCLOCK 64–74 1-based), K4 vs null median / 95th pct.

## Rank rule and labels (fixed now)
M = 168 nulls (8 + 160). One-sided upper rank p: p_up(X) = (1 + #{nulls with X ≥ X_K4}) / (M + 1); lower p_low analogous with ≤.
Clopper–Pearson 95 % interval on the tail rate #{X_null ≥ X_K4}/M is printed. Six rank tests are reported (2 periods × R / D2 /
D3); the p 21 R / D2 pair is primary, the rest descriptive; no tail claim beyond the empirical rank.
- **p 21:** p_up(R) > 0.05 → `NOT AN EXCESS (168 nulls; the 8-null observation was chance-level)`.
  p_up(R) ≤ 0.05 and p_up(D2) > 0.05 → `STRUCTURAL MULTIPLICITY` (excess explained by duplicate crib placements).
  p_up(R) ≤ 0.05 and p_up(D2) ≤ 0.05 → `EXCESS PERSISTS AFTER COLLAPSE`, then the decrypt bar decides: any D2 cell with ≥ 49
  determined letters and mean log10 quadgram ≥ −6.0 (qg.bin, as cycle 219) → `CANDIDATE (manual read)`; else
  `NO-SIGNAL (crib-consistent excess, gibberish)` + the structural tables as diagnosis.
- **p 20:** p_low(R) printed (descriptive; Voynich expected it to resolve with ~21 nulls); every K4 p 20 cell is decrypted with the
  same bar. The case 205 label at p 20 (`INSUFFICIENT-DISCRIMINATION` for the exclusion claim) does not change from a rank alone.
- Any K4 cell at p 20 / 21 meeting the decrypt bar → `CANDIDATE` regardless of ranks.

## Budget
Heavy ≤ 8 min wall, `setsid` + `timeout 480`, own process group. Timing measured on a random non-registered string only: ≈ 14.5 s
CPU per text (w 9 + w 10, two periods) → ≈ 5.3 min on 8 cores for 169 texts + plants.

## Disclosures
Known before filing: case 205's K4 / null counts at every p (published), the Voynich desk's reading (0185ed5). Plants and the 160
null strings were generated before filing (plants223.tsv sha256 6bc523e4…, nulls223.tsv b9b6915d…, k123_eng.txt b81e8e7b…,
qg.bin 4a02ba4e…, k4.txt 2797de14…); col21 has been run only on one random smoke string. Nothing has been run on K4, plants or nulls.

## Blind spots
Same family as case 205 (w 9–10 only; w 11 is I-312; no rotations, non-tableau alphabets, running keys, dropped / inserted letters,
two errors). The rank rule is empirical (M = 168): resolution 1/169; six tests, no multiplicity correction claimed beyond reporting all.
A structural explanation is descriptive, not a proof of mechanism.

## Owed paperwork
None from the Voynich desk since 386e342 (filed in cycle 222). Case 205 gets an addendum pointing to case 209.

# PREREG228 — Cycle 228 (free slot): I-312 chunk 3 (width-11 orders, π[0] ∈ {4, 5}) read with the house NC bar, plus the I-331 NC re-read

Filed 2026-11-20 23:50 PT, before any K4, plant or null run of chunk 3. Base: origin/main c2af592 (c227 published). Case file 214.
Slot: free (I-334: 228 free among I-312 chunk 3, I-331, I-337; 229 audit I-333; 230 new family).

## Why this pair
- **I-312 chunk 3** is the next exact slice of an open one-error exclusion (cases 206 / 211 did π[0] ∈ {0,1} and {2,3}); the tool,
  plants and nulls are frozen and the cost is measured (≈ 480 s wall), so it is the highest-value item that fits the budget. It is
  also the first w 11 chunk read with the I-330 NC bar and the tie = '?' rule (cases 206 / 211 used the retired all-letter bar).
- **I-331** (NC re-read of the published crib-consistent cells of cases 205 / 206 / 211) costs seconds, needs no new run, and closes
  the gap the bar change opened: those cells were only ever read with the old bar. It reuses the same reader (`nc228.py`).
- I-337 (full-scale nulls for the case 213 edges) stays queued: it can only move edge labels, and 229 is an audit slot anyway.

## Part A — I-312 chunk 3 (search, exact within scope)
- Tool `tools/cycle220/col1e4.c` **verbatim** (sha256 de865865…e573f), NAL = 4; `tools/cycle228/run228.sh` (= run225.sh with
  π[0] ∈ {4,5}); split by π[1] into 10 sub-slices per π[0] (resumable: a `.raw` is complete iff it ends with a C line).
- Family exactly as cases 206 / 211: ragged grid of width 11 (rotation 0, short last row = leftmost columns), COL / ROW read, σ and
  σ⁻¹, Vigenère (= variant) or Beaufort, key before (A) or after (B) the transposition, p 1–18, alphabet pairs A–Z, KRYPTOS
  (Quagmire III), Quagmire I, Quagmire II. One error = excess ≤ 1 (one crib seat dissents). 2 × 10! = 7,257,600 orders per text.
- **Binary / file formats:** inputs are 97-letter A–Z strings in TSV (`texts.tsv`: label TAB text; `plants228.tsv`, `nulls228.tsv`
  as plant225.py). `.raw` = col1e4 text output (H lines: label w mode dir al be model p excess bad π₀…π₁₀; C line: per-p
  strict / one-error counts). `qg.bin` = 26⁴ float32 little-endian log10 quadgram probabilities, index ((a·26+b)·26+c)·26+d,
  sha256 4a02ba4e…9f69. **Dedup order:** hit lines are kept in file order (π[0] then π[1] sub-slice, then col1e4's enumeration);
  D2 cells = first hit of each (w, mode, dir, al, be, model, p, carved positions under the 24 crib seats) signature in that order.
- **Gate T:** K4, π[0] = 0, π[1] = 1 rerun now must be byte-identical to `data/cycle225/gateT/w11_f0_s1.raw` (sha256 12a6ae3d…33922).
- **Gate R (weak):** K4 strict count 0 at every p ≤ 18 in the chunk (case 114 Part B).
- **Gate P (plants, seed 209549, `plant228.py` = plant225.py with π[0] forced into {4,5}):** 20 plants (5 per alphabet pair, odd ids
  one corrupted carved crib letter, p 1–18, English windows from `k123_eng.txt` sha256 b81e8e7b…2615), each run on its true
  (π[0], π[1]) sub-slice. PASS ⇔ ≥ 19/20 found at the true configuration and period with the decrypt matching outside the corrupted
  key class (first-vote reading, as case 211, for comparability). Wilson 95 % interval printed beside the count. Also reported: the
  share of plants with known ≥ 49 and ≥ 10 NC quadgrams that clear NC ≥ −6.0 under tie = '?' (target ≥ 90 %, Wilson printed;
  a miss is reported, not a gate failure, and would weaken only the decrypt-level reading).
- **Nulls:** eight shuffled K4 (seeds 209550–209557, `random.Random(seed).shuffle`), same chunk, full scale. Invariance pre-check
  (done before filing, on the published case 211 plants, a control): under the same hit, NC moves from −3.9…−4.7 (planted English)
  to unscorable or −8.05 (ciphertext shuffled), and tie = '?' moves `known` 91 → 86 on plant 5; the statistics move.
- **Decrypt reading (pre-registered):** every D2 cell of K4 and every null is decrypted with `nc228.py`: tie = '?' (a residue class
  whose crib-seat key values tie for the top multiplicity reads '?'), candidate iff known ≥ 49, ≥ 10 non-crib quadgrams, NC ≥ −6.0
  (I-330). **Null NC passes are counted per distinct decrypt text** (identical strings from different hits / forms / families
  collapse to one), and the null NC maximum per p is printed beside K4's.
- **Labels per p (chunk scope):** K4 0 and ≤ 2/8 nulls non-zero → `EXACT-EXCL (one-error scope, discriminating)`; K4 0 with ≥ 3/8
  nulls non-zero → `EXACT-EXCL (exact but saturated-null)`; K4 > 0 with K4 ≤ max null → `INSUFFICIENT-DISCRIMINATION` (D2 rank
  p_up = (1 + #nulls with D2 ≥ K4's) / 9, occupancy with Wilson interval); K4 > 0 above every null → manual read, `NO-SIGNAL` unless a
  decrypt passes the NC bar and reads as coherent English. Raw counts printed beside family-collapsed D2 counts and the top-3 D2
  family share (the c226 column agreed with the Voynich desk). The crib filter has no "null" of its own: its exclusion is exact by
  construction, and a shuffled-ciphertext comparison only scales the count; we label that comparison "non-informative by
  construction" beside each EXACT-EXCL, as K088 asked.

## Part B — I-331 NC re-read (no rerun)
- Inputs: the published hit lines of `data/cycle219/` (case 205: col1e w 9–10, one-error p ≤ 18 and strict at all p printed),
  `data/cycle220/` (case 206) and `data/cycle225/` (case 211), K4 and every published null; `tools/cycle228/reread228.py`.
- **Input delta printed:** H lines read per p vs the stamped per-p counts; cells with known < 49 or < 10 NC quadgrams are listed as
  unreachable by any decrypt test. Unprinted cells (case 205 one-error p 19–22) are out of reach and stated.
- Reading: as Part A (D2 unit, tie = '?', NC ≥ −6.0, distinct-text null pass count). The first-vote NC maximum is printed beside it.
- Labels: K4 0 passes → the cells keep their count-level label and gain "decrypt-level NO-SIGNAL (NC)"; any K4 pass → manual read.
- **Disclosure:** a smoke test of `reread228.py` printed the first case 205 lines (K4 p 18: 2 cells, NC max −7.97; p 22: 242 D2
  cells, −7.30; null1_124, 209234, 209235 likewise 0 passes) before this file was committed. No other output was seen.

## Budget, seeds
`run228.sh` inside `setsid timeout 660` (own process group, `xargs -P 8`), ≈ 8 min. Seeds: 209549 plants, 209550–209557 nulls.
Next free seed: **209558**.

## Not in scope
π[0] ∈ {6,7}, {8,9}, {10}; two errors, dropped / inserted letters; p > 18; Quagmire IV; rotations ≠ 0; Quagmire I / II one-error
at w 9–10.

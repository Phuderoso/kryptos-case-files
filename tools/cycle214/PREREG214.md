# PREREG214 — cycle 214 pre-registration (filed before anything below is run)

Filed 2026-11-13 ~23:55 PT (America/Vancouver). Slots: 212 new family, 213 audit, so **214 is a new-family cycle** (I-293).
Seeds: next free 209223. Reserved here: 209223 (A1 nulls), 209224 (A2 nulls), 209225 (A plants). Next free after this cycle: 209226.

## Part A (new family, I-295): digit-keyed polyalphabetic on two keyed alphabets (Gronsfeld / Gromark "keyed on both sides")

**Why.** The coverage table has Gromark with one arbitrary cipher alphabet and plain A–Z/KRYPTOS (cases 143, 164), annealed
both-arbitrary at L 5–6 (cycle 65), but never a digit key with **both** alphabets keyed by words, and never the key-agnostic
digit-range constraint. kryptosbot's findings page lists "Gromark with keyed alphabets on both sides" as only partly tested there
(I-293 pointer; theirs is a pointer, not a result). K1–K3 style: keyed alphabets named by meaningful words; a digit key is the
classic Gronsfeld/Gromark hand-cipher reading of "change the base".

**Model.** Plaintext p, plain alphabet X, cipher alphabet Y, key digit k ∈ {0..9} per letter:
Vigenère form c = Y[x(p)+k], variant c = Y[x(p)−k], Beaufort form c = Y[k−x(p)] (mod 26). x(·), y(·) = positions in X, Y.
Behind a transposition (model Q): the substitution-layer letter at plaintext position i is carved at S[i] (S = family row, dir 0,
or its inverse, dir 1), so the crib pair is (p_i, K4[S[i]]).

**Key-agnostic filter (order-free).** A (S, X, Y, form) is *digit-consistent* iff all 24 crib digits k_i lie in 0..9. This holds
for ANY digit key stream (Gronsfeld periodic, Gromark chain, running digits, dates…), and for both layer orders (the crib pairing
does not depend on which index the key runs on).

**Gromark layer (on digit-consistent survivors only).** Chain addition k_n = k_{n−L} + k_{n−L+1} mod 10, primer length L 1–40,
key index = plaintext position i (index 0) or carved position S[i] (index 1). Consistency = the 24 crib digits are in the image of
the linear map primer → (k at crib indices) mod 10, decided exactly by elimination mod 2 and mod 5. Periodic Gronsfeld (k periodic,
P 1–40) checked the same way (equal index mod P → equal digit).

**Scopes.**
- A1 direct (S = identity): X, Y ∈ the 86,731-alphabet list (`alpha.bin`, sha 2b4ffb69…), all ordered pairs (X = Y allowed),
  3 forms.
- A2 behind the 165,065-row bank (`bank.bin`, sha 004ffc24…) and the 165,782 K3-law decimations/routes (`all.bin`, sha 8a9e1b32…),
  both dirs: X, Y ∈ the 144 themed alphabets (`alpha_themed180.txt`, sha 9afa2b6b…), all ordered pairs, 3 forms.

**Gates.** G-plant: 20 planted ciphertexts (seed 209225: random X, Y from the list in use, form, Gromark primer L 2–10 on either
index, English filler from K1–K3 plaintext pieces + cribs; 10 direct with X, Y from alpha.bin; 10 behind a random bank/all.bin row
with themed X, Y, the tool run on a 101-row slice around the true row). Pass: ≥ 19/20 recover the true (row, dir, X, Y, form) as
digit-consistent AND Gromark-consistent at the true L and index. G-recount: an independent Python checker re-derives every
reported survivor (digits, Gromark consistency) from scratch; 0 mismatches.

**Nulls.** A1: 20 shuffled K4 (random.Random(209223), i-th shuffle), each on X ≡ i (mod 20) of the alpha list (20 disjoint X
slices = one full-search equivalent). A2: 10 shuffled K4 (random.Random(209224)) per family, null i on rows q ≡ i (mod 10).
Analytic expectation E = Σ over pair-forms of Π_i P(digit) reported next to them.

**Labels (fixed now).** Digit-consistent level: K4 count compared with the null-equivalent count (cluster rule of Part C for
counting); if K4 is within the null band → `NO-SIGNAL` (any digit key; not an exclusion). Gromark/periodic level per L: K4 0 and
null-equivalent ≤ 1 (expected ≪ 1) → `EXACT-EXCL` (discriminating) for that L and scope; K4 0 with nulls > 1 → `NO-DISCRIMINATION`;
K4 > 0 → full decrypt + readability check (quadgram score vs plants and nulls) → `NO-SIGNAL` or escalate.
**Budget:** ≤ 8 min heavy wall time for A + B together, own process group (setsid + timeout), resumable outputs.

## Part B (audit, I-292): the Voynich desk's 10 blind grid-aligned wrapped-offset L 16 plants G01–G10

Inputs: `/workspace/voynich/kryptos-audits/case-i292-aligned-wrapped-plants/ciphertexts.txt` (sha256 21d476a2ab01cd435e4702d1f361b73c57ae4401703d64151b31826675e5c8ea);
sealed truths sha256(sealed/truths.json) = 4daad92bd271ebe84a58ff14b504417b4d30f5b6ba698304c559a1c59a256562 — `sealed/` is NOT opened
before the blind results file is committed. Each ciphertext through the **unchanged** `wrbank` (source sha 1001272d…, binary sha
614082dc…) on the full bank, L 16 only: `wrbank CT bank.bin 16 16 200000`. Every S-line is recorded. Detection rule = her README
(survivor at the true perm, dir, tm, L 16, segE EASTNORTH|EAST, segB BERLINCLOCK, o1, o2 with the planted key at every determined
index). Pass ≥ 9/10.

## Part C (method, I-291): cluster rule registered before the cases 193–198 recount

From the Voynich desk (case199-null58-cluster, credit), adopted unchanged: cells of one text are one cluster iff (a) same family,
tm/form, L, segE, segB, o1, o2 (and for Part A: same X, Y, form), and (b) single-linkage on effective maps agreeing on ≥ 16/24 crib
positions; identical effective maps (inverse twins) always merge. Report raw cells, distinct maps and clusters side by side. The
193–198 recount itself is not run in this cycle unless time remains after A and B.

## Part D (documentary): case 198 addendum citing the Voynich desk's L 15 Poisson tail
(case198-L15-poisson/results.md: P(N_cells ≥ 2 | E 1.6134) = 0.479, L 16-calibrated 0.308 → chance level). No new computation.

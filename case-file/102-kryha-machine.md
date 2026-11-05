# 102 — The Kryha machine (cycle 114)

**Question.** Is K4 the output of a Kryha cipher machine (1920s–1950s German commercial device): a fixed alphabet
facing a movable alphabet ring that is stepped an irregular number of places per letter by a toothed code wheel?
No earlier cycle tested it. It is the closest mechanical cousin of the Alberti disk (cycles 106–107), and it was
sold widely, so a sculptor reading about classic machines could have met it.

**Source (precise text, not photos).** J.-F. Bouchaudy, *How the Kryha works*,
<http://www.jfbouch.fr/crypto/kryha/working.html> (read 2026-11-05). It follows P. Marks, "Operational Use and
Cryptanalysis of the Kryha Cipher Machine", *Cryptologia* 35(2):114–155 (2011), and Deavours & Kruh, *Machine
Cryptography and Modern Cryptanalysis* (1985). The mechanism is also in US patent 1,744,347 (Kryha, "Coding machine").
Our model reproduces Bouchaudy's worked V1 example (`XYICPNDEAMAPDTRAX` → `THECOURTISUNABLET`, standard 17-sector
wheel, sector 15) exactly.

**Model.** c_i = M[F⁻¹(p_i) + σ·s_i] with s_i cumulative mod 26.
- **V1:** a removable code wheel; one sector per letter; step = teeth + 4. Published wheels (Marks): 15, 17
  (standard), 18, 19 and 23 sectors.
- **V2:** a universal disk with 52 sectors and fixed tooth counts (published list); screws open any set H of holes;
  one step = all teeth from the current open hole to the next one (no +4).
- "Shift before/after encryption" and the ring's start position are absorbed by the start sector and s0. σ covers the
  ring direction and the encrypt/decrypt mode. Once both alphabets are free, σ = −1 is redundant (negate f, m and s).

**Tests** (`tools/cycle114/`, raw output in `data/cycle114/`). Cribs: EASTNORTHEAST at 21–33 and BERLINCLOCK at
63–73 (0-based), 24 letters.

| test | space | method | K4 | shuffled nulls | planted controls |
|---|---|---|---|---|---|
| A: V1 published wheels, **both alphabets free** | 5 wheels × every start × σ = 184 | exact (weighted union-find + injective placement) | **0 / 184** | 200 shuffles: 91 with 0 (45.5 %), mean 13.7 consistent | 30/30 true setting recovered |
| B1: V1 **any n-sector wheel** (n 1–48, teeth 1–9), K1–K3-style fixed alphabets | 2,356 alphabet pairs × σ × n = 226,176 | exact (residue logic + DP over the gap) | **0** | 20/20 with 0 | 10/10 recovered |
| B2: V2 universal disk, **any set of open holes**, any start hole, fixed alphabets | 4,712 (pair, σ) × every (K, a, s0) | exact (C, greedy earliest holes) | **0** | 20/20 with 0 | 10/10 true (pair, σ) found; true plaintext reproduced |
| C: V1 any n-sector wheel (teeth 1–9), **both alphabets free** | n 1–7 (10 nulls each), n 8–20 K4 only | exact CP-SAT | UNSAT n = 1–4, 6, 7, 9; SAT n = 5, 8, 10–13, 15–20; n = 14 unknown at 90 s | SAT at n 1/2/3/4/5/6/7: 0/3/2/6/6/7/8 of 10 | 6/6 SAT with the true wheel fixed |

Alphabet pairs for B: F ∈ {A–Z, KRYPTOS, and both reversed} × M ∈ the 264 themed keyword alphabets
(`data/cycle114/a264.txt`, the `a264.bin` set of cycles 59–77), the same with F and M swapped, and F = M (the
manual allows identical alphabets).

**Reading.**
- With the Kryha's own published wheels, no pair of alphabets at all, keyword or random, fits the cribs. Shuffled
  nulls fit 0 configurations 45 % of the time, so this 0 alone is weak (p ≈ 0.45). It is still a clean exclusion of
  the configuration, and every planted message passed.
- With K1–K3-style alphabets, the Kryha is excluded for **any** V1 wheel up to 48 sectors and for **any** hole setting of
  the V2 universal disk. These tests have power: random texts never fit, and every planted Kryha message did.
- With free alphabets and a free wheel, the cribs bind only short wheels. Above about 5 sectors, 60–80 % of nulls fit
  too, so the 24 cribs cannot decide. K4 is UNSAT at n = 6, 7 and 9 while most nulls are SAT. That is odd but not
  evidence *for* a Kryha: a real Kryha message is always SAT at its own n.

**Verdict.** Negative. No Kryha configuration in the tested space reproduces the cribs, except the crib-underdetermined
free-alphabet, free-wheel case, which needs a language score to go further.

**Still open.** Free alphabets × free wheel with n ≥ 5 (needs a whole-text language score, like cycle 111's M-209);
V2 with free alphabets; Kryha behind a transposition; non-published V1 wheels with teeth outside 1–9.

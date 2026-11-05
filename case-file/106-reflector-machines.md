# 106 — Reflector machines: Enigma, Typex, NEMA (cycle 118)

**Question.** Machines with a reflector (Enigma in every model, Typex, the Swiss NEMA) send the signal back through the rotors, so at every position the substitution is a fixed-point-free involution: **no letter ever enciphers to itself**. The same holds for any hand cipher built the same way. Does K4 allow such a machine, directly or behind a transposition? The family was not yet in the coverage table.

**Code.** [`tools/cycle118/enigma118.py`](../tools/cycle118/enigma118.py), output [`data/cycle118/enigma118.out`](../data/cycle118/enigma118.out). About 2 seconds.

## A. Direct: excluded, and robust to one carving slip
At the official positions the carved letter equals the plaintext letter twice: **S under S at position 32** (the second S of EASTNORTHEAST, carved S) and **K under K at position 73** (BERLINCLOC**K**). One self-encryption is enough to rule out any reflector machine (plugboard included, since the plugboard is applied symmetrically and keeps the no-fixed-point property).

Because there are two independent witnesses, the exclusion survives any **single** carving anomaly of the kinds in [case file 23](23-one-letter-anomaly.md): a changed or swapped letter can remove at most one of them, and one dropped or extra letter shifts the crib blocks by (±1, ±1) or (0, ±1); every such shift still leaves at least one self-encryption (table in the output). The exclusion only fails under larger, combined shifts, for example both blocks moved by −2 or −3, or block 1 moved by +3 and block 2 by +1 — that needs two or more anomalies and is not a K1–K3-style slip.

## B. Behind a transposition: not excludable by the cribs
If the machine output is then transposed (or the plaintext is transposed first), the only crib-level test is that no crib letter lands on an identical carved letter. Over the 165,065-permutation bank (which is closed under inversion, so both layer orders give identical counts):

| Text | permutations passing |
|---|---|
| K4 | 51,023 (30.9 %) |
| 20 shuffled K4 nulls | min 46,685, median 56,860, max 65,659 |
| random expectation (25/26)²⁴ | 39 % |

K4 sits in the lower part of the null range (3 of 20 nulls lower) — not significant. Planted controls (random fixed-point-free involution per position, then a bank permutation) survive at their true permutation (2/2), and a planted direct reflector text shows 0 self-encryptions, as it must.

So about 51 thousand bank transpositions remain open to a reflector machine. Testing those needs the actual rotor wirings and a bombe-style search per permutation (no plugboard: ~10⁹ settings per permutation; with plugboard, menu loops from only 24 letters spread over two blocks). That is brute force without a stylistic reason: nothing in K1–K3 or in Sanborn's and Scheidt's statements points to a rotor machine, and Scheidt has described hand "masking" methods.

## Verdict
**Negative (direct, exact, robust to one carving slip). Open but unmotivated behind transposition.**

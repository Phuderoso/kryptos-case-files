# 90 — One rotor, any wiring (cycle 96)
> *Before Enigma there was a wheel with 26 wires in it and a ratchet that turned it one notch per letter. Nobody had tried that wheel on K4.*

## 1. Why
The diversity rule required a family not yet in the case files. Rotor machines are not: case file 03 only noted that self-encryptions (S→S at 33, K→K at 74) rule out a *direct* Enigma-style reflector. A single rotor (Hebern, 1917) is a mechanical way to get a non-repeating-looking polyalphabetic from one secret object. Ed Scheidt, who taught Sanborn the methods, had chaired the CIA Cryptographic Center. It also fits the "simple thing in layers" hunch: one wheel, one stepping rule, plus perhaps one transposition.

## 2. Model and reduction
Letters are numbered by an alphabet ordering *s* (A–Z, the KRYPTOS alphabet, or a keyed alphabet). The rotor advances once every *m* letters (t = ⌊i/m⌋). Entry contacts move *d₁* and exit contacts move *d₂* per advance:

  **W( s(pᵢ) + d₁·t ) = s(cᵢ) + d₂·t  (mod 26)**, with the wiring W **arbitrary** (any of 26!).

Real Hebern stepping is d₁ = d₂. Allowing them to differ also covers a rotor between two independently turning rings. The starting position is absorbed into W. So each known plaintext letter gives one (input contact, output contact) pair, and the 24 pairs must form a partial bijection. That is an exact test with no search over the wiring. Reflector variant: W is a fixed-point-free involution (one rotor + reflector, Enigma-style), which is impossible directly (self-encryptions) but possible behind a transposition.

## 3. Tool and controls
`tools/cycle96/rotor.c`, `tools/cycle96/ctl96.py`. Four planted texts with a random wiring: KA alphabet + step 3; keyed alphabet + m = 2, d₁ = 5, d₂ = 11; A–Z behind a cycle-12 transposition; KA + reflector behind a transposition. **4/4 recovered.** The extra hits in the control runs are exact symmetric equivalents (a reversed or rotated ordering with complementary steps, or a transposition that agrees on all 24 crib positions), listed in the [data](../data/cycle96/results.txt).

## 4. Results
| Test | Runs | K4 hits | Shuffled nulls (3) |
|---|---|---|---|
| Direct: 86,731 keyed alphabets × m 1–4 × d₁, d₂ 0–25 | 2.3 × 10⁸ | **0** | 0, 0, 0 |
| Direct: 20,946 themed alphabets × m 1–4 × d₁, d₂ | 5.7 × 10⁷ | **0** | — |
| Transposition (96,630 cycle-12) then rotor: 264 themed alphabets × d₁, d₂, m = 1 | 1.7 × 10¹⁰ | **0** | 0, 0, 0 |
| Same with rotor + reflector | 6.4 × 10⁸ | **0** | — |

## 5. Verdict
| Hypothesis | Status |
|---|---|
| One rotor, arbitrary wiring, keyed/themed contact numbering, steps every 1–4 letters, any entry/exit step rates | **excluded** (direct) |
| Same behind 96,630 transpositions (m = 1), incl. rotor + reflector | **excluded** for 264 themed numberings |
| Two or more rotors (odometer stepping), irregular stepping (Enigma double-step, pin wheels), plugboard + rotor + reflector behind transposition with m > 1 | **open** |

Note: with d₁ = d₂ on A–Z this is a special case of the period-26 "both alphabets arbitrary" family left open by cycle 11b. That case is now closed for this rotor structure, though not in general.

## Addendum, cycle 97: the rotor behind K3-style rearrangements

Cycle 96 put the single rotor behind the c12 columnar family only. Cycle 97 put it behind the two rearrangement families that look most like K3: the K3-law decimations (159,712 perms, step `s` over a padded length `M = 97..112`, both directions) and the K3-grid routes (6,070 spiral, diagonal and serpentine reads). The same exact partial-bijection crib test was used.

| Layer under the rotor | Alphabets | Step period m | Configurations | K4 hits | Planted control |
|---|---|---|---|---|---|
| K3-law decimations | 264 themed | 1 | 28.5 billion | 0 | found (a=100, t=12345, d=5/5) |
| K3-grid routes | 264 themed | 1–4 | 4.33 billion | 0 | found (a=7, t=4321, m=3, d=2/9) |
| K3-grid routes, rotor + reflector | 264 themed | 1–4 | 160 million | 0 | (reflector path checked in cycle 96) |
| 165k transposition family | AZ, KA | 1–4 | 891 million | 0 | found (KA, t=100000, m=2, d=4/4) |

A shuffled-K4 null behind the routes also gave 0 hits. Each control was the only hit in its run, so the test is sharp enough that one survivor would have meant something.

**What this rules out:** a single rotor with *any* wiring, stepping every 1–4 letters, behind a K3-law decimation (m=1) or a K3-grid route (m≤4), with the entry and exit alphabets drawn from the 264 themed set. It also rules out an AZ/KA rotor behind the 165k transposition family with m≤4.

**What it does not rule out:** decimations with m>1, any alphabets outside the themed set, two or more rotors, and stepping that isn't a plain odometer.

**The two-rotor case.** With both wirings free, the unknowns come to about 2^177 (two 26! wirings, plus offsets) against roughly 113 bits of constraint from 24 cribs. An exact crib test can't decide it. Any search there has to score English across all 97 letters, and that's where false positives breed. That is why it stays in the queue instead of being run carelessly.

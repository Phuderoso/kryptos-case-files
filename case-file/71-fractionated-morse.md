# 71 — Fractionated Morse: the Morse stones as a cipher (cycle 73)

**Type:** new family (diversity rule: cycle 72 was an audit).

## Why this door
Morse is literally in plain sight at Kryptos: the copper "Morse stones" by the entrance (VIRTUALLYINVISIBLE, SHADOWFORCES,
TISYOURPOSITION…). The classic letter-output Morse cipher is **Fractionated Morse**: plaintext → Morse, `x` after each
letter (`xx` between words), the stream cut into trigraphs over {`.`,`-`,`x`}, and the 26 trigraphs other than `xxx` mapped to
a keyed alphabet. It also uses `x` as a separator, which echoes K1–K3's X marks. Nothing in case files 1–70 tested it.

## Method (exact, no English scoring)
1. **Positional crib counting proof (any key, any alphabet).** Three Morse symbols per ciphertext letter. Ciphertext
   positions 64–74 (11 letters) carry 33 symbols. BERLINCLOCK needs 34 dots/dashes plus 10 letter separators = **44 > 33**.
   Even with no separators at all, 34 > 33. EASTNORTHEAST needs exactly 39 = 13 × 3 (just fits, a coincidence). So under
   the official positional reading of the cribs, Fractionated Morse (and any Morse fractionation with ≥ 3 symbols per
   letter, the minimum for 26 outputs) is **impossible**.
2. **Unspaced plaintext (K1–K3 style, no word gaps).** Then `xx` never occurs, which removes four trigraphs
   (`.xx`, `-xx`, `xx.`, `xx-`): at most **22** distinct ciphertext letters. Controls: 200 enciphered English texts, max 22
   distinct letters. K4 has **26** → excluded, with no need for cribs.
3. **Spaced plaintext, crib-free SAT** (`tools/cycle73_fractionated_morse_sat.py`). Unknown bijection letter → trigraph;
   every consecutive pair and triple of K4 must decode to a legal stream (no `xxx`, each complete dot/dash run a valid
   letter code, cut runs a valid prefix/suffix). Result: **K4 SAT** (41 s), planted controls 2/2 SAT, shuffled-K4 nulls
   2/2 SAT. The test has no discriminating power for spaced text; it is reported as **inconclusive**, not as support.

## Result
**Negative.** Fractionated Morse is excluded under the positional cribs (counting proof), and the unspaced form is
excluded even without them (alphabet size). Only "spaced Fractionated Morse with cribs not at their stated positions"
survives, and that contradicts Sanborn's published clues. Results: `data/cycle73/fm_results.json`.

## Open
- Morse-based schemes whose output is digits (Morbit, Pollux) need a digit → letter step; no natural convention for K4.
- A Morse layer *underneath* a length-preserving layer is still bound by the same count (the crib positions are
  ciphertext positions), so it is excluded too unless the cribs were placed after a length-changing step.

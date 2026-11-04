# 11 — SAT proofs with both alphabets unknown, base-change keywords, and phrase alphabets (cycle 11b)

> *The loop had already worked the digit-window angle (case files 09 and 10). I came at it from the other side. I took the alphabets away from the attacker's guesswork completely and asked a SAT solver one question: can this family make the 24 crib letters with **any** two alphabets at all? Where the answer is no, the family is dead for good. Where it's yes, I went looking for a key or an alphabet a human could actually have picked. Nada.*

Numbering note: the scheduled loop had already published its own cycles 11–12 (case files 09–10) when this owner-requested cycle ran, so this one is filed as **11b / case file 11**.

## 0. News & tools scan (Nov 2026)
- **Paradigm** ([paradigm.xyz/kryptos/k4](https://paradigm.xyz/kryptos/k4), [writing/kryptos](https://www.paradigm.xyz/writing/kryptos)) runs the K4 verifier. It checks an HMAC of a SHA-256 hash of the answer, and each submission costs **$1**. Paradigm also runs a **Kryptos CTF**: 10 Kryptos-style puzzles at $1,000 each, framed as a benchmark for cryptanalysis tools. Per the instructions we submit nothing.
- **kryptosbot.com** ([FAQ](https://www.kryptosbot.com/faq/)) is a community project. It reports 597 experiments covering 721.7 billion configurations. As of Sept 2026 it lists as *open gaps*: "repeating-key ciphers that use two different keyword-mixed alphabets" and "a Gromark cipher with keyed alphabets on both sides". Sections 2–3 below go straight at both.
- **Tools installed on the box:** `z3-solver` 4.x and `python-sat` (CaDiCaL 1.5.3). z3's integer encoding stalled (it returned "unknown" on 60 s timeouts, even on a planted control). I switched to a one-hot CNF encoding in pysat, which finishes most instances in under 1 s. The z3 attempt is kept as `tools/k4_smt.py` with its control log.

## 1. SAT: which cipher families can produce the cribs at all? (`tools/k4_sat.py`)
**Model.** CA⁻¹(c_i) = PA⁻¹(p_i) + k_i (mod 26). PA and CA are **two independent, completely unknown permutations**. Only the letters that touch the cribs get variables, and this is exact, because any injective partial map extends to a full alphabet. Rotation symmetry is broken by fixing one value. Beaufort is the same model with PA reversed, and plain Vigenère and Quagmire I–III are special cases, so all of them are covered. **Assumption:** ciphertext position i corresponds directly to plaintext position i, with no transposition layer.

| family | UNSAT (impossible, proven) | SAT (not excluded) |
|---|---|---|
| F1 periodic key, period P (Quagmire IV) | P = 1–7, 9–12, 14, 15, 17, 18, 21, 22, 25 | P = 8, 13, 16, 19, 20, 23, 24, 26 |
| F2 Gromark, base b, primer L | b=2,3: every L from 2 to 7 · b=4,5: L ≤ 6 · b=6: L ≤ 5 · b=7: L ≤ 4 · b=8–16: L ≤ 3 · b=26: L ≤ 4 | b=4,5: L=7 · b=6: L ≥ 6 · b=7: L ≥ 5 · b=8–10, 12, 16: L ≥ 4 · b=26: L ≥ 5 |
| F3 progressive key a + s·i | **UNSAT** | — |
| F4 plaintext autokey, lag L | L = 1–4, 8, 10, 42 | the other lags from 1 to 49 (few links between cribs, so weakly constrained) |
| F5 ciphertext autokey, lag L | **L = 1–35**, 38, 42, 45, 49 | L = 36, 37, 39–41, 43, 44, 46–48 |

**Controls** (`analysis/k4_sat_control.txt`):
- A planted Quagmire IV (random PA and CA, P = 7) gives P = 7 SAT, and also P = 6, 12 and 14. That is expected: the cribs can't tell some periods apart.
- A planted Gromark (b10, primer 27182, random alphabets) gives b10 L5 SAT, b10 L4 UNSAT and b5 L5 UNSAT.
- My b10 L5 SAT result agrees with Bean's 39 feasible primers (case file 08).

**What this says (and doesn't):**
- With direct position correspondence, **no periodic key of period ≤ 7, 9–12, 14, 15, 17, 18, 21, 22 or 25 works with ANY pair of mixed alphabets**. That is stronger than the published keyword-alphabet eliminations.
- **Period 8 is the smallest period that survives.** I flag this as a constraint, not a lead. Most larger periods are underdetermined by 24 cribs.
- Proven dead under direct correspondence:
  - progressive keys;
  - ciphertext autokey with lag ≤ 35;
  - Gromark with base ≤ 3, or with primer length ≤ 3 in any base from 2 to 26.

## 2. "Change the base": keyword → number → digits (`tools/k4_cycle11.py` part 1)
**Search.**
- Words: 24,223 (Gutenberg vocabulary of 3–14 letters, plus the listed Kryptos phrases).
- Numberings, 3 per word: base-26 value with A=0; decimal concatenation with A=1…Z=26; base-26 value on KA indices.
- Digits in bases 2–16, used two ways: repeated as a periodic key, or the first L=4/5/6 digits as a Gromark primer in the same base.
- Total: **4,302,293 keys**, each tested against the cribs with arbitrary PA/CA (union-find, then an exact SAT re-check).

**Result.**
- 879 keys are feasible with *some* alphabet pair, and all 879 are confirmed by SAT.
- A random-digit null predicts **≈923** (`tools/basechange_baseline.py`, `analysis/basechange_baseline.txt`). So the count is chance.
- **(1b)** Each of the 879 was then tried against every keyword and phrase alphabet as PA × CA (96,935² pairs per key, 8.3×10¹² pair tests). **0 hits.**

**Control.** A planted key (PALIMPSEST, decimal concatenation A=1…Z=26, base 7, repeated, random alphabets) is recovered as the unique feasible key among 900.

## 3. Phrase alphabets for the double-mixed Gromark and Quagmire IV (`tools/k4_cycle11.py` part 2)
**Phrase alphabets: 31,418 distinct ones.**
- Sources:
  - every substring of length 4–30 of the K1/K2/K3 plaintexts (all K3 is Carter's diary text);
  - 41 listed phrases, among them CANYOUSEEANYTHING, YESWONDERFULTHINGS (Carter), DELIVERINGAMESSAGE, WELTZEITUHR, MENGENLEHREUHR, PALIMPSESTABSCISSA and CHANGETHEBASE.
- Each source is keyed on AZ and on KA, plus the reverses.
- The partner alphabet comes from 96,935 alphabets (the phrase alphabets plus all cycle-10 word alphabets: keyed, reversed and columnar).

**Test.** Exact hash join, with the phrase alphabet as PA or as CA. Families:
- Gromark with all 39 of Bean's b10 L5 primers;
- Quagmire IV with P = 1–26 and a free key.

That is 3.96×10¹¹ pair tests.

**Result.**
- **Gromark: 0.**
- **Quagmire IV: 0 for every P ≤ 23**, including the SAT-surviving periods 8, 13, 16, 19, 20 and 23.
- The only hits are at P = 24 (733) and P = 26 (2.4×10⁸). At those periods almost every residue class holds a single crib letter, so there is nothing left to constrain.

**Controls** (`analysis/k4_cycle11_control.txt`):
- A planted Quagmire IV with P = 8, PA = keyed(THEYUSEDTHEEARTHSMAGNETICFIELD) and CA = keyed(ABSCISSA) is recovered, along with its mirror pair.
- A planted Gromark 27182 with PA = keyed(SANBORN) and CA = KA-keyed(DOESLANGLEYKNOWABOUTTHIS) is recovered uniquely.

## Verdict
- **Direct correspondence:**
  - Every period from 1 to 7 is impossible for a two-alphabet periodic cipher with *any* alphabets.
  - Short-primer Gromark is impossible.
  - Progressive keys are impossible.
  - Short-lag ciphertext autokey is impossible.
- **Keyed-alphabet gaps** listed by kryptosbot: closed for our vocabulary, Bean's primers, and phrases from K1–K3 and Carter.
- **Base-change keywords:** chance-level only, and none pairs with a keyword alphabet.
- What's still open: a transposition layer before or after (cycle 12 began on this), alphabets outside our vocabulary, and families outside this model.

## Reproduce
```
pip install --break-system-packages python-sat z3-solver
python3 tools/k4_sat.py control; python3 tools/k4_sat.py          # ~9 min
python3 tools/k4_cycle11.py control; python3 tools/k4_cycle11.py  # ~2.5 min, needs data/ vocab as in cycle 10
python3 tools/basechange_baseline.py
```

"""Cycle 75: length-changing families.
Part A: counting lemma for expanding schemes (Morse-based, digit-pair, ADFGX...).
Part B: length-reducing scheme = null letters inserted anywhere OUTSIDE the two crib spans,
        key applied in plaintext order (nulls skipped). Periodic key, fixed KA/AZ tableau,
        Vigenere/Beaufort/variant, p 1-26, b = #nulls between the cribs 0-29. Exact.
Part C: same, but each key class mod p is an ARBITRARY substitution alphabet (most general
        periodic substitution). Exact injectivity check.
Usage: python3 nulls75.py <ciphertext-file or K4> -> JSON on stdout."""
import sys, json
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIBS = [(21, "EASTNORTHEAST"), (63, "BERLINCLOCK")]
MORSE = dict(zip(AZ, ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()))

def lemma():
    out = {}
    for s, w in CRIBS:
        sym = sum(len(MORSE[ch]) for ch in w)
        out[w] = {"cipher_slots": len(w), "morse_symbols": sym, "letter_gaps": len(w) - 1,
                  "pollux_digits_min": sym + len(w) - 1,          # one digit per symbol/gap
                  "morbit_digits_min": (sym + len(w) - 1 + 1) // 2,  # pairs of symbols per digit
                  "two_symbol_schemes": 2 * len(w)}               # ADFGX, Polybius, Nihilist, Grandpre
    out["distinct_crib_letters"] = len(set(CRIBS[0][1] + CRIBS[1][1]))  # vs <= 8 one-digit checkerboard letters
    out["97_is_prime"] = all(97 % d for d in range(2, 97))
    return out

def keyval(mode, alph, c, p):
    ci, pi = alph.index(c), alph.index(p)
    return {"vig": (ci - pi) % 26, "beau": (ci + pi) % 26, "var": (pi - ci) % 26}[mode]

def crib_pairs(ct, b):
    # plaintext index (up to a constant shift a, which never matters) for each crib letter
    res = []
    for s, w in CRIBS:
        shift = 0 if s == 21 else b
        for k, ch in enumerate(w):
            res.append((s + k - shift, ct[s + k], ch))
    return res

def partB(ct):
    hits = []
    for alph_name, alph in (("AZ", AZ), ("KA", KA)):
        for mode in ("vig", "beau", "var"):
            for p in range(1, 27):
                for b in range(0, 30):
                    cls = {}
                    ok = True
                    for j, c, pl in crib_pairs(ct, b):
                        k = keyval(mode, alph, c, pl)
                        if cls.setdefault(j % p, k) != k:
                            ok = False; break
                    if ok:
                        hits.append({"alph": alph_name, "mode": mode, "p": p, "b": b,
                                     "key": {r: cls[r] for r in sorted(cls)}})
    return hits

def partC(ct):
    hits = []
    for p in range(1, 27):
        for b in range(0, 30):
            fwd, bwd, ok = {}, {}, True
            for j, c, pl in crib_pairs(ct, b):
                r = j % p
                if fwd.setdefault((r, pl), c) != c or bwd.setdefault((r, c), pl) != pl:
                    ok = False; break
            if ok:
                hits.append({"p": p, "b": b})
    return hits

if __name__ == "__main__":
    ct = K4 if sys.argv[1] == "K4" else open(sys.argv[1]).read().strip()
    assert len(ct) == 97
    print(json.dumps({"lemma": lemma(), "partB": partB(ct), "partC": partC(ct)}))

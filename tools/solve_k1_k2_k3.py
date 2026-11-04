"""Reproducible decryption of K1, K2, K3. Run: python3 tools/solve_k1_k2_k3.py"""
from kryptos_text import K1, K2, K3, KA

def vig_dec(ct, key, alpha=KA):
    out, j = [], 0
    for c in ct:
        if c not in alpha: out.append(c); continue  # '?' passes through, key does not advance
        out.append(alpha[(alpha.index(c) - alpha.index(key[j % len(key)])) % 26]); j += 1
    return "".join(out)

def k3_dec(ct):
    # Double rotational transposition: 14x24 grid of 336 letters -> rotate CW -> regrid width 8 -> rotate CW -> read.
    def rot(text, w):
        rows = [text[i:i+w] for i in range(0, len(text), w)]
        return "".join("".join(r[c] for r in reversed(rows)) for c in range(w))
    body = ct.rstrip('?')  # 336 letters; the final '?' is plaintext punctuation
    return rot(rot(body, 24), 8) + ct[len(body):]

if __name__ == "__main__":
    print("K1:", vig_dec(K1, "PALIMPSEST"))
    print("K2 (as carved):", vig_dec(K2, "ABSCISSA"))
    k2fix = K2[:-8] + "S" + K2[-8:]  # restoring the omitted S here yields WESTXLAYERTWO (Sanborn, 2006)
    print("K2 (S restored):", vig_dec(k2fix, "ABSCISSA"))
    print("K3:", k3_dec(K3))

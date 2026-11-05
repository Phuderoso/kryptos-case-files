"""Cycle 121 planted controls: seriated Playfair + periodic outer key (independent of C checker)."""
import json, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kryptos_text import KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 97
rng = random.Random(12101)
CRIB_POS = list(range(21, 34)) + list(range(63, 74))
CRIB_SET = set(CRIB_POS)
CRIB = "EASTNORTHEASTBERLINCLOCK"
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = open(os.path.join(HERE, "eng.txt")).read()

def square(word, om, fill):
    drop = "Q" if om else "J"
    used = set(drop); s0 = []
    for ch in word:
        if not om and ch == "J": ch = "I"
        if ch not in used and "A" <= ch <= "Z": used.add(ch); s0.append(ch)
    for ch in (KA if fill == 1 else AZ):
        if ch not in used: used.add(ch); s0.append(ch)
    assert len(s0) == 25
    return [s0[(i % 5) * 5 + i // 5] for i in range(25)] if fill == 2 else s0

def pf_enc(a, b, sq):
    p1, p2 = sq.index(a), sq.index(b)
    r1, c1, r2, c2 = p1 // 5, p1 % 5, p2 // 5, p2 % 5
    if r1 == r2: return sq[r1 * 5 + (c1 + 1) % 5], sq[r2 * 5 + (c2 + 1) % 5]
    if c1 == c2: return sq[((r1 + 1) % 5) * 5 + c1], sq[((r2 + 1) % 5) * 5 + c2]
    return sq[r1 * 5 + c2], sq[r2 * 5 + c1]

def pairs_col(w, ph=0):
    out = []
    for c in range(w):
        col = [c + r * w for r in range((N - c + w - 1) // w)]
        for i in range(ph, len(col) - 1, 2):
            out.append((col[i], col[i + 1]))
    return out

def pairs_row(w, ph=0):
    out = []
    for start in range(0, N, w):
        row = list(range(start, min(start + w, N)))
        for i in range(ph, len(row) - 1, 2):
            out.append((row[i], row[i + 1]))
    return out

def fix_double(pt, a, b):
    if pt[a] != pt[b]:
        return
    repl = "X" if pt[a] != "X" else "Z"
    if b not in CRIB_SET:
        pt[b] = repl
    elif a not in CRIB_SET:
        pt[a] = repl
    else:
        pt[b] = repl

def encipher(pt, sq, ser, w, ph, T, mode, key, order=0):
    pt = list(pt)
    pairs = pairs_col(w, ph) if ser == 0 else pairs_row(w, ph)
    p = len(key)
    if order == 0:
        for a, b in pairs:
            fix_double(pt, a, b)
        mid = pt[:]
        for a, b in pairs:
            mid[a], mid[b] = pf_enc(pt[a], pt[b], sq)
        ct = []
        for i, m in enumerate(mid):
            k = T.index(key[i % p]); q = T.index(m)
            c = (q + k) if mode == 0 else (k - q) if mode == 1 else (q - k)
            ct.append(T[c % 26])
        return "".join(ct), "".join(pt), "".join(mid)
    mid = []
    for i, ch in enumerate(pt):
        k = T.index(key[i % p]); q = T.index(ch)
        c = (q + k) if mode == 0 else (k - q) if mode == 1 else (q - k)
        mid.append(T[c % 26])
    sqset = set(sq)
    mid2 = []
    for ch in mid:
        if ch not in sqset:
            if ch == "J" and "I" in sqset:
                ch = "I"
            else:
                ch = "X" if "X" in sqset else sq[0]
        mid2.append(ch)
    mid = mid2
    for a, b in pairs:
        if mid[a] == mid[b]:
            mid[b] = "X" if mid[a] != "X" else "Z"
    ct = mid[:]
    for a, b in pairs:
        ct[a], ct[b] = pf_enc(mid[a], mid[b], sq)
    return "".join(ct), "".join(pt), "".join(mid)

def make_pt(om, sq):
    o = rng.randrange(max(1, len(ENG) - 100))
    base = (ENG * 30)[o:o + 97]
    pt = list(base)
    for i, ch in zip(CRIB_POS, CRIB):
        pt[i] = ch
    sqset = set(sq)
    out = []
    for c in pt:
        if not om and c == "J":
            c = "I"
        if c not in sqset:
            c = "X" if "X" in sqset else sq[0]
        out.append(c)
    return out

SPECS = [
    ("PALIMPSEST", 0, 0, 0, 5, 0, "KA", 0, "ABSCISSA", 0),
    ("SHADOW", 1, 1, 0, 4, 1, "AZ", 1, "BERLIN", 0),
    ("LUCID", 0, 2, 1, 5, 0, "KA", 2, "LANGLEY", 0),
    ("ILLUSION", 0, 1, 0, 3, 0, "AZ", 0, "COMPASS", 0),
    ("UNDERGRUUND", 1, 0, 0, 8, 0, "KA", 1, "CLOCKS", 1),
    ("MEMORY", 0, 0, 1, 7, 1, "KA", 0, "EAST", 0),
]

def main():
    out = []
    for n, (word, om, fill, ser, w, ph, tab, mode, key, order) in enumerate(SPECS):
        sq = square(word, om, fill)
        T = KA if tab == "KA" else AZ
        ok = False
        for _ in range(200):
            pt = make_pt(om, sq)
            ct, pt_s, mid = encipher(pt, sq, ser, w, ph, T, mode, key, order=order)
            if pt_s[21:34] == "EASTNORTHEAST" and pt_s[63:74] == "BERLINCLOCK":
                ok = True
                break
        assert ok, f"control {n} failed to plant cribs"
        out.append(dict(ctl=n, word=word, om=om, fill=fill, ser=ser, w=w, ph=ph, tab=tab,
                        mode=mode, key=key, p=len(key), order=order, ct=ct, pt=pt_s,
                        square="".join(sq)))
        print(n, word, f"ser={ser} w={w} ph={ph} ord={order}", tab, f"mode={mode}", key, "ok")
    os.makedirs("/tmp/kcf/data/cycle121", exist_ok=True)
    json.dump(out, open("/workspace/k4c121/controls121.json", "w"), indent=1)
    json.dump(out, open("/tmp/kcf/data/cycle121/controls121.json", "w"), indent=1)
    open("/workspace/k4c121/words_ctl.txt", "w").write("\n".join(dict.fromkeys(c["word"] for c in out)) + "\n")
    print("OK", len(out))

if __name__ == "__main__":
    main()

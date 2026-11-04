"""Cycle 10 (B2): search keyword-derived alphabet pairs (PA, CA) for the 39 Bean primers (and all 100,000 primers).
Condition: CA.index(c_i) - PA.index(p_i) - k_i = s (const mod 26) at all 24 cribs -> hashed normalised vectors.
Alphabet candidates: AZ, KA, keyed(w), reversed keyed(w), ACA columnar-mixed(w) for every word (3-14 letters) in the
Gutenberg vocabulary used for the quadgram table plus the cycle-7 plain-sight words. Hits are decrypted in full and
scored with English quadgrams (English ~ -4.1/char, random ~ -8).
Run: python3 tools/gromark_keyword.py [control]"""
import sys, re, json, math
import numpy as np
sys.path.insert(0, "tools")
from kryptos_text import K4
from k4_anneal import AZ, KA, KN
from gromark_alphabet import keys, keyed, aca_columnar
from k4_layers import WORDS
N = 97; CR = sorted(KN.items()); CI = [i for i, _ in CR]
_Q = json.load(open("data/quadgrams.json")); Q = _Q["q"]
FLOOR = _Q["floor"]
def qscore(t): return sum(Q.get(t[i:i + 4], FLOOR) for i in range(len(t) - 3)) / (len(t) - 3)
def vocab():
    w = set(WORDS if isinstance(WORDS, (list, set, tuple)) else WORDS.split())
    for f in ("g1342", "g1661", "g2701", "g84", "g98"):
        w |= set(re.findall(r"[A-Z]{3,14}", open(f"data/{f}.txt", encoding="utf-8", errors="ignore").read().upper()))
    return sorted(w)
def alphabets(words):
    A = {"AZ": AZ, "KA": KA, "ZA": AZ[::-1]}
    for w in words:
        A["k:" + w] = keyed(w); A["c:" + w] = aca_columnar(w); A["r:" + w] = keyed(w)[::-1]
    uniq = {}
    for n, a in A.items(): uniq.setdefault(a, n)
    return {n: a for a, n in uniq.items()}
def norm(v): v = np.asarray(v) % 26; return tuple((v - v[0]) % 26)
def run(CT, primers=None):
    prim, K = keys(); KC = K[:, CI]
    if primers is not None:
        sel = [i for i in range(len(prim)) if "".join(map(str, prim[i])) in primers]; prim, K, KC = prim[sel], K[sel], KC[sel]
    A = alphabets(vocab()); names = list(A)
    pt_idx = {}; 
    for n in names:   # plain side: a_i = PA.index(p_i)
        pt_idx.setdefault(norm([A[n].index(p) for _, p in CR]), []).append(n)
    hits = []
    for n in names:   # cipher side: b_i - k_i ; need b - k - a = s  <=> norm(b-k) == norm(a)
        b = np.array([A[n].index(K4c) for K4c in (CT[i] for i in CI)])
        X = (b[None, :] - KC) % 26; X = (X - X[:, :1]) % 26
        for r in range(len(prim)):
            t = tuple(X[r])
            if t in pt_idx:
                for pn in pt_idx[t]:
                    PA, CA = A[pn], A[n]; s = (b[0] - KC[r, 0] - PA.index(CR[0][1])) % 26
                    pt = "".join(PA[(CA.index(CT[i]) - int(K[r, i]) - s) % 26] for i in range(N))
                    hits.append((round(qscore(pt), 3), "".join(map(str, prim[r])), pn, n, int(s), pt))
    return len(names), len(prim), sorted(hits, reverse=True)
if __name__ == "__main__":
    CT = K4
    if len(sys.argv) > 1 and sys.argv[1] == "control":
        eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"[:N]
        pt = list(eng)
        for i, ch in KN.items(): pt[i] = ch
        prim, K = keys(); PA, CA = keyed("LANTERN"), aca_columnar("COMPASS"); kk = K[27182]
        CT = "".join(CA[(PA.index(p) + int(kk[i])) % 26] for i, p in enumerate(pt))
        print("CONTROL: PA=keyed(LANTERN) CA=aca_columnar(COMPASS) primer", "".join(map(str, prim[27182])))
        na, np_, hits = run(CT, primers={"".join(map(str, prim[27182]))})
    else:
        bean = json.load(open("analysis/gromark_feasible.json"))["general"]
        na, np_, hits = run(CT, primers=set(bean))
    print(f"alphabets {na:,} (each used as plain and as cipher) x primers {np_}: pairs checked {na*na*np_:,}; hits {len(hits)}")
    for h in hits[:15]: print("  ", h)

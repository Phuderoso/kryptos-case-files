"""Partial decryption for a coordinate-key configuration: letters whose column and row both fall in a component
fixed by the 24 cribs are determined (the gauge a+t, b-t cancels). Prints the plaintext with '.' elsewhere and the
quadgram score per determined 4-gram (for English-readability inspection)."""
import sys, json, math
import numpy as np
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
Q = json.load(open("/workspace/k4c25/quadgrams.json")); qf, qq = Q["floor"], Q["q"]
cpos = list(range(21, 34)) + list(range(63, 74)); crib = "EASTNORTHEAST" + "BERLINCLOCK"
def partial(carved, pi, alph, mode, model, w, o):
    A = KA if alph == 0 else AZ; P = [int(x) for x in perms[pi]]
    keyidx = (lambda i: i) if model == "A" else (lambda i: P[i])
    val, par = {}, {}
    def f(x):
        s = 0
        while par.setdefault(x, x) != x: s += val.get(x, 0); x = par[x]
        return x, s % 26
    for j, i in enumerate(cpos):
        X = A.index(carved[P[i]]); p = A.index(crib[j]); K = (X - p) % 26 if mode == 0 else (X + p) % 26
        q = keyidx(i) + o; (rc, pc), (rr, pr) = f(("c", q % w)), f(("r", q // w))
        if rc == rr: assert (pc - pr) % 26 == K, "inconsistent"
        else: par[rc] = rr; val[rc] = (K - pc + pr) % 26
    out = []
    for i in range(97):
        q = keyidx(i) + o; (rc, pc), (rr, pr) = f(("c", q % w)), f(("r", q // w))
        if rc != rr: out.append("."); continue
        K = (pc - pr) % 26; X = A.index(carved[P[i]])
        out.append(A[(X - K) % 26] if mode == 0 else A[(K - X) % 26])
    s = "".join(out); grams = [s[i:i+4] for i in range(94) if "." not in s[i:i+4]]
    sc = sum(qq.get(g, qf) for g in grams) / len(grams) if grams else None
    return s, sum(c != "." for c in s), sc
if __name__ == "__main__":
    carved = open(sys.argv[1]).read().strip()
    for line in sys.stdin:
        if not line.startswith("HIT"): continue
        d = dict(kv.split("=") for kv in line.split()[1:])
        s, n, sc = partial(carved, int(d["perm"]), int(d["alph"]), int(d["mode"]), d["model"], int(d["w"]), int(d["o"]))
        print(line.strip(), "|", s, "| determined", n, "| quadgram/4gram", None if sc is None else round(sc, 3))

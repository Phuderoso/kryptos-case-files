"""Cycle 173 add-on (IDEAS I-104): do cycle 172's Quagmire IV survivors at p 15-16 have a vocabulary-word key?
For each M line, rebuild the crib-fixed key values per residue class (as decode172.py), read the key letters three ways
(on CA, on PA, on A-Z), and compare with every vocabulary word of length p at every cyclic shift ('?' = unknown class).
The vocabulary (data/cycle158, 10,056 words) has no word of 15 or 16 letters, so the key is tested as ONE word of length p
(none exist) or TWO vocabulary words joined (lengths a + (p - a), a 3..p-3), every cyclic shift; '?' classes match any letter.
Prints every survivor with an exact one- or two-word key; summary counts.
usage: wordkey173.py CT perms.bin alpha.txt vocab.txt outputs.txt [label]"""
import sys, re, numpy as np
ct, pf, af, vf, of = sys.argv[1:6]; lab = sys.argv[6] if len(sys.argv) > 6 else None
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
AL = {l.split()[1]: l.split()[0] for l in open(af)}
P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
V = {}
for w in open(vf):
    w = w.strip().upper()
    if w.isalpha(): V.setdefault(len(w), set()).add(w)
def fits(seg, S):
    if "?" not in seg: return seg in S
    rx = re.compile(seg.replace("?", ".")); return any(rx.fullmatch(w) for w in S)
n = 0; exact = 0; out = []
for l in open(of):
    if not l.startswith("M "): continue
    _, lb, q, ix, p, mode, pa, ca, m = l.split()
    if lab and lb != lab: continue
    q, ix, p = int(q), int(ix), int(p); PA, CA = AL[pa], AL[ca]; S = P[q]
    key = {}
    for j, c in CRIB.items():
        r = (int(S[j]) if ix else j) % p; kv = (CA.index(ct[S[j]]) - PA.index(c)) % 26 if mode == "vig" else (CA.index(ct[S[j]]) + PA.index(c)) % 26
        assert key.setdefault(r, kv) == kv, l
    n += 1; hits = []
    for rd, A in (("CA", CA), ("PA", PA), ("AZ", AZ)):
        ks = "".join(A[key[r]] if r in key else "?" for r in range(p))
        for s in range(p):
            k2 = ks[s:] + ks[:s]
            if fits(k2, V.get(p, set())): hits.append(f"{rd}:{k2}=1word")
            for a in range(3, p - 2):
                if fits(k2[:a], V.get(a, set())) and fits(k2[a:], V.get(p - a, set())): hits.append(f"{rd}:{k2[:a]}+{k2[a:]}")
    if hits: exact += 1; print(f"{lb} q={q} ix={ix} p={p} {mode} {pa}->{ca} WORDKEY {' '.join(hits)}")
print(f"SUMMARY survivors={n} with_word_key={exact} (vocabulary words of length 15/16: {len(V.get(15, ()))}/{len(V.get(16, ()))})")

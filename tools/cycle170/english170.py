"""English check for decoded candidates: mean log10 quadgram over windows without '?', crib windows excluded
(positions 21-33, 63-73 are forced). Usage: english170.py quadgrams.json decodes.txt [planted-decode lines file]"""
import sys, json
Q = json.load(open(sys.argv[1])); fl, q = Q['floor'], Q['q']
CR = set(range(21, 34)) | set(range(63, 74))
def score(pt):
    w = [q.get(pt[i:i+4], fl) for i in range(94) if '?' not in pt[i:i+4] and not (set(range(i, i+4)) <= CR) and not (set(range(i, i+4)) & CR)]
    return (sum(w) / len(w) if w else None), len(w)
rows = []
for l in open(sys.argv[2]):
    pt = l.split(' PT ')[-1].strip(); s, n = score(pt)
    if s is not None: rows.append((s, n, l.strip()))
rows.sort(reverse=True)
print(f"candidates {len(rows)}; best 5 (mean log10 quadgram outside the cribs, windows):")
for s, n, l in rows[:5]: print(f"{s:.3f} n={n} {l}")
import statistics; print("median", round(statistics.median(r[0] for r in rows), 3))

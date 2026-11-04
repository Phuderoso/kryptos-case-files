"""Build English quadgram log-probabilities from Project Gutenberg texts (#1661 Sherlock Holmes, #1342 Pride and Prejudice,
#2701 Moby Dick, #84 Frankenstein, #98 A Tale of Two Cities). Downloads to data/ (not committed).
Run from repo root: python3 tools/build_quadgrams.py"""
import os, re, json, math, urllib.request
from collections import Counter
os.makedirs("data", exist_ok=True)
c = Counter()
for n in (1661, 1342, 2701, 84, 98):
    p = f"data/g{n}.txt"
    if not os.path.exists(p): urllib.request.urlretrieve(f"https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt", p)
    t = re.sub("[^A-Z]", "", open(p, encoding="utf-8", errors="ignore").read().upper())
    c.update(t[i:i+4] for i in range(len(t) - 3))
tot = sum(c.values())
json.dump({"floor": math.log10(0.01 / tot), "q": {k: math.log10(v / tot) for k, v in c.items()}}, open("data/quadgrams.json", "w"))
print(f"quadgrams: {len(c)} distinct, {tot} total")

"""Cycle 11: null baseline for the base-change test: expected number of crib-feasible keys if digit strings were random
(same base, same use, same digit length distribution). Compares to observed survivors."""
import sys, json, random, collections
sys.path.insert(0, "tools")
import k4_cycle11 as C, gromark_keyword as GK
from gromark_alphabet import feasible
from kryptos_text import K4
words = sorted(w for w in GK.vocab() if 3 <= len(w) <= 14) + sorted(C.phrases() & set(C.EXTRA))
tests = collections.Counter(); lens = collections.defaultdict(list)
for w in words:
    for nm, n in C.nums(w).items():
        for b in range(2, 17):
            d = C.digits(n, b)
            if len(d) < 3: continue
            tests[(b, "rep")] += 1; lens[b].append(len(d))
            for L in (4, 5, 6):
                if len(d) >= L: tests[(b, f"grom{L}")] += 1
obs = collections.Counter((b, u) for _, _, b, u, _ in json.load(open("analysis/k4_basechange_feasible.json")))
rng = random.Random(7); exp = 0; out = []
for (b, u), t in sorted(tests.items()):
    S = 3000; f = 0
    for _ in range(S):
        if u == "rep":
            L = rng.choice(lens[b]); d = [rng.randrange(b) for _ in range(L)]; k = [d[i % L] for i in range(97)]
        else: k = C.gromark([rng.randrange(b) for _ in range(int(u[-1]))], b)
        f += feasible(K4, [k[i] for i in C.CI])[0]
    e = t * f / S; exp += e; out.append(f"b={b:2d} {u:6s} tests={t:7d} random-rate={f/S:.4f} expected={e:7.1f} observed={obs[(b,u)]}")
out.append(f"TOTAL expected under null ~{exp:.0f} ; observed {sum(obs.values())}")
open("analysis/basechange_baseline.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))

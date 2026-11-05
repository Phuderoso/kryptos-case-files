"""Shuffled-ciphertext baselines for nulls75 (same letters, random order; cribs unchanged)."""
import random, json
from collections import Counter
import nulls75
from kryptos_text import K4
def summ(ct):
    B = nulls75.partB(ct); C = nulls75.partC(ct)
    return {"B_count": len(B), "B_minp": min([h["p"] for h in B], default=None),
            "B_by_p": dict(Counter(h["p"] for h in B)),
            "C_count": len(C), "C_minp": min([h["p"] for h in C], default=None),
            "C_p6": sum(h["p"] == 6 for h in C), "C_p7": sum(h["p"] == 7 for h in C),
            "C_p6_b": [h["b"] for h in C if h["p"] == 6]}
rng = random.Random(75)
k4 = summ(K4)
nulls = []
for t in range(500):
    l = list(K4); rng.shuffle(l); nulls.append(summ("".join(l)))
out = {"K4": k4,
       "null_C_minp": dict(Counter(n["C_minp"] for n in nulls)),
       "null_frac_C_p6_ge1": sum(n["C_p6"] >= 1 for n in nulls) / len(nulls),
       "null_mean_C_p6": sum(n["C_p6"] for n in nulls) / len(nulls),
       "null_frac_C_p6_ge_K4": sum(n["C_p6"] >= k4["C_p6"] for n in nulls) / len(nulls),
       "null_B_minp": dict(Counter(n["B_minp"] for n in nulls)),
       "null_mean_B_count": sum(n["B_count"] for n in nulls) / len(nulls),
       "null_frac_B_count_ge_K4": sum(n["B_count"] >= k4["B_count"] for n in nulls) / len(nulls)}
print(json.dumps(out, indent=1))

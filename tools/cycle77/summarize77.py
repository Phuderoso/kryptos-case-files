"""Summarise cycle 77: histograms of consistent configurations by exact-check count, K4 vs shuffled K4."""
import glob, json, os
def hist(tag):
    fs = sorted(glob.glob(f"out_{tag}_[0-7].txt"))
    if len(fs) < 8 or not all(open(f).read().rstrip().endswith("DONE") for f in fs): return None
    h = {"A": [0]*25, "B": [0]*25}
    for f in fs:
        for l in open(f):
            if l.startswith("HIST"):
                m = l.split()[1][-1]; h[m] = [a+b for a, b in zip(h[m], map(int, l.split()[2:]))]
    return h
def mx(v): return max([i for i, x in enumerate(v) if x] or [0])
def ge(v, k): return sum(v[k:])
def direct(tag):
    for l in open(f"out_{tag}_direct264.txt"):
        if l.startswith("HIST model=A"): return list(map(int, l.split()[2:]))
S = {"k4": None, "nulls": {}}
for tag in ["k4"] + [f"null{i}" for i in range(20)]:
    h = hist(tag); d = direct(tag)
    rec = {"direct264_max": mx(d), "direct264_ge2": ge(d, 2)}
    if h: rec.update({f"{m}_max": mx(h[m]) for m in "AB"}); rec.update({f"{m}_ge4": ge(h[m], 4) for m in "AB"}); rec["hist"] = h
    if tag == "k4": S["k4"] = rec
    else: S["nulls"][tag] = rec
json.dump(S, open("cycle77_summary.json", "w"), indent=1)
k = S["k4"]; print("K4", {x: k[x] for x in k if x != "hist"})
done = {t: r for t, r in S["nulls"].items() if "A_max" in r}
print("nulls with transposition run:", len(done))
for key in ["A_max", "B_max", "A_ge4", "B_ge4"]:
    v = sorted(r[key] for r in done.values()); print(key, "min", v[0], "median", v[len(v)//2], "max", v[-1], "K4", k[key])
v = sorted(r["direct264_max"] for r in S["nulls"].values()); print("direct264_max nulls (20):", v, "K4", k["direct264_max"])

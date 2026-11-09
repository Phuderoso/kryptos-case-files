"""Cycle 152 summary: merge the C lines of out/*.txt per text (K4, null1, null2) for direct and bank runs."""
import glob, re, collections
def parse(line):
    d = {}; toks = line.split(); d["cfg"] = int(re.search(r"cfg=(\d+)", line).group(1)); d["printed"] = int(re.search(r"printed=(\d+)", line).group(1))
    sec = None; d["h"] = collections.defaultdict(collections.Counter)
    for t in toks[2:]:
        if t.startswith("histCT"): sec = "histCT"; continue
        if t.startswith("CTfull"): sec = "CTfull"; continue
        if t.startswith("CTnear2"): sec = "CTnear2"; continue
        if t.startswith("CTnear"): sec = "CTnear"; continue
        if t.startswith("histPTfull"): sec = "PTfull"; continue
        if sec and re.fullmatch(r"\d+:\d+", t): a, b = map(int, t.split(":")); d["h"][sec][a] += b
    return d
for mode in ("D", "B"):
    print("== %s ==" % ("direct" if mode == "D" else "behind the 165,065-entry bank (both directions, model Q + carved order)"))
    for lab in ("K4", "null1", "null2"):
        fs = glob.glob(f"out/{lab}_{mode}_*.txt"); tot = {"cfg": 0, "printed": 0}; H = collections.defaultdict(collections.Counter)
        for f in fs:
            for line in open(f):
                if line.startswith("C "):
                    d = parse(line); tot["cfg"] += d["cfg"]; tot["printed"] += d["printed"]
                    for k, v in d["h"].items(): H[k].update(v)
        best = max(H["histCT"]) if H["histCT"] else None
        tail = " ".join(f"{m}:{H['histCT'][m]}" for m in sorted(H["histCT"]) if m >= 12)
        def big(sec, lo): return " ".join(f"n{n}:{H[sec][n]}" for n in sorted(H[sec]) if n >= lo) or "none"
        print(f"{lab:6s} chunks={len(fs)} cfg={tot['cfg']:,} printed={tot['printed']} CT best m={best} tail(m>=12) {tail}")
        print(f"       CT m=n (exact, n>=12): {big('CTfull',12)} | m=n-1 (n>=12): {big('CTnear',12)} | m=n-2 (n>=14): {big('CTnear2',14)}")
        print(f"       CT m=n at n 8-11: {' '.join(f'n{n}:{H['CTfull'][n]}' for n in range(8,12) if H['CTfull'][n]) or 'none'} | PT m=n (n>=7): {big('PTfull',7)}")

"""Cycle 219 analysis: gate R (reproduce case 112 strict counts), gate P (plants), per-p one-error counts K4 vs 8 nulls,
crib-distinct collapse, crib-key decrypt + quadgram score of every K4 hit at p <= 18, labels per PREREG219.
usage: analyze219.py WORK qg.bin OUTDIR"""
import sys, os, glob, json, hashlib, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plant219 import reading_order, KA, AZ, CRP, CRS
from stamp219 import header
W, QG, OUT = sys.argv[1:4]
TOOL = os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "col1e.c"))
qg = np.fromfile(QG, dtype=np.float32)
texts = dict(l.rstrip("\n").split("\t") for l in open(f"{W}/texts.tsv"))
plants = [l.rstrip("\n").split("\t") for l in open(f"{W}/plants219.tsv")][1:]
for p in plants: texts["plant" + p[0]] = p[13]
def S_of(w, pi, mode, dir_):
    order = reading_order(w, pi, mode); sig = [0]*97
    for m, cell in enumerate(order): sig[cell] = m
    if dir_ == 0: return sig
    inv = [0]*97
    for i in range(97): inv[sig[i]] = i
    return inv
def load(lab):
    hits, cnt = [], collections.defaultdict(lambda: [0, 0]); files = sorted(glob.glob(f"{W}/out/{lab}/*.raw")); nperm = 0
    for f in files:
        for line in open(f):
            a = line.split()
            if a[0] == "H": hits.append(tuple(int(x) for x in a[2:11]) + (tuple(int(x) for x in a[11:]),))
            elif a[0] == "C":
                nperm += int(a[5])
                for tok in a[6:]:
                    p, v = tok[1:].split("="); s0, s1 = v.split("/"); cnt[int(p)][0] += int(s0); cnt[int(p)][1] += int(s1)
    return hits, dict(cnt), nperm, files
def decrypt(ct, h):
    w, mode, dir_, al, be, model, p, e, bad, pi = h
    A = AZ if al == 0 else KA; S = S_of(w, list(pi), mode, dir_)
    cls = lambda i: (i if model == 0 else S[i]) % p
    votes = collections.defaultdict(collections.Counter)
    for t, i in enumerate(CRP):
        c = A.index(ct[S[i]]); x = A.index(CRS[t]); votes[cls(i)][(c + x) % 26 if be else (c - x) % 26] += 1
    key = {r: v.most_common(1)[0][0] for r, v in votes.items()}
    P = []
    for i in range(97):
        r = cls(i)
        if r not in key: P.append("?"); continue
        c = A.index(ct[S[i]]); P.append(A[(key[r] - c) % 26] if be else A[(c - key[r]) % 26])
    return "".join(P), key, S, cls
def score(P):
    q = [qg[((ord(P[i])-65)*26 + ord(P[i+1])-65)*676 + (ord(P[i+2])-65)*26 + ord(P[i+3])-65]
         for i in range(94) if "?" not in P[i:i+4]]
    return (float(np.mean(q)) if q else -9.0), len(q)
R = {"inputs": {}, "scope": "col1e: all orders w9 (362,880) + w10 (3,628,800), ROW/COL, dir 0/1, AZ/KA, Vig(=variant)/Beau, model A/B, p 1-22; one error = excess <= 1"}
os.makedirs(OUT, exist_ok=True)
# per-text counts
counts = {}
for lab, ct in texts.items():
    hits, cnt, nperm, files = load(lab)
    counts[lab] = {"nperm": nperm, "strict": [cnt.get(p, [0, 0])[0] for p in range(1, 23)], "one": [cnt.get(p, [0, 0])[1] for p in range(1, 23)]}
    R["inputs"][lab] = {"input_sha256": hashlib.sha256(ct.encode()).hexdigest(), "files": len(files)}
    if not lab.startswith("plant"):
        body = "".join(open(f).read() for f in files)
        with open(f"{OUT}/{lab}.txt", "w") as fo:
            fo.write("\n".join(header("I-007 one-error audit, full scope w9+w10 p1-22 (hit lines: excess<=1 at p<=18, strict at all p)",
                                      lab, ct, TOOL, "n/a" if lab == "K4" else lab, ["col1e", "CT", "w", "first", "22", "18"])) + "\n")
            fo.write(f"# per p strict/one-error: " + " ".join(f"p{p}={counts[lab]['strict'][p-1]}/{counts[lab]['one'][p-1]}" for p in range(1, 23)) + "\n")
            fo.write(body)
# gate R
k4s = counts["K4"]["strict"]; n1s = counts["null1_124"]["strict"]
R["gateR"] = {"K4_strict_p1_21_zero": all(x == 0 for x in k4s[:21]), "K4_strict_p22": k4s[21], "null1_p21": n1s[20], "null1_p22": n1s[21],
              "null1_p1_20_zero": all(x == 0 for x in n1s[:20]), "nperm_K4": counts["K4"]["nperm"]}
R["gateR"]["PASS"] = R["gateR"]["K4_strict_p1_21_zero"] and k4s[21] == 720 and n1s[20] == 4 and n1s[21] == 144 and R["gateR"]["null1_p1_20_zero"]
# gate P
prow = []
for p in plants:
    pid, w, mode, dir_, al, form, model, per = map(int, p[:8]); pi = tuple(int(x) for x in p[9].split(",")); seat = int(p[10]); P0 = p[12]; ct = p[13]
    be = 1 if form == 2 else 0
    hits, _, _, _ = load("plant" + p[0])
    mine = [h for h in hits if h[:7] == (w, mode, dir_, al, be, model, per) and h[9] == pi]
    ok = False; info = {}
    if mine:
        h = mine[0]; D, key, S, cls = decrypt(ct, h)
        badcls = cls(CRP[seat]) if seat >= 0 else None
        mism = [i for i in range(97) if D[i] != "?" and D[i] != P0[i] and (badcls is None or cls(i) != badcls)]
        ok = len(mism) == 0; info = {"excess": h[7], "bad": h[8], "mismatch": len(mism), "known": 97 - D.count("?")}
    prow.append({"pid": pid, "w": w, "p": per, "model": model, "form": form, "seat": seat, "found": bool(mine), "pass": ok, **info})
R["gateP"] = {"passes": sum(r["pass"] for r in prow), "n": len(prow), "bar": 19, "rows": prow}
R["gateP"]["PASS"] = R["gateP"]["passes"] >= 19
# K4 hits p<=18
nulls = [l for l in texts if l.startswith("null2092")]
hits, _, _, _ = load("K4"); k4ct = texts["K4"]
distinct = {}
for h in hits:
    if h[6] > 18 or (h[7] == 0 and h[6] > 18): continue
    D, key, S, cls = decrypt(k4ct, h)
    sig = h[:7] + tuple(S[i] for i in CRP)
    if sig not in distinct:
        sc, nq = score(D); distinct[sig] = {"cfg": list(h[:9]), "pi": list(h[9]), "known": 97 - D.count("?"), "qg": sc, "nq": nq, "pt": D, "raw": 0}
    distinct[sig]["raw"] += 1
def ndist(lab):
    hs, _, _, _ = load(lab); seen = collections.defaultdict(set)
    for h in hs:
        if h[6] > 18: continue
        S = S_of(h[0], list(h[9]), h[1], h[2]); seen[h[6]].add(h[:7] + tuple(S[i] for i in CRP))
    return {p: len(v) for p, v in seen.items()}
nd = {lab: ndist(lab) for lab in ["K4"] + nulls}
labels = {}
for p in range(1, 23):
    k = counts["K4"]["strict"][p-1] + counts["K4"]["one"][p-1]
    nv = [counts[l]["strict"][p-1] + counts[l]["one"][p-1] for l in nulls]
    row = {"K4": k, "nulls": nv, "K4_distinct": nd["K4"].get(p, 0) if p <= 18 else None, "null_distinct": [nd[l].get(p, 0) for l in nulls] if p <= 18 else None}
    if p >= 19: lab = "INSUFFICIENT-DISCRIMINATION (strict claim already underdetermined)" if k else "EXACT-EXCL (one-error scope, p>=19, saturated-null)" if any(nv) else "EXACT-EXCL (one-error scope)"
    elif k == 0: lab = "EXACT-EXCL (one-error scope, discriminating)" if sum(1 for x in nv if x == 0) >= 6 else "EXACT-EXCL (one-error scope, exact but saturated-null)"
    else:
        cands = [d for d in distinct.values() if d["cfg"][6] == p and d["known"] >= 49 and d["qg"] >= -6.0]
        if cands: lab = "CANDIDATE (manual read)"
        elif k <= max(nv): lab = "INSUFFICIENT-DISCRIMINATION"
        else: lab = "NO-SIGNAL (excess over 8 nulls, gibberish)"
    row["label"] = lab; labels[p] = row
R["per_p"] = labels; R["counts"] = counts
R["K4_hits_distinct"] = sorted(distinct.values(), key=lambda d: -d["qg"])
with open(f"{OUT}/summary219.json", "w") as f: json.dump(R, f, indent=1)
print("gateR", R["gateR"]); print("gateP", R["gateP"]["passes"], "/20", [ (r["pid"], r["pass"]) for r in prow if not r["pass"]])
for p in range(1, 23): print(p, labels[p])
for d in R["K4_hits_distinct"][:15]: print(round(d["qg"], 2), d["known"], d["raw"], d["cfg"], d["pt"])

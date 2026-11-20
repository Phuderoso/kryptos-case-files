"""Cycle 223 analysis (PREREG223): gate T (reproduce case 205 p 20 / 21 counts), gate P (plants), R / D2 / D3 per text and period,
rank rule on 168 nulls, structural tables, crib-key decrypt + quadgram of K4's p 20 / 21 cells (collapsed by D2).
usage: analyze223.py WORK qg.bin OUTDIR REPO"""
import sys, os, glob, json, hashlib, collections, math
import numpy as np
W, QG, OUT, REPO = sys.argv[1:5]
sys.path.insert(0, f"{REPO}/tools/cycle219")
from plant219 import reading_order, KA, AZ, CRP, CRS
from stamp219 import header
TOOL = "tools/cycle223/col21.c"
qg = np.fromfile(QG, dtype=np.float32)
texts = dict(l.rstrip("\n").split("\t") for l in open(f"{W}/texts.tsv"))
plants = [l.rstrip("\n").split("\t") for l in open(f"{REPO}/data/cycle223/plants223.tsv")][1:]
S219 = json.load(open(f"{REPO}/data/cycle219/summary219.json"))
PS = (20, 21)
def load(lab):
    hits, cnt, nperm = [], collections.Counter(), 0
    for f in sorted(glob.glob(f"{W}/out/{lab}/*.raw")):
        for line in open(f):
            a = line.split()
            if a[0] == "H":
                bar = a.index("|"); v = [int(x) for x in a[2:11]]
                hits.append((tuple(v), tuple(int(x) for x in a[11:bar]), tuple(int(x) for x in a[bar+1:])))
            elif a[0] == "C":
                nperm += int(a[5])
                for tok in a[6:]:
                    p, v = tok[1:].split("="); s0, s1 = v.split("/"); cnt[int(p)] += int(s0) + int(s1)
    return hits, cnt, nperm
def kv_res(ct, h, j):
    w, mode, dir_, al, be, model, p, e, bad = h; A = AZ if al == 0 else KA
    kv = tuple(((A.index(ct[j[t]]) + A.index(CRS[t])) % 26) if be else ((A.index(ct[j[t]]) - A.index(CRS[t])) % 26) for t in range(24))
    res = tuple(((CRP[t] if model == 0 else j[t]) % p) for t in range(24))
    return kv, res
def S_of(w, pi, mode, dir_):
    order = reading_order(w, list(pi), mode); sig = [0]*97
    for m, cell in enumerate(order): sig[cell] = m
    if dir_ == 0: return sig
    inv = [0]*97
    for i in range(97): inv[sig[i]] = i
    return inv
def decrypt(ct, h, pi):
    w, mode, dir_, al, be, model, p, e, bad = h; A = AZ if al == 0 else KA; S = S_of(w, pi, mode, dir_)
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
    return "".join(P), cls
def score(P):
    q = [qg[((ord(P[i])-65)*26 + ord(P[i+1])-65)*676 + (ord(P[i+2])-65)*26 + ord(P[i+3])-65] for i in range(94) if "?" not in P[i:i+4]]
    return (float(np.mean(q)) if q else -9.0), len(q)
def cp(k, n):
    from scipy.stats import beta
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return [round(float(lo), 4), round(float(hi), 4)]
def stats(lab):
    hits, cnt, nperm = load(lab); ct = texts[lab]; out = {"nperm": nperm}
    for p in PS:
        hp = [h for h in hits if h[0][6] == p]
        d2 = set((h[0][3], h[0][4], h[0][5], p, h[2]) for h in hp)
        d3 = set((h[0][3], h[0][4], h[0][5], p) + kv_res(ct, h[0], h[2]) for h in hp)
        tab = collections.defaultdict(collections.Counter)
        for h in hp:
            v = h[0]; key2 = (v[3], v[4], v[5], p, h[2])
            for name, k in (("model", "AB"[v[5]]), ("w", v[0]), ("read_dir", f"{'ROW' if v[1]==0 else 'COL'}/{'sig' if v[2]==0 else 'inv'}"),
                            ("alph_form", f"{'AZ' if v[3]==0 else 'KA'}/{'Vig' if v[4]==0 else 'Beau'}"),
                            ("seat", "strict" if v[8] == -2 else "ambig" if v[8] == -1 else f"s{v[8]:02d}")):
                tab[name + ":R"][k] += 1
        for name in ("model", "seat"):
            seen = collections.defaultdict(set)
            for h in hp:
                v = h[0]; k = "AB"[v[5]] if name == "model" else ("strict" if v[8] == -2 else "ambig" if v[8] == -1 else f"s{v[8]:02d}")
                seen[k].add((v[3], v[4], v[5], p, h[2]))
            tab[name + ":D2"] = collections.Counter({k: len(s) for k, s in seen.items()})
        out[p] = {"R": len(hp), "R_counted": cnt[p], "D2": len(d2), "D3": len(d3), "tables": {k: dict(v) for k, v in tab.items()}}
    return out, hits
os.makedirs(OUT, exist_ok=True)
R = {"scope": "col21 (col1e verbatim): all orders w9+w10, ROW/COL, sig/inv, AZ/KA, Vig(=variant)/Beau, model A/B, p 20 and 21, excess <= 1",
     "inputs": {}, "per_text": {}}
nulls = [l for l in texts if l.startswith("null")]
allhits = {}
for lab in ["K4"] + nulls:
    st, hits = stats(lab); R["per_text"][lab] = st; R["inputs"][lab] = hashlib.sha256(texts[lab].encode()).hexdigest()
    if lab == "K4" or lab in ("null209234",): allhits[lab] = hits
    with open(f"{OUT}/results_{lab}.txt", "w") as fo:
        fo.write("\n".join(header("I-318 audit, w9+w10, p 20/21, every excess<=1 cell with crib-seat carved positions", lab, texts[lab], TOOL,
                                  "n/a" if lab == "K4" else lab[4:], ["col21", "CT", "w", "first", "20,21"])) + "\n")
        fo.write(f"# p20 R={st[20]['R']} D2={st[20]['D2']} D3={st[20]['D3']} | p21 R={st[21]['R']} D2={st[21]['D2']} D3={st[21]['D3']}\n")
        for f in sorted(glob.glob(f"{W}/out/{lab}/*.raw")): fo.write(open(f).read())
# gate T
c219 = S219["counts"]; gT = {}
for lab in ["K4"] + [f"null{s}" for s in range(209234, 209242)]:
    for p in PS:
        exp = c219[lab]["strict"][p-1] + c219[lab]["one"][p-1]; got = R["per_text"][lab][p]["R_counted"]
        gT[f"{lab}_p{p}"] = [got, exp]
R["gateT"] = {"rows": gT, "PASS": all(a == b for a, b in gT.values()) and all(R["per_text"][l][p]["R"] == R["per_text"][l][p]["R_counted"] for l in R["per_text"] for p in PS)}
# gate P
prow = []
for pr in plants:
    pid, w, mode, dir_, al, form, model, per = map(int, pr[:8]); pi = tuple(int(x) for x in pr[9].split(",")); seat = int(pr[10]); P0 = pr[12]; ct = pr[13]
    be = 1 if form == 2 else 0; texts["plant" + pr[0]] = ct
    hits, _, _ = load("plant" + pr[0])
    mine = [h for h in hits if h[0][:7] == (w, mode, dir_, al, be, model, per) and h[1] == pi]
    ok = False; info = {}
    if mine:
        h = mine[0]; D, cls = decrypt(ct, h[0], h[1]); S = S_of(w, pi, mode, dir_)
        badcls = cls(CRP[seat]) if seat >= 0 else None
        mism = [i for i in range(97) if D[i] != "?" and D[i] != P0[i] and (badcls is None or cls(i) != badcls)]
        d2key = (al, be, model, per, h[2]); d2ok = any((x[0][3], x[0][4], x[0][5], x[0][6], x[2]) == d2key for x in hits)
        ok = len(mism) == 0 and d2ok; info = {"excess": h[0][7], "bad": h[0][8], "mismatch": len(mism), "known": 97 - D.count("?"), "d2_present": d2ok}
    prow.append({"pid": pid, "w": w, "p": per, "model": model, "form": form, "seat": seat, "found": bool(mine), "pass": ok, **info})
R["gateP"] = {"passes": sum(r["pass"] for r in prow), "n": len(prow), "bar": 19, "rows": prow, "PASS": sum(r["pass"] for r in prow) >= 19}
# rank rule
M = len(nulls); R["M"] = M; ranks = {}
for p in PS:
    for s in ("R", "D2", "D3"):
        k = R["per_text"]["K4"][p][s]; nv = [R["per_text"][l][p][s] for l in nulls]
        ge = sum(x >= k for x in nv); le = sum(x <= k for x in nv)
        ranks[f"p{p}_{s}"] = {"K4": k, "null_min": min(nv), "null_median": float(np.median(nv)), "null_p95": float(np.percentile(nv, 95)), "null_max": max(nv),
                              "n_ge": ge, "p_up": round((1 + ge) / (M + 1), 4), "cp95_tail_ge": cp(ge, M), "n_le": le, "p_low": round((1 + le) / (M + 1), 4)}
R["ranks"] = ranks
# structural tables K4 vs nulls (median, p95)
struct = {}
for p in PS:
    for tname in R["per_text"]["K4"][p]["tables"]:
        keys = set()
        for l in ["K4"] + nulls: keys |= set(R["per_text"][l][p]["tables"].get(tname, {}).keys())
        for k in sorted(keys, key=str):
            nv = [R["per_text"][l][p]["tables"].get(tname, {}).get(k, 0) for l in nulls]; kk = R["per_text"]["K4"][p]["tables"].get(tname, {}).get(k, 0)
            struct[f"p{p} {tname} {k}"] = {"K4": kk, "null_median": float(np.median(nv)), "null_p95": float(np.percentile(nv, 95)), "null_max": max(nv),
                                          "p_up": round((1 + sum(x >= kk for x in nv)) / (M + 1), 4)}
R["struct"] = struct
# K4 decrypts (D2 collapsed)
dec = {}
for h in allhits["K4"]:
    key2 = (h[0][3], h[0][4], h[0][5], h[0][6], h[2])
    if key2 in dec: dec[key2]["raw"] += 1; continue
    D, cls = decrypt(texts["K4"], h[0], h[1]); sc, nq = score(D)
    dec[key2] = {"cfg": list(h[0]), "pi": list(h[1]), "known": 97 - D.count("?"), "qg": round(sc, 3), "nq": nq, "pt": D, "raw": 1}
decl = sorted(dec.values(), key=lambda d: -d["qg"])
cands = [d for d in decl if d["known"] >= 49 and d["qg"] >= -6.0]
R["K4_cells_D2"] = decl; R["K4_candidates"] = cands
r21R, r21D = ranks["p21_R"]["p_up"], ranks["p21_D2"]["p_up"]
if cands: lab21 = "CANDIDATE (manual read)"
elif r21R > 0.05: lab21 = "NOT AN EXCESS (168 nulls; the 8-null observation was chance-level)"
elif r21D > 0.05: lab21 = "STRUCTURAL MULTIPLICITY"
else: lab21 = "EXCESS PERSISTS AFTER COLLAPSE -> NO-SIGNAL (crib-consistent excess, gibberish)"
R["labels"] = {"p21": lab21, "p20": "CANDIDATE (manual read)" if any(d["cfg"][6] == 20 for d in cands) else
               f"INSUFFICIENT-DISCRIMINATION (unchanged); no K4 p 20 cell meets the decrypt bar; p_low(R) = {ranks['p20_R']['p_low']}"}
with open(f"{OUT}/summary223.json", "w") as f:
    f.write(json.dumps(R, indent=1))
print("gateT", R["gateT"]["PASS"], {k: v for k, v in gT.items() if k.startswith("K4")})
print("gateP", R["gateP"]["passes"], "/20", [(r["pid"], r) for r in prow if not r["pass"]])
for k, v in ranks.items(): print(k, v)
print("labels", R["labels"])
for d in decl[:12]: print(d["qg"], d["known"], d["raw"], d["cfg"], d["pt"])

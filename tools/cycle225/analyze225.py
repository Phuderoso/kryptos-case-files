"""Cycle 225 analysis (I-312 chunk 2): gates T / R / P, per-p labels for K4 vs eight nulls over w 11 pi[0] in {2,3}.
analyze220.py with: chunk {2,3}, gate S replaced by gate T (byte identity vs cycle 220), D2 rank + null occupancy columns.
usage: analyze225.py W OUT QGBIN REF_RAW"""
import collections, glob, hashlib, json, os, sys
import numpy as np
W, OUT, QG, REF = sys.argv[1:5]
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; PAIRS = [(AZ, AZ), (KA, KA), (AZ, KA), (KA, AZ)]
CRP = list(range(21, 34)) + list(range(63, 74)); CRS = "EASTNORTHEASTBERLINCLOCK"
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle220", "col1e4.c")
qg = np.fromfile(QG, dtype=np.float32)
sha = lambda b: hashlib.sha256(b).hexdigest()
texts = dict(l.rstrip("\n").split("\t") for l in open(f"{W}/texts.tsv"))
plants = [l.rstrip("\n").split("\t") for l in open(f"{W}/plants225.tsv")][1:]
def reading_order(w, pi, mode):
    rows = (97 + w - 1) // w; col_at = sorted(range(w), key=lambda c: pi[c])
    if mode == 1: return [r*w + c for c in col_at for r in range(rows) if r*w + c < 97]
    return [r*w + c for r in range(rows) for c in col_at if r*w + c < 97]
def S_of(w, pi, mode, dir_):
    sig = [0]*97
    for m, cell in enumerate(reading_order(w, pi, mode)): sig[cell] = m
    if dir_ == 0: return sig
    inv = [0]*97
    for i in range(97): inv[sig[i]] = i
    return inv
def load(lab, pmax=18):
    hits, cnt, nperm, files, incomplete = [], collections.defaultdict(lambda: [0, 0]), 0, sorted(glob.glob(f"{W}/out/{lab}/*.raw")), []
    for f in files:
        lines = open(f).read().splitlines()
        if not lines or not lines[-1].startswith("C "): incomplete.append(f); continue
        for line in lines:
            a = line.split()
            if a[0] == "H": hits.append(tuple(int(x) for x in a[2:11]) + (tuple(int(x) for x in a[11:]),))
            elif a[0] == "C":
                nperm += int(a[5])
                for tok in a[6:]:
                    p, v = tok[1:].split("="); s0, s1 = v.split("/"); cnt[int(p)][0] += int(s0); cnt[int(p)][1] += int(s1)
    return hits, dict(cnt), nperm, files, incomplete
def decrypt(ct, h):
    w, mode, dir_, al, be, model, p, e, bad, pi = h
    CA, PA = PAIRS[al]; S = S_of(w, list(pi), mode, dir_)
    cls = lambda i: (i if model == 0 else S[i]) % p
    votes = collections.defaultdict(collections.Counter)
    for t, i in enumerate(CRP):
        c = CA.index(ct[S[i]]); x = PA.index(CRS[t]); votes[cls(i)][(c + x) % 26 if be else (c - x) % 26] += 1
    key = {r: v.most_common(1)[0][0] for r, v in votes.items()}
    P = []
    for i in range(97):
        r = cls(i)
        if r not in key: P.append("?"); continue
        c = CA.index(ct[S[i]]); P.append(PA[(key[r] - c) % 26] if be else PA[(c - key[r]) % 26])
    return "".join(P), key, S, cls
def score(P):
    q = [qg[((ord(P[i])-65)*26 + ord(P[i+1])-65)*676 + (ord(P[i+2])-65)*26 + ord(P[i+3])-65] for i in range(94) if "?" not in P[i:i+4]]
    return (float(np.mean(q)) if q else -9.0), len(q)
R = {"scope": "I-312 chunk 2: col1e4 NAL=4, w11 orders with pi[0] in {2,3} (7,257,600), ROW/COL, dir 0/1, AZ/KA/QuagI/QuagII, Vig(=variant)/Beau, model A/B, p 1-18; one error = excess <= 1",
     "inputs": {}}
os.makedirs(OUT, exist_ok=True)
# gate T
gt = open(f"{W}/out/gateT/w11_f0_s1.raw", "rb").read(); ref = open(REF, "rb").read()
R["gateT"] = {"new_sha256": sha(gt), "ref_sha256": sha(ref), "PASS": gt == ref}
counts = {}; inc = {}
for lab, ct in texts.items():
    hits, cnt, nperm, files, incomplete = load(lab)
    counts[lab] = {"nperm": nperm, "files": len(files), "incomplete": len(incomplete), "strict": [cnt.get(p, [0, 0])[0] for p in range(1, 19)], "one": [cnt.get(p, [0, 0])[1] for p in range(1, 19)]}
    R["inputs"][lab] = {"input_sha256": sha(ct.encode())}
    with open(f"{OUT}/results_{lab.lower()}.txt", "w") as fo:
        fo.write(f"# scope={R['scope']}\n# text={lab} input_sha256={sha(ct.encode())} (97-letter string, no newline)\n# tool=tools/cycle220/col1e4.c tool_sha256={sha(open(TOOL,'rb').read())}\n")
        fo.write(f"# seed={'n/a' if lab == 'K4' else lab[4:]} args=col1e4 CT 11 first(2,3) 18 18 label 4 second(0..10)\n# orders={nperm} files={len(files)} incomplete={len(incomplete)}\n")
        fo.write("# per p strict/one-error: " + " ".join(f"p{p}={counts[lab]['strict'][p-1]}/{counts[lab]['one'][p-1]}" for p in range(1, 19)) + "\n")
        for h in hits: fo.write("H " + " ".join(map(str, h[:9])) + " " + ",".join(map(str, h[9])) + "\n")
R["gateR"] = {"K4_strict_all_zero": all(x == 0 for x in counts["K4"]["strict"]), "K4_orders": counts["K4"]["nperm"], "PASS": all(x == 0 for x in counts["K4"]["strict"])}
prow = []
for p in plants:
    pid, w, mode, dir_, al, form, model, per = map(int, p[:8]); pi = tuple(int(x) for x in p[9].split(",")); seat = int(p[10]); P0 = p[12]; ct = p[13]
    be = 1 if form == 2 else 0
    hits = load("plant" + p[0])[0]
    mine = [h for h in hits if h[:7] == (w, mode, dir_, al, be, model, per) and h[9] == pi]
    ok = False; info = {}
    if mine:
        h = mine[0]; D, key, S, cls = decrypt(ct, h); badcls = cls(CRP[seat]) if seat >= 0 else None
        mism = [i for i in range(97) if D[i] != "?" and D[i] != P0[i] and (badcls is None or cls(i) != badcls)]
        ok = not mism; info = {"excess": h[7], "bad": h[8], "mismatch": len(mism), "known": 97 - D.count("?")}
    prow.append({"pid": pid, "al": al, "p": per, "model": model, "form": form, "seat": seat, "found": bool(mine), "pass": ok, **info})
R["gateP"] = {"passes": sum(r["pass"] for r in prow), "n": len(prow), "bar": 19, "rows": prow}; R["gateP"]["PASS"] = R["gateP"]["passes"] >= 19
nulls = [l for l in texts if l.startswith("null")]
k4ct = texts["K4"]; distinct = {}
for h in load("K4")[0]:
    D, key, S, cls = decrypt(k4ct, h); sig = h[:7] + tuple(S[i] for i in CRP)
    if sig not in distinct:
        sc, nq = score(D); distinct[sig] = {"cfg": list(h[:9]), "pi": list(h[9]), "known": 97 - D.count("?"), "qg": sc, "nq": nq, "pt": D, "raw": 0}
    distinct[sig]["raw"] += 1
def ndist(lab):
    seen = collections.defaultdict(set)
    for h in load(lab)[0]:
        S = S_of(h[0], list(h[9]), h[1], h[2]); seen[h[6]].add(h[:7] + tuple(S[i] for i in CRP))
    return {p: len(v) for p, v in seen.items()}
nd = {lab: ndist(lab) for lab in ["K4"] + nulls}
labels = {}
for p in range(1, 19):
    k = counts["K4"]["strict"][p-1] + counts["K4"]["one"][p-1]; nv = [counts[l]["strict"][p-1] + counts[l]["one"][p-1] for l in nulls]
    row = {"K4": k, "nulls": nv, "K4_distinct": nd["K4"].get(p, 0), "null_distinct": [nd[l].get(p, 0) for l in nulls]}
    if k == 0: lab = "EXACT-EXCL (one-error scope, discriminating)" if sum(1 for x in nv if x == 0) >= 6 else "EXACT-EXCL (one-error scope, exact but saturated-null)"
    else:
        cands = [d for d in distinct.values() if d["cfg"][6] == p and d["known"] >= 49 and d["qg"] >= -6.0]
        lab = "CANDIDATE (manual read)" if cands else "INSUFFICIENT-DISCRIMINATION" if k <= max(nv) else "NO-SIGNAL (excess over 8 nulls, gibberish)"
    kd = row["K4_distinct"]; row["null_occupancy"] = sum(1 for x in nv if x > 0)
    row["D2_rank_p_up"] = (1 + sum(1 for x in row["null_distinct"] if x >= kd)) / (len(nulls) + 1) if k > 0 else None
    row["flag_more_nulls"] = bool(k > 0 and all(kd > x for x in row["null_distinct"]))
    row["label"] = lab; labels[p] = row
R["per_p"] = labels; R["counts"] = counts; R["K4_hits_distinct"] = sorted(distinct.values(), key=lambda d: -d["qg"])
R["complete"] = all(c["incomplete"] == 0 and c["nperm"] == 7257600 for c in counts.values())
with open(f"{OUT}/summary225.json", "w") as f: json.dump(R, f, indent=1)
print("complete", R["complete"], {l: (c["nperm"], c["incomplete"]) for l, c in counts.items()})
print("gateT", R["gateT"]); print("gateR", R["gateR"]); print("gateP", R["gateP"]["passes"], "/20", [(r["pid"], r) for r in prow if not r["pass"]])
for p in range(1, 19): print(p, labels[p])
for d in R["K4_hits_distinct"][:12]: print(round(d["qg"], 2), d["known"], d["raw"], d["cfg"], d["pt"])

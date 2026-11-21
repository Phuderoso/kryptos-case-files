"""Cycle 228 analysis (I-312 chunk 3): gates T / R / P (+ plant NC share), per-p labels for K4 vs eight nulls over w 11 pi[0] in {4,5}.
= analyze225.py with: chunk {4,5}; decrypts read by nc228.py (tie='?', I-330 NC bar); null NC passes counted per DISTINCT TEXT
(identical decrypt strings collapsed across hits / forms / families); Wilson 95 % intervals beside gate P and null occupancy;
family-collapsed (D2 = distinct crib tests) and top-3-family share beside raw counts.
usage: analyze228.py W OUT QGBIN REF_RAW"""
import collections, glob, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc228 as N
W, OUT, QG, REF = sys.argv[1:5]; N.load_qg(QG)
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cycle220", "col1e4.c")
sha = lambda b: hashlib.sha256(b).hexdigest()
texts = dict(l.rstrip("\n").split("\t") for l in open(f"{W}/texts.tsv"))
plants = [l.rstrip("\n").split("\t") for l in open(f"{W}/plants228.tsv")][1:]
SCOPE = "I-312 chunk 3: col1e4 NAL=4, w11 orders with pi[0] in {4,5} (7,257,600), ROW/COL, dir 0/1, AZ/KA/QuagI/QuagII, Vig(=variant)/Beau, model A/B, p 1-18; one error = excess <= 1"
def load(lab):
    hits, cnt, nperm, files, incomplete = [], collections.defaultdict(lambda: [0, 0]), 0, sorted(glob.glob(f"{W}/out/{lab}/*.raw")), []
    for f in files:
        lines = open(f).read().splitlines()
        if not lines or not lines[-1].startswith("C "): incomplete.append(f); continue
        for line in lines:
            a = line.split()
            if a[0] == "H": hits.append(N.parse_H(line))
            elif a[0] == "C":
                nperm += int(a[5])
                for tok in a[6:]:
                    p, v = tok[1:].split("="); s0, s1 = v.split("/"); cnt[int(p)][0] += int(s0); cnt[int(p)][1] += int(s1)
    return hits, dict(cnt), nperm, files, incomplete
R = {"scope": SCOPE, "inputs": {}, "qg_sha256": sha(open(QG, "rb").read()), "tool_sha256": sha(open(TOOL, "rb").read())}
os.makedirs(OUT, exist_ok=True)
gt = open(f"{W}/out/gateT/w11_f0_s1.raw", "rb").read(); ref = open(REF, "rb").read()
R["gateT"] = {"new_sha256": sha(gt), "ref_sha256": sha(ref), "PASS": gt == ref}
counts, H = {}, {}
for lab, ct in texts.items():
    hits, cnt, nperm, files, incomplete = load(lab); H[lab] = hits
    counts[lab] = {"nperm": nperm, "files": len(files), "incomplete": len(incomplete), "strict": [cnt.get(p, [0, 0])[0] for p in range(1, 19)], "one": [cnt.get(p, [0, 0])[1] for p in range(1, 19)]}
    R["inputs"][lab] = {"input_sha256": sha(ct.encode())}
    with open(f"{OUT}/results_{lab.lower()}.txt", "w") as fo:
        fo.write(f"# scope={SCOPE}\n# text={lab} input_sha256={sha(ct.encode())} (97-letter string, no newline)\n# tool=tools/cycle220/col1e4.c tool_sha256={R['tool_sha256']}\n")
        fo.write(f"# seed={'n/a' if lab == 'K4' else lab[4:]} args=col1e4 CT 11 first(4,5) 18 18 label 4 second(0..10)\n# orders={nperm} files={len(files)} incomplete={len(incomplete)}\n")
        fo.write("# per p strict/one-error: " + " ".join(f"p{p}={counts[lab]['strict'][p-1]}/{counts[lab]['one'][p-1]}" for p in range(1, 19)) + "\n")
        fo.write("# hit line: H w mode dir al be model p excess bad pi(comma)\n")
        for h in hits: fo.write("H " + " ".join(map(str, h[:9])) + " " + ",".join(map(str, h[9])) + "\n")
R["gateR"] = {"K4_strict_all_zero": all(x == 0 for x in counts["K4"]["strict"]), "K4_orders": counts["K4"]["nperm"]}; R["gateR"]["PASS"] = R["gateR"]["K4_strict_all_zero"]
prow = []
for p in plants:
    pid, w, mode, dir_, al, form, model, per = map(int, p[:8]); pi = tuple(int(x) for x in p[9].split(",")); seat = int(p[10]); P0 = p[12]; ct = p[13]
    be = 1 if form == 2 else 0
    hits = load("plant" + p[0])[0]
    mine = [h for h in hits if h[:7] == (w, mode, dir_, al, be, model, per) and h[9] == pi]
    ok = False; info = {}
    if mine:
        h = mine[0]; D, key, S, cls = N.decrypt(ct, h, tie="first"); badcls = cls(N.CRP[seat]) if seat >= 0 else None
        mism = [i for i in range(97) if D[i] != "?" and D[i] != P0[i] and (badcls is None or cls(i) != badcls)]
        ok = not mism; rd = N.read(ct, h)
        info = {"excess": h[7], "bad": h[8], "mismatch": len(mism), "known_tieq": rd["known"], "nq": rd["nq"], "nc": rd["nc"], "barred": rd["barred"], "nc_pass": rd["pass"]}
    prow.append({"pid": pid, "al": al, "p": per, "model": model, "form": form, "seat": seat, "found": bool(mine), "pass": ok, **info})
gp = sum(r["pass"] for r in prow); nb = [r for r in prow if r.get("barred")]; nbp = sum(r["nc_pass"] for r in nb)
R["gateP"] = {"passes": gp, "n": len(prow), "bar": 19, "wilson95": N.wilson(gp, len(prow)), "PASS": gp >= 19,
              "nc_barred": len(nb), "nc_pass": nbp, "nc_wilson95": N.wilson(nbp, len(nb)), "nc_target": 0.9, "rows": prow}
nulls = [l for l in texts if l.startswith("null")]
def cells(lab):
    """per p: raw cells, D2 groups (sizes), decrypt reads per D2 group (first hit), NC-pass distinct texts"""
    ct = texts[lab]; out = collections.defaultdict(lambda: {"raw": 0, "d2": collections.Counter(), "reads": {}})
    for h in H[lab]:
        c = out[h[6]]; c["raw"] += 1; s = N.d2sig(h); c["d2"][s] += 1
        if s not in c["reads"]: c["reads"][s] = (h, N.read(ct, h))
    res = {}
    for p, c in out.items():
        rd = [r for _, r in c["reads"].values()]; barred = [r for r in rd if r["barred"]]
        passtexts = sorted({r["pt"] for r in rd if r["pass"]}); top3 = sum(n for _, n in c["d2"].most_common(3))
        res[p] = {"raw": c["raw"], "D2": len(c["d2"]), "top3_share": top3 / c["raw"], "barred": len(barred),
                  "nc_max": max((r["nc"] for r in barred), default=None), "nc_pass_texts": len(passtexts), "pass_pts": passtexts,
                  "best": max(((r["nc"], r["pt"], list(h[:9]), list(h[9]), r["known"]) for h, r in c["reads"].values() if r["barred"]), default=None)}
    return res
C = {lab: cells(lab) for lab in ["K4"] + nulls}
labels = {}
for p in range(1, 19):
    k = counts["K4"]["strict"][p-1] + counts["K4"]["one"][p-1]; nv = [counts[l]["strict"][p-1] + counts[l]["one"][p-1] for l in nulls]
    kc = C["K4"].get(p, {}); nd = [C[l].get(p, {}).get("D2", 0) for l in nulls]; occ = sum(1 for x in nv if x > 0)
    row = {"K4": k, "K4_D2": kc.get("D2", 0), "K4_top3_share": kc.get("top3_share"), "nulls": nv, "null_D2": nd,
           "null_occupancy": occ, "occ_wilson95": N.wilson(occ, len(nulls)),
           "K4_barred": kc.get("barred", 0), "K4_nc_pass_texts": kc.get("nc_pass_texts", 0), "K4_nc_max": kc.get("nc_max"),
           "null_nc_pass_texts": [C[l].get(p, {}).get("nc_pass_texts", 0) for l in nulls],
           "null_nc_max": max((C[l][p]["nc_max"] for l in nulls if p in C[l] and C[l][p]["nc_max"] is not None), default=None)}
    if k == 0: lab = "EXACT-EXCL (one-error scope, discriminating)" if occ <= 2 else "EXACT-EXCL (one-error scope, exact but saturated-null)"
    else:
        if row["K4_nc_pass_texts"] > 0: lab = "CANDIDATE (manual read)"
        elif k <= max(nv): lab = "INSUFFICIENT-DISCRIMINATION"
        else: lab = "NO-SIGNAL (K4 cells over every null count, decrypts below the NC bar)"
    row["D2_rank_p_up"] = (1 + sum(1 for x in nd if x >= row["K4_D2"])) / (len(nulls) + 1) if k > 0 else None
    row["label"] = lab; labels[p] = row
R["per_p"] = labels; R["counts"] = counts
R["K4_cells"] = {p: {kk: vv for kk, vv in c.items()} for p, c in C["K4"].items()}
R["null_nc_pass_texts_total"] = {l: sum(c["nc_pass_texts"] for c in C[l].values()) for l in nulls}
R["null_nc_pass_pts"] = {l: [t for c in C[l].values() for t in c["pass_pts"]] for l in nulls}
R["complete"] = all(c["incomplete"] == 0 and c["nperm"] == 7257600 for c in counts.values())
with open(f"{OUT}/summary228.json", "w") as f: json.dump(R, f, indent=1, default=str)
print("complete", R["complete"], {l: (c["nperm"], c["incomplete"]) for l, c in counts.items()})
print("gateT", R["gateT"]); print("gateR", R["gateR"])
print("gateP", gp, "/20 wilson", [round(x, 3) for x in R["gateP"]["wilson95"]], "NC", nbp, "/", len(nb), [round(x, 3) for x in R["gateP"]["nc_wilson95"]], [r for r in prow if not r["pass"] or (r.get("barred") and not r["nc_pass"])])
for p in range(1, 19): print(p, {k: v for k, v in labels[p].items()})
print("null NC pass texts", R["null_nc_pass_texts_total"])
for p, c in sorted(C["K4"].items()): print("K4 p", p, "best", c["best"])

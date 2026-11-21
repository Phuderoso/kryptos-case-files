"""Cycle 228 I-331 re-read: every published crib-consistent cell of cases 205 (data/cycle219, col1e w 9-10), 206 (data/cycle220)
and 211 (data/cycle225) (col1e4 w 11), K4 and every published null, decrypted with nc228.py (tie='?', I-330 NC bar).
Input = the published hit lines only (no rerun). Input delta printed per text: H lines read vs the stamped per-p counts.
Unit = D2 cell (distinct crib test, case 209 rule); null NC passes counted per distinct decrypt text.
usage: reread228.py REPO QGBIN OUTJSON"""
import collections, glob, hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc228 as N
REPO, QG, OUTJ = sys.argv[1:4]; N.load_qg(QG)
CASES = [("205", "cycle219", True), ("206", "cycle220", False), ("211", "cycle225", False)]
out = {"qg_sha256": hashlib.sha256(open(QG, "rb").read()).hexdigest(), "cases": {}}
for case, cyc, lab_in_H in CASES:
    d = f"{REPO}/data/{cyc}"; texts = dict(l.rstrip("\n").split("\t") for l in open(f"{d}/texts.tsv"))
    files = {"K4": f"{d}/K4.txt" if case == "205" else f"{d}/results_k4.txt"}
    for lab in texts:
        if lab != "K4": files[lab] = f"{d}/{lab}.txt" if case == "205" else f"{d}/results_{lab}.txt"
    oc = {}
    for lab, fn in files.items():
        ct = texts[lab]; lines = open(fn).read().splitlines()
        stamp = [l for l in lines if l.startswith("# per p")][0]
        pub = {int(m.group(1)): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r"p(\d+)=(\d+)/(\d+)", stamp)}
        hits = []
        for l in lines:
            if l.startswith("H "):
                if lab_in_H: hits.append(N.parse_H(l, True))
                else:
                    a = l.split(); hits.append(tuple(int(x) for x in a[1:10]) + (tuple(int(x) for x in a[10].split(",")),))
        byp = collections.defaultdict(list)
        for h in hits: byp[h[6]].append(h)
        delta = {p: {"H_lines": len(byp.get(p, [])), "published_strict_plus_one": pub[p][0] + pub[p][1], "published_strict": pub[p][0]} for p in sorted(pub) if pub[p][0] + pub[p][1] or byp.get(p)}
        cells = {}
        for p, hs in sorted(byp.items()):
            grp = {}
            for h in hs:
                s = N.d2sig(h)
                if s not in grp: grp[s] = (h, N.read(ct, h), N.read(ct, h, tie="first"))
            rd = [r for _, r, _ in grp.values()]; barred = [r for r in rd if r["barred"]]
            pt = sorted({r["pt"] for r in rd if r["pass"]})
            best = max(((r["nc"], r["pt"], r["known"], r["nq"], list(h[:9]), list(h[9])) for h, r, _ in grp.values() if r["barred"]), default=None)
            cells[p] = {"raw": len(hs), "D2": len(grp), "barred": len(barred), "unreachable_known_lt49_or_nq_lt10": len(rd) - len(barred),
                        "nc_max": max((r["nc"] for r in barred), default=None), "nc_pass_texts": len(pt), "pass_pts": pt,
                        "nc_max_tiefirst": max((r2["nc"] for _, _, r2 in grp.values() if r2["barred"]), default=None),
                        "best": best}
        oc[lab] = {"input_sha256": hashlib.sha256(ct.encode()).hexdigest(), "delta": delta, "cells": cells}
    out["cases"][case] = oc
json.dump(out, open(OUTJ, "w"), indent=1, default=str)
for case, oc in out["cases"].items():
    print("== case", case)
    for lab, o in oc.items():
        dl = {p: (v["H_lines"], v["published_strict_plus_one"]) for p, v in o["delta"].items()}
        cs = {p: (c["raw"], c["D2"], c["barred"], None if c["nc_max"] is None else round(c["nc_max"], 3), c["nc_pass_texts"]) for p, c in o["cells"].items()}
        print(lab, "delta(H,pub)", dl, "| cells p:(raw,D2,barred,NCmax,passTexts)", cs)
    k = oc["K4"]["cells"]
    for p, c in k.items(): print("  K4 best p", p, c["best"][:4] if c["best"] else None)

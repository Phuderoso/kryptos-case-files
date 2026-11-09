"""Cycle 175: run slip175 / hill175 on every planted slice and check each plant.
Slip plants: found at slot t=100 with the planted d, dropped crib, PA, CA, mode, frame and p, crib-fixed key letters = planted key
('strict': any dropped crib; 'neg' (two changed crib letters): must be MISSED). Replay of cycle 173's ctl10: found with crib 5 dropped.
Hill plants: a K line at q=100 in the planted sub-cell (n 4, aff, numbering, ix, offset) whose decode equals the plaintext at
every non-'?' position; the Hill 'neg' plant must give no K line there.
usage: checkctl175.py ctl_dir run_dir"""
import sys, subprocess, re, json
D, RUN = sys.argv[1], sys.argv[2]; ok = tot = 0; L = []
def slip(slice_, n, model, ct):
    return subprocess.run([f"{RUN}/slip175", slice_, str(n), model, ct, "26", "26", "4", "0", "200"], capture_output=True, text=True).stdout
def hits(out):
    for h in out.splitlines():
        m = re.match(r"HIT t=(\d+) d=(\d+) drop=(\d+) PA=(\w+) CA=(\w+) mode=(\w+) idx=(\w+) p=(\d+) info=(\d) key=(\S+)", h)
        if m: g = m.groups(); yield (int(g[0]), int(g[1]), int(g[2]), g[3], g[4], g[5], g[6], int(g[7]), int(g[8]), g[9])
for r in json.load(open(f"{D}/plants.json")):
    nm = r["name"]; ct = open(f"{D}/{nm}.txt").read().strip(); tot += 1
    if r["kind"] == "slip":
        model = "insx" if r["model"] == "insx" else "delx"; out = slip(f"{D}/{nm}_slice.bin", r["n"], model, ct)
        open(f"{D}/{nm}_out.txt", "w").write(out)
        F = [h for h in hits(out) if h[:2] == (100, r["d"]) and h[3:8] == (r["PA"], r["CA"], r["mode"], r["idx"], r["p"])
             and all(a in "?" + b for a, b in zip(h[9], r["key"]))]
        if r["model"] in ("delx", "insx"): F = [h for h in F if h[2] == r["drop"][0]]
        found = bool(F); good = (not found) if r["model"] == "neg" else found
        nh = sum(1 for h in hits(out) if h[7] == r["p"])
        L.append(f"{nm} {r['model']} p={r['p']} drop={r['drop']} {'FOUND key=' + F[0][9] + ' info=' + str(F[0][8]) + ' (' + str(len(F)) + ' matching drops)' if found else 'MISSED'}"
                 f"{' (expected miss)' if r['model'] == 'neg' else ''} hits_at_p_in_slice={nh} -> {'PASS' if good else 'FAIL'}")
    else:
        out = subprocess.run([f"{RUN}/hill175", ct, f"{D}/{nm}_slice.bin", nm, "0", "200", "4", "4", "4"], capture_output=True, text=True).stdout
        open(f"{D}/{nm}_out.txt", "w").write(out)
        K = [w for w in (l.split() for l in out.splitlines()) if w[0] == "K" and int(w[2]) == 100 and w[3:8] == ["4", str(r["aff"]), r["num"], str(r["ix"]), str(r["off"])]]
        dec = [w for w in K if all(a == "?" or a == b for a, b in zip(w[10], r["pt"]))]
        found = bool(dec); good = (not K) if r["neg"] else found
        ks = sum(1 for l in out.splitlines() if l.startswith("K "))
        L.append(f"{nm} hill n4 aff={r['aff']} {r['num']} ix={r['ix']} off={r['off']}{' NEG' if r['neg'] else ''}: "
                 f"{'FOUND, decode = plaintext (' + str(dec[0][10].count('?')) + ' ? letters), ninv=' + dec[0][8] + ', checks=' + dec[0][9] if found else ('MISSED' if not K else 'K line but decode differs')}"
                 f"{' (expected miss)' if r['neg'] else ''}; K lines in slice {ks} -> {'PASS' if good else 'FAIL'}")
    ok += good
# replay of cycle 173 ctl10 (del + one changed crib letter at plaintext 26 = crib index 5)
R = f"{D}/replay173"; ct = open(f"{R}/ctl10.txt").read().strip(); out = slip(f"{R}/ctl10_slice.bin", 98, "delx", ct); tot += 1
F = [h for h in hits(out) if h[:3] == (100, 65, 5) and h[3:8] == ("KA", "KA", "vig", "pt", 7) and all(a in "?" + b for a, b in zip(h[9], "COMPASS"))]
ok += bool(F); L.append(f"replay173_ctl10 delx p=7 drop=5 {'FOUND key=' + F[0][9] if F else 'MISSED'} -> {'PASS' if F else 'FAIL'}")
print("\n".join(L)); print(f"CONTROLS {ok}/{tot} PASS")

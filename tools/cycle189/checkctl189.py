"""Check cycle 189 controls. Positive: an M line at the planted perm (index q; 0 for direct), planted alphabet, reduced form
(odd number of Beaufort layers -> beau, else vig), planted model, planted (m, n). Negatives N1-N3: no M line at the planted perm with
excess >= 5 (cells with full power); fits at lower excess are listed (expected by chance, LOW-POWER cells)."""
import sys
ok = 0; tot = 0
form = {"P1": "vig", "P2": "vig", "P3": "vig", "P4": "beau", "P5": "vig", "P6": "beau", "P7": "vig"}
for l in open(sys.argv[1]):
    name, q, alab, model, per, ct = l.split(); q = int(q); ms = sorted(int(x) for x in per.split("/"))
    M = [x.split() for x in open(f"{sys.argv[2]}/{name}.txt") if x.startswith("M")]
    ended = any(x.startswith("END") for x in open(f"{sys.argv[2]}/{name}.txt"))
    qq = 0 if q < 0 else q
    at = [x for x in M if int(x[2]) == qq]
    if name.startswith("P"):
        hit = [x for x in at if x[3] == alab and x[4] == form[name] and x[5] == model and int(x[6]) == ms[0] and int(x[7]) == ms[1]]
        good = ended and len(hit) > 0; tot += 1; ok += good
        print(name, "PASS" if good else "FAIL", "hits", hit[:1], "fits at q", len(at), "fits in window", len(M))
    else:
        bad = [x for x in at if int(x[8]) >= 5]; good = ended and not bad; tot += 1; ok += good
        print(name, "PASS" if good else "FAIL", "full-power fits at q", len(bad), "low-power fits at q", len(at), "window", len(M), bad[:2])
print(f"controls {ok}/{tot}")

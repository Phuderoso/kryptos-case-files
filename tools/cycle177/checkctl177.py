"""Cycle 177: check the planted controls. Positive one-error plants must appear at the planted perm / primer (or config) / PA /
form (variant as Beaufort) with a drop mask that is NOT full (the strict test misses them) and contains the planted error slot
(PG: miss slot = planted slot). Strict plants (no error slots) must appear with a full mask (PG: miss -1). Negatives (two errors)
must NOT appear at their planted config.   usage: checkctl177.py controls177.txt ctldir"""
import sys
ok = n = 0
for l in open(sys.argv[1]):
    nm, ct, model, ix, L, pa, form, b, q, key, slots = l.split(); n += 1
    sl = [] if slots == "-" else [int(x) for x in slots.split(",")]
    want_form = "beau" if form == "var" else form
    hits = [h.split() for h in open(f"{sys.argv[2]}/{nm}.txt") if h.startswith("M ")]
    if model == "G":
        at = [h for h in hits if h[2] == ix and h[4] == pa and h[5] == want_form and h[6] == b and h[7] == q and h[8] == key]
        masks = [int(h[9], 16) for h in at]
        if not sl: found = any(m == 0xFFFFFF for m in masks); how = "full mask" if found else f"masks {[hex(m) for m in masks]}"
        else: found = any(m != 0xFFFFFF and (m >> sl[0]) & 1 for m in masks); how = f"masks {[format(m,'06x') for m in masks]}"
    else:
        at = [h for h in hits if h[2] == ix and h[3] == want_form and h[4] == q and h[5] == key]
        miss = [int(h[6]) for h in at]
        found = (-1 in miss) if not sl else (sl[0] in miss); how = f"miss {miss}"
    if nm.startswith("neg"): found = len(at) > 0; how = f"{len(at)} lines at planted config"
    good = (not found) if nm.startswith("neg") else found
    ok += good
    print(nm, model, f"ix{ix}", f"L{L}", pa, form, f"b{b}", f"q{q}", key, f"err-slots {slots}", "fits_in_run", len(hits), how, "PASS" if good else "FAIL")
print(f"controls {ok}/{n}")

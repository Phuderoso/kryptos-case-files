"""Cycle 176: check the planted controls: each positive plant must appear among its run's fits at the planted perm, primer/config,
PA and form (variant plants appear as Beaufort); the negative must NOT appear at its perm and primer.
usage: checkctl176.py controls176.txt ctldir"""
import sys
ok = 0; n = 0
for l in open(sys.argv[1]):
    nm, ct, model, ix, L, pa, form, q, key = l.split(); n += 1
    want_form = "beau" if form == "var" else form
    hits = [h.split() for h in open(f"{sys.argv[2]}/{nm}.txt") if h.startswith("M ")]
    if model == "G": found = any(h[2] == ix and h[4] == pa and h[5] == want_form and h[6] == q and h[7] == key for h in hits)
    else: found = any(h[2] == ix and h[3] == want_form and h[4] == q and h[5] == key for h in hits)
    good = (not found) if nm.startswith("neg") else found
    ok += good; print(nm, model, f"ix{ix}", f"L{L}", pa, form, f"q{q}", key, "fits_in_run", len(hits), "planted_found" if found else "planted_not_found", "PASS" if good else "FAIL")
print(f"controls {ok}/{n}")

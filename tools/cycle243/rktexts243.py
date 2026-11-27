"""Cycle 243 (PREREG243, I-402): running-key texts for the 27-cell groups.
Carved texts = cycle 34's 12 texts (tools/carved_texts.py -> carved.txt, forward and reversed);
books = cycle 35's sources: Carter & Mace vol. I (Internet Archive tomboftutankhame00cart_1 djvu OCR) and
G. Elliot Smith (Project Gutenberg #59783, pglaf mirror), cleaned exactly as tools/bookrk_texts.py, forward and reversed.
Writes texts243.txt: 'name TEXT' lines (28 texts)."""
import re
def clean(s):
    s = re.sub(r"[¬\-]\s*\n\s*", "", s)
    return re.sub("[^A-Z]", "", s.upper())
c = clean(open("carter1.txt", encoding="utf-8", errors="ignore").read())
g = open("smith59783.txt", encoding="utf-8", errors="ignore").read()
g = g[g.find("*** START"):g.find("*** END")]; g = g[g.find("\n"):]
s = clean(g)
out = [l.split() for l in open("carved.txt") if l.strip()]
for n, t in (("carter1", c), ("smith", s)):
    out.append([n, t]); out.append([n + "_rev", t[::-1]])
with open("texts243.txt", "w") as f:
    for n, t in out: f.write(f"{n} {t}\n")
for n, t in out: print(n, len(t))
print("K3 passage in carter1 at", c.find("SLOWLYDESPERATELYSLOWLY"))

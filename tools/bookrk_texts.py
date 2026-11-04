"""Cycle 35: K3's own source as a running key. Carter & Mace, The Tomb of Tut.ankh.Amen vol. I (1923,
Internet Archive OCR 'tomboftutankhame00cart_1', MIT copy) and G. Elliot Smith, Tutankhamen and the
Discovery of His Tomb (1923, Project Gutenberg #59783). Letters only, hyphen breaks joined, forward and reversed."""
import re
def clean(s):
    s = re.sub(r"[¬\-]\s*\n\s*", "", s)           # rejoin words split across lines
    return re.sub("[^A-Z]", "", s.upper())
c = clean(open("carter1.txt", encoding="utf-8", errors="ignore").read())
g = open("smith59783.txt", encoding="utf-8", errors="ignore").read()
g = g[g.find("*** START"):g.find("*** END")]; g = g[g.find("\n"):]
s = clean(g)
texts = {"carter1": c, "smith": s}
with open("texts.txt", "w") as f:
    for n, t in texts.items():
        f.write(f"{n} {t}\n"); f.write(f"{n}_rev {t[::-1]}\n")
for n, t in texts.items(): print(n, len(t))
i = c.find("SLOWLYDESPERATELYSLOWLY"); print("K3 source found at", i, c[i:i+120])

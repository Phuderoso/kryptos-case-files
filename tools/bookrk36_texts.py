"""Cycle 36 key texts. (1) cycle 34's carved texts (K1-K3 pt/ct, K0 Morse, KA tableau), now under all 29 substitutions;
(2) plain-sight texts: KJV Gospel of John (CIA lobby motto, John 8:32; Gutenberg #10), KJV New Testament,
Reagan's Brandenburg Gate speech 1987 (reaganlibrary.gov), National Security Act of 1947 as amended (govinfo COMPS-1493 USLM).
Letters only; forward and reversed."""
import re, html
def clean(s): return re.sub("[^A-Z]", "", s.upper())
out = {}
for l in open("../k4c34/texts.txt"):
    n, t = l.split(); out["c34_" + n] = t
kjv = open("src/kjv.txt", encoding="utf-8").read()
nt0 = kjv.find("The Gospel According to Saint Matthew", kjv.find("The Gospel According to Saint Matthew") + 10)
j0 = kjv.find("The Gospel According to Saint John", kjv.find("The Gospel According to Saint John") + 10)
j1 = kjv.find("The Acts of the Apostles", j0)
end = kjv.find("*** END")
john = clean(re.sub(r"\d+:\d+", " ", kjv[j0:j1])); nt = clean(re.sub(r"\d+:\d+", " ", kjv[nt0:end]))
assert "YESHALLKNOWTHETRUTHANDTHETRUTHSHALLMAKEYOUFREE" in john
out["kjv_john"] = john; out["kjv_nt"] = nt
r = re.sub("<[^>]+>", " ", open("src/reagan.html").read()); r = html.unescape(r)
i = r.find("Thank you very much. Chancellor Kohl"); k = r.find("God bless you all", i)
out["reagan_berlin"] = clean(r[i:k + 20])
x = open("src/nsa47.html").read(); x = re.sub(r"<(note|notes|sourceCredit|toc)[^>]*>.*?</\1>", " ", x, flags=re.S)
out["natsec_act_1947_amended"] = clean(html.unescape(re.sub("<[^>]+>", " ", x)))
with open("texts.txt", "w") as f:
    for n, t in out.items():
        if n.startswith("c34_"): f.write(f"{n} {t}\n"); continue
        f.write(f"{n} {t}\n"); f.write(f"{n}_rev {t[::-1]}\n")
for n, t in out.items(): print(n, len(t), t[:40])

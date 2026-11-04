"""Cycle 4: city-name alphabets and running keys from the Berlin Weltzeituhr (Urania World Clock).
City list = CURRENT (post-1997) rotunda, as transcribed column-by-column on hu.wikipedia 'Urania vilagora' (148 entries).
The pre-1997 80-city list could not be reconstructed (see journal); the 1997 additions confirmed by press
(Oslo, Jerusalem, Kapstadt, Tel Aviv, Managua) and renames (Leningrad, Alma Ata, Mexico City, Bratislava) are
also tested in an 'ORIGINAL-APPROX' variant (current minus confirmed additions, with old names restored).
Tests (no transposition, direct cribs): (1) each city as keyword-mixed alphabet, Quagmire I/II/III with periods 1-26 ->
crib consistency; (2) city sequence concatenated as running key, every offset, Vigenere/Beaufort, AZ/KA."""
import sys, unicodedata, re
sys.path.insert(0, "tools"); import kryptos_text
K4 = kryptos_text.K4; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = kryptos_text.KA
KN = {p - 1 + i: ch for p, w in {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}.items() for i, ch in enumerate(w)}
COLS = """Amsterdam, Berlin, Brüssel, Budapest, Madrid, Paris, Prag, Stockholm, Warschau, Oslo, Kopenhagen, Wien, Bern, Pressburg, Belgrad, Rom, Tunis, Kinshasa
Helsinki, Riga, Tallinn, Wilna, Minsk, Kiew, Bukarest, Sofia, Nikosia, Ankara, Istanbul, Athen, Tel Aviv, Jerusalem, Beirut, Damaskus, Kairo, Kapstadt
Murmansk, St. Petersburg, Moskau, Teheran, Bagdad, Aden, Sanaa, Addis Abeba, Mogadischu, Daressalam, Antananarivo, Kuwait
Nischnij Nowgorod, Wolgograd, Baku, Tiflis, Eriwan, Kabul, Mauritius
Jekaterinburg, Aschgabat, Bischkek, Duschanbe, New Delhi, Karachi, Colombo
Omsk, Almaty, Taschkent, Nowosibirsk, Rangun, Dhaka
Krasnojarsk, Hanoi, Bangkok, Phnom Penh, Jakarta
Irkutsk, Ulan-Bator, Peking, Shanghai, Manila, Perth, Hongkong, Kuala Lumpur, Singapur
Jakutsk, Pjöngjang, Tokyo, Seoul, Chabarowsk, Wladiwostok, Sydney, Canberra, Melbourne
Magadan, Sachalin
Kamtschatka, Wellington
Datumsgrenze
Kap Deschnew, Apia
Honolulu, Marquesas In.
Nome, Fairbanks, Anchorage
Vancouver, Dawson, San Francisco, Los Angeles
Edmonton, Denver
New Orleans, Mexiko-Stadt, Guatemala-Stadt, Managua, Galápagos In.
Montreal, Washington, New York, Havanna, Panama, Santafé de Bogotá, Quito, Lima
Halifax, Caracas, La Paz, Asunción, Santiago de Chile
Westgrönland, Brasilia, Rio de Janeiro, São Paulo, Montevideo, Buenos Aires
Ostgrönland
Azoren, Kap Verde
Reykjavik, Dublin, London, Lissabon, Madeira, Bissau, Casablanca, Conakry, Dakar, Bamako, Accra"""
def norm(s):
    s = s.replace("ü","UE").replace("ö","OE").replace("ä","AE").replace("Ü","UE").replace("Ö","OE")
    s = unicodedata.normalize("NFKD", s); return re.sub("[^A-Z]", "", s.upper())
CUR = [c.strip() for line in COLS.splitlines() for c in line.split(",") if c.strip()]
ADDED = {"Oslo", "Jerusalem", "Kapstadt", "Tel Aviv", "Managua"}
RENAME = {"St. Petersburg": "Leningrad", "Almaty": "Alma Ata", "Mexiko-Stadt": "Mexico City", "Pressburg": "Bratislava"}
ORIG = [RENAME.get(c, c) for c in CUR if c not in ADDED]
def mixed(kw):
    out = ""
    for ch in norm(kw) + AZ:
        if ch not in out: out += ch
    return out
def consistent(pt_alpha, ct_alpha, P, mode):
    keys = {}
    for i, p in KN.items():
        c = K4[i]
        v = (ct_alpha.index(c) - pt_alpha.index(p)) % 26 if mode == "vig" else (ct_alpha.index(c) + pt_alpha.index(p)) % 26
        if keys.setdefault(i % P, v) != v: return False
    return True
def ncons(P):  # number of redundant constraints (pairs of crib positions sharing a key residue)
    from collections import Counter
    return sum(v - 1 for v in Counter(i % P for i in KN).values())
def main():
    print(f"cities current: {len(CUR)}; original-approx: {len(ORIG)}")
    names = sorted(set(CUR) | set(ORIG)); hits = []; tests = 0
    for c in names:
        M = mixed(c)
        for qname, pa, ca in (("Q1", M, AZ), ("Q2", AZ, M), ("Q3", M, M), ("Q3KA-pt", KA, M), ("Q3KA-ct", M, KA)):
            for P in range(1, 27):
                for mode in ("vig", "beau"):
                    tests += 1
                    if consistent(pa, ca, P, mode): hits.append((c, qname, P, mode))
    strong = [h for h in hits if ncons(h[2]) >= 6]
    print(f"(1) keyword-alphabet tests: {tests}; consistent: {len(hits)} (all at P with <6 redundant constraints: "
          f"{sorted(set(h[2] for h in hits))}, ncons={sorted(set(ncons(h[2]) for h in hits))}); with >=6 constraints: {len(strong)}")
    for h in strong: print("   SURVIVOR", h)
    for label, L in (("current", CUR), ("original-approx", ORIG)):
        for order in ("forward", "reverse"):
            seq = [norm(c) for c in (L if order == "forward" else L[::-1])]
            for joined in ("names",):
                rk = "".join(seq)
                best = 0
                for off in range(len(rk) - 97):
                    for alpha in (AZ, KA):
                        for mode in ("vig", "beau", "varbeau"):
                            m = 0
                            for i, p in KN.items():
                                k = alpha.index(rk[off + i]); c = alpha.index(K4[i]); q = alpha.index(p)
                                e = (q + k) % 26 if mode == "vig" else (k - q) % 26 if mode == "beau" else (q - k) % 26
                                m += (e == c)
                            best = max(best, m)
                print(f"(2) running key {label}/{order}: length {len(rk)}, best crib matches {best}/24")
main()

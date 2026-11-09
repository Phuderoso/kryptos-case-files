"""Cycle 172 (IDEAS I-095): alphabet list for Quagmire IV behind decimations/routes.
Each vocabulary word (data/cycle158/vocabulary_all.txt, 10,056 words) keyed two ways:
  Z  = word letters, then the rest of A-Z (K1/K2 construction)
  K  = word letters, then the rest in KRYPTOS-alphabet order (KRYPTOSABCDEFGHIJLMNQUVWXZ)
plus plain A-Z and the KRYPTOS alphabet. Duplicates dropped (first label kept).
Output: one line per unique alphabet: ALPHABET label"""
import sys
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
def keyed(w,base):
    s=""
    for c in w+base:
        if c in AZ and c not in s: s+=c
    return s
words=open(sys.argv[1]).read().split()
seen={}
seen.setdefault(AZ,"AZ"); seen.setdefault(KA,"KA")
for w in words: seen.setdefault(keyed(w,AZ),w+"/Z")
for w in words: seen.setdefault(keyed(w,KA),w+"/K")
for a,l in seen.items(): assert sorted(a)==list(AZ); print(a,l)

"""Cycle 159 quick planted controls for the reused cycle-155 solver (model P, digit primers, L 8):
random cipher alphabet v, free group offsets o_g (g = (i//L) % L), digits by chain addition from an 8-digit primer.
Equation (as gromark1e.c): v(ct_i) - o_g = pa(p_i) + d_i (vig) or d_i - pa(p_i) (beau).
Plaintext = random letters with both cribs at 21-33 / 63-73.  Output: name CT pa form primer note"""
import random,sys
AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA="KRYPTOSABCDEFGHIJLMNQUVWXZ"
POS=list(range(21,34))+list(range(63,74))
def gs(pr,n=97):
    d=list(pr); L=len(d)
    while len(d)<n: d.append((d[-L]+d[-L+1])%10)
    return d
def plant(rng,L,PA,form,err=None):
    p=[rng.choice(AZ) for _ in range(97)]
    for i,c in zip(range(21,34),"EASTNORTHEAST"): p[i]=c
    for i,c in zip(range(63,74),"BERLINCLOCK"): p[i]=c
    pr=[rng.randrange(10) for _ in range(L)]; d=gs(pr); v=list(range(26)); rng.shuffle(v); vinv={x:AZ[i] for i,x in enumerate(v)}
    o=[rng.randrange(26) for _ in range(L)]
    pt=p[:]
    if err=='crib':                      # true plaintext differs from the crib at one position
        pos=rng.choice(POS); pt[pos]=rng.choice([c for c in AZ if c!=p[pos]])
    ct=[vinv[(((PA.index(pt[i])+d[i]) if form==0 else (d[i]-PA.index(pt[i])))+o[(i//L)%L])%26] for i in range(97)]
    note='clean'
    if err=='carved':
        pos=rng.choice(POS); ct[pos]=rng.choice([c for c in AZ if c!=ct[pos]]); note=f'carved-error@{pos}'
    elif err=='crib': note=f'wrong-crib-letter@{pos}'
    return ''.join(ct),''.join(map(str,pr)),note
rng=random.Random(15901)
for name,PA,form,err in (("p1",AZ,0,'carved'),("p2",KA,1,'crib'),("p3",AZ,1,None),("p4",KA,0,'carved')):
    ct,pr,note=plant(rng,8,PA,form,err); print(name,ct,'az' if PA==AZ else 'ka','vig' if form==0 else 'beau',pr,note)

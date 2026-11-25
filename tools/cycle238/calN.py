import random,sys
sys.argv=['x']
src=open('audit238.py').read().split('def main')[0]
exec(src)
r=random.Random(209709); n=0; fl=0
for _ in range(100000):
    w=[r.randrange(26) for _ in range(97)]
    if flags(w): fl+=1
print('gate N: random windows flagged',fl,'/100000')

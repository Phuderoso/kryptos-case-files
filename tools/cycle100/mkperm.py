import sys,struct,glob
# read CONS lines from given .out files, write perms (plaintext pos -> cipher pos) as int16 bin, inv applied as homocol does
out=open(sys.argv[1],'wb'); n=0
for fn in sys.argv[2:]:
    for line in open(fn):
        if not line.startswith('CONS'): continue
        p=line.split(); w=int(p[1][2:]); inv=int(p[2][4:]); ordr=[int(x) for x in p[3][4:].strip(',').split(',')]
        s=[0]*97;k=0
        for col in ordr:
            for r in range(col,97,w): s[r]=k;k+=1
        if inv: t=[0]*97; [t.__setitem__(s[i],i) for i in range(97)]; s=t
        out.write(struct.pack('<97h',*s)); n+=1
print(n,file=sys.stderr)

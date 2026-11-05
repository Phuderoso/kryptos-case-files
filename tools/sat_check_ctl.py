# Sanity check for wheat71_sat.py: fix the outer alphabet to ctl_4's planted one and confirm the encoding is SAT.
import z3,runpy,sys
A=open("a264.bin","rb").read();seq=[chr(65+x) for x in A[3*26:4*26]];seq.insert(26,' ')  # gap=25 -> blank after last letter
cells={c:(k+1)%27 for k,c in enumerate(seq)}  # rotate so blank is cell 0
orig=z3.Solver.check
def chk(self,*a):
    for c,v in cells.items():
        if c!=' ': self.add(z3.Int("p_"+c)==v)
    return orig(self,*a)
z3.Solver.check=chk;sys.argv=["x","ctl_4.txt"];runpy.run_path("wheat71_sat.py")

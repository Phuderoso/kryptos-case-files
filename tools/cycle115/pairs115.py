"""Export the 2,160 keyword-alphabet pairs of cycle 114 test B (same list, same order) for the C scanner."""
import sys; sys.path.insert(0,'/tmp/kcf/tools/cycle114')
from testB114 import PAIRS
with open('/workspace/k4c115/pairs.txt','w') as f:
    for F,M in PAIRS: f.write(F+" "+M+"\n")
print(len(PAIRS))

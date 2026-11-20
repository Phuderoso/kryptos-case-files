#!/bin/bash
# Gate P: run gn217 on each plant's slice (direct: Y stride 1000; families: row stride 2000) and check with check221.py
export OMP_NUM_THREADS=8; mkdir -p P; : > P/summary.txt
while IFS=$'\t' read -r id scope ct qi dr ix x y f w seat pt; do
  if [ "$scope" = direct ]; then ./gn217 "$ct" x alpha.bin alpha.bin keys221a.bin 1000 $((y%1000)) 100000 > P/p$id.txt; XA=alpha.bin; PF=x
  else ./gn217 "$ct" $scope.bin themed144.bin themed144.bin keys221a.bin 2000 $((qi%2000)) 100000 > P/p$id.txt; XA=themed144.bin; PF=$scope.bin; fi
  echo "$ct" > P/ct$id.txt
  python3 check221.py P/ct$id.txt $PF $XA $XA keys221a.bin P/p$id.txt > P/c$id.tsv 2>P/c$id.err
  python3 - "$id" "$scope" "$qi" "$dr" "$ix" "$x" "$y" "$f" "$w" "$pt" <<'PY' >> P/summary.txt
import sys; a=sys.argv[1:]; pid,scope,qi,dr,ix,x,y,f,w,pt=a; K=open('keys221a.bin','rb').read()
kw=K[int(w)*97:(int(w)+1)*97]; ok=False; n=0
for l in open(f'P/c{pid}.tsv'):
    t=l.rstrip('\n').split('\t'); d=dict(kv.split('=') for kv in t[0].split()[1:]); n+=1
    same=(int(d['perm'])==int(qi) and int(d['X'])==int(x) and int(d['Y'])==int(y) and int(d['form'])==int(f)
          and K[int(d['w'])*97:(int(d['w'])+1)*97]==kw and (scope=='direct' or (int(d['dir'])==int(dr) and int(d['ix'])==int(ix))))
    if same and sum(a!=b for a,b in zip(t[4],pt))<=1: ok=True
print(pid, scope, 'lines', n, 'PASS' if ok else 'FAIL')
PY
done < plants221.tsv
grep -c PASS P/summary.txt

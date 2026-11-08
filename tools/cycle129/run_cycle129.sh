#!/bin/bash
# Cycle 129: ACA Periodic Gromark x transposition bank. Needs perms97.bin (support data, cycle 22 export_perms.py).
set -e; W=${W:-/workspace/k4c129}; BANK=${BANK:-/home/box/kryptos_support_backup/perms97.bin}; D=$(dirname "$0")
mkdir -p $W; gcc -O2 -o $W/pgcheck $D/pgcheck.c; cd $W
python3 $D/mkcfg.py > cfg.txt; python3 $D/plant.py > controls.txt
python3 $D/mkcfg.py ctl PALIMPSEST SHADOW BERLIN LAYERTWO > ctlcfg.txt
for x in ctl1 ctl2 ctl3 ctl4; do ./pgcheck $(grep "^$x " controls.txt|cut -d' ' -f2) ctlcfg.txt $BANK $x; done
split -n l/8 -d cfg.txt part
for T in K4 null1 null2; do
  if [ $T = K4 ]; then CT=$(cat $D/../../data/k4.txt); else CT=$(grep "^$T " controls.txt|cut -d' ' -f2); fi
  for p in part0*; do ./pgcheck $CT $p $BANK $T > res_${T}_$p.txt & done; wait
  cat res_${T}_part0* | grep -c "^S" || true
done

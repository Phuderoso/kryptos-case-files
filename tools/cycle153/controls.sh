#!/bin/bash
# Cycle 153 controls: plant -> hillk1e at each control's own configuration -> independent Python check.
W=${W:-/workspace/k153}; P=/home/box/kryptos_support_backup/perms97.bin; T=/tmp/kcf/tools/cycle153; cd "$W"
python3 $T/plant.py > controls.txt
while read nm n k src q d ix nu o cpos wpos t; do [[ $nm == ctl* ]] || continue
  if [ $src = - ]; then COMBOCAP=2000000 THR=-4.6 ./hillk1e $t - $nm 0 1 1 $n $k; else COMBOCAP=2000000 THR=-4.6 ./hillk1e $t $P $nm $q $((q+1)) 1 $n $k; fi
done < controls.txt > controls_out.txt
python3 $T/check.py controls.txt controls_out.txt > controls_check.txt

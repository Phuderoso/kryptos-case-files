#!/bin/bash
# PREREG244 T5: rk243 (unchanged) on K4 + null 209771 (gate T) + 24 fresh nulls 209783-209806; four scopes as run243.sh.
# Usage: setsid timeout 300 ./run244.sh  (dir with rk243, alpha.bin, azka.bin, themed144.bin, texts243.txt, qg.bin, nulls244.tsv, null771.tsv, k4.txt)
set -u
run1 () { mkdir -p out/$1
  for sc in S1 S2 S3a S3b; do f=out/$1/$sc.txt
    if [ -s $f ] && tail -1 $f | grep -q '^T confs'; then continue; fi
    case $sc in
      S1) ./rk243 $2 alpha.bin alpha.bin eq texts243.txt qg.bin 100000 50 > $f.tmp ;;
      S2) ./rk243 $2 themed144.bin themed144.bin all texts243.txt qg.bin 100000 50 > $f.tmp ;;
      S3a) ./rk243 $2 alpha.bin azka.bin all texts243.txt qg.bin 100000 50 > $f.tmp ;;
      S3b) ./rk243 $2 azka.bin alpha.bin all texts243.txt qg.bin 100000 50 > $f.tmp ;;
    esac; mv $f.tmp $f; done
  echo "$(date +%T) done $1"; }
run1 K4 $(cat k4.txt)
while IFS=$'\t' read -r s ct; do run1 N$s $ct; done < null771.tsv
while IFS=$'\t' read -r s ct; do run1 N$s $ct; done < nulls244.tsv

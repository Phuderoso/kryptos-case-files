#!/bin/bash
# PREREG243 run: every text (plants, K4, nulls) through 4 scopes. Resumable: a finished scope file ends with a 'T confs' line.
# Usage: setsid timeout 480 ./run243.sh  (in a dir with rk243, alpha.bin, azka.bin, themed144.bin, texts243.txt, qg.bin, plants243.tsv, nulls243.tsv, k4.txt)
set -u
run1 () { # name ct
  mkdir -p out/$1
  for sc in S1 S2 S3a S3b; do
    f=out/$1/$sc.txt
    if [ -s $f ] && tail -1 $f | grep -q '^T confs'; then continue; fi
    case $sc in
      S1) ./rk243 $2 alpha.bin alpha.bin eq texts243.txt qg.bin 100000 50 > $f.tmp ;;
      S2) ./rk243 $2 themed144.bin themed144.bin all texts243.txt qg.bin 100000 50 > $f.tmp ;;
      S3a) ./rk243 $2 alpha.bin azka.bin all texts243.txt qg.bin 100000 50 > $f.tmp ;;
      S3b) ./rk243 $2 azka.bin alpha.bin all texts243.txt qg.bin 100000 50 > $f.tmp ;;
    esac
    mv $f.tmp $f
  done
  echo "$(date +%T) done $1"
}
while IFS=$'\t' read -r id sc x y g f M src o es ct; do run1 P$id $ct; done < plants243.tsv
[ "${PLANTS_ONLY:-0}" = 1 ] && exit 0
run1 K4 $(cat k4.txt)
while IFS=$'\t' read -r s ct; do run1 N$s $ct; done < nulls243.tsv

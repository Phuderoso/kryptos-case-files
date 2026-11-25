#!/bin/bash
s=$(date +%s); ./runP.sh > runP.log 2>&1; echo "P done $(( $(date +%s)-s ))s" >> stage.txt
./runA.sh > runA.log 2>&1; echo "A done $(( $(date +%s)-s ))s" >> stage.txt

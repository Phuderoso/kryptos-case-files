#!/bin/bash
# PREREG238 Part A2: textual scan of every key-generator source for size caps / early stops / silent zero returns (descriptive, reviewed by hand)
for f in ../cycle217/*.py ../cycle218/keys218.py ../cycle221/keys221*.py ../cycle222/keys222*.py ../cycle233/keys233.py ../cycle234/keys234.py ../cycle236/keys236.py ../cycle237/keys237.py ../cycle237/las_exact.py; do
  [ -f "$f" ] && grep -nE '10 *\*\* *[0-9]|1e[0-9]|[^a-z]cap[^a-z]|limit|MAX|break|return 0|\[: *[0-9]+\]|len\(.*\) *[<>]=? *[0-9]{3,}' "$f" | sed "s|^|$f:|"
done

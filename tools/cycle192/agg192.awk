# Cycle 192 on-the-fly reducer: sums cmp192 H lines over tableau pairs per (model, form, m, n) -> "A model form m n configs fits strictfits Usum";
# passes M, B and END lines through unchanged (keeps the direct/C3 outputs small).
$1=="H" { k=$3" "$5" "$6" "$7; c[k]+=$8; f[k]+=$9; s[k]+=$10; u[k]+=$11; next }
$1=="M" || $1=="B" || $1=="END" { print; next }
END { for (k in c) printf "A %s %d %d %d %.6g\n", k, c[k], f[k], s[k], u[k] }

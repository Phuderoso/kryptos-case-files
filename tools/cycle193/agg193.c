/* Cycle 193 aggregator (from agg191.c): reads cmp193 (sumtabs) outputs outputs (files listed on stdin), sums H lines per (model, form, m, n) over all tableau pairs and
   routes, sums B lines per band, copies M lines and counts END lines. out: A model form m n configs fits sols E ; B ... ; M ... ; ENDS n */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void) {
  static long long cf[2][4][27][27], ft[2][4][27][27]; static double so[2][4][27][27], ee[2][4][27][27];
  long long bc[30] = {0}, bf[30] = {0}; double bs[30] = {0}, be[30] = {0}; long ends = 0, nf = 0;
  char fn[4096], line[512];
  while (fgets(fn, sizeof fn, stdin)) { fn[strcspn(fn, "\n")] = 0; FILE *f = fopen(fn, "r"); if (!f) continue; nf++;
    while (fgets(line, sizeof line, f)) {
      if (line[0] == 'H') { char lab[64], md, tab[128], fm[3]; int m, n; long long c, x; double s, e;
        if (sscanf(line, "H %63s %c %127s %2s %d %d %lld %lld %lf %lf", lab, &md, tab, fm, &m, &n, &c, &x, &s, &e) == 10) {
          int a = md == '2', b = (fm[0] == 'B') * 2 + (fm[1] == 'B'); cf[a][b][m][n] += c; ft[a][b][m][n] += x; so[a][b][m][n] += s; ee[a][b][m][n] += e; } }
      else if (line[0] == 'B') { char lab[64]; int bd; long long c, x; double s, e;
        if (sscanf(line, "B %63s %d %lld %lld %lf %lf", lab, &bd, &c, &x, &s, &e) == 6) { bc[bd] += c; bf[bd] += x; bs[bd] += s; be[bd] += e; } }
      else if (line[0] == 'M') fputs(line, stdout);
      else if (!strncmp(line, "END", 3)) ends++; }
    fclose(f); }
  const char *FN[4] = {"VV", "VB", "BV", "BB"};
  for (int a = 0; a < 2; a++) for (int b = 0; b < 4; b++) for (int m = 2; m <= 26; m++) for (int n = 2; n <= 26; n++) if (cf[a][b][m][n])
    printf("A %c %s %d %d %lld %lld %.6g %.6g\n", a ? '2' : '1', FN[b], m, n, cf[a][b][m][n], ft[a][b][m][n], so[a][b][m][n], ee[a][b][m][n]);
  for (int i = 0; i < 30; i++) if (bc[i]) printf("B agg %d %lld %lld %.6g %.6g\n", i, bc[i], bf[i], bs[i], be[i]);
  printf("ENDS %ld files %ld\n", ends, nf); return 0; }
/* note (cycle 193): model labels are '1' (S1: a plaintext index, b carved index) and '2' (S2: the reverse); pairs include m = n. */

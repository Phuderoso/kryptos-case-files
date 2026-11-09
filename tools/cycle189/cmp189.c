/* Cycle 189 (IDEAS I-189): compound key = two arbitrary periodic keys of periods m and n stacked on ONE tableau
   (any Vig/Beau/variant stacking on the same tableau reduces to c = p + K or c = K - p in alphabet-index space,
   K[i] = a[i mod m] + b[i mod n] mod 26), behind K3-law decimations / routes, key on the plaintext index (model P:
   substitute, then transpose) or on the carved index (model C: transpose, then substitute). Same keyed alphabet on
   both sides (A-Z, KRYPTOS, or a Quagmire III keyed alphabet).
   Exact test: the 24 crib equations a[u] - b'[v] = K (b' = -b) are checked by a weighted union-find over Z26
   (no division, so exact mod 26 directly). excess = 24 - (number of merging edges) = number of independent checks.
   usage: cmp189 CT perms.bin alphas.txt label qlo qhi mmax nmax printexcess
   out: H label model form m n configs fits chance(sum 26^-excess over configs) ; M label perm alpha form model m n excess ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
static const char *PTC = "EASTNORTHEASTBERLINCLOCK";
static int CI[24];
#define MAXP 28
int main(int argc, char **argv) {
  if (argc < 10) { fprintf(stderr, "usage\n"); return 1; }
  const char *ct = argv[1]; const char *lab = argv[4]; long qlo = atol(argv[5]), qhi = atol(argv[6]);
  int MM = atoi(argv[7]), NM = atoi(argv[8]), PE = atoi(argv[9]);
  for (int t = 0; t < 13; t++) CI[t] = 21 + t; for (int t = 0; t < 11; t++) CI[13 + t] = 63 + t;
  FILE *f = fopen(argv[2], "rb"); fseek(f, 0, SEEK_END); long np = ftell(f) / (97 * 2); fseek(f, 0, SEEK_SET);
  short *P = malloc(np * 97 * 2); if (fread(P, 2, np * 97, f) != (size_t)(np * 97)) return 2; fclose(f);
  if (qhi > np) qhi = np; if (qlo < 0) qlo = 0;
  char (*AL)[27] = malloc(40000 * 27); char (*AN)[64] = malloc(40000 * 64); int na = 0; char buf[256];
  f = fopen(argv[3], "r"); while (fgets(buf, 256, f)) { char a[64], b[64]; if (sscanf(buf, "%63s %63s", a, b) == 2 && strlen(a) == 26) { memcpy(AL[na], a, 27); strcpy(AN[na], b); na++; } } fclose(f);
  int pm[400], pn[400], npair = 0;
  for (int m = 2; m <= MM; m++) for (int n = m + 1; n <= NM; n++) if (n % m) { pm[npair] = m; pn[npair] = n; npair++; }
  /* accumulators [model][form][pair] */
  long long *cfg = calloc(2 * 2 * npair, 8), *fit = calloc(2 * 2 * npair, 8); double *chs = calloc(2 * 2 * npair, 8);
  double p26[25]; p26[0] = 1; for (int e = 1; e < 25; e++) p26[e] = p26[e - 1] / 26.0;
  #pragma omp parallel
  {
    long long *lc = calloc(4 * npair, 8), *lf = calloc(4 * npair, 8); double *lh = calloc(4 * npair, 8);
    int lpar[64], loff[64];
    #pragma omp for schedule(dynamic, 64)
    for (long q = qlo; q < qhi; q++) {
      const short *S = P + q * 97;
      for (int a = 0; a < na; a++) {
        int idx[26]; for (int i = 0; i < 26; i++) idx[AL[a][i] - 'A'] = i;
        int xp[24], xc[24]; for (int t = 0; t < 24; t++) { xp[t] = idx[PTC[t] - 'A']; xc[t] = idx[ct[S[CI[t]]] - 'A']; }
        for (int fm = 0; fm < 2; fm++) {
          int K[24]; for (int t = 0; t < 24; t++) K[t] = fm == 0 ? (xc[t] - xp[t] + 26) % 26 : (xc[t] + xp[t]) % 26;
          for (int md = 0; md < 2; md++) {
            int pos[24]; for (int t = 0; t < 24; t++) pos[t] = md == 0 ? CI[t] : S[CI[t]];
            for (int pi = 0; pi < npair; pi++) {
              int m = pm[pi], n = pn[pi], ok = 1, merges = 0;
              for (int x = 0; x < m + n; x++) { lpar[x] = x; loff[x] = 0; }
              for (int t = 0; t < 24 && ok; t++) {
                int u = pos[t] % m, v = m + pos[t] % n, ou = 0, ov = 0, ru = u, rv = v;
                while (lpar[ru] != ru) { ou += loff[ru]; ru = lpar[ru]; } while (lpar[rv] != rv) { ov += loff[rv]; rv = lpar[rv]; }
                ou %= 26; ov %= 26;            /* val(u) = val(ru) + ou ; constraint val(u) - val(v) = K */
                if (ru == rv) { if (((ou - ov - K[t]) % 26 + 52) % 26) ok = 0; }
                else { lpar[ru] = rv; loff[ru] = ((K[t] + ov - ou) % 26 + 52) % 26; merges++; }
              }
              int k3 = (md * 2 + fm) * npair + pi; lc[k3]++;
              if (ok) {
                /* finish merges count over all edges (loop exited only on fail) */
                int ex = 24 - merges; lf[k3]++; 
                if (ex >= PE) {
                  #pragma omp critical
                  printf("M %s %ld %s %s %c %d %d %d\n", lab, q, AN[a], fm ? "beau" : "vig", md ? 'C' : 'P', m, n, ex);
                }
              }
              /* chance: the excess depends only on (route, model, pair): computed once per route (a = 0, vig), credited to every alphabet and form */
              if (a == 0 && fm == 0) { int rp[64]; for (int x = 0; x < m + n; x++) rp[x] = x; int mg = 0;
                for (int t = 0; t < 24; t++) { int u = pos[t] % m, v = m + pos[t] % n; while (rp[u] != u) u = rp[u]; while (rp[v] != v) v = rp[v]; if (u != v) { rp[u] = v; mg++; } }
                lh[k3] += na * p26[24 - mg]; lh[(md * 2 + 1) * npair + pi] += na * p26[24 - mg]; }
            }
          }
        }
      }
    }
    #pragma omp critical
    for (int i = 0; i < 4 * npair; i++) { cfg[i] += lc[i]; fit[i] += lf[i]; chs[i] += lh[i]; }
  }
  for (int md = 0; md < 2; md++) for (int fm = 0; fm < 2; fm++) for (int pi = 0; pi < npair; pi++) {
    int k3 = (md * 2 + fm) * npair + pi;
    printf("H %s %c %s %d %d %lld %lld %.6g\n", lab, md ? 'C' : 'P', fm ? "beau" : "vig", pm[pi], pn[pi], cfg[k3], fit[k3], chs[k3]);
  }
  printf("END %s perms %ld-%ld alphas %d pairs %d\n", lab, qlo, qhi, na, npair);
  return 0;
}

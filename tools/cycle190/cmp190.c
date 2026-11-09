/* Cycle 190 (IDEAS I-191): one-error audit of case 176. Compound key K[i] = a[i mod m] + b[i mod n] (two periodic keys on ONE
   tableau; c = p + K or c = K - p in alphabet-index space), behind K3-law decimations/routes, key on the plaintext index (P) or
   the carved index (C); same keyed alphabet on both sides. ONE-ERROR scope: a config fits if the 24 crib equations are consistent
   after deleting at most one crib slot t (one wrong carved or crib letter anywhere in the cribs). Exact mod 26 (weighted union-find).
   Search: the strict pass stops at the first inconsistent edge t_f; a consistent G minus t needs t <= t_f, so only t in 0..t_f is tried,
   each from the shared prefix state (edges 0..t-1) plus edges t+1..23.
   Chance (exact, per route x model x pair; independent of alphabet and form): with ex = strict excess and ncls = number of series
   classes of non-bridge edges (2-edge-cut classes, found by XOR cycle hashing with 64-bit labels),
     P(one-error fit) = 26^-ex + ncls * (26^(1-ex) - 26^-ex)   (capped at 1),
   because the events "G minus t consistent and G not" are equal inside a series class and disjoint across classes (regular matroid).
   usage: cmp190 CT perms.bin alphas.txt label qlo qhi mmax nmax printexcess
   out: H label model form m n configs fits strictfits chance ; M label perm alpha form model m n slot ex_after ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
static const char *PTC = "EASTNORTHEASTBERLINCLOCK";
static int CI[24];
static uint64_t LBL[24];
static int findw(const int *par, const int *off, int x, int *o) { int s = 0; while (par[x] != x) { s += off[x]; x = par[x]; } *o = s % 26; return x; }
/* add edge (u,v,K): returns 1 merged, 0 consistent cycle, -1 inconsistent */
static int addE(int *par, int *off, int u, int v, int K) {
  int ou, ov, ru = findw(par, off, u, &ou), rv = findw(par, off, v, &ov);
  if (ru == rv) return (((ou - ov - K) % 26 + 52) % 26) ? -1 : 0;
  par[ru] = rv; off[ru] = ((K + ov - ou) % 26 + 52) % 26; return 1;
}
/* series classes: spanning forest by plain union-find in edge order; non-tree edge e gets label LBL[e], XORed onto every tree edge of its
   fundamental cycle; bridges keep 0. returns ex (strict excess) and *ncls (distinct nonzero labels). */
static int structure(const int *U, const int *V, int nn, int *ncls) {
  int rp[64], tree[24], nt = 0; uint64_t lab[24];
  for (int x = 0; x < nn; x++) rp[x] = x;
  for (int t = 0; t < 24; t++) { int u = U[t], v = V[t]; while (rp[u] != u) u = rp[u]; while (rp[v] != v) v = rp[v];
    lab[t] = 0; if (u != v) { rp[u] = v; tree[t] = 1; nt++; } else { tree[t] = 0; lab[t] = LBL[t]; } }
  int ex = 24 - nt;
  /* tree adjacency: parent pointers by BFS from each component root */
  int head[64], nxt[48], to[48], eid[48], ne = 0; for (int x = 0; x < nn; x++) head[x] = -1;
  for (int t = 0; t < 24; t++) if (tree[t]) { to[ne] = V[t]; eid[ne] = t; nxt[ne] = head[U[t]]; head[U[t]] = ne++; to[ne] = U[t]; eid[ne] = t; nxt[ne] = head[V[t]]; head[V[t]] = ne++; }
  int par[64], pe[64], dep[64], seen[64] = {0}, qq[64];
  for (int s = 0; s < nn; s++) if (!seen[s]) { int h = 0, tl = 0; qq[tl++] = s; seen[s] = 1; par[s] = -1; pe[s] = -1; dep[s] = 0;
    while (h < tl) { int x = qq[h++]; for (int e = head[x]; e >= 0; e = nxt[e]) if (!seen[to[e]]) { seen[to[e]] = 1; par[to[e]] = x; pe[to[e]] = eid[e]; dep[to[e]] = dep[x] + 1; qq[tl++] = to[e]; } } }
  for (int t = 0; t < 24; t++) if (!tree[t]) { int u = U[t], v = V[t];
    while (u != v) { if (dep[u] >= dep[v]) { lab[pe[u]] ^= LBL[t]; u = par[u]; } else { lab[pe[v]] ^= LBL[t]; v = par[v]; } } }
  uint64_t d[24]; int nd = 0;
  for (int t = 0; t < 24; t++) if (lab[t]) { int f = 0; for (int k = 0; k < nd; k++) if (d[k] == lab[t]) { f = 1; break; } if (!f) d[nd++] = lab[t]; }
  *ncls = nd; return ex;
}
int main(int argc, char **argv) {
  if (argc < 10) { fprintf(stderr, "usage\n"); return 1; }
  const char *ct = argv[1]; const char *lab = argv[4]; long qlo = atol(argv[5]), qhi = atol(argv[6]);
  int MM = atoi(argv[7]), NM = atoi(argv[8]), PE = atoi(argv[9]);
  for (int t = 0; t < 13; t++) CI[t] = 21 + t; for (int t = 0; t < 11; t++) CI[13 + t] = 63 + t;
  uint64_t s = 0x9E3779B97F4A7C15ULL; for (int t = 0; t < 24; t++) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; LBL[t] = s | 1; }
  FILE *f = fopen(argv[2], "rb"); fseek(f, 0, SEEK_END); long np = ftell(f) / (97 * 2); fseek(f, 0, SEEK_SET);
  short *P = malloc(np * 97 * 2); if (fread(P, 2, np * 97, f) != (size_t)(np * 97)) return 2; fclose(f);
  if (qhi > np) qhi = np; if (qlo < 0) qlo = 0;
  char (*AL)[27] = malloc(40000 * 27); char (*AN)[64] = malloc(40000 * 64); int na = 0; char buf[256];
  f = fopen(argv[3], "r"); while (fgets(buf, 256, f)) { char a[64], b[64]; if (sscanf(buf, "%63s %63s", a, b) == 2 && strlen(a) == 26) { memcpy(AL[na], a, 27); strcpy(AN[na], b); na++; } } fclose(f);
  int pm[400], pn[400], npair = 0;
  for (int m = 2; m <= MM; m++) for (int n = m + 1; n <= NM; n++) if (n % m) { pm[npair] = m; pn[npair] = n; npair++; }
  long long *cfg = calloc(4 * npair, 8), *fit = calloc(4 * npair, 8), *sfit = calloc(4 * npair, 8); double *chs = calloc(4 * npair, 8);
  double p26[26]; p26[0] = 1; for (int e = 1; e < 26; e++) p26[e] = p26[e - 1] / 26.0;
  #pragma omp parallel
  {
    long long *lc = calloc(4 * npair, 8), *lf = calloc(4 * npair, 8), *ls = calloc(4 * npair, 8); double *lh = calloc(4 * npair, 8);
    int par[64], off[64], sp[64], so[64];
    #pragma omp for schedule(dynamic, 2)
    for (long q = qlo; q < qhi; q++) {
      const short *S = P + q * 97;
      for (int md = 0; md < 2; md++) {
        int pos[24]; for (int t = 0; t < 24; t++) pos[t] = md == 0 ? CI[t] : S[CI[t]];
        for (int pi = 0; pi < npair; pi++) {
          int m = pm[pi], n = pn[pi], U[24], V[24], ncls;
          for (int t = 0; t < 24; t++) { U[t] = pos[t] % m; V[t] = m + pos[t] % n; }
          int ex = structure(U, V, m + n, &ncls);
          double pr = ex == 0 ? 1.0 : p26[ex] + ncls * (p26[ex - 1] - p26[ex]); if (pr > 1) pr = 1;
          lh[(md * 2) * npair + pi] += na * pr; lh[(md * 2 + 1) * npair + pi] += na * pr;
          for (int a = 0; a < na; a++) {
            int idx[26]; for (int i = 0; i < 26; i++) idx[AL[a][i] - 'A'] = i;
            int xp[24], xc[24]; for (int t = 0; t < 24; t++) { xp[t] = idx[PTC[t] - 'A']; xc[t] = idx[ct[S[CI[t]]] - 'A']; }
            for (int fm = 0; fm < 2; fm++) {
              int K[24]; for (int t = 0; t < 24; t++) K[t] = fm == 0 ? (xc[t] - xp[t] + 26) % 26 : (xc[t] + xp[t]) % 26;
              int k3 = (md * 2 + fm) * npair + pi; lc[k3]++;
              for (int x = 0; x < m + n; x++) { par[x] = x; off[x] = 0; }
              int tf = -1; for (int t = 0; t < 24; t++) if (addE(par, off, U[t], V[t], K[t]) < 0) { tf = t; break; }
              if (tf < 0) { lf[k3]++; ls[k3]++; if (ex >= PE) {
                  #pragma omp critical
                  printf("M %s %ld %s %s %c %d %d -1 %d\n", lab, q, AN[a], fm ? "beau" : "vig", md ? 'C' : 'P', m, n, ex); }
                continue; }
              /* prefix state (edges 0..t-1) in sp/so */
              for (int x = 0; x < m + n; x++) { sp[x] = x; so[x] = 0; }
              int found = -1, exf = 0;
              for (int t = 0; t <= tf && found < 0; t++) {
                memcpy(par, sp, (m + n) * sizeof(int)); memcpy(off, so, (m + n) * sizeof(int));
                int okk = 1, mg = 0;
                for (int x = 0; x < m + n; x++) if (par[x] != x) mg++;   /* merges so far = non-root nodes */
                for (int u = t + 1; u < 24; u++) { int r = addE(par, off, U[u], V[u], K[u]); if (r < 0) { okk = 0; break; } mg += r; }
                if (okk) { found = t; exf = 23 - mg; }
                addE(sp, so, U[t], V[t], K[t]);   /* consistent: t < tf */
              }
              if (found >= 0) { lf[k3]++; if (exf >= PE) {
                  #pragma omp critical
                  printf("M %s %ld %s %s %c %d %d %d %d\n", lab, q, AN[a], fm ? "beau" : "vig", md ? 'C' : 'P', m, n, found, exf); } }
            }
          }
        }
      }
    }
    #pragma omp critical
    for (int i = 0; i < 4 * npair; i++) { cfg[i] += lc[i]; fit[i] += lf[i]; sfit[i] += ls[i]; chs[i] += lh[i]; }
  }
  for (int md = 0; md < 2; md++) for (int fm = 0; fm < 2; fm++) for (int pi = 0; pi < npair; pi++) {
    int k3 = (md * 2 + fm) * npair + pi;
    printf("H %s %c %s %d %d %lld %lld %lld %.6g\n", lab, md ? 'C' : 'P', fm ? "beau" : "vig", pm[pi], pn[pi], cfg[k3], fit[k3], sfit[k3], chs[k3]);
  }
  printf("END %s perms %ld-%ld alphas %d pairs %d\n", lab, qlo, qhi, na, npair);
  return 0;
}

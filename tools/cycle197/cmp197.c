/* Cycle 197 (IDEAS I-196 / I-215): compound key with ONE DROPPED or EXTRA carved letter.
   Two key layers as in cases 176 (one tableau, additive: K[i] = a[i mod m] + b[i mod n]) and 178 (two tableaux, A-Z/KRYPTOS either
   order, bijection graph), but the carved text is the true ciphertext C' with one slip:
     del: C' has N = 98 letters, C'[d] (d = 0..97) was left off the copper;
     ins: C' has N = 96 letters, an extra letter was carved at carved index d (d = 0..96).
   A configuration is a RECORD: for each of the 24 cribs t, kp[t] = plaintext index (key index, model P), kc[t] = C' index (key index,
   model C), cv[t] = carved index of the ciphertext letter, or -1 if that letter is the dropped one (crib unusable).
   Modes:  perm: records generated here from a transposition bank (int16 x N per perm, out[k] = C' index of plaintext position k), every d,
                 keeping only d values that change the record (d at or next to a crib's C' index), cribs at plaintext 21-33, 63-73 (0-based).
           rec:  records read from a text file (direct application; built by recs197.py), model P only (kp = kc).
   Solvers: A additive (case 176 weighted union-find over Z26, alphabets file, vig c = p + K / beau c = K - p, pairs m < n, n % m != 0)
            B bijection graph (case 178 cmp191 core, tabpairs file, forms VV VB BV BB, ordered pairs m != n), lost cribs skipped.
   Chance (I-193): A: E_config = 26^-(used - merges); B: E_config = prod_cyclic 26^(1 - r_c). Exact for uniform carved letters.
   usage: cmp197 MODE CT src N kind label qlo qhi alphas.txt tabpairs.txt pairsA.txt pairsB.txt PE
     MODE perm|rec; kind del|ins (perm mode); pairs files: lines "P|C m n" (P only used in rec mode); "-" to skip a solver.
   out: M A label q d model alpha form m n ex E ; M B label q d model tab form m n E nsol ;
        H A label model alpha form m n configs fits E ; H B label model tab form m n configs fits sols E ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
static const char *PTC = "EASTNORTHEASTBERLINCLOCK";
static int CI[24];
#define NV 56
typedef struct { short kp[24], kc[24], cv[24]; int q, d; } Rec;
typedef struct { unsigned char typ, w, from, t; } Op;
static int npA[2], pAm[2][400], pAn[2][400], npB[2], pBm[2][700], pBn[2][700];
int main(int argc, char **argv) {
  if (argc < 14) { fprintf(stderr, "usage\n"); return 1; }
  const char *mode = argv[1], *ct = argv[2], *src = argv[3]; int N = atoi(argv[4]); const char *kind = argv[5], *lab = argv[6];
  long qlo = atol(argv[7]), qhi = atol(argv[8]); double PE = atof(argv[13]);
  int isrec = !strcmp(mode, "rec"), isdel = !strcmp(kind, "del");
  if (strlen(ct) != 97) { fprintf(stderr, "ct len\n"); return 1; }
  for (int t = 0; t < 13; t++) CI[t] = 21 + t; for (int t = 0; t < 11; t++) CI[13 + t] = 63 + t;
  /* pairs */
  for (int s = 0; s < 2; s++) { const char *fn = argv[11 + s]; int *np = s ? npB : npA; np[0] = np[1] = 0;
    if (strcmp(fn, "-")) { FILE *f = fopen(fn, "r"); if (!f) { fprintf(stderr, "no %s\n", fn); return 2; } char md; int m, n;
      while (fscanf(f, " %c %d %d", &md, &m, &n) == 3) { int k = md == 'C'; if (s == 0) { pAm[k][npA[k]] = m; pAn[k][npA[k]] = n; npA[k]++; } else { pBm[k][npB[k]] = m; pBn[k][npB[k]] = n; npB[k]++; } }
      fclose(f); } }
  int NM = isrec ? 1 : 2;
  /* records */
  Rec *R = NULL; long nr = 0; short *PB = NULL; long np = 0;
  if (isrec) { FILE *f = fopen(src, "r"); if (!f) return 2; long cap = 1 << 16; R = malloc(cap * sizeof(Rec)); int q;
    while (fscanf(f, "%d", &q) == 1) { Rec r; r.q = q; int d; if (fscanf(f, "%d", &d) != 1) return 3; r.d = d;
      for (int t = 0; t < 24; t++) { int v; if (fscanf(f, "%d", &v) != 1) return 3; r.kp[t] = v; r.kc[t] = v; }
      for (int t = 0; t < 24; t++) { int v; if (fscanf(f, "%d", &v) != 1) return 3; r.cv[t] = v; }
      if (nr == cap) { cap *= 2; R = realloc(R, cap * sizeof(Rec)); } R[nr++] = r; }
    fclose(f); if (qhi > nr) qhi = nr; }
  else { FILE *f = fopen(src, "rb"); if (!f) return 2; fseek(f, 0, SEEK_END); np = ftell(f) / (N * 2); fseek(f, 0, SEEK_SET);
    PB = malloc(np * N * 2); if (fread(PB, 2, np * N, f) != (size_t)(np * N)) return 2; fclose(f); if (qhi > np) qhi = np; }
  if (qlo < 0) qlo = 0;
  /* alphabets (solver A) */
  static char AL[20000][27]; static char AN[20000][64]; int na = 0; char buf[256];
  if (strcmp(argv[9], "-")) { FILE *f = fopen(argv[9], "r"); while (fgets(buf, 256, f) && na < 20000) { char a[64], b[64]; if (sscanf(buf, "%63s %63s", a, b) == 2 && strlen(a) == 26) { memcpy(AL[na], a, 27); strcpy(AN[na], b); na++; } } fclose(f); }
  int NAC = na < 2 ? na : (na == 2 ? 2 : 3);  /* alphabet classes: 0 AZ-line, 1 KA-line, 2 the rest */
  static int AIDX[20000][26]; for (int a = 0; a < na; a++) for (int i = 0; i < 26; i++) AIDX[a][AL[a][i] - 'A'] = i;
  /* tableau pairs (solver B) */
  static char T1[8][27], T2[8][27], TN[8][64]; int nt = 0;
  if (strcmp(argv[10], "-")) { FILE *f = fopen(argv[10], "r"); while (fgets(buf, 256, f) && nt < 8) { char a[64], b[64], c[64]; if (sscanf(buf, "%63s %63s %63s", a, b, c) == 3) { memcpy(T1[nt], a, 27); memcpy(T2[nt], b, 27); strcpy(TN[nt], c); nt++; } } fclose(f); }
  /* FF[k][fm][t][zletter][a] = b ; GG inverse */
  static unsigned char FF[8][4][24][26][26], GG[8][4][24][26][26];
  for (int k = 0; k < nt; k++) { int i1[26], i2[26]; for (int i = 0; i < 26; i++) { i1[T1[k][i] - 'A'] = i; i2[T2[k][i] - 'A'] = i; }
    int sig[26]; for (int y = 0; y < 26; y++) sig[y] = i2[T1[k][y] - 'A'];
    for (int fm = 0; fm < 4; fm++) { int s1 = (fm & 2) ? -1 : 1, s2 = (fm & 1) ? -1 : 1;
      for (int t = 0; t < 24; t++) { int x = i1[PTC[t] - 'A'];
        for (int L = 0; L < 26; L++) { int z = i2[L];
          for (int a = 0; a < 26; a++) { int y = ((s1 * x + a) % 26 + 26) % 26; int b = ((z - s2 * sig[y]) % 26 + 26) % 26; FF[k][fm][t][L][a] = b; GG[k][fm][t][L][b] = a; } } } } }
  int CA = NM * (NAC > 0 ? NAC : 1) * 2 * 400, CB = NM * (nt > 0 ? nt : 1) * 4 * 700;
  long long *cA = calloc(CA, 8), *fA = calloc(CA, 8); double *eA = calloc(CA, 8);
  long long *cB = calloc(CB, 8), *fB = calloc(CB, 8); double *sB = calloc(CB, 8), *eB = calloc(CB, 8);
  long long nrec = 0;
  double p26[26]; p26[0] = 1; for (int e = 1; e < 26; e++) p26[e] = p26[e - 1] / 26.0;
  #pragma omp parallel reduction(+:nrec)
  {
    long long *lcA = calloc(CA, 8), *lfA = calloc(CA, 8); double *leA = calloc(CA, 8);
    long long *lcB = calloc(CB, 8), *lfB = calloc(CB, 8); double *lsB = calloc(CB, 8), *leB = calloc(CB, 8);
    Rec *loc = malloc(128 * sizeof(Rec));
    #pragma omp for schedule(dynamic, 8)
    for (long q = qlo; q < qhi; q++) {
      int nl = 0;
      if (isrec) loc[nl++] = R[q];
      else { const short *S = PB + q * N; int c[24]; char isc[100] = {0}; for (int t = 0; t < 24; t++) { c[t] = S[CI[t]]; isc[c[t]] = 1; }
        int dmax = isdel ? N - 1 : N;
        for (int d = 0; d <= dmax; d++) { if (!(d == 0 || isc[d - 1] || (isdel && d < N && isc[d]))) continue;
          Rec r; r.q = q; r.d = d;
          for (int t = 0; t < 24; t++) { r.kp[t] = CI[t]; r.kc[t] = c[t];
            if (isdel) r.cv[t] = c[t] < d ? c[t] : (c[t] == d ? -1 : c[t] - 1); else r.cv[t] = c[t] < d ? c[t] : c[t] + 1; }
          loc[nl++] = r; } }
      for (int ir = 0; ir < nl; ir++) { const Rec *r = &loc[ir]; nrec++;
        int ut[24], nu = 0, Lt[24]; for (int t = 0; t < 24; t++) if (r->cv[t] >= 0) { ut[nu++] = t; Lt[t] = ct[r->cv[t]] - 'A'; }
        for (int md = 0; md < NM; md++) {
          const short *pos = md ? r->kc : r->kp;
          /* ---- solver A ---- */
          for (int pi = 0; pi < npA[md]; pi++) { int m = pAm[md][pi], n = pAn[md][pi];
            int rp[64]; for (int x = 0; x < m + n; x++) rp[x] = x; int mg = 0;
            for (int j = 0; j < nu; j++) { int t = ut[j], u = pos[t] % m, v = m + pos[t] % n; while (rp[u] != u) u = rp[u]; while (rp[v] != v) v = rp[v]; if (u != v) { rp[u] = v; mg++; } }
            int ex = nu - mg; double Ec = p26[ex];
            for (int a = 0; a < na; a++) { int ac = a < 2 ? a : 2;
              for (int fm = 0; fm < 2; fm++) {
                int k3 = ((md * NAC + ac) * 2 + fm) * 400 + pi; lcA[k3]++; leA[k3] += Ec;
                if (ex == 0) { lfA[k3]++; continue; }
                int lpar[64], loff[64], ok = 1; for (int x = 0; x < m + n; x++) { lpar[x] = x; loff[x] = 0; }
                for (int j = 0; j < nu && ok; j++) { int t = ut[j]; int xp = AIDX[a][PTC[t] - 'A'], xc = AIDX[a][Lt[t]];
                  int K = fm == 0 ? (xc - xp + 26) % 26 : (xc + xp) % 26;
                  int u = pos[t] % m, v = m + pos[t] % n, ou = 0, ov = 0, ru = u, rv = v;
                  while (lpar[ru] != ru) { ou += loff[ru]; ru = lpar[ru]; } while (lpar[rv] != rv) { ov += loff[rv]; rv = lpar[rv]; }
                  ou %= 26; ov %= 26;
                  if (ru == rv) { if (((ou - ov - K) % 26 + 52) % 26) ok = 0; }
                  else { lpar[ru] = rv; loff[ru] = ((K + ov - ou) % 26 + 52) % 26; } }
                if (ok) { lfA[k3]++; if (Ec <= PE) {
                  #pragma omp critical
                  printf("M A %s %d %d %c %s %s %d %d %d %.4g\n", lab, r->q, r->d, isrec ? 'D' : (md ? 'C' : 'P'), AN[a], fm ? "beau" : "vig", m, n, ex, Ec); } }
              } } }
          /* ---- solver B ---- */
          for (int pi = 0; pi < npB[md] && nt; pi++) { int m = pBm[md][pi], n = pBn[md][pi], V = m + n;
            int eu[24], ev[24], et[24], ne = 0; for (int j = 0; j < nu; j++) { int t = ut[j]; eu[ne] = pos[t] % m; ev[ne] = m + pos[t] % n; et[ne] = t; ne++; }
            int par[NV]; for (int x = 0; x < V; x++) par[x] = x;
            for (int e = 0; e < ne; e++) { int u = eu[e], v = ev[e]; while (par[u] != u) u = par[u]; while (par[v] != v) v = par[v]; if (u != v) par[u] = v; }
            int root[NV], ecount[NV], vcount[NV], touched[NV];
            for (int x = 0; x < V; x++) { int rr = x; while (par[rr] != rr) rr = par[rr]; root[x] = rr; ecount[x] = 0; vcount[x] = 0; touched[x] = 0; }
            for (int e = 0; e < ne; e++) { ecount[root[eu[e]]]++; touched[eu[e]] = 1; touched[ev[e]] = 1; }
            for (int x = 0; x < V; x++) if (touched[x]) vcount[root[x]]++;
            Op ops[24][32]; int nops[24], crt[24], ncy = 0; double cE = 1.0;
            for (int rr = 0; rr < V; rr++) if (vcount[rr] && ecount[rr] > vcount[rr] - 1) {
              int cyc = ecount[rr] - vcount[rr] + 1; cE *= pow(26.0, 1 - cyc);
              int deg[NV]; memset(deg, 0, sizeof deg); for (int e = 0; e < ne; e++) if (root[eu[e]] == rr) { deg[eu[e]]++; deg[ev[e]]++; }
              int st = -1; for (int x = 0; x < V; x++) if (root[x] == rr && touched[x] && (st < 0 || deg[x] > deg[st])) st = x;
              int asg[NV], used[24], qu[NV], qh = 0, qt = 0, no = 0; memset(asg, 0, sizeof asg); memset(used, 0, sizeof used);
              asg[st] = 1; qu[qt++] = st;
              while (qh < qt) { int x = qu[qh++];
                for (int e = 0; e < ne; e++) if (!used[e] && (eu[e] == x || ev[e] == x)) { int y = eu[e] == x ? ev[e] : eu[e]; used[e] = 1;
                  if (!asg[y]) { asg[y] = 1; qu[qt++] = y; ops[ncy][no++] = (Op){0, (unsigned char)y, (unsigned char)x, (unsigned char)e};
                    for (int e2 = 0; e2 < ne; e2++) if (!used[e2] && (eu[e2] == y || ev[e2] == y)) { int o = eu[e2] == y ? ev[e2] : eu[e2];
                      if (asg[o]) { used[e2] = 1; ops[ncy][no++] = (Op){1, (unsigned char)eu[e2], (unsigned char)ev[e2], (unsigned char)e2}; } } }
                  else ops[ncy][no++] = (Op){1, (unsigned char)eu[e], (unsigned char)ev[e], (unsigned char)e}; } }
              nops[ncy] = no; crt[ncy] = st; ncy++; }
            for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) {
              int c4 = ((md * nt + k) * 4 + fm) * 700 + pi; lcB[c4]++; leB[c4] += cE;
              double ns = 1.0; int ok = 1;
              for (int c = 0; c < ncy && ok; c++) { int cnt = 0;
                for (int rho = 0; rho < 26; rho++) { unsigned char val[NV]; val[crt[c]] = rho; int good = 1;
                  for (int o = 0; o < nops[c]; o++) { Op op = ops[c][o]; int t = et[op.t];
                    if (op.typ == 0) val[op.w] = op.w < m ? GG[k][fm][t][Lt[t]][val[op.from]] : FF[k][fm][t][Lt[t]][val[op.from]];
                    else if (FF[k][fm][t][Lt[t]][val[op.w]] != val[op.from]) { good = 0; break; } }
                  cnt += good; }
                if (!cnt) ok = 0; ns *= cnt; }
              if (ok) { lfB[c4]++; lsB[c4] += ns; if (cE <= PE) {
                #pragma omp critical
                printf("M B %s %d %d %c %s %c%c %d %d %.4g %.0f\n", lab, r->q, r->d, isrec ? 'D' : (md ? 'C' : 'P'), TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', m, n, cE, ns); } }
            } }
        } } }
    #pragma omp critical
    { for (int i = 0; i < CA; i++) { cA[i] += lcA[i]; fA[i] += lfA[i]; eA[i] += leA[i]; }
      for (int i = 0; i < CB; i++) { cB[i] += lcB[i]; fB[i] += lfB[i]; sB[i] += lsB[i]; eB[i] += leB[i]; } }
  }
  const char *ACN[3] = {"AZ", "KA", "OTHER"};
  for (int md = 0; md < NM; md++) {
    for (int ac = 0; ac < NAC; ac++) for (int fm = 0; fm < 2; fm++) for (int pi = 0; pi < npA[md]; pi++) { int k3 = ((md * NAC + ac) * 2 + fm) * 400 + pi;
      printf("H A %s %c %s %s %d %d %lld %lld %.6g\n", lab, isrec ? 'D' : (md ? 'C' : 'P'), na == 1 ? AN[0] : ACN[ac], fm ? "beau" : "vig", pAm[md][pi], pAn[md][pi], cA[k3], fA[k3], eA[k3]); }
    for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) for (int pi = 0; pi < npB[md]; pi++) { int c4 = ((md * nt + k) * 4 + fm) * 700 + pi;
      printf("H B %s %c %s %c%c %d %d %lld %lld %.6g %.6g\n", lab, isrec ? 'D' : (md ? 'C' : 'P'), TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', pBm[md][pi], pBn[md][pi], cB[c4], fB[c4], sB[c4], eB[c4]); }
  }
  printf("END %s %s %s q %ld-%ld records %lld alphas %d tabpairs %d\n", lab, mode, kind, qlo, qhi, nrec, na, nt);
  return 0;
}

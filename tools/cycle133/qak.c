/* Cycle 133: key-at-plaintext autokey families behind the 165k bank, hashed.
   Model Q: substitution at the plaintext position, then one bank transposition
   (either direction).  Each permutation is reduced to the crib letters that the
   primer length can determine; a hash hit is fully decrypted and checked
   against all 24 official crib letters.

   Families
   (Q)  Quagmire III PT-autokey.  Keyed alphabet from word W (unique letters then
        A-Z remainder: the K1/K2 construction).  Primer R of length L.
        I[i] = enc(P[i], K[i]) on that alphabet, K[i] = R[i] (i < L) else P[i-L].
        Directions: Vigenere / Beaufort / variant Beaufort.
   (KA) Repeating keyword W on the A-Z or KRYPTOS tableau, then PT-autokey with
        primer R whose feedback is the first layer's output I1.
   (AK) PT-autokey of P with primer R, then repeating keyword W.  Both layers
        share one AZ or KA tableau; 3 x 3 directions.

   Primer lengths 3..10: n = 24-2L determined crib letters, enough for the hash
   filter.  CT-fed autokey is blind on this vocabulary (longest word 14; a CT
   primer must reach position 21 before any crib I-letter is determined).
   L >= 11 left open (n <= 2, filter underpowered).

   usage: qak CT words.txt perms.bin label lo hi
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 97
#define HB 21
#define HMASK ((1<<HB)-1)
#define MAXW 20000
#define MAXN 340000
#define LMIN 3
#define LMAX 10

static const char *KASTR = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const char *C1 = "EASTNORTHEAST";
static const char *C2 = "BERLINCLOCK";

static int AZ_A[26], AZ_I[26], KA_A[26], KA_I[26];
static char W1[MAXW][32], W2[MAXW][32];
static int L1[MAXW], L2[MAXW];
static int cp[24], cl[24];
static int C[N];
static short *Perm;
static long np;

static uint64_t keyA[1<<HB], keyB[1<<HB];
static int32_t hd[1<<HB];
static int32_t nperm[MAXN], nnext[MAXN];
static int nused;

static int op(int f, int a, int s){
  int r = f==0 ? a+s : f==1 ? s-a : a-s;
  return ((r % 26) + 26) % 26;
}
static int enc(const int *A, const int *inv, int f, int p, int k){
  return A[op(f, inv[p], inv[k])];
}
static int dec(const int *A, const int *inv, int f, int c, int k){
  /* inverse of enc: vig C=A[p+k] => p=c-k; beau C=A[k-p] => p=k-c; var C=A[p-k] => p=c+k */
  int ci = inv[c], ki = inv[k];
  int r = f==0 ? ci-ki : f==1 ? ki-ci : ci+ki;
  return A[((r % 26) + 26) % 26];
}

static int rd(const char *fn, char W[][32], int *L){
  FILE *f = fopen(fn, "r");
  if (!f) { perror(fn); exit(1); }
  int n = 0;
  while (n < MAXW && fscanf(f, "%31s", W[n]) == 1) { L[n] = (int)strlen(W[n]); n++; }
  fclose(f);
  return n;
}

static void keyed(const char *w, int *A, int *inv){
  int used[26] = {0}, n = 0;
  for (const char *p = w; *p; p++) {
    int c = *p - 'A';
    if (c >= 0 && c < 26 && !used[c]) { used[c] = 1; A[n++] = c; }
  }
  for (int c = 0; c < 26; c++) if (!used[c]) A[n++] = c;
  for (int i = 0; i < 26; i++) inv[A[i]] = i;
}

static uint64_t hh(uint64_t a, uint64_t b){
  uint64_t h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  return h ^ (h >> 29);
}

static void hclear(void){ memset(hd, -1, sizeof hd); nused = 0; }

static void pack(const int *lets, int n, uint64_t *a, uint64_t *b){
  int n1 = n / 2, n2 = n - n1;
  uint64_t x = 0, y = 0;
  for (int t = 0; t < n1; t++) x = x * 26 + (uint64_t)lets[t];
  for (int t = 0; t < n2; t++) y = y * 26 + (uint64_t)lets[n1 + t];
  *a = x; *b = y;
}

static void ins(uint64_t a, uint64_t b, int v){
  uint64_t h = hh(a, b) & HMASK;
  while (hd[h] >= 0 && !(keyA[h] == a && keyB[h] == b)) h = (h + 1) & HMASK;
  if (hd[h] < 0) { keyA[h] = a; keyB[h] = b; }
  if (nused >= MAXN) { fprintf(stderr, "node pool full\n"); exit(1); }
  nperm[nused] = v; nnext[nused] = hd[h]; hd[h] = nused++;
}

static int look(uint64_t a, uint64_t b){
  uint64_t h = hh(a, b) & HMASK;
  while (hd[h] >= 0) {
    if (keyA[h] == a && keyB[h] == b) return hd[h];
    h = (h + 1) & HMASK;
  }
  return -1;
}

/* determined crib-indices for primer length L (n = 24-2L) */
static int det_idx[16][24], det_n[16];
static void init_det(void){
  for (int L = LMIN; L <= LMAX; L++) {
    int n = 0;
    for (int t = 0; t < 13; t++) if (t >= L) det_idx[L][n++] = t;
    for (int t = 0; t < 11; t++) if (t >= L) det_idx[L][n++] = 13 + t;
    det_n[L] = n; /* 24-2L */
  }
}

static void sig_from_perm(const short *s, int L, uint64_t *a, uint64_t *b){
  int lets[24];
  int n = det_n[L];
  for (int t = 0; t < n; t++) lets[t] = C[s[cp[det_idx[L][t]]]];
  pack(lets, n, a, b);
}

static void get_sigma(int v, short *out){
  if (v < np) {
    memcpy(out, Perm + (long)v * N, N * sizeof(short));
  } else {
    const short *s = Perm + (v - np) * N;
    for (int i = 0; i < N; i++) out[s[i]] = (short)i;
  }
}

static int check_cribs(const int *P){
  for (int t = 0; t < 24; t++) if (P[cp[t]] != cl[t]) return 0;
  return 1;
}

/* recover I[i] = C[sigma[i]], decrypt family, require all 24 cribs */
static int verify_Q(int v, const int *A, const int *inv, int f, const char *pr, int Lp){
  short s[N]; get_sigma(v, s);
  int I[N], P[N];
  for (int i = 0; i < N; i++) I[i] = C[s[i]];
  for (int i = 0; i < N; i++) {
    int k = (i < Lp) ? pr[i] - 'A' : P[i - Lp];
    P[i] = dec(A, inv, f, I[i], k);
  }
  return check_cribs(P);
}
static int verify_KA(int v, const int *A, const int *inv, int f1, int f2,
                     const char *w, int Lw, const char *pr, int Lp){
  /* I2 --dec autokey(f2, key=primer|I1)--> I1 --dec keyword(f1)--> P */
  short s[N]; get_sigma(v, s);
  int I2[N], I1[N], P[N];
  for (int i = 0; i < N; i++) I2[i] = C[s[i]];
  for (int i = 0; i < N; i++) {
    int k = (i < Lp) ? pr[i] - 'A' : I1[i - Lp];
    I1[i] = dec(A, inv, f2, I2[i], k);
    P[i] = dec(A, inv, f1, I1[i], w[i % Lw] - 'A');
  }
  return check_cribs(P);
}
static int verify_AK(int v, const int *A, const int *inv, int f1, int f2,
                     const char *w, int Lw, const char *pr, int Lp){
  /* I2 --dec keyword(f2)--> I1 --dec autokey(f1, key=primer|P)--> P */
  short s[N]; get_sigma(v, s);
  int I2[N], I1[N], P[N];
  for (int i = 0; i < N; i++) {
    I2[i] = C[s[i]];
    I1[i] = dec(A, inv, f2, I2[i], w[i % Lw] - 'A');
  }
  for (int i = 0; i < N; i++) {
    int k = (i < Lp) ? pr[i] - 'A' : P[i - Lp];
    P[i] = dec(A, inv, f1, I1[i], k);
  }
  return check_cribs(P);
}

static void emit(const char *lab, const char *fam, const char *w1, const char *w2,
                 int T, int f1, int f2, int v){
  printf("S %s %s %s %s T=%d f1=%d f2=%d perm=%ld dir=%d\n",
         lab, fam, w1, w2, T, f1, f2, (long)(v % np), (int)(v / np));
}

int main(int argc, char **argv){
  if (argc < 7) {
    fprintf(stderr, "usage: qak CT words.txt perms.bin label lo hi\n");
    return 2;
  }
  const char *Cs = argv[1];
  if ((int)strlen(Cs) != N) { fprintf(stderr, "CT length %zu != 97\n", strlen(Cs)); return 2; }
  for (int i = 0; i < N; i++) C[i] = Cs[i] - 'A';
  int n1 = rd(argv[2], W1, L1);
  /* same file for both sides */
  int n2 = rd(argv[2], W2, L2);
  const char *lab = argv[4];
  long lo = atol(argv[5]), hi = atol(argv[6]);
  if (hi > n1) hi = n1;
  if (lo < 0) lo = 0;

  for (int i = 0; i < 26; i++) { AZ_A[i] = i; AZ_I[i] = i; }
  for (int i = 0; i < 26; i++) KA_A[i] = KASTR[i] - 'A';
  for (int i = 0; i < 26; i++) KA_I[KA_A[i]] = i;

  for (int i = 0; i < 13; i++) { cp[i] = 21 + i; cl[i] = C1[i] - 'A'; }
  for (int i = 0; i < 11; i++) { cp[13 + i] = 63 + i; cl[13 + i] = C2[i] - 'A'; }
  init_det();

  FILE *pf = fopen(argv[3], "rb");
  if (!pf) { perror(argv[3]); return 1; }
  fseek(pf, 0, SEEK_END);
  np = ftell(pf) / (2 * N);
  rewind(pf);
  Perm = malloc((size_t)np * N * sizeof(short));
  if (!Perm) { fprintf(stderr, "malloc perms\n"); return 1; }
  if (fread(Perm, 2, (size_t)np * N, pf) != (size_t)np * N) { fprintf(stderr, "read perms\n"); return 1; }
  fclose(pf);

  long cfg = 0, surv = 0, nsig_total = 0, skipped = 0;

  for (int L = LMIN; L <= LMAX; L++) {
    hclear();
    long nsig = 0;
    for (long q = 0; q < np; q++) {
      const short *s = Perm + q * N;
      short u[N];
      for (int i = 0; i < N; i++) u[s[i]] = (short)i;
      uint64_t a, b;
      sig_from_perm(s, L, &a, &b); ins(a, b, (int)q);
      sig_from_perm(u, L, &a, &b); ins(a, b, (int)(np + q));
      nsig += 2;
    }
    nsig_total = nsig;

    /* Primers of this length.  For L<=10 no crib sits in the primer region, so
       the partial signature does not depend on the primer letters — only on W,
       L and the setting.  Look up once, then try every primer only on a hit. */
    int pidx[MAXW], npL = 0;
    for (int y = 0; y < n2; y++) if (L2[y] == L) pidx[npL++] = y;

    for (long x = lo; x < hi; x++) {
      const char *w = W1[x];
      int lw = L1[x];
      int QA[26], QI[26];
      keyed(w, QA, QI);

      /* --- (Q) Quagmire III PT-autokey: 3 directions --- */
      for (int f = 0; f < 3; f++) {
        int lets[24];
        for (int t = 0; t < det_n[L]; t++) {
          int idx = det_idx[L][t];
          lets[t] = enc(QA, QI, f, cl[idx], cl[idx - L]);
        }
        uint64_t a, b; pack(lets, det_n[L], &a, &b);
        int nd0 = look(a, b);
        cfg += npL;
        if (nd0 >= 0) {
          for (int yi = 0; yi < npL; yi++) {
            const char *pr = W2[pidx[yi]];
            for (int nd = nd0; nd >= 0; nd = nnext[nd]) {
              if (verify_Q(nperm[nd], QA, QI, f, pr, L)) {
                surv++; emit(lab, "Q", w, pr, 2, f, -1, nperm[nd]);
              }
            }
          }
        }
      }

      /* --- (KA) and (AK) on AZ (T=0) and KA (T=1), 3 x 3 directions --- */
      for (int T = 0; T < 2; T++) {
        const int *A = T ? KA_A : AZ_A;
        const int *inv = T ? KA_I : AZ_I;
        for (int f1 = 0; f1 < 3; f1++) for (int f2 = 0; f2 < 3; f2++) {
          /* KA: I1 = enc_kw(P, W); I2 = enc_ak(I1, previous I1) */
          {
            int lets[24];
            for (int t = 0; t < det_n[L]; t++) {
              int idx = det_idx[L][t];
              int i = cp[idx], i0 = cp[idx - L];
              int I1p = enc(A, inv, f1, cl[idx], w[i % lw] - 'A');
              int I1k = enc(A, inv, f1, cl[idx - L], w[i0 % lw] - 'A');
              lets[t] = enc(A, inv, f2, I1p, I1k);
            }
            uint64_t a, b; pack(lets, det_n[L], &a, &b);
            int nd0 = look(a, b);
            cfg += npL;
            if (nd0 >= 0) {
              for (int yi = 0; yi < npL; yi++) {
                const char *pr = W2[pidx[yi]];
                for (int nd = nd0; nd >= 0; nd = nnext[nd]) {
                  if (verify_KA(nperm[nd], A, inv, f1, f2, w, lw, pr, L)) {
                    surv++; emit(lab, "KA", w, pr, T, f1, f2, nperm[nd]);
                  }
                }
              }
            }
          }
          /* AK: I1 = enc_ak(P, previous P); I2 = enc_kw(I1, W) */
          {
            int lets[24];
            for (int t = 0; t < det_n[L]; t++) {
              int idx = det_idx[L][t];
              int i = cp[idx];
              int I1p = enc(A, inv, f1, cl[idx], cl[idx - L]);
              lets[t] = enc(A, inv, f2, I1p, w[i % lw] - 'A');
            }
            uint64_t a, b; pack(lets, det_n[L], &a, &b);
            int nd0 = look(a, b);
            cfg += npL;
            if (nd0 >= 0) {
              for (int yi = 0; yi < npL; yi++) {
                const char *pr = W2[pidx[yi]];
                for (int nd = nd0; nd >= 0; nd = nnext[nd]) {
                  if (verify_AK(nperm[nd], A, inv, f1, f2, w, lw, pr, L)) {
                    surv++; emit(lab, "AK", w, pr, T, f1, f2, nperm[nd]);
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  /* count skipped primer lengths (L<3 or L>10) for the rows this worker saw, so totals add up */
  for (long x = lo; x < hi; x++)
    for (int y = 0; y < n2; y++)
      if (L2[y] < LMIN || L2[y] > LMAX) skipped++;

  printf("C %s configs %ld signatures %ld survivors %ld skipped_pairs %ld\n",
         lab, cfg, nsig_total, surv, skipped);
  return 0;
}

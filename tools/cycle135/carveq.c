/* Cycle 135: transposition-first periodic Quagmire with vocabulary alphabets.
   After a bank transposition the periodic key is read at the carved position
   (residue = carved_index % L).  Each permutation is bucketed by the 24 crib
   landing residues; implied key letters must agree inside each bucket, so any
   key of length L is tested (not just dictionary words).

   ix=0: key at the plaintext position, then transpose (model Q, cycle 13).
   ix=1: transpose first, key at the carved position (the new index).

   Families
     III  Quagmire III: PA = CA = keyed(W)   (K1/K2 construction)
     I    Quagmire I:   PA = keyed(W), CA = A-Z
     II   Quagmire II:  PA = A-Z,      CA = keyed(W)
   Modes: vig (K = C-P; variant Beaufort is the dual and shares consistency)
          beau (K = C+P).

   usage: carveq CT words.txt perms.bin label lo hi [PMAX]
   A configuration is a survivor if it is crib-consistent with at least MINCHK
   extra constraints.  Survivors are fully checked against all 24 crib letters.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 97
#define MAXW 12000
#define MINCHK 6
#define PDEFAULT 16

static const int CI[24] = {
  21,22,23,24,25,26,27,28,29,30,31,32,33,
  63,64,65,66,67,68,69,70,71,72,73
};
static const char *PT = "EASTNORTHEASTBERLINCLOCK";

static char W[MAXW][32];
static int WL[MAXW];
static unsigned char A[MAXW][26], INV[MAXW][26];
static int PV[MAXW][24];          /* PA-index of each crib letter (QIII / QI) */
static int PV_AZ[24];             /* A-Z index of each crib letter (QII) */

static void keyed(const char *w, unsigned char *alph, unsigned char *inv){
  int used[26] = {0}, n = 0;
  for (const char *p = w; *p; p++) {
    int c = *p - 'A';
    if (c < 0 || c > 25 || used[c]) continue;
    used[c] = 1; alph[n++] = (unsigned char)c;
  }
  for (int c = 0; c < 26; c++) if (!used[c]) alph[n++] = (unsigned char)c;
  for (int i = 0; i < 26; i++) inv[alph[i]] = (unsigned char)i;
}

int main(int argc, char **argv){
  if (argc < 7) {
    fprintf(stderr, "usage: carveq CT words.txt perms.bin label lo hi [PMAX]\n");
    return 1;
  }
  const char *Cs = argv[1];
  if ((int)strlen(Cs) != N) { fprintf(stderr, "CT length %zu != 97\n", strlen(Cs)); return 1; }
  int C[N];
  for (int i = 0; i < N; i++) C[i] = Cs[i] - 'A';
  const char *lab = argv[4];
  long lo = atol(argv[5]), hi = atol(argv[6]);
  int PMAX = argc > 7 ? atoi(argv[7]) : PDEFAULT;
  if (PMAX < 1) PMAX = 1;
  if (PMAX > 32) PMAX = 32;

  FILE *wf = fopen(argv[2], "r");
  if (!wf) { perror(argv[2]); return 1; }
  int nw = 0;
  while (nw < MAXW && fscanf(wf, "%31s", W[nw]) == 1) {
    WL[nw] = (int)strlen(W[nw]);
    keyed(W[nw], A[nw], INV[nw]);
    nw++;
  }
  fclose(wf);
  if (lo < 0) lo = 0;
  if (hi > nw) hi = nw;
  if (lo >= hi) {
    printf("C %s x x x x 0 consistent 0 survivors 0 alphabets 0-%ld\n", lab, (long)nw);
    return 0;
  }

  for (int i = 0; i < 24; i++) {
    int p = PT[i] - 'A';
    PV_AZ[i] = p;
    for (int a = 0; a < nw; a++) PV[a][i] = INV[a][p];
  }

  FILE *pf = fopen(argv[3], "rb");
  if (!pf) { perror(argv[3]); return 1; }
  fseek(pf, 0, SEEK_END);
  long np = ftell(pf) / (2 * N);
  rewind(pf);
  short *Perm = malloc((size_t)np * N * sizeof(short));
  if (!Perm || fread(Perm, sizeof(short), (size_t)np * N, pf) != (size_t)np * N) {
    fprintf(stderr, "failed to read perms\n"); return 1;
  }
  fclose(pf);

  /* Bucket census: unique carved-residue 24-tuples per period (printed once, from the lo==0 worker). */
  if (lo == 0 && getenv("CENSUS")) {
    enum { HB = 22, HMASK = (1 << HB) - 1 };
    uint64_t *ka = malloc((size_t)(1u << HB) * sizeof(uint64_t));
    uint64_t *kb = malloc((size_t)(1u << HB) * sizeof(uint64_t));
    unsigned char *occ = malloc((size_t)(1u << HB));
    if (ka && kb && occ) {
      for (int per = 1; per <= PMAX; per++) {
        memset(occ, 0, (size_t)(1u << HB));
        long long uniq = 0, tot = 0;
        for (long q = 0; q < np; q++) {
          const short *s = Perm + q * N;
          short u[N];
          for (int i = 0; i < N; i++) u[s[i]] = (short)i;
          for (int dir = 0; dir < 2; dir++) {
            const short *S = dir ? u : s;
            uint64_t a = 0, b = 0;
            for (int t = 0; t < 12; t++) a = a * (uint64_t)per + (unsigned)(S[CI[t]] % per);
            for (int t = 12; t < 24; t++) b = b * (uint64_t)per + (unsigned)(S[CI[t]] % per);
            uint64_t h = (a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL);
            h &= HMASK;
            while (occ[h] && (ka[h] != a || kb[h] != b)) h = (h + 1) & HMASK;
            if (!occ[h]) { occ[h] = 1; ka[h] = a; kb[h] = b; uniq++; }
            tot++;
          }
        }
        printf("B %s p=%d buckets=%lld of %lld (%.3f perms/bucket)\n", lab, per, uniq, tot, tot / (double)uniq);
      }
    }
    free(ka); free(kb); free(occ);
  }

  long long tests = 0, cons = 0, surv = 0;
  long long hist[3][2][2][33]; /* fam, mode, ix, L */
  memset(hist, 0, sizeof hist);
  const char *FN[3] = {"I", "II", "III"};
  const char *MN[2] = {"vig", "beau"};
  const char *XN[2] = {"pt", "carved"};

  for (long q = 0; q < np; q++) {
    const short *s = Perm + q * N;
    short u[N];
    for (int i = 0; i < N; i++) u[s[i]] = (short)i;
    for (int dir = 0; dir < 2; dir++) {
      const short *S = dir ? u : s;
      int tc[24];
      for (int t = 0; t < 24; t++) tc[t] = S[CI[t]];

      /* Constraint pairs for each (ix, period): chain of crib indices sharing a residue. */
      int npair[2][33];
      unsigned char pi[2][33][24], pj[2][33][24];
      for (int ix = 0; ix < 2; ix++) {
        for (int per = 1; per <= PMAX; per++) {
          int last[32];
          for (int r = 0; r < per; r++) last[r] = -1;
          int n = 0;
          for (int i = 0; i < 24; i++) {
            int r = (ix ? tc[i] : CI[i]) % per;
            if (last[r] >= 0) { pi[ix][per][n] = (unsigned char)last[r]; pj[ix][per][n] = (unsigned char)i; n++; }
            last[r] = i;
          }
          npair[ix][per] = n;
        }
      }

      int CT_AZ[24];
      for (int t = 0; t < 24; t++) CT_AZ[t] = C[tc[t]];

      for (long a = lo; a < hi; a++) {
        int Pv3[24], Pv1[24], Cv3[24], Cv1[24], Cv2[24];
        const unsigned char *In = INV[a];
        for (int t = 0; t < 24; t++) {
          Pv3[t] = PV[a][t];
          Pv1[t] = PV[a][t];
          Cv3[t] = In[CT_AZ[t]];
          Cv1[t] = CT_AZ[t];          /* CA = A-Z */
          Cv2[t] = In[CT_AZ[t]];
        }
        /* fam 0=I (P keyed, C AZ), 1=II (P AZ, C keyed), 2=III (both keyed) */
        int *Pvs[3] = { Pv1, PV_AZ, Pv3 };
        int *Cvs[3] = { Cv1, Cv2, Cv3 };

        for (int fam = 0; fam < 3; fam++) {
          int *Pp = Pvs[fam], *Cc = Cvs[fam];
          for (int m = 0; m < 2; m++) {
            int kvv[24];
            if (m == 0) for (int t = 0; t < 24; t++) kvv[t] = (Cc[t] - Pp[t] + 26) % 26;
            else        for (int t = 0; t < 24; t++) kvv[t] = (Cc[t] + Pp[t]) % 26;
            for (int ix = 0; ix < 2; ix++) {
              for (int per = 1; per <= PMAX; per++) {
                tests++;
                int n = npair[ix][per], ok = 1;
                unsigned char *pii = pi[ix][per], *pjj = pj[ix][per];
                for (int k = 0; k < n; k++) {
                  if (kvv[pii[k]] != kvv[pjj[k]]) { ok = 0; break; }
                }
                if (!ok) continue;
                cons++;
                hist[fam][m][ix][per]++;
                if (n < MINCHK) continue;
                /* Recover the (partial) key and verify all 24 crib letters. */
                int key[32];
                for (int r = 0; r < per; r++) key[r] = -1;
                for (int t = 0; t < 24; t++) {
                  int r = (ix ? tc[t] : CI[t]) % per;
                  key[r] = kvv[t];
                }
                int crib_ok = 1;
                for (int t = 0; t < 24; t++) {
                  int r = (ix ? tc[t] : CI[t]) % per;
                  int expect = m == 0 ? (Pp[t] + key[r]) % 26 : (key[r] - Pp[t] + 26) % 26;
                  if (expect != Cc[t]) { crib_ok = 0; break; }
                }
                if (!crib_ok) continue;
                surv++;
                char ks[40];
                for (int r = 0; r < per; r++) {
                  if (key[r] < 0) ks[r] = '?';
                  else {
                    /* Letter in the cipher alphabet: QI uses A-Z, II/III use keyed(W). */
                    if (fam == 0) ks[r] = (char)('A' + key[r]);
                    else ks[r] = (char)('A' + A[a][key[r]]);
                  }
                }
                ks[per] = 0;
                char ps[N+1]; ps[N] = 0; int fully = 1;
                for (int r = 0; r < per; r++) if (key[r] < 0) fully = 0;
                if (fully) {
                  for (int i = 0; i < N; i++) {
                    int j = S[i];                 /* carved position of plaintext i */
                    int pos = ix ? j : i;         /* key index */
                    int kr = key[pos % per];
                    int cidx = (fam == 0) ? C[j] : In[C[j]];
                    int pidx = m == 0 ? (cidx - kr + 26) % 26 : (kr - cidx + 26) % 26;
                    int plet = (fam == 1) ? pidx : A[a][pidx];
                    ps[i] = (char)('A' + plet);
                  }
                } else {
                  ps[0] = 0;
                }
                printf("S %s fam=%s word=%s %s ix=%s p=%d perm=%ld dir=%d checks=%d key=%s",
                       lab, FN[fam], W[a], MN[m], XN[ix], per, q, dir, n, ks);
                if (fully) printf(" plain=%s", ps);
                printf("\n");
              }
            }
          }
        }
      }
    }
  }

  printf("C %s x x x x %lld consistent %lld survivors %lld alph=%ld..%ld nperm=%ld pmax=%d minchk=%d\n",
         lab, tests, cons, surv, lo, hi, np, PMAX, MINCHK);
  for (int fam = 0; fam < 3; fam++)
    for (int m = 0; m < 2; m++)
      for (int ix = 0; ix < 2; ix++) {
        printf("H %s fam=%s %s ix=%s", lab, FN[fam], MN[m], XN[ix]);
        for (int per = 1; per <= PMAX; per++) printf(" %d:%lld", per, hist[fam][m][ix][per]);
        printf("\n");
      }
  free(Perm);
  return 0;
}

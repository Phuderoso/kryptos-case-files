/* Cycle 120: one-crib-error audit of Quagmire I/II/III behind a transposition bank.
   Adapt of tools/c/periodic_perm.c (cycle 13). Same search space, but also allow exactly
   one crib letter dropped: remaining 23 must agree on the key letter in each residue class.

   Soft check is O(cribs), not 24 full retries: a period is soft-OK iff every residue has
   ≤1 distinct key among the cribs that remain after dropping one shared crib index.

   Usage:
     gcc -O3 -fopenmp -o q1crib120 q1crib120.c
     ./q1crib120 alpha.bin perm.bin CT M PMAX [PRINT_CAP]
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";

/* Analyse one (kv, residues) configuration.
   *ok24 = all 24 agree; *oksoft = some single drop works; *drop = which crib (or -1 if ok24). */
static inline void analyse(const int *kv, const int *res, int per,
                           int *ok24, int *oksoft, int *drop_out){
  /* For each residue: count of each key value, and which crib indices hold each value.
     We only need: number of distinct keys, and for each key the crib list (max 24). */
  int nkey[32];          /* distinct key count per residue */
  int keys[32][4];       /* up to 4 distinct keys tracked; >2 already fails soft */
  int kcnt[32][4];       /* how many cribs hold that key */
  int kcrib[32][4][8];   /* crib indices for that key (cap 8; if more, singleton impossible for that side) */
  memset(nkey,0,sizeof nkey);
  for(int i=0;i<24;i++){
    if(res[i]<0) continue;
    int r=res[i], k=kv[i];
    int found=-1;
    for(int j=0;j<nkey[r];j++) if(keys[r][j]==k){ found=j; break; }
    if(found<0){
      if(nkey[r]>=4){ /* too many distinct — soft fails */ nkey[r]=4; continue; }
      found=nkey[r]; keys[r][found]=k; kcnt[r][found]=0; nkey[r]++;
    }
    if(kcnt[r][found]<8) kcrib[r][found][kcnt[r][found]]=i;
    kcnt[r][found]++;
  }
  int strict=1, soft_possible=1;
  int required_drop=-2; /* -2=unset, -1=any/no drop needed for conflicts, >=0 = must drop this */
  for(int r=0;r<per;r++){
    if(nkey[r]<=1) continue;
    strict=0;
    if(nkey[r]>=3){ soft_possible=0; break; }
    /* exactly 2 distinct keys: one drop fixes iff one side is a singleton crib */
    int s0=kcnt[r][0], s1=kcnt[r][1];
    int cand=-1;
    if(s0==1 && s1>=1) cand=kcrib[r][0][0];
    else if(s1==1 && s0>=1) cand=kcrib[r][1][0];
    else { soft_possible=0; break; } /* both sides size>=2 */
    if(required_drop==-2) required_drop=cand;
    else if(required_drop!=cand){ soft_possible=0; break; }
  }
  *ok24=strict;
  if(strict){ *oksoft=1; *drop_out=-1; }
  else if(soft_possible && required_drop>=0){ *oksoft=1; *drop_out=required_drop; }
  else { *oksoft=0; *drop_out=-1; }
}

int main(int argc,char**argv){
  if(argc<6){ fprintf(stderr,"usage: %s alpha.bin perm.bin CT M PMAX [PRINT_CAP]\n",argv[0]); return 1; }
  FILE*f=fopen(argv[1],"rb"); if(!f) return 1; fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); if(fread(A,26,na,f)!=(size_t)na) return 1; fclose(f);
  f=fopen(argv[2],"rb"); if(!f) return 1; fseek(f,0,2); long nt=ftell(f)/194; fseek(f,0,0);
  short*Pm=malloc(nt*194); if(fread(Pm,194,nt,f)!=(size_t)nt) return 1; fclose(f);
  const char*CT=argv[3]; long M=atol(argv[4]); if(M>na) M=na; int PMAX=atoi(argv[5]);
  int PRINT_CAP=argc>6?atoi(argv[6]):0;
  unsigned char*INV=malloc(na*26);
  for(long a=0;a<na;a++) for(int j=0;j<26;j++) INV[a*26+A[a*26+j]]=j;

  long long hist_s[64], hist_soft[64], hist_only[64];
  memset(hist_s,0,sizeof hist_s); memset(hist_soft,0,sizeof hist_soft); memset(hist_only,0,sizeof hist_only);
  long long total_s=0, total_soft=0, total_only=0;
  int printed=0;

  #pragma omp parallel
  {
    long long hs[64], hsoft[64], honly[64];
    memset(hs,0,sizeof hs); memset(hsoft,0,sizeof hsoft); memset(honly,0,sizeof honly);
    long long ts=0,tsoft=0,tonly=0;
    #pragma omp for schedule(dynamic,64)
    for(long t=0;t<nt;t++){
      const short*p=Pm+t*97; int tc[24];
      for(int i=0;i<24;i++) tc[i]=p[CI[i]];
      for(long a=0;a<M;a++) for(int pr=0;pr<3;pr++){
        if(pr&&a==0) continue;
        const unsigned char*ip=INV+(pr==1?0:a)*26, *ic=INV+(pr==2?0:a)*26;
        int Pv[24],Cv[24];
        for(int i=0;i<24;i++){ Pv[i]=ip[PT[i]-65]; Cv[i]= tc[i]<0?0:ic[(unsigned char)CT[tc[i]]-65]; }
        for(int m=0;m<2;m++){
          int kv[24];
          for(int i=0;i<24;i++) kv[i]=m?(Cv[i]+Pv[i])%26:(Cv[i]-Pv[i]+26)%26;
          for(int ix=0;ix<2;ix++){
            int res_pt[24], res_cv[24];
            /* precompute residues for all periods? periods differ — compute per period */
            for(int per=1;per<=PMAX;per++){
              int res[24];
              for(int i=0;i<24;i++){
                if(tc[i]<0) res[i]=-1;
                else res[i]=(ix?tc[i]:CI[i])%per;
              }
              int ok24, oksoft, drop;
              analyse(kv,res,per,&ok24,&oksoft,&drop);
              if(ok24){ hs[per]++; ts++; }
              if(oksoft){ hsoft[per]++; tsoft++; }
              if(oksoft&&!ok24){
                honly[per]++; tonly++;
                if(PRINT_CAP){
                  #pragma omp critical
                  if(printed<PRINT_CAP){
                    printed++;
                    printf("SOFT_ONLY t=%ld a=%ld pair=%s %s idx=%s p=%d drop=%d key=",
                      t,a,pr==0?"QIII":pr==1?"QII":"QI", m?"beau":"vig", ix?"carved":"pt", per, drop);
                    int key[32]; for(int r=0;r<per;r++) key[r]=-1;
                    for(int i=0;i<24;i++){
                      if(i==drop||tc[i]<0) continue;
                      int r=res[i];
                      if(key[r]<0) key[r]=kv[i];
                    }
                    for(int r=0;r<per;r++) printf("%c",key[r]<0?'?':'A'+key[r]);
                    printf("\n");
                  }
                }
              }
            }
          }
        }
      }
    }
    #pragma omp critical
    {
      for(int i=0;i<64;i++){ hist_s[i]+=hs[i]; hist_soft[i]+=hsoft[i]; hist_only[i]+=honly[i]; }
      total_s+=ts; total_soft+=tsoft; total_only+=tonly;
    }
  }
  printf("TRANSPOSITIONS %ld ALPHABETS_USED %ld PMAX %d\n",nt,M,PMAX);
  printf("TOTAL_STRICT %lld TOTAL_SOFT %lld TOTAL_SOFT_ONLY %lld\n",total_s,total_soft,total_only);
  printf("HIST_STRICT"); for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist_s[i]); printf("\n");
  printf("HIST_SOFT"); for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist_soft[i]); printf("\n");
  printf("HIST_SOFT_ONLY"); for(int i=1;i<=PMAX;i++) printf(" %d:%lld",i,hist_only[i]); printf("\n");
  return 0;
}

/* Cycle 95: generalized Chaocipher-style dynamic wheels. Each wheel's move after a letter found at index k:
   rotate so index (k+o) is at the zenith, pluck the letter at position p, re-insert it at position q.
   Moves depend only on k, so the cycle-94 lemma holds: input wheel enumerated, output wheel arbitrary (any of 26!).
   Rubin's Chaocipher = left (o0,p1,q13), right (o1,p2,q13).
   Rule grid per wheel: o in {0,1,2}, p in 1..5, q in {12,13,14} -> 45; all 2025 (input,output) rule pairs.
   Usage: ./chaogen CT alphabets.bin M   [prints hits; summary of near-misses]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
typedef struct{int o,p,q;} Rule;
static inline void mv(unsigned char*w,int k,Rule r){unsigned char t[26];int s=k+r.o;for(int j=0;j<26;j++)t[j]=w[(s+j)%26];
  unsigned char x=t[r.p]; if(r.q>r.p){memmove(t+r.p,t+r.p+1,r.q-r.p);} else if(r.q<r.p){memmove(t+r.q+1,t+r.q,r.p-r.q);} t[r.q]=x; memcpy(w,t,26);}
int main(int argc,char**argv){ const char*CT=argv[1]; FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  unsigned char*A=malloc(na*26); fread(A,26,na,f); fclose(f); long M=atol(argv[3]); if(M>na)M=na;
  Rule R[45]; int nr=0; int os[3]={0,1,2},qs[3]={12,13,14}; for(int a=0;a<3;a++)for(int p=1;p<=5;p++)for(int b=0;b<3;b++){R[nr].o=os[a];R[nr].p=p;R[nr].q=qs[b];nr++;}
  int pa[13],pb[13],np=0,da[300],db[300],nd=0; for(int a=0;a<24;a++)for(int b=a+1;b<24;b++){ if(PT[a]==PT[b]){pa[np]=a;pb[np]=b;np++;} else {da[nd]=a;db[nd]=b;nd++;} }
  long long runs=0,hits=0,eqall=0;
  #pragma omp parallel for schedule(dynamic,8) reduction(+:runs,hits,eqall)
  for(long a=0;a<M;a++) for(int ri=0;ri<nr;ri++) for(int ro=0;ro<nr;ro++){ unsigned char in[26],out[26],u[74];
    memcpy(in,A+a*26,26); for(int k=0;k<26;k++)out[k]=k;
    for(int j=0;j<74;j++){ int x=CT[j]-65,i=0; while(in[i]!=x)i++; u[j]=out[i]; mv(in,i,R[ri]); mv(out,i,R[ro]); }
    runs++; int ok=1; for(int q=0;q<np&&ok;q++) if(u[CI[pa[q]]]!=u[CI[pb[q]]]) ok=0; if(!ok) continue; eqall++;
    for(int q=0;q<nd&&ok;q++) if(u[CI[da[q]]]==u[CI[db[q]]]) ok=0;
    if(ok){ hits++;
      #pragma omp critical
      printf("HIT a=%ld in=(%d,%d,%d) out=(%d,%d,%d)\n",a,R[ri].o,R[ri].p,R[ri].q,R[ro].o,R[ro].p,R[ro].q); } }
  printf("ALPHABETS %ld RULEPAIRS %d RUNS %lld EQ_ALL %lld HITS %lld\n",M,nr*nr,runs,eqall,hits); return 0; }

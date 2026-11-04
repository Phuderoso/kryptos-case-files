/* Cycle 55b: classic Ragbaby (step d=1, both directions) followed by a transposition: intermediate I[j]=CT[p[j]]
   for each of the 96,630 cycle-12 permutations (c12_perm.bin, uint16 x 97, enc and dec forms), tested against the
   cribs exactly as in ragbaby.c, over a themed subset of alphabets (themed_idx.txt).
   usage: ragperm CT alpha.bin c12_perm.bin themed_idx.txt [p0 p1] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define LMAX 20
static const char *C[2]={"EASTNORTHEAST","BERLINCLOCK"}; static const int P[2]={21,63},L[2]={13,11};
static int G_cnt,G_L,G_P; static const int*G_t;
static void dfs(int j,int start,int cur){
  if(G_cnt) return; if(j==G_L){ G_cnt++; return; }
  int pos=G_P+j;
  if(G_t[j]==cur) dfs(j+1,start,cur);
  if(start>=0){ if(G_t[j]==((cur+1-(pos-start))%26+26)%26) dfs(j+1,pos,G_t[j]); }
  else { for(int len=pos-G_P;len<=LMAX;len++) if(G_t[j]==((cur+1-len)%26+26)%26){ dfs(j+1,pos,G_t[j]); break; } }
}
static int fit(int cb,const int*t){ G_cnt=0;G_L=L[cb];G_P=P[cb];G_t=t; dfs(1,-1,t[0]); return G_cnt; }
int main(int argc,char**argv){
  const char*ct=argv[1];
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); int NA=ftell(f)/26; rewind(f); unsigned char(*AL)[26]=malloc(NA*26); if(fread(AL,26,NA,f)!=(size_t)NA)return 1; fclose(f);
  f=fopen(argv[3],"rb"); fseek(f,0,2); int NP=ftell(f)/(2*N); rewind(f); unsigned short(*PM)[N]=malloc((size_t)NP*N*2); if(fread(PM,2*N,NP,f)!=(size_t)NP)return 1; fclose(f);
  int *S=malloc(sizeof(int)*NA),ns=0; f=fopen(argv[4],"r"); while(fscanf(f,"%d",&S[ns])==1) ns++; fclose(f);
  int p0= argc>5?atoi(argv[5]):0, p1= argc>6?atoi(argv[6]):NP;
  static int IDX[86731][26]; for(int k=0;k<ns;k++) for(int i=0;i<26;i++) IDX[k][AL[S[k]][i]]=i;
  long c1=0,c2=0,both=0;
  for(int p=p0;p<p1;p++){ unsigned char I[N]; for(int j=0;j<N;j++) I[j]=ct[PM[p][j]]-'A';
    for(int k=0;k<ns;k++){ int*idx=IDX[k];
      for(int dir=-1;dir<=1;dir+=2){ int t[13], ok;
        for(int j=0;j<13;j++){ int pos=21+j; t[j]=((dir*(idx[I[pos]]-idx[C[0][j]-'A'])-pos)%26+26)%26; }
        ok=fit(0,t); if(!ok) continue; c1++;
        for(int j=0;j<11;j++){ int pos=63+j; t[j]=((dir*(idx[I[pos]]-idx[C[1][j]-'A'])-pos)%26+26)%26; }
        if(fit(1,t)){ both++; if(both<=20) printf("BOTH perm=%d alpha=%d dir=%d\n",p,S[k],dir); }
      } } }
  printf("perms=%d..%d alphabets=%d crib1_fit=%ld both=%ld\n",p0,p1,ns,c1,both);
  return 0; }

/* Cycle 174 (IDEAS I-108): classic Ragbaby (step d = 1, both directions, any word division) on a keyed alphabet,
   followed by one of the 165,782 K3-law decimations / routes of all.bin (CT = T(Rag(P)); plaintext index i <->
   carved S[i], so the Ragbaby ciphertext at plaintext index i is C[S[i]]).  Crib test exactly as tools/ragperm.c
   (case 53): t_i = dir*(idx c_i - idx p_i) - i is constant inside a word and jumps by 1 - (b - a) at a word break;
   the word in progress at a crib start may have begun up to LMAX letters earlier.  Change from ragperm: t is computed
   lazily inside the DFS (same verdicts, faster), alphabets from a text list, perms from all.bin.
   usage: rag174 CT alpha.txt perms.bin label qlo qhi
   Output: B lab q alpha_label dir   (both cribs fit) ; R lab configs crib1 both ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define LMAX 20
#define MAXA 20000
static const char *CR[2]={"EASTNORTHEAST","BERLINCLOCK"}; static const int P0[2]={21,63},L[2]={13,11};
static int G_cnt,G_L,G_P,G_dir; static const int*G_idx; static const int*G_c; static const int*G_p;
static inline int tval(int j){int pos=G_P+j; int v=G_dir*(G_idx[G_c[j]]-G_idx[G_p[j]])-pos; v%=26; if(v<0)v+=26; return v;}
static void dfs(int j,int start,int cur){
  if(G_cnt) return; if(j==G_L){G_cnt++;return;}
  int pos=G_P+j, tj=tval(j);
  if(tj==cur) dfs(j+1,start,cur);
  if(G_cnt) return;
  if(start>=0){ if(tj==((cur+1-(pos-start))%26+26)%26) dfs(j+1,pos,tj); }
  else { for(int len=pos-G_P;len<=LMAX;len++) if(tj==((cur+1-len)%26+26)%26){ dfs(j+1,pos,tj); break; } }
}
static int fit(int cb,const int*c,const int*p,const int*idx,int dir){G_cnt=0;G_L=L[cb];G_P=P0[cb];G_c=c;G_p=p;G_idx=idx;G_dir=dir;dfs(1,-1,tval(0));return G_cnt;}
static int IDX[MAXA][26]; static char LB[MAXA][48];
int main(int argc,char**argv){
  if(argc<7)return 1; const char*Cs=argv[1]; if(strlen(Cs)!=N)return 1;
  int na=0; char al[64],lb[64]; FILE*f=fopen(argv[2],"r"); while(na<MAXA&&fscanf(f,"%63s %47s",al,lb)==2){for(int i=0;i<26;i++)IDX[na][al[i]-'A']=i;strcpy(LB[na],lb);na++;} fclose(f);
  f=fopen(argv[3],"rb"); fseek(f,0,2); long np=ftell(f)/(2*N); rewind(f); short*PM=malloc(np*N*2); if(fread(PM,2,np*N,f)!=(size_t)(np*N))return 2; fclose(f);
  const char*lab=argv[4]; long qlo=atol(argv[5]),qhi=atol(argv[6]); if(qhi>np)qhi=np;
  int p1[13],p2[11]; for(int j=0;j<13;j++)p1[j]=CR[0][j]-'A'; for(int j=0;j<11;j++)p2[j]=CR[1][j]-'A';
  long cfg=0,c1=0,both=0;
  for(long q=qlo;q<qhi;q++){const short*S=PM+q*N; int c1v[13],c2v[11];
    for(int j=0;j<13;j++)c1v[j]=Cs[S[21+j]]-'A'; for(int j=0;j<11;j++)c2v[j]=Cs[S[63+j]]-'A';
    for(int a=0;a<na;a++) for(int dir=-1;dir<=1;dir+=2){cfg++;
      if(!fit(0,c1v,p1,IDX[a],dir))continue; c1++;
      if(fit(1,c2v,p2,IDX[a],dir)){both++; printf("B %s %ld %s %d\n",lab,q,LB[a],dir);} } }
  printf("R %s %ld %ld %ld\nEND %s\n",lab,cfg,c1,both,lab); return 0; }

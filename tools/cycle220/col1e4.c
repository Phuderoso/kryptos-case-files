/* Cycle 220 (I-312 chunk 1): col1e.c of cycle 219 extended (diff kept minimal): optional NAL=4 adds Quagmire I (keyed PT alphabet, straight CT alphabet)
   and Quagmire II (straight PT, keyed CT) to the matching pairs A-Z/A-Z and KRYPTOS/KRYPTOS (= Quagmire III); optional SECOND fixes pi[1] (plant sub-slices).
   usage: col1e4 CT w first PMAX PPRINT label NAL [second]   (NAL=2 reproduces col1e exactly)
   Original header (cycle 219): every column order of width w (9 or 10) x periodic tableau key, ONE crib error tolerated.
   Written independently of tools/cycle124/allcol.c: the transposition is built by ranking grid cells
   (COL: by (read rank of column, row); ROW: by (row, read rank of column)), not by allcol's place() formula.
   Family (same as case 112): ragged 97-letter grid of width w, rotation 0, short last row = columns 0..97%w-1;
   COL = textbook columnar read, ROW = rows read with permuted columns; dir 0: carved[sig[i]] = layer[i], dir 1: sigma inverse.
   Key: periodic p, A-Z or KRYPTOS tableau, Vigenere (variant has the same consistency) or Beaufort,
   model A = key indexed by plaintext position (key before transposition), model B = by carved position (after).
   Test: excess = sum over residue classes of (class size - largest equal-value group). excess 0 = strict (all 24 agree),
   excess 1 = exactly one crib seat (wrong crib letter or wrong carved letter at a crib seat) disagrees.
   usage: col1e CT w first PMAX PPRINT label    (first = pi[0] slice, -1 = all orders)
   prints: H lines for every excess<=1 hit with p<=PPRINT and for every strict hit p<=PMAX;
           final C line: strict and one-error counts per p. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const int CRP[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *CRS="EASTNORTHEASTBERLINCLOCK";
static long s0[40], s1[40];
/* returns excess (0,1) or 2 meaning >=2; *bad = dropped seat for excess 1 (-1 if the class had 2 members: either seat) */
static int excess(const int *res,const int *kv,int p,int *bad){
  int v1[40],c1[40],v2[40],c2[40],e=0,cls=-1;
  for(int r=0;r<p;r++){c1[r]=0;c2[r]=0;}
  for(int t=0;t<24;t++){int r=res[t],v=kv[t];
    if(!c1[r]){v1[r]=v;c1[r]=1;continue;}
    if(v==v1[r]){c1[r]++;}
    else if(!c2[r]){v2[r]=v;c2[r]=1;}
    else if(v==v2[r]){c2[r]++;}
    else return 2;
    if(c2[r]){int m=c1[r]<c2[r]?c1[r]:c2[r]; if(m>=2) return 2; if(cls>=0&&cls!=r) return 2; cls=r;}
  }
  if(cls<0){*bad=-2;return 0;}
  e=c1[cls]<c2[cls]?c1[cls]:c2[cls]; if(e>1) return 2;
  if(c1[cls]==1&&c2[cls]==1){*bad=-1;return 1;}
  int minor=c1[cls]<c2[cls]?v1[cls]:v2[cls];
  for(int t=0;t<24;t++) if(res[t]==cls&&kv[t]==minor){*bad=t;break;}
  return 1;
}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  const char*s=argv[1]; int w=atoi(argv[2]), first=atoi(argv[3]), PMAX=atoi(argv[4]), PPRINT=atoi(argv[5]); const char*lab=argv[6]; int NAL=atoi(argv[7]); int SECOND=argc>8?atoi(argv[8]):-1;
  if((int)strlen(s)!=N){fprintf(stderr,"CT must be 97 letters\n");return 1;}
  int ct[N],ai[2][26]; for(int i=0;i<N;i++) ct[i]=s[i]-'A';
  for(int i=0;i<26;i++){ai[0][i]=i; ai[1][KA[i]-'A']=i;}
  static const int CA[4]={0,1,0,1}, PA[4]={0,1,1,0}; /* 0 AZ/AZ, 1 KA/KA (Quag III), 2 Quag I (PT keyed), 3 Quag II (CT keyed) */
  int pt[4][24]; for(int t=0;t<24;t++) for(int a=0;a<4;a++) pt[a][t]=ai[PA[a]][CRS[t]-'A'];
  int rows=(N+w-1)/w;
  int pi[16]; /* pi[c] = read rank of column c */
  int rest[16],nr=0;
  int f0 = first<0?0:first, f1 = first<0?w-1:first;
  long np=0;
  for(int f=f0;f<=f1;f++){
    nr=0; for(int v=0;v<w;v++) if(v!=f) rest[nr++]=v;
    while(1){
      pi[0]=f; for(int c=1;c<w;c++) pi[c]=rest[c-1];
      if(SECOND>=0 && pi[1]!=SECOND){ if(pi[1]>SECOND) break; goto nextperm; }
      np++;
      int col_at[16]; for(int c=0;c<w;c++) col_at[pi[c]]=c;
      for(int mode=0;mode<2;mode++){ /* 0 = ROW, 1 = COL (labels as allcol) */
        int sig[N],inv[N],q=0;
        if(mode==1){ for(int k=0;k<w;k++){int c=col_at[k]; for(int r=0;r<rows;r++){int cell=r*w+c; if(cell<N) sig[cell]=q++;}} }
        else { for(int r=0;r<rows;r++) for(int k=0;k<w;k++){int cell=r*w+col_at[k]; if(cell<N) sig[cell]=q++;} }
        for(int i=0;i<N;i++) inv[sig[i]]=i;
        for(int dir=0;dir<2;dir++){ const int*S=dir?inv:sig; int j[24]; for(int t=0;t<24;t++) j[t]=S[CRP[t]];
          for(int al=0;al<NAL;al++) for(int be=0;be<2;be++){ int kv[24];
            for(int t=0;t<24;t++){int a=ai[CA[al]][ct[j[t]]], b=pt[al][t]; kv[t]=be?(a+b)%26:(a-b+26)%26;}
            for(int model=0;model<2;model++) for(int p=1;p<=PMAX;p++){ int res[24],bad=-3;
              for(int t=0;t<24;t++) res[t]=(model?j[t]:CRP[t])%p;
              int e=excess(res,kv,p,&bad);
              if(e==0) s0[p]++; else if(e==1) s1[p]++; else continue;
              if(e==0 || p<=PPRINT){
                printf("H %s %d %d %d %d %d %d %d %d %d",lab,w,mode,dir,al,be,model,p,e,bad);
                for(int c=0;c<w;c++) printf(" %d",pi[c]); printf("\n"); }
            } } } }
      nextperm: ;
      /* next permutation of rest */
      int i=nr-2; while(i>=0&&rest[i]>=rest[i+1]) i--; if(i<0) break;
      int jj=nr-1; while(rest[jj]<=rest[i]) jj--; int t=rest[i];rest[i]=rest[jj];rest[jj]=t;
      for(int l=i+1,r=nr-1;l<r;l++,r--){t=rest[l];rest[l]=rest[r];rest[r]=t;}
    }
  }
  printf("C %s w%d first%d perms %ld",lab,w,first,np);
  for(int p=1;p<=PMAX;p++) printf(" p%d=%ld/%ld",p,s0[p],s1[p]); printf("\n"); return 0;
}

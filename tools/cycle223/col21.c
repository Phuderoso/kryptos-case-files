/* Cycle 223 (I-318 audit): col1e.c (cycle 219) restricted to a short list of periods (cycle 223: 20 and 21), printing every excess<=1 cell
   with the carved positions j[24] of the 24 crib seats, so cells can be collapsed by what the crib test actually sees.
   Enumeration, transposition, key forms, models and the excess function are copied verbatim from tools/cycle219/col1e.c.
   usage: col21 CT w first PLIST label   (first = pi[0] slice, -1 = all orders; PLIST = comma list of periods, e.g. 20,21)
   prints: H label w mode dir al be model p e bad pi[0..w-1] | j[0..23]
           C label w first perms strict/one-error */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const int CRP[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *CRS="EASTNORTHEASTBERLINCLOCK";
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
  if(argc<6){fprintf(stderr,"usage\n");return 1;}
  const char*s=argv[1]; int w=atoi(argv[2]), first=atoi(argv[3]); int PL[8],npl=0; {char b[64]; strncpy(b,argv[4],63); b[63]=0; for(char*q=strtok(b,",");q&&npl<8;q=strtok(NULL,",")) PL[npl++]=atoi(q);} const char*lab=argv[5];
  if((int)strlen(s)!=N){fprintf(stderr,"CT must be 97 letters\n");return 1;}
  int ct[N],ai[2][26]; for(int i=0;i<N;i++) ct[i]=s[i]-'A';
  for(int i=0;i<26;i++){ai[0][i]=i; ai[1][KA[i]-'A']=i;}
  int pt[2][24]; for(int t=0;t<24;t++) for(int a=0;a<2;a++) pt[a][t]=ai[a][CRS[t]-'A'];
  int rows=(N+w-1)/w; int pi[16],rest[16],nr=0;
  int f0 = first<0?0:first, f1 = first<0?w-1:first; long np=0, s0[8]={0}, s1[8]={0};
  for(int f=f0;f<=f1;f++){
    nr=0; for(int v=0;v<w;v++) if(v!=f) rest[nr++]=v;
    while(1){
      pi[0]=f; for(int c=1;c<w;c++) pi[c]=rest[c-1];
      np++;
      int col_at[16]; for(int c=0;c<w;c++) col_at[pi[c]]=c;
      for(int mode=0;mode<2;mode++){
        int sig[N],inv[N],q=0;
        if(mode==1){ for(int k=0;k<w;k++){int c=col_at[k]; for(int r=0;r<rows;r++){int cell=r*w+c; if(cell<N) sig[cell]=q++;}} }
        else { for(int r=0;r<rows;r++) for(int k=0;k<w;k++){int cell=r*w+col_at[k]; if(cell<N) sig[cell]=q++;} }
        for(int i=0;i<N;i++) inv[sig[i]]=i;
        for(int dir=0;dir<2;dir++){ const int*S=dir?inv:sig; int j[24]; for(int t=0;t<24;t++) j[t]=S[CRP[t]];
          for(int al=0;al<2;al++) for(int be=0;be<2;be++){ int kv[24];
            for(int t=0;t<24;t++){int a=ai[al][ct[j[t]]], b=pt[al][t]; kv[t]=be?(a+b)%26:(a-b+26)%26;}
            for(int model=0;model<2;model++) for(int pk=0;pk<npl;pk++){ int p=PL[pk], res[24],bad=-3;
              for(int t=0;t<24;t++) res[t]=(model?j[t]:CRP[t])%p;
              int e=excess(res,kv,p,&bad);
              if(e==0) s0[pk]++; else if(e==1) s1[pk]++; else continue;
              printf("H %s %d %d %d %d %d %d %d %d %d",lab,w,mode,dir,al,be,model,p,e,bad);
              for(int c=0;c<w;c++) printf(" %d",pi[c]); printf(" |");
              for(int t=0;t<24;t++) printf(" %d",j[t]); printf("\n");
            } } } }
      int i=nr-2; while(i>=0&&rest[i]>=rest[i+1]) i--; if(i<0) break;
      int jj=nr-1; while(rest[jj]<=rest[i]) jj--; int t=rest[i];rest[i]=rest[jj];rest[jj]=t;
      for(int l=i+1,r=nr-1;l<r;l++,r--){t=rest[l];rest[l]=rest[r];rest[r]=t;}
    }
  }
  printf("C %s w%d first%d perms %ld",lab,w,first,np); for(int pk=0;pk<npl;pk++) printf(" p%d=%ld/%ld",PL[pk],s0[pk],s1[pk]); printf("\n"); return 0;
}

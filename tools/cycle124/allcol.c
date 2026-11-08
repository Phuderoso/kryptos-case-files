/* Cycle 124: ALL column orders of width w (9 or 10), rotation 0 (plain keyword-columnar family),
   read by columns (COL = textbook columnar) or by rows with permuted columns (ROW),
   both directions (dir0: plaintext written into grid; dir1: sigma inverse),
   x periodic tableau key p=1..PMAX: alphabet AZ or KRYPTOS (KA), Vig (k=c-p; variant has same consistency) or Beau (k=c+p),
   key residue model A = plaintext index mod p (key applied before transposition), B = ciphertext index mod p (after).
   Exact: survivor = all 24 crib letters consistent.  Ragged 97-letter grid, short last row holds columns 0..97%w-1.
   usage: allcol CT w first PMAX label   (first = value of pi[0], -1 = all; lets runs split across cores)
   output: one line per survivor: label w mode dir alpha beau model p pi... ; final line: counts per p */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const int CRP[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *CRS="EASTNORTHEASTBERLINCLOCK";
static int ct[N],ai[2][26],w,pi_[16],L[16],slotoff[16],hs,rem,PMAX; static long cnt[64];
static int place(int c,int r,int mode){ if(mode==1) return slotoff[pi_[c]]+r;
  if(r<hs) return r*w+pi_[c]; int k=0; for(int d=0;d<rem;d++) if(pi_[d]<pi_[c]) k++; return w*hs+k; }
static int nextperm(int*a,int n){int i=n-2;while(i>=0&&a[i]>=a[i+1])i--;if(i<0)return 0;int j=n-1;while(a[j]<=a[i])j--;
  int t=a[i];a[i]=a[j];a[j]=t;for(int l=i+1,r=n-1;l<r;l++,r--){t=a[l];a[l]=a[r];a[r]=t;}return 1;}
int main(int argc,char**argv){ const char*s=argv[1]; w=atoi(argv[2]); int first=atoi(argv[3]); PMAX=atoi(argv[4]); const char*lab=argv[5];
  for(int i=0;i<N;i++) ct[i]=s[i]-'A';
  for(int i=0;i<26;i++){ai[0][i]=i; ai[1][KA[i]-'A']=i;}
  hs=N/w; rem=N%w; for(int c=0;c<w;c++) L[c]=hs+(c<rem);
  for(int i=0;i<w;i++) pi_[i]=i;
  long np=0;
  do{ if(first>=0 && pi_[0]!=first) { if(pi_[0]>first) break; continue; }
    np++;
    int col_at[16]; for(int c=0;c<w;c++) col_at[pi_[c]]=c;
    int o=0; for(int k=0;k<w;k++){ slotoff[k]=o; o+=L[col_at[k]]; }
    for(int mode=0;mode<2;mode++){
      int sig[N], inv[N];
      for(int i=0;i<N;i++){ sig[i]=place(i%w,i/w,mode); }
      for(int i=0;i<N;i++) inv[sig[i]]=i;
      for(int dir=0;dir<2;dir++){ const int*S = dir? inv: sig; int j[24]; for(int t=0;t<24;t++) j[t]=S[CRP[t]];
        for(int al=0;al<2;al++) for(int be=0;be<2;be++){ int kv[24];
          for(int t=0;t<24;t++){int a=ai[al][ct[j[t]]], b=ai[al][CRS[t]-'A']; kv[t]=be? (a+b)%26 : (a-b+26)%26;}
          for(int model=0;model<2;model++) for(int p=1;p<=PMAX;p++){ int key[64]; memset(key,-1,sizeof(int)*p); int ok=1;
            for(int t=0;t<24;t++){ int r=(model? j[t]:CRP[t])%p; if(key[r]<0) key[r]=kv[t]; else if(key[r]!=kv[t]){ok=0;break;} }
            if(ok){ cnt[p]++; printf("S %s %d %d %d %d %d %d %d",lab,w,mode,dir,al,be,model,p); for(int c=0;c<w;c++) printf(" %d",pi_[c]); printf("\n"); }
          } } } }
  } while(nextperm(pi_,w));
  printf("C %s w%d first%d perms %ld",lab,w,first,np); for(int p=1;p<=PMAX;p++) printf(" p%d=%ld",p,cnt[p]); printf("\n"); return 0; }

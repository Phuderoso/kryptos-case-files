/* Cycle 57: NICODEMUS (ACA), exact crib test, generalised.
   Encipher: plaintext in rows of width w; column c gets a Vigenere/Beaufort shift k_c (any letter, per column) on a
   tableau built from one mixed alphabet A; columns re-ordered by sigma; then read off in BLOCKS of h rows: for each
   block, read down each column (in sigma order) through that block's rows only (ragged last row skipped).
   h >= rows reduces to ordinary columnar + period-w key (control overlap with cycle 13).
   Test: for each (A, w, sigma, h, mode) the crib key values r = a(c)-a(p) (vig) or a(c)+a(p) (beau) must be
   constant within each plaintext column. Variant Beaufort = vig with negated key (same consistency).
   usage: nicodemus CT alpha.bin nalpha_small wmax_small wmax_az hmax   (alphabet 0 must be A-Z, 1 KRYPTOS)
   all orders for w <= wmax_small on nalpha_small alphabets; w <= wmax_az on alphabets 0-1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *PT="EASTNORTHEASTBERLINCLOCK";
static unsigned char AL[100000][26]; static int NA;
static const char*CT; static long hits=0,tests=0;
static void perm_of(int w,const int*sig,int h,int*pos){ /* pos[i] = carved index of plaintext position i */
  int rows=(N+w-1)/w; int k=0;
  for(int r0=0;r0<rows;r0+=h){ int r1=r0+h<rows?r0+h:rows;
    for(int s=0;s<w;s++){ int c=sig[s]; for(int r=r0;r<r1;r++){ int i=r*w+c; if(i<N) pos[i]=k++; } } } }
static double QG[26*26*26*26]; static int haveq=0;
static void report(int a,int w,const int*sig,int h,int mode,const int*pos){
  int idx[26]; for(int i=0;i<26;i++) idx[AL[a][i]]=i;
  int key[16]; for(int c=0;c<w;c++) key[c]=-1;
  for(int i=0;i<24;i++){ int p=CI[i]; int cv=idx[CT[pos[p]]-65], pv=idx[PT[i]-65];
    key[p%w]= mode==0? (cv-pv+26)%26 : (cv+pv)%26; }
  char out[N+1]; for(int i=0;i<N;i++){ int c=i%w; int cv=idx[CT[pos[i]]-65];
    if(key[c]<0){ out[i]='?'; continue; } int pv= mode==0? (cv-key[c]+26)%26 : (key[c]-cv+26)%26; out[i]='A'+AL[a][pv]; }
  out[N]=0; double s=0; int n=0;
  if(haveq) for(int i=0;i+3<N;i++){ if(out[i]=='?'||out[i+1]=='?'||out[i+2]=='?'||out[i+3]=='?') continue;
    s+=QG[((out[i]-65)*26+(out[i+1]-65))*26*26+(out[i+2]-65)*26+(out[i+3]-65)]; n++; }
  #pragma omp critical
  { hits++; printf("HIT a=%d w=%d h=%d mode=%s sigma=",a,w,h,mode?"beau":"vig"); for(int s2=0;s2<w;s2++) printf("%d",sig[s2]);
    printf(" key="); for(int c=0;c<w;c++) printf("%c",key[c]<0?'?':'A'+AL[a][key[c]]); printf(" q=%.3f PT=%s\n",n?s/n:0,out); }
}
static void test(int a,int w,const int*sig,int hmax){
  int idx[26]; for(int i=0;i<26;i++) idx[AL[a][i]]=i;
  int pv[24]; for(int i=0;i<24;i++) pv[i]=idx[PT[i]-65];
  int rows=(N+w-1)/w;
  for(int h=1;h<=hmax;h++){ if(h>rows) continue; int pos[N]; perm_of(w,sig,h,pos);
    for(int mode=0;mode<2;mode++){ int key[16]; for(int c=0;c<w;c++) key[c]=-1; int ok=1; tests++;
      for(int i=0;i<24&&ok;i++){ int p=CI[i]; int cv=idx[CT[pos[p]]-65]; int r= mode==0?(cv-pv[i]+26)%26:(cv+pv[i])%26;
        int c=p%w; if(key[c]<0) key[c]=r; else if(key[c]!=r) ok=0; }
      if(ok) report(a,w,sig,h,mode,pos); } } }
static int nextperm(int*a,int n){ int i=n-2; while(i>=0&&a[i]>a[i+1]) i--; if(i<0) return 0;
  int j=n-1; while(a[j]<a[i]) j--; int t=a[i];a[i]=a[j];a[j]=t; for(int l=i+1,r=n-1;l<r;l++,r--){t=a[l];a[l]=a[r];a[r]=t;} return 1; }
int main(int argc,char**argv){
  CT=argv[1]; if(strlen(CT)!=N){fprintf(stderr,"len\n");return 1;}
  FILE*f=fopen(argv[2],"rb"); NA=fread(AL,26,100000,f); fclose(f);
  int nas=atoi(argv[3]), wms=atoi(argv[4]), wmaz=atoi(argv[5]), hmax=atoi(argv[6]);
  FILE*q=fopen("data/cycle57/qg.bin","rb"); if(q){ haveq=fread(QG,sizeof(double),26*26*26*26,q)>0; fclose(q);}
  for(int w=2;w<=wmaz;w++){ int na= w<=wms? nas:2;
    for(int a=0;a<na;a++){ int sig[16]; for(int i=0;i<w;i++) sig[i]=i;
      do test(a,w,sig,hmax); while(nextperm(sig,w)); } }
  printf("SUMMARY tests=%ld hits=%ld\n",tests,hits); return 0; }

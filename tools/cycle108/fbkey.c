/* Cycle 108: feedback-key cipher. Key stream k[i] = a*k[i-1] + b*p[i-L] + e*x[i-L] + d (mod 26),
   x = cipher stream before transposition (model A: x[j] = carved[t[j]]), L = 1..3.
   Covers Vigenere-cumulative autokey (a=1,b=1), CT-cumulative (a=1,e=1), plain PT/CT autokey (a=0),
   progressive (a=1,b=e=0), constant key, and every affine mix of them.
   Tableau modes: 0 Vig AZ, 1 Beau AZ, 2 Vig KA, 3 Beau KA (letters numbered in that alphabet; variant = Vig up to sign).
   Exact: the crib-internal equations are linear in (a,b,e,d); solvable mod 26 iff solvable mod 2 and mod 13.
   Survivors: propagate the key from crib 1 through the gap and require all 11 BERLINCLOCK letters.
   usage: fbkey CT perm.bin nperm  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef LMAX
#define LMAX 3
#endif
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
int inv13[13];
/* gaussian elim mod m (prime) on n eq x 4 unknowns + rhs; returns -1 if inconsistent else rank */
int solve(int n,int A[][5],int m,int sol[4]){
  int M[64][5]; for(int i=0;i<n;i++)for(int j=0;j<5;j++)M[i][j]=((A[i][j]%m)+m)%m;
  int r=0,piv[4]={-1,-1,-1,-1};
  for(int c=0;c<4&&r<n;c++){ int s=-1; for(int i=r;i<n;i++) if(M[i][c]){s=i;break;} if(s<0) continue;
    for(int j=0;j<5;j++){int t=M[r][j];M[r][j]=M[s][j];M[s][j]=t;}
    int iv = m==2?1:inv13[M[r][c]]; for(int j=0;j<5;j++) M[r][j]=M[r][j]*iv%m;
    for(int i=0;i<n;i++) if(i!=r&&M[i][c]){int f=M[i][c]; for(int j=0;j<5;j++) M[i][j]=((M[i][j]-f*M[r][j])%m+m)%m;}
    piv[c]=r; r++; }
  for(int i=r;i<n;i++) if(M[i][4]) return -1;
  for(int c=0;c<4;c++) sol[c]= piv[c]>=0 ? M[piv[c]][4] : 0;  /* one particular solution (free vars 0) */
  return r;
}
int main(int argc,char**argv){
  for(int i=1;i<13;i++)for(int j=1;j<13;j++) if(i*j%13==1) inv13[i]=j;
  const char*ct=argv[1]; int np=atoi(argv[3]); int verbose=argc>4;
  short*P=malloc((size_t)np*97*2); FILE*f=fopen(argv[2],"rb"); if(fread(P,2,(size_t)np*97,f)!=(size_t)np*97) fprintf(stderr,"short\n"); fclose(f);
  char pt[97]; memset(pt,0,97); const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  for(int i=0;i<13;i++) pt[21+i]=c1[i]; for(int i=0;i<11;i++) pt[63+i]=c2[i];
  int idx[2][26]; for(int i=0;i<26;i++){idx[0][i]=i; idx[1][KA[i]-65]=i;}
  long surv=0, full=0; int hist[30]={0};
  for(int q=0;q<np;q++){ short*t=P+(size_t)q*97; int X[97];
    for(int mode=0;mode<4;mode++){ int al=mode>>1, beau=mode&1;
      for(int j=0;j<97;j++) X[j]=idx[al][ct[t[j]]-65];
      int K[97],Pn[97]; for(int j=0;j<97;j++){ if(pt[j]){Pn[j]=idx[al][pt[j]-65]; K[j]= beau? (X[j]+Pn[j])%26 : ((X[j]-Pn[j])%26+26)%26;} else Pn[j]=-1; }
      for(int L=1;L<=LMAX;L++){ int A[64][5]; int n=0;
        for(int j=1;j<97;j++){ if(!pt[j]||!pt[j-1]||j-L<0||!pt[j-L]) continue;
          A[n][0]=K[j-1]; A[n][1]=Pn[j-L]; A[n][2]=X[j-L]; A[n][3]=1; A[n][4]=K[j]; n++; }
        int s2[4],s13[4]; int r2=solve(n,A,2,s2); if(r2<0) continue; int r13=solve(n,A,13,s13); if(r13<0) continue;
        surv++; int chk=n-r13; hist[chk<30?chk:29]++;
        /* full propagation over all solutions mod 26: enumerate (a,b,e,d) consistent with every equation, then propagate */
        for(int a=0;a<26;a++)for(int b=0;b<26;b++)for(int e=0;e<26;e++)for(int d=0;d<26;d++){
          int ok=1; for(int i=0;i<n&&ok;i++) if((a*A[i][0]+b*A[i][1]+e*A[i][2]+d-A[i][4])%26) ok=0; if(!ok) continue;
          int kk[97],pp[97]; for(int j=21;j<34;j++){kk[j]=K[j];pp[j]=Pn[j];}
          int match=0; for(int j=34;j<97;j++){ kk[j]=(a*kk[j-1]+b*pp[j-L]+e*X[j-L]+d)%26; pp[j]= beau? ((kk[j]-X[j])%26+26)%26 : ((X[j]-kk[j])%26+26)%26; if(j>=63&&j<74&&pp[j]==Pn[j]) match++; }
          if(match>=11){ full++; if(full<=50){ printf("FULL perm=%d mode=%d L=%d a=%d b=%d e=%d d=%d tail=",q,mode,L,a,b,e,d); for(int j=21;j<97;j++) putchar(al?KA[pp[j]]:65+pp[j]); putchar('\n');} }
          else if(verbose && match>=8) printf("near %d perm=%d mode=%d L=%d\n",match,q,mode,L);
        }
      }
    }
  }
  printf("RESULT survivors(crib-internal)=%ld full(BERLINCLOCK by propagation)=%ld checks-hist:",surv,full);
  for(int i=0;i<30;i++) if(hist[i]) printf(" %d:%d",i,hist[i]); printf("\n");
}

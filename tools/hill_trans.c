/* Cycle 27: Hill cipher (n = 2..5) on either side of the cycle-19 transposition family.
   Exact test (decryption form): does ANY n x n matrix D mod 26 satisfy Y_block = D * Z_block
   at every known crib letter? Each of the 24 crib letters is one linear equation on one row of D
   (Z is fully known ciphertext), so partially known blocks count too.
   Consistency is decided per prime (mod 2 and mod 13) by Gaussian elimination, which is
   exact for Z/26 by the Chinese remainder theorem.
   order b: CT = T(Hill(P))  -> Y = P (cribs at carved positions), Z[i] = CT[perm[i]]
   order a: CT = Hill(T(P))  -> Z = CT, Y[perm[i]] = P[i]
   alphabets: AZ numbering and KRYPTOS-keyed (KA) numbering.
   usage: hill_trans perms.bin N ct.txt  -> prints one line per consistent config, then a summary */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int inv_mod(int a,int p){for(int x=1;x<p;x++) if(a*x%p==1) return x; return -1;}
/* is M r = z solvable mod p ? M is m x n */
static int solvable(int m,int n,int M[][5],int *z,int p){
  int A[64][6]; for(int i=0;i<m;i++){for(int j=0;j<n;j++)A[i][j]=((M[i][j]%p)+p)%p; A[i][n]=((z[i]%p)+p)%p;}
  int r=0;
  for(int c=0;c<n && r<m;c++){
    int piv=-1; for(int i=r;i<m;i++) if(A[i][c]){piv=i;break;}
    if(piv<0) continue;
    for(int k=0;k<=n;k++){int t=A[r][k];A[r][k]=A[piv][k];A[piv][k]=t;}
    int iv=inv_mod(A[r][c],p);
    for(int k=0;k<=n;k++) A[r][k]=A[r][k]*iv%p;
    for(int i=0;i<m;i++) if(i!=r && A[i][c]){int f=A[i][c]; for(int k=0;k<=n;k++) A[i][k]=((A[i][k]-f*A[r][k])%p+p)%p;}
    r++;
  }
  for(int i=r;i<m;i++) if(A[i][n]) return 0;
  return 1;
}
int main(int argc,char**argv){
  int N=atoi(argv[2]);
  short *perms=malloc((size_t)N*97*2); FILE*f=fopen(argv[1],"rb"); fread(perms,2,(size_t)N*97,f); fclose(f);
  char ct[200]; f=fopen(argv[3],"r"); fscanf(f,"%s",ct); fclose(f);
  const char *c1="EASTNORTHEAST", *c2="BERLINCLOCK";
  int ptk[97]; char pt[97]; memset(ptk,0,sizeof ptk);
  for(int i=0;i<13;i++){pt[21+i]=c1[i];ptk[21+i]=1;}
  for(int i=0;i<11;i++){pt[63+i]=c2[i];ptk[63+i]=1;}
  long tested[6]={0},untest[6]={0},hits[6]={0},rejected_weak[6]={0};
  for(int pi=0;pi<N;pi++){ short*pm=perms+(size_t)pi*97;
   for(int order=0;order<2;order++) for(int al=0;al<2;al++){
    int num[128]; for(int i=0;i<26;i++) num[al? (unsigned char)KA[i] : 'A'+i]=i;
    int Y[97],Yk[97],Z[97];
    for(int i=0;i<97;i++){Yk[i]=0;}
    if(order==1){ /* b */ for(int i=0;i<97;i++){Y[i]=ptk[i]?num[(int)pt[i]]:0;Yk[i]=ptk[i];Z[i]=num[(int)ct[pm[i]]];} }
    else { for(int i=0;i<97;i++){Z[i]=num[(int)ct[i]]; Yk[pm[i]]=ptk[i]; Y[pm[i]]=ptk[i]?num[(int)pt[i]]:0;} }
    for(int n=2;n<=5;n++) for(int a=0;a<n;a++){
      int good=1, testable=1, minEq=999;
      for(int j=0;j<n;j++){
        int M[64][4+1]; int zz[64]; int m=0;
        for(int s=a;s+n<=97;s+=n){ if(!Yk[s+j]) continue; for(int k=0;k<n;k++) M[m][k]=Z[s+k]; zz[m]=Y[s+j]; m++; }
        if(m<minEq) minEq=m;
        if(m<n+1){testable=0;}
        if(good && (!solvable(m,n,M,zz,2)||!solvable(m,n,M,zz,13))) good=0;
      }
      if(!testable){untest[n]++; if(!good) rejected_weak[n]++; continue;}
      tested[n]++;
      if(good){hits[n]++; printf("HIT perm=%d order=%c alph=%s n=%d align=%d mineq=%d\n",pi,order?'b':'a',al?"KA":"AZ",n,a,minEq);}
    }
   }
  }
  for(int n=2;n<=5;n++) printf("SUMMARY n=%d testable=%ld consistent=%ld | weak(some row < n+1 eqs)=%ld of which rejected anyway=%ld\n",n,tested[n],hits[n],untest[n],rejected_weak[n]);
  return 0;
}

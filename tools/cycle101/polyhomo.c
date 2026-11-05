/* Cycle 101: polyalphabetic homophonic = periodic shift key + ANY many-to-one map f (26 -> 26), optional transposition s.
   Model A (shift, then f):  P_i = f( ix(C_s(i)) - k[q%L] )
   Model B (f, then shift):  ix(P_i) = f(C_s(i)) + k[q%L]
   q = i (key on plaintext position) or s(i) (key on carved position). Alphabet AZ or KRYPTOS (ix). Beaufort/variant forms are
   absorbed by f (f arbitrary). k[0] fixed to 0 (a common shift is absorbed by f). Exact crib-consistency test.
   Usage: ./polyhomo CT Lmin Lmax maxprint [perms.bin ...]  (no files = identity only) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int ix[2][26],crib[N],cp[24]; long cnt[2][2][2][16],tot[16]; int maxprint,printed=0;
void run(const char*CT,const int*s,const char*tag,long n,int inv,int Lmin,int Lmax){
  for(int t=0;t<2;t++){ int c[N]; for(int i=0;i<N;i++) c[i]=ix[t][CT[s[i]]-65]; int pv[24]; for(int q=0;q<24;q++) pv[q]=ix[t][crib[cp[q]]];
   for(int kp=0;kp<2;kp++){ if(kp==1 && s[0]==0 && s[96]==96 && s[50]==50) { int idn=1; for(int i=0;i<N;i++) if(s[i]!=i){idn=0;break;} if(idn) continue; }
    int pos[24]; for(int q=0;q<24;q++) pos[q]= kp? s[cp[q]] : cp[q];
    for(int L=Lmin;L<=Lmax;L++){ long nk=1; for(int r=1;r<L;r++) nk*=26; tot[L]+=nk;
     for(long code=0;code<nk;code++){ int k[16]; k[0]=0; long cc=code; for(int r=1;r<L;r++){k[r]=cc%26;cc/=26;}
      for(int m=0;m<2;m++){ int f[26]; memset(f,-1,sizeof f); int ok=1;
        for(int q=0;q<24;q++){ int kk=k[pos[q]%L]; int x,y; if(m==0){x=(c[cp[q]]-kk+26)%26; y=pv[q];} else {x=c[cp[q]]; y=(pv[q]-kk+26)%26;}
          if(f[x]<0) f[x]=y; else if(f[x]!=y){ok=0;break;} }
        if(ok){ cnt[t][kp][m][L]++; if(printed<maxprint){ printed++; printf("CONS %s n=%ld inv=%d t=%d kp=%d m=%d L=%d key=",tag,n,inv,t,kp,m,L); for(int r=0;r<L;r++)putchar(65+k[r]); putchar('\n'); } }
      } } } } }
}
int main(int argc,char**argv){ const char*CT=argv[1]; int Lmin=atoi(argv[2]),Lmax=atoi(argv[3]); maxprint=atoi(argv[4]);
  const char*a="EASTNORTHEAST",*b="BERLINCLOCK"; for(int i=0;i<N;i++)crib[i]=-1;
  for(int i=0;i<13;i++)crib[21+i]=a[i]-65; for(int i=0;i<11;i++)crib[63+i]=b[i]-65; int nc=0; for(int i=0;i<N;i++) if(crib[i]>=0) cp[nc++]=i;
  for(int t=0;t<2;t++)for(int k=0;k<26;k++)ix[t][AL[t][k]-65]=k;
  if(argc<=5){ int id[N]; for(int i=0;i<N;i++)id[i]=i; run(CT,id,"identity",0,0,Lmin,Lmax); }
  for(int A=5;A<argc;A++){ FILE*fp=fopen(argv[A],"rb"); fseek(fp,0,2); long np=ftell(fp)/194; fseek(fp,0,0); short*S=malloc(np*194); fread(S,194,np,fp); fclose(fp);
    for(long n=0;n<np;n++) for(int inv=0;inv<2;inv++){ int s[N]; if(!inv)for(int i=0;i<N;i++)s[i]=S[n*N+i]; else for(int i=0;i<N;i++)s[S[n*N+i]]=i; run(CT,s,argv[A],n,inv,Lmin,Lmax);} free(S);}
  for(int L=Lmin;L<=Lmax;L++){ fprintf(stderr,"L=%d keys/perm=%ld",L,tot[L]); for(int t=0;t<2;t++)for(int kp=0;kp<2;kp++)for(int m=0;m<2;m++) fprintf(stderr," t%dk%dm%d:%ld",t,kp,m,cnt[t][kp][m][L]); fprintf(stderr,"\n"); } }

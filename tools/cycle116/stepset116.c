/* Cycle 116: generic stepping disk.  Any machine whose ring shift is cumulative, s_{i+1} = s_i + d_i with every step d_i
   drawn from a step set S (any order, no period): Alberti-with-steps, Kryha (S = 5..13 / V2 sums), M-209-like
   cumulative keys, progressive keys (|S| = 1) ...  With fixed alphabet pair (F, M) and sense sigma the 22 adjacent crib
   differences D = {r_{k+1} - r_k} are forced, so S must contain D; the 30-letter gap needs a 30-step sum from S equal to
   r_63 - r_33 (checked exactly for the minimal S = D).  Reported: m = |D| (the smallest step set any such machine needs).
   Model A only (substitution first, then transposition: cribs stay adjacent).  Identity transposition = direct.
   usage: stepset116 CT perms.bin nperm pairs.txt [print threshold m, default 5]  -> histogram of minimal m over all configs, and best configs. */
#include <stdio.h>
#include <stdlib.h>
static const char *CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
int NP; char F[3000][27],M[3000][27]; int fi[3000][26],mi[3000][26];
static int reach30(int mask,int tgt){ unsigned r=1; for(int s=0;s<30;s++){ unsigned n=0; for(int x=0;x<26;x++) if(r>>x&1) for(int d=0;d<26;d++) if(mask>>d&1) n|=1u<<((x+d)%26); r=n;} return r>>tgt&1; }
int main(int argc,char**argv){
  const char*ct=argv[1]; int np=atoi(argv[3]); int TH=argc>5?atoi(argv[5]):5;
  short*P=malloc((size_t)np*97*2); FILE*f=fopen(argv[2],"rb"); if(fread(P,2,(size_t)np*97,f)!=(size_t)np*97) return 1; fclose(f);
  f=fopen(argv[4],"r"); NP=0; while(fscanf(f,"%26s %26s",F[NP],M[NP])==2){for(int i=0;i<26;i++){fi[NP][F[NP][i]-65]=i;mi[NP][M[NP][i]-65]=i;}NP++;} fclose(f);
  int cpos[24],pl[24]; for(int k=0;k<13;k++){cpos[k]=21+k;pl[k]=CR1[k]-65;} for(int k=0;k<11;k++){cpos[13+k]=63+k;pl[13+k]=CR2[k]-65;}
  int C[97]; for(int i=0;i<97;i++)C[i]=ct[i]-65;
  long hist[27]={0}, histbest[27]={0}; int gmin=99;
  for(int p=-1;p<np;p++){ int cl[24]; for(int k=0;k<24;k++) cl[k]= p<0 ? C[cpos[k]] : C[P[(size_t)p*97+cpos[k]]];
    int pmin=99;
    for(int pi=0;pi<NP;pi++) for(int sg=-1;sg<=1;sg+=2){ int r[24];
      for(int k=0;k<24;k++) r[k]=(((sg*(mi[pi][cl[k]]-fi[pi][pl[k]]))%26)+26)%26;
      int mask=0; for(int k=0;k<23;k++) if(k!=12) mask|=1<<((r[k+1]-r[k]+26)%26);
      int m=__builtin_popcount(mask);
      if(m<=6 && !reach30(mask,(r[13]-r[12]+26)%26)) m+=100;   /* gap not reachable with S = D: needs one more step value */
      if(m>=100) m=m-100+1;
      hist[m]++; if(m<pmin)pmin=m;
      if(m<=TH) printf("BEST perm=%d pair=%d sg=%d m=%d mask=%07x\n",p,pi,sg,m,mask);
      if(m<gmin) gmin=m;
    }
    histbest[pmin]++;
    if(p<0){ printf("DIRECT min m=%d\n",pmin); }
  }
  printf("HIST all configs:"); for(int m=0;m<27;m++) if(hist[m]) printf(" %d:%ld",m,hist[m]); printf("\nHIST per-perm min:"); for(int m=0;m<27;m++) if(histbest[m]) printf(" %d:%ld",m,histbest[m]); printf("\nGLOBAL min m=%d\n",gmin);
  return 0;
}

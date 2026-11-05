/* Cycle 119: carving-error audit of cycle 116 (generic stepping disk).  Same model as stepset116 (model A, keyword
   alphabet pairs, both senses, identity + bank perms), but one crib letter may be wrong: for each config and each
   dropped crib k, the steps touching k are discarded and m1 = min_k |distinct remaining steps|.  This is a LOWER BOUND
   on the step-set size a machine needs if exactly one crib position was mis-carved (the merged two-step constraint and
   the 30-letter gap test are ignored, so it can only under-count).
   usage: stepset119 CT perms.bin nperm pairs.txt [print threshold]  */
#include <stdio.h>
#include <stdlib.h>
static const char *CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
int NP; char F[3000][27],M[3000][27]; int fi[3000][26],mi[3000][26];
int main(int argc,char**argv){
  const char*ct=argv[1]; int np=atoi(argv[3]); int TH=argc>5?atoi(argv[5]):4;
  short*P=malloc((size_t)np*97*2); FILE*f=fopen(argv[2],"rb"); if(np&&fread(P,2,(size_t)np*97,f)!=(size_t)np*97) return 1; fclose(f);
  f=fopen(argv[4],"r"); NP=0; while(fscanf(f,"%26s %26s",F[NP],M[NP])==2){for(int i=0;i<26;i++){fi[NP][F[NP][i]-65]=i;mi[NP][M[NP][i]-65]=i;}NP++;} fclose(f);
  int cpos[24],pl[24]; for(int k=0;k<13;k++){cpos[k]=21+k;pl[k]=CR1[k]-65;} for(int k=0;k<11;k++){cpos[13+k]=63+k;pl[13+k]=CR2[k]-65;}
  /* steps j=0..22 except 12: step j joins crib j and j+1 */
  int C[97]; for(int i=0;i<97;i++)C[i]=ct[i]-65;
  long hist[27]={0},histbest[27]={0},hist0[27]={0}; int gmin=99;
  for(int p=-1;p<np;p++){ int cl[24]; for(int k=0;k<24;k++) cl[k]= p<0 ? C[cpos[k]] : C[P[(size_t)p*97+cpos[k]]];
    int pmin=99;
    for(int pi=0;pi<NP;pi++) for(int sg=-1;sg<=1;sg+=2){ int r[24],d[23],cnt[26]={0},m0=0;
      for(int k=0;k<24;k++) r[k]=(((sg*(mi[pi][cl[k]]-fi[pi][pl[k]]))%26)+26)%26;
      for(int j=0;j<23;j++){ if(j==12){d[j]=-1;continue;} d[j]=(r[j+1]-r[j]+26)%26; if(!cnt[d[j]]++) m0++; }
      int best=m0, bk=-1;
      for(int k=0;k<24;k++){ int a=k-1,b=k; int m=m0;
        if(a>=0&&d[a]>=0){ if(--cnt[d[a]]==0) m--; }
        if(b<23&&d[b]>=0){ if(--cnt[d[b]]==0) m--; }
        if(m<best){best=m;bk=k;}
        if(a>=0&&d[a]>=0) cnt[d[a]]++; if(b<23&&d[b]>=0) cnt[d[b]]++; }
      hist[best]++; hist0[m0]++; if(best<pmin)pmin=best; if(best<gmin)gmin=best;
      if(best<=TH) printf("BEST perm=%d pair=%d sg=%d m1=%d drop=%d m0=%d\n",p,pi,sg,best,bk,m0);
    }
    histbest[pmin]++; if(p<0) printf("DIRECT min m1=%d\n",pmin);
  }
  printf("HIST m1 all configs:"); for(int m=0;m<27;m++) if(hist[m]) printf(" %d:%ld",m,hist[m]);
  printf("\nHIST m1 per-perm min:"); for(int m=0;m<27;m++) if(histbest[m]) printf(" %d:%ld",m,histbest[m]);
  printf("\nGLOBAL min m1=%d\n",gmin); return 0; }

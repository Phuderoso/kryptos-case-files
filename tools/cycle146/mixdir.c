/* Cycle 146: mixed-direction periodic key. Each phase j of a period-P key has its own key letter k_j AND its own
   direction: Vigenere (L = p + k) or Beaufort (L = k - p) (variant = Vigenere with negated key, same test).
   Tableau numbering A-Z or KRYPTOS. Direct, or behind a bank permutation S (both directions):
     ix=0 (model Q, substitution then transposition): stream L[i]=CT[S[i]], plaintext position i
     ix=1 (carved, transposition then substitution):  stream L = CT, crib p sits at stream position S[p]
   Per phase, the crib pairs (L,p) are consistent with Vig iff L-p is constant, with Beau iff L+p is constant: exact.
   Phases with one crib are form-ambiguous; all form choices are enumerated (cap 4096) and each decoding scored by
   mean log10 quadgram over windows of decided non-crib letters.  checks = sum over phases of (cribs-1).
   usage: mixdir CT perms.bin|- label lo hi Pmin Pmax minchecks */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *NUMS[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
static const char *CRIB="EASTNORTHEASTBERLINCLOCK"; static int cpos[24],ISCRIB[97]; static float *Q;
int main(int ac,char**av){
  if(ac<9)return 1; const char*CT=av[1]; const char*lab=av[3]; long lo=atol(av[4]),hi=atol(av[5]);
  int Pmin=atoi(av[6]),Pmax=atoi(av[7]),minchk=atoi(av[8]);
  {int k=0;for(int i=21;i<=33;i++){ISCRIB[i]=1;cpos[k++]=i;}for(int i=63;i<=73;i++){ISCRIB[i]=1;cpos[k++]=i;}}
  Q=malloc(456976*4);{FILE*f=fopen("/home/box/kryptos_support_backup/quad.bin","rb");if(!f||fread(Q,4,456976,f)!=456976)return 2;fclose(f);}
  long np=1; short*bank=NULL; if(strcmp(av[2],"-")){FILE*f=fopen(av[2],"rb");fseek(f,0,2);np=ftell(f)/194;fseek(f,0,0);bank=malloc(np*194);if(fread(bank,194,np,f)!=(size_t)np)return 3;fclose(f);}
  if(hi>np)hi=np; long cfg=0,cons=0,printed=0; double gbest=-99; char gpt[98]="";
  for(long q=lo;q<hi;q++)for(int dir=0;dir<(bank?2:1);dir++){
    int S[97]; if(bank){for(int i=0;i<97;i++)S[i]=bank[q*97+i]; if(dir){int T[97];for(int i=0;i<97;i++)T[S[i]]=i;memcpy(S,T,sizeof S);}} else for(int i=0;i<97;i++)S[i]=i;
    for(int nu=0;nu<2;nu++)for(int ix=0;ix<(bank?2:1);ix++){
      const char*N=NUMS[nu]; int idx[26]; for(int i=0;i<26;i++)idx[N[i]-'A']=i;
      int L[97],kp[97]; for(int i=0;i<97;i++)kp[i]=-1;
      if(ix==0){for(int i=0;i<97;i++)L[i]=idx[CT[S[i]]-'A']; for(int k=0;k<24;k++)kp[cpos[k]]=idx[CRIB[k]-'A'];}
      else{for(int i=0;i<97;i++)L[i]=idx[CT[i]-'A']; for(int k=0;k<24;k++)kp[S[cpos[k]]]=idx[CRIB[k]-'A'];}
      for(int P=Pmin;P<=Pmax;P++){ cfg++;
        int okV[26],okB[26],kV[26],kB[26],m[26],bad=0,chk=0;
        for(int j=0;j<P;j++){okV[j]=okB[j]=1;kV[j]=kB[j]=-1;m[j]=0;}
        for(int i=0;i<97;i++)if(kp[i]>=0){int j=i%P;m[j]++;int v=(L[i]-kp[i]+26)%26,b=(L[i]+kp[i])%26;
          if(kV[j]<0)kV[j]=v;else if(kV[j]!=v)okV[j]=0; if(kB[j]<0)kB[j]=b;else if(kB[j]!=b)okB[j]=0;}
        int amb[26],na=0; for(int j=0;j<P;j++){if(m[j]&&!okV[j]&&!okB[j]){bad=1;break;} if(m[j])chk+=m[j]-1; if(m[j]&&okV[j]&&okB[j])amb[na++]=j;}
        if(bad)continue; cons++; if(chk<minchk)continue;
        int nc=na>12?12:na; double best=-99; char bpt[98];
        for(int c=0;c<(1<<nc);c++){ int form[26]; for(int j=0;j<P;j++)form[j]=okV[j]?0:1;
          for(int a=0;a<nc;a++)form[amb[a]]=(c>>a)&1;
          char out[98],pt[98]; for(int i=0;i<97;i++){int j=i%P; if(!m[j]){out[i]=0;continue;}
            int p=form[j]==0?(L[i]-kV[j]+26)%26:(kB[j]-L[i]+26)%26; out[i]=N[p];}
          if(ix==0)memcpy(pt,out,97); else for(int p=0;p<97;p++)pt[p]=out[S[p]];
          double tot=0;int w=0; for(int i=0;i+4<=97;i++){int g=1,id=0;for(int z=0;z<4;z++){char ch=pt[i+z];if(!ch||ISCRIB[i+z]){g=0;break;}id=id*26+ch-'A';} if(g){tot+=Q[id];w++;}}
          double s=w>=8?tot/w:-99; if(s>best){best=s;for(int i=0;i<97;i++)bpt[i]=pt[i]?pt[i]:'.';bpt[97]=0;}}
        if(best>gbest){gbest=best;strcpy(gpt,bpt);}
        printf("S %s P=%d perm=%ld dir=%d ix=%d num=%d chk=%d amb=%d meanQ=%.3f %s\n",lab,P,q,dir,ix,nu,chk,na,best,bpt);printed++;
      }}}
  printf("C %s cfg=%ld consistent=%ld printed=%ld best=%.3f %s\n",lab,cfg,cons,printed,gbest,gpt); return 0;}

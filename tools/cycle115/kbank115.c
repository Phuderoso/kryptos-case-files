/* Cycle 115: Kryha V1 (ANY code wheel, n = 1..48 sectors, step = teeth+4 in 5..13) with K1-K3-style KEYWORD alphabet
   pairs (cycle 114 test B list, 2,356 pairs x 2 senses), behind every transposition of the 165,065 bank (perms97.bin).
   Model A (Kryha then transposition): X[j] = C[t[j]], Kryha letter index = plaintext position j  -> exact (cycle 114 b1).
   Model B (transposition then Kryha): crib at plaintext j sits at carved q = t[j]; Kryha letter index = q.
           Exact for the five PUBLISHED wheels (15,17,18,19,23 sectors, any start).  Any-wheel model B is crib-
           underdetermined (a gap-filter left ~6,400 (n,config) hits per perm on K4), so it is not claimed.
   r_k = sigma*(M^-1(c_k) - F^-1(p_k)) mod 26 must equal ring shift s_{index}.
   usage: kbank115 CT perms.bin nperm pairs.txt [maxprint]   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *CR1="EASTNORTHEAST",*CR2="BERLINCLOCK";
static int isstep(int d){return d>=5&&d<=13;}
int NP; char F[3000][27],M[3000][27]; int fi[3000][26],mi[3000][26];
int main(int argc,char**argv){
  const char*ct=argv[1]; int np=atoi(argv[3]); int maxp=argc>5?atoi(argv[5]):50;
  short*P=malloc((size_t)np*97*2); FILE*f=fopen(argv[2],"rb"); if(fread(P,2,(size_t)np*97,f)!=(size_t)np*97){fprintf(stderr,"perm read\n");return 1;} fclose(f);
  f=fopen(argv[4],"r"); NP=0; while(fscanf(f,"%26s %26s",F[NP],M[NP])==2){for(int i=0;i<26;i++){fi[NP][F[NP][i]-65]=i;mi[NP][M[NP][i]-65]=i;}NP++;} fclose(f);
  int cpos[24],pl[24]; for(int k=0;k<13;k++){cpos[k]=21+k;pl[k]=CR1[k]-65;} for(int k=0;k<11;k++){cpos[13+k]=63+k;pl[13+k]=CR2[k]-65;}
  int C[97]; for(int i=0;i<97;i++)C[i]=ct[i]-65;
  static const int WL[5]={15,17,18,19,23}; static const int WT[5][23]={{2,1,2,7,5,4,2,4,6,9,5,8,4,3,2},{3,2,3,1,2,3,2,4,2,6,1,2,1,3,2,1,5},
   {3,3,5,6,5,4,5,1,3,4,4,2,5,4,5,6,2,2},{1,2,3,4,1,2,4,1,3,2,1,2,5,3,1,2,1,3,5},{2,5,4,6,2,5,3,4,6,3,5,4,6,2,3,5,6,1,3,2,1,3,6}};
  static int WS[92][97],WN[92],WSt[92]; int nws=0;
  for(int w=0;w<5;w++) for(int st=0;st<WL[w];st++){ WS[nws][0]=0; for(int i=0;i<96;i++) WS[nws][i+1]=(WS[nws][i]+WT[w][(st+i)%WL[w]]+4)%26; WN[nws]=WL[w]; WSt[nws]=st; nws++; }
  static int blist[26][92],bcnt[26];
  long hitA=0,hitB=0,preB=0,printed=0; long hitAn[49]={0},hitBn[49]={0};
  for(int p=0;p<np;p++){ short*t=P+(size_t)p*97; int cl[24],q[24];
    for(int k=0;k<24;k++){q[k]=t[cpos[k]];cl[k]=C[q[k]];}
    memset(bcnt,0,sizeof bcnt); for(int ws=0;ws<nws;ws++){int v=((WS[ws][q[1]]-WS[ws][q[0]])%26+26)%26; blist[v][bcnt[v]++]=ws;}
    /* (ordering kept for reference) */
    int ord[24]; for(int k=0;k<24;k++)ord[k]=k;
    for(int a=1;a<24;a++){int x=ord[a],b=a-1;while(b>=0&&q[ord[b]]>q[x]){ord[b+1]=ord[b];b--;}ord[b+1]=x;}
    for(int pi=0;pi<NP;pi++) for(int sg=-1;sg<=1;sg+=2){
      int r[24]; for(int k=0;k<24;k++) r[k]=(((sg*(mi[pi][cl[k]]-fi[pi][pl[k]]))%26)+26)%26;
      /* ---- model A (exact) ---- */
      int ok=1; int d[97];
      for(int k=0;k<12&&ok;k++){d[k]=(r[k+1]-r[k]+26)%26; if(!isstep(d[k])) ok=0;}
      for(int k=13;k<23&&ok;k++){d[k]=(r[k+1]-r[k]+26)%26; if(!isstep(d[k])) ok=0;}
      if(ok){ int tgt=(r[13]-r[12]+26)%26;
        for(int n=1;n<=48;n++){ int need[48]; for(int j=0;j<n;j++) need[j]=-1; int g=1;
          for(int k=0;k<12&&g;k++){int j=(21+k)%n; if(need[j]<0)need[j]=d[k]; else if(need[j]!=d[k]) g=0;}
          for(int k=13;k<23&&g;k++){int j=(63+k-13)%n; if(need[j]<0)need[j]=d[k]; else if(need[j]!=d[k]) g=0;}
          if(!g) continue;
          int fixed=0,mult[48]={0}; for(int i=33;i<63;i++){int j=i%n; if(need[j]>=0) fixed+=need[j]; else mult[j]++;}
          char reach[26]={0}; reach[fixed%26]=1;
          for(int j=0;j<n;j++) if(mult[j]){ char nr[26]={0}; for(int x=0;x<26;x++) if(reach[x]) for(int s=5;s<=13;s++) nr[(x+mult[j]*s)%26]=1; memcpy(reach,nr,26);}
          if(reach[tgt]){ hitA++; hitAn[n]++; if(printed<maxp){printed++; printf("A perm=%d pair=%d sg=%d n=%d\n",p,pi,sg,n);} }
        } }
      /* ---- model B (exact, five published V1 wheels, any start sector, +4 rule) ---- */
      { int v=(r[1]-r[0]+26)%26; for(int c=bcnt[v]-1;c>=0;c--){ int ws=blist[v][c]; int *S=WS[ws]; int e=1;
          for(int k=2;k<24;k++) if(((r[k]-r[0]-S[q[k]]+S[q[0]])%26+52)%26){e=0;break;}
          if(e){ hitB++; hitBn[WN[ws]]++; if(printed<maxp){printed++; printf("B perm=%d pair=%d sg=%d wheel=%d start=%d\n",p,pi,sg,WN[ws],WSt[ws]);} } } }
    }
  }
  printf("SUMMARY A_exact=%ld B_exact_published=%ld\nAn:",hitA,hitB); for(int n=1;n<=48;n++) if(hitAn[n]) printf(" %d:%ld",n,hitAn[n]);
  printf("\nBn:"); for(int n=1;n<=48;n++) if(hitBn[n]) printf(" %d:%ld",n,hitBn[n]); printf("\n");
  return 0;
}

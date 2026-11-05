/* Cycle 122: Kryha V1 any-wheel leave-one-out.
   Input: "id r0..r23" residues at POS (same order as v2).
   For each n=1..48: strict B1; soft = exists drop making B1 pass.
   Output: "id nstrict_ns nsoft_only_ns first_soft_drop first_soft_n"
   Counts are over n in 1..48 (one line covers one alphabet pair × sense).
*/
#include <stdio.h>
#include <string.h>
static const int POS[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const int STEPS[9]={5,6,7,8,9,10,11,12,13};
static int in_steps(int d){ for(int i=0;i<9;i++) if(STEPS[i]==d) return 1; return 0; }

/* B1 with optional drop (-1 = none). Adjacent single-letter constraints among remaining
   consecutive crib positions only (merged 2-steps ignored = soft lower-bound spirit of c119). */
static int b1(const int *r, int n, int drop){
  int R[97]; memset(R,-1,sizeof R);
  for(int k=0;k<24;k++) if(k!=drop) R[POS[k]]=r[k];
  int need[48]; memset(need,-1,sizeof need);
  /* east adjacent */
  for(int i=21;i<33;i++){
    if(R[i]<0 || R[i+1]<0) continue;
    if(i+1!=i+1) {}
    int d=(R[i+1]-R[i]+26)%26;
    if(!in_steps(d)) return 0;
    int j=i%n;
    if(need[j]<0) need[j]=d; else if(need[j]!=d) return 0;
  }
  /* berlin adjacent */
  for(int i=63;i<73;i++){
    if(R[i]<0 || R[i+1]<0) continue;
    int d=(R[i+1]-R[i]+26)%26;
    if(!in_steps(d)) return 0;
    int j=i%n;
    if(need[j]<0) need[j]=d; else if(need[j]!=d) return 0;
  }
  /* gap: last remaining east crib (<=33) to first remaining berlin (>=63) */
  int left=-1,right=-1;
  for(int i=33;i>=21;i--) if(R[i]>=0){ left=i; break; }
  for(int i=63;i<=73;i++) if(R[i]>=0){ right=i; break; }
  if(left<0 || right<0) return 1; /* no gap check */
  int tgt=(R[right]-R[left]+26)%26;
  int fixed=0; int mult[48]; memset(mult,0,sizeof mult);
  for(int k=left;k<right;k++){
    int j=k%n;
    if(need[j]>=0) fixed+=need[j];
    else mult[j]++;
  }
  /* reachability of tgt from fixed via free sector counts */
  unsigned char reach[26]={0}, nreach[26];
  reach[fixed%26]=1;
  for(int j=0;j<n;j++) if(mult[j]){
    memset(nreach,0,26);
    for(int x=0;x<26;x++) if(reach[x])
      for(int si=0;si<9;si++) nreach[(x+mult[j]*STEPS[si])%26]=1;
    memcpy(reach,nreach,26);
  }
  return reach[tgt%26];
}

int main(){
  char id[64]; int r[24];
  while(scanf("%63s",id)==1){
    for(int k=0;k<24;k++) scanf("%d",&r[k]);
    int nstrict=0, nsoft=0, fdrop=-1, fn=-1;
    for(int n=1;n<=48;n++){
      int st=b1(r,n,-1);
      if(st){ nstrict++; continue; }
      for(int d=0;d<24;d++){
        if(b1(r,n,d)){
          nsoft++;
          if(fdrop<0){ fdrop=d; fn=n; }
          break;
        }
      }
    }
    printf("%s %d %d %d %d\n",id,nstrict,nsoft,fdrop,fn); fflush(stdout);
  }
  return 0;
}

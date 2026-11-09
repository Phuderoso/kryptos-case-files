#define MAXS 64
typedef struct{int n;int sol[MAXS][16];long tot;int ovf;}SolSet;
static void solve0(int p,int L,const int*kk,SolSet*S){          /* identical algebra to lr178.c solve0 */
  int n=L+1,A[24][17],nr=0;S->n=0;S->tot=0;S->ovf=0;
  for(int i=21+L;i<=33;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  for(int i=63+L;i<=73;i++){for(int j=1;j<=L;j++)A[nr][j-1]=kk[i-j-21];A[nr][L]=1;A[nr][n]=kk[i-21];nr++;}
  int piv[17],rk=0;for(int col=0;col<n&&rk<nr;col++){int r=-1;for(int i=rk;i<nr;i++)if(A[i][col]%p){r=i;break;}if(r<0)continue;
    if(r!=rk)for(int j=0;j<=n;j++){int t=A[r][j];A[r][j]=A[rk][j];A[rk][j]=t;}
    int iv=p==2?1:inv13[A[rk][col]%p];for(int j=0;j<=n;j++)A[rk][j]=(A[rk][j]*iv)%p;
    for(int i=0;i<nr;i++)if(i!=rk&&A[i][col]%p){int f=A[i][col];for(int j=0;j<=n;j++)A[i][j]=md(A[i][j]-f*A[rk][j],p);}
    piv[rk++]=col;}
  for(int i=rk;i<nr;i++)if(A[i][n]%p)return;
  int isp[17]={0};for(int r=0;r<rk;r++)isp[piv[r]]=1;int fr[17],nf=0;for(int j=0;j<n;j++)if(!isp[j])fr[nf++]=j;
  long ns=1;for(int i=0;i<nf;i++){ns*=p;if(ns>5000000){S->ovf=1;return;}}
  for(long z=0;z<ns;z++){int x[17];long y=z;for(int i=0;i<nf;i++){x[fr[i]]=y%p;y/=p;}
    for(int r=0;r<rk;r++){int v=A[r][n];for(int i=0;i<nf;i++)v-=A[r][fr[i]]*x[fr[i]];x[piv[r]]=md(v,p);}
    int s[53];memcpy(s,kk,13*sizeof(int));int ok=1;
    for(int i=34;i<=73&&ok;i++){int v=x[L];for(int j=1;j<=L;j++)v+=x[j-1]*s[i-j-21];v%=p;s[i-21]=v;if(i>=63&&v!=kk[i-21])ok=0;}
    if(!ok)continue;S->tot++;if(S->n<MAXS){memcpy(S->sol[S->n],x,n*sizeof(int));S->n++;}}
}

//Author : Kazi Istiak Uddin
//Brainiac Luthor
#include<bits/stdc++.h>
using namespace std;
#define ll long long int
ll isprime[1005],a[1005];
ll bigmod(ll a,ll b, ll mod){
    if(b==0) return 1;
    ll x=bigmod(a,b/2,mod);         
    x=(x*x)%mod;
    if(b%2) x=(x*a)%mod;
    return x;
}
ll phi(ll n){
    double result=n;
    for (ll p=2;p*p<=n;++p){
        if (n%p==0){
            while(n%p==0)   n/=p;
            result*=(1.0-(1.0/(double)p));
        }
    }
    if(n>1)
        result*=(1.0-(1.0/(double)n));
    return (ll)result;
}
ll power(ll d,ll s){
    if(s==1) return d;      
    else if(s==0) return 1;
    //else if(d==1) return d;
    else{
        ll v = d;
        for(ll u = 1 ;  u < s ; u++)    d=d*v;
        
        return d;
    }
}


int main(){
    //finding primitive roots//
    //seive//
    ll i,j,euler1,euler2,k,chq,s,chq1;
    for(i=2;i*i<=1000;i++)
    {
        if(!isprime[i])
        {
            for(j=i*i;j<=1000;j=j+i)
                isprime[j]=1;
        }
    }
    //for(i=1;i<=100;i++) cout<<isprime[i]<<" ";
    for(i=1;i<=1000;i++)
    {
        if(i==1)
        {
            printf("%lld ", i);
            printf("NO Primitive root\n");
        }
        else if(!isprime[i])
        {
            vector<ll>v;
            cout<<i<<" ";
            euler1=i-1;
            k=euler1;         
            euler2=phi(euler1);
            
            
            cout<<euler2<<" "<<"Primitive roots"<<" ";
            
            
            //factorizimg euler1//
            for(j=2;j*j<=euler1;j++)
            {
                if(!(euler1%j))
                {
                    v.push_back(j);
                    while(!(euler1%j)) euler1/=j;
                }
            }
            if(euler1>1) v.push_back(euler1);
            euler1=k;        
            
            
            cout<<"They are {";
            
            
            for(j=1;j<i;j++)
            {
                ll chq=0;
                for(k=0;k<v.size();k++)
                {
                    s=euler1/v[k];
                    if(bigmod(j,s,i)==1)
                    {
                        chq=1;break;
                    }
                }
                if(chq==0) cout<<j<<" ";
            }
            cout<<"}"<<endl<<endl;

        }
        else
        {
            //we have to check somethhing whether i can be powerr of any prime or 2*anyprime^k; also prime can't be 2,but only suitable for 4//
            if(i==4)
            {
                cout<<i<<" "<<"1 primitive root {"<<3<<"}"<<endl<<endl;
            }
            else
            {
                ll chq=0,k=i,x=0;
                if(!(k%2)) {
                    k/=2;
                }
                for(j=2;j*j<=k;j++)
                {
                    if(k%j==0)
                    {
                        if(j==2)
                        {
                            chq=1;   x=0;   break;
                        }
                        x++;
                        while(!(k%j)) 
                            k/=j;
                    }
                }
                if(x==0&&chq)
                {
                    cout<<i<<" "<<"NO Primitive root"<<endl<<endl;
                    continue;
                }
                else if(k>1)  x++;
                if(x>1)  cout<<i<<" "<<"NO Primitive root"<<endl<<endl;
                else
                {
                    vector<ll>v;
                    cout<<i<<" ";    k=i;
                    euler1=phi(k);
                    k=euler1;    
                    euler2=phi(k);
                    
                    
                    cout<<euler2<<" "<<"Primitive roots"<<" ";
                    
                    
                    
                    //factorizimg euler1//
                    for(j=2;j*j<=euler1;j++)
                    {
                        if((euler1%j)==0)
                        {
                            v.push_back(j);
                            while((euler1%j)==0)
                                euler1/=j;
                        }
                    }
                    if(euler1>1) v.push_back(euler1);
                    euler1=k;
                    //cout<<euler1<<" "<<v.size()<<" ";
                    cout<<"They are {";
                    for(j=1;j<i;j++)
                    {
                            ll chq=0;chq1=0;
                        for(k=0;k<v.size();k++)
                        {
                            s=euler1/v[k];
                            if(bigmod(j,s,i)==i-1)  chq=1;
                            else if(bigmod(j,s,i)==1)   chq1=1;
                        }
                        if(chq+chq1==1&&chq) cout<<j<<" ";
                        //else if(chq==1&&v.size()==1) cout<<j<<" ";
                    }
                    cout<<"}"<<endl<<endl;;
                }
            }

        }

    }
}

#include<bits/stdc++.h>
using namespace std;
#define ll long long int
#define RANGE 1000

ll isprime[RANGE+5], a[RANGE+5];

// Function to compute (a^b) % mod using recursion
ll bigmod(ll a, ll b, ll mod) {
    if(b == 0) return 1;
    ll x = bigmod(a, b / 2, mod);
    x = (x * x) % mod;
    if(b % 2) x = (x * a) % mod;
    return x;
}

// Function to compute Euler's Totient function φ(n)
ll phi(ll n) {
    double result = n;
    for(ll p = 2; p * p <= n; ++p) {
        if(n % p == 0) {
            while(n % p == 0) n /= p;
            result *= (1.0 - (1.0 / (double)p));
        }
    }
    if(n > 1)
        result *= (1.0 - (1.0 / (double)n));
    return (ll)result;
}

//what is priitive roots?
//primitive root of a prime number p is an integer g such that for any integer a coprime to p, there is an integer k for which g^k ≡ a (mod p).
//primitive root of a composite number n is an integer g such that for any integer a coprime to n, there is an integer k for which g^k ≡ a (mod n).
//primitive root of a prime power p^k is an integer g such that for any integer a coprime to p, there is an integer k for which g^k ≡ a (mod p^k).

// Main function to find and display primitive roots
int main() {
    // Sieve of Eratosthenes to find prime numbers up to RANGE

    for(ll i = 2; i * i <= RANGE; i++) {
        if(!isprime[i]) {
            for(ll j = i * i; j <= RANGE; j += i)
                isprime[j] = 1;
        }
    }

    // Loop to find primitive roots foreach number from 1 to RANGE
    for(ll i = 1; i <= RANGE; i++) {
        if(i == 1) {
            cout << i << " NO Primitive root\n";
        } 
        else if(!isprime[i]) {
            // ifi is prime
            vector<ll> factors;
            ll euler1 = i - 1;
            ll euler2 = phi(euler1);

            cout << i << " --> " << euler2 << " Primitive roots ";

            // Factorizing euler1
            for(ll j = 2; j * j <= euler1; j++) {
                if(euler1 % j == 0) {
                    factors.push_back(j);
                    while(euler1 % j == 0) {
                        euler1 /= j;
                    }
                }
            }
            if(euler1 > 1) factors.push_back(euler1);
            euler1 = i - 1;

            cout << "\nThey are { ==";
            for(ll j = 1; j < i; j++) {
                bool isPrimitive = true;
                for(ll k = 0; k < factors.size(); k++) {
                    ll s = euler1 / factors[k];
                    if(bigmod(j, s, i) == 1) {
                        isPrimitive = false;
                        break;
                    }
                }
                if(isPrimitive) cout << j << " ";
            }
            cout << " == }\n\n";

        } 
        else {
            // i is composite number
            if(i == 4) {
                cout << i << " 1 primitive root {3}\n\n";
            } 
            else {
                ll k = i;
                if(k % 2 == 0) k /= 2;
                ll x = 0;
                bool hasInvalidPrimeFactor = false;

                for(ll j = 2; j * j <= k; j++) {
                    if(k % j == 0) {
                        if(j == 2) {
                            hasInvalidPrimeFactor = true;
                            break;
                        }
                        x++;
                        while(k % j == 0) {
                            k /= j;
                        }
                    }
                }
                if(k > 1) x++; // x is the number of prime factors of i

                if(x > 1 || hasInvalidPrimeFactor) {
                    cout << i << " --> NO Primitive root\n\n"; 
                } 
                else {
                    // Finding primitive roots forthe remaining composite numbers
                    vector<ll> factors;
                    ll euler1 = phi(i);
                    ll euler2 = phi(euler1);

                    cout << i << " --> " << euler2 << " Primitive roots ";

                    // Factorizing euler1
                    for(ll j = 2; j * j <= euler1; j++) {
                        if(euler1 % j == 0) {
                            factors.push_back(j);
                            while(euler1 % j == 0) {
                                euler1 /= j;
                            }
                        }
                    }
                    if(euler1 > 1) factors.push_back(euler1);
                    euler1 = phi(i);

                    cout << "\nThey are { == ";
                    for(ll j = 1; j < i; j++) {
                        bool isPrimitive = false;
                        bool isNonPrimitive = false;
                        for(ll k = 0; k < factors.size(); k++) {
                            ll s = euler1 / factors[k];
                            if(bigmod(j, s, i) == i - 1) isPrimitive = true;
                            if(bigmod(j, s, i) == 1) isNonPrimitive = true;
                        }
                        if(isPrimitive && !isNonPrimitive) cout << j << " ";
                    }
                    cout << " == }\n\n";
                }
            }
        }
    }
}

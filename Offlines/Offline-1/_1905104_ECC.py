from Crypto.Util import number
from Crypto.Random import random
import copy
import math
import time

def bigmod(a,b,m) :
    if b == 0 : 
        return 1
    if b % 2 == 0 : 
        r = (r * r) % m
        return  r
    return ((a%m)*bigmod(a,b-1,m)%m)%m

def genShared(bits) :
    p = number.getPrime(bits)
    e = p + 1 - int(math.sqrt(2*p))
    a = number.getRandomRange(2,p-1)

    r = (4* a**3) % p 
    b = number.getRandomRange(2,p-1) 
    while (r + 27*b*b) % p == 0 :
        b = number.getRandomRange(2,p-1)
    
    return e,p,a,b

                
# y^2 = ( x^3 + ax + b ) % p
# has solution for y iff a^(p-1)/2 = 1 mod p
# euler criterion

def func(x,a,b,p) :
    y = (x**3) + a*x + b

    y = y%p

    inv = pow(y,(p-1)//2 ,p)
    if inv == 1 :
        return pow(y,(p+1)//4,p) 
    else :
        return None 

def genG(p,a,b) :
    g_y = None
    while not g_y :
        g_x = number.getRandomRange(2,p-1)
        g_y = func(g_x,a,b,p)
    
    return g_x,g_y

def double_and_add(Px,Py,privateKey,p,a,b) :
    #Initialize T = P
    Tx = Px
    Ty = Py
    tot_bits = privateKey.bit_length()

    for i in range(tot_bits - 1 , -1 ,-1) :
        s = (((3*Tx**2+a) %p) * (pow(2*Ty,p-2,p) % p))%p
        x3 = (s*s - Tx - Tx) % p
        y3 = (s*(Tx-x3) - Ty) % p
        Tx,Ty = x3,y3 

        di = privateKey & (1 << i)

        if di == 1:
            s = (Py-Ty) * pow((Px-Tx),p-2,p) % p
            x3 = (s**2 - Tx - Px) % p
            y3 = (s*(Tx-x3) - Ty) % p
            Tx,Ty = x3,y3 
    
    return Tx,Ty

if __name__ == "__main__":

    bits = [128,192,256]
    A_time = 0
    B_time = 0
    S_time = 0

    for i in range(len(bits)) :

        print("Trial for bits : ",bits[i],end = "\n\n")
        for j in range(5):

            e,p, a, b = genShared(bits[i])
            [g_x,g_y] = genG(p,a,b)
            # p ,a,b,g_x,g_y = [997,7,-19,4,5]

            pr_ka = number.getRandomRange(2,e-1)
            pr_kb = number.getRandomRange(2,e-1)

            start = time.time()
            pu_ka = double_and_add(g_x,g_y,pr_ka,p,a,b)
            A_time+= time.time() - start

            start = time.time()
            pu_kb = double_and_add(g_x,g_y,pr_kb,p,a,b)
            B_time+= time.time() - start

            # print("Alice's private key : ",pr_ka)
            # print("Bob's private key : ",pr_kb,end = "\n\n")

            # print("Alic's public key : ",pu_ka)
            # print("Bob's public key : ",pu_kb,end = "\n\n")

            start = time.time()
            shared_kb = double_and_add(pu_ka[0],pu_ka[1],pr_kb,p,a,b)
            shared_ka = double_and_add(pu_kb[0],pu_kb[1],pr_ka,p,a,b)

            S_time+= time.time() - start

            # print(p,a,b,g_x,g_y)
            # print(pr_ka,pu_ka)
            # print("Alice's secret key : ",shared_ka[0])
            # print("Bob's secret key : ",shared_kb[0],end = "\n\n")


        print("Generating A taking time : ", (A_time/5)*1000," miliseconds")
        print("Generating B takes : ", (B_time/5)*1000, " miliseconds")
        print("Public to secret key generation time  : ",(S_time/5)*1000," miliseconds",end = "\n\n\n")



    # print(pow(12,-1,3))
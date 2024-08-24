import random
import math
import time

def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b,a%b)
    
def modinverse(a, b):
    x , y = 0 ,1
    x1 , y1 = 1, 0
    m = b
    while b :
        q = a // b
        a, b = b, a % b
        x, x1 = x1 - q * x , x
        y, y1 = y1 - q * y , y
    if a != 1 :
        return None
    else :
        return (x1 % m + m) % m
    

## calculate x^y under modulo p
def pow(x, y, p):
    res = 1; 
    x = x % p; 
    while y :
        if y & 1 :
            res = res * x
            res = res % p 
        y = y>>1
        x = (x * x) % p;
     
    return res;
 
# b0 = a^m mod n
# b1 = b0^2 mod n
# b2 = b1^2 mod n
# ...
# ...
# if bx == -1 mod n then n is probably prime
# if bx == 1 mod n then n is composite
def isComposite(a,m,n,c) :
    b = pow(a,m,n)
    if b == 1 or b == n-1 :
        return False
    for i in range(1,c) :
        b = (b*b) % n
        # b = pow(b,2,n)
        if b == n-1 :
            return False
    return True

# Miller-Rabin primality test
# n is the number to be tested
# c is the number of times to test
def MilerRabinisPrime(n,iter) :
    if n < 2 :
        return False # 1 is not prime
    if n == 2 :
        return True # 2 is prime
    if n & 1 == 0 :
        return False # n is even
    m = n-1
    c = 0
    # n-1 = 2^k * m
    while m % 2 == 0 :
        m>>=1   # m = m//2  ; floor division
        c = c+1
    for i in range(iter) :
        # a need to in range 1 < a < n-1
        a = random.randint(2,n-1)
        # checking if a is a witness for compositeness
        if isComposite(a,m,n,c) :
            return False
    return True

######################################################################################
# Proof------------------------------------------------------------------------------#
# let n = 2^k * m  ------------------------------------------------------------------#
#     m must be an odd number -------------------------------------------------------#
#     we select a random number a in range 1 < a < n-1 ------------------------------#
#     b = a^m mod n -----------------------------------------------------------------#
#     m is a divisor of n-1 ---------------------------------------------------------#
#     now , -------------------------------------------------------------------------#
#         x^(n-1) - 1= x^(2^k * m -1) - 1 -------------------------------------------#
#        if we factorize it we will get ---------------------------------------------#
#         x^(n-1) - 1 = (x^k-1)(x^k+1)(x^2k+1).....(x^(2^(c-1))k + 1) ---------------#
#         replace x with a ----------------------------------------------------------#
#         Then if n is prime and 1 < a < n-1 ; --------------------------------------#
#         using fermats theorem a^(n-1) = 1 mod n ; as phi(n) = n-1 for prime n -----#
#         so a^(n-1) - 1 = 0 mod n --------------------------------------------------#
#         so a^(n-1) - 1 = (a^k-1)(a^k+1)(a^2k+1).....(a^(2^(c-1))k + 1) = 0 mod n --#
#         so one of these factors must be 0 mod n -----------------------------------#
#         a^k = 1 mod n or a^(2^q * k) = -1 mod n for some q such that 1 < q < c-1 --#
######################################################################################

def gen_prime(length):
    p = random.getrandbits(length)
    while not MilerRabinisPrime(p,100) :
        p = random.getrandbits(length)
    
    return p


def encrypt(msg_plaintext, e, n):
    msg_ciphertext = []
    for c in msg_plaintext :
        msg_ciphertext.append(pow(ord(c), e, n))
    return msg_ciphertext


def decrypt(msg_ciphertext, d, n):
    msg_plaintext = []
    for c in msg_ciphertext :
        msg_plaintext.append(chr(pow(c, d, n)))
    return (''.join(msg_plaintext))


def genKey(length) :
    key = length # key length
    p , q = gen_prime(key//2) , gen_prime(key//2)
    while p == q :
        q = gen_prime(key//2)
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randint(2,phi-1)
    while gcd(e,phi) != 1 :
        e = random.randint(2,phi-1)
    d = modinverse(e,phi)

    return e,d,n

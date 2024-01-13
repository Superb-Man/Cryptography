import RSA
import random

if __name__ == "__main__":

    e,d,n = RSA.genKey(1024)
    print("public key : {",e,",",n,"}")
    print("private key : {",d,",",n,"}")
    msg = input("Write msg: ")
    encrypted_msg = RSA.encrypt(msg, e, n)
    print("Encrypted msg: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypted msg: ")
    print(RSA.decrypt(encrypted_msg, d, n))
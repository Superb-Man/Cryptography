import socket	
import copy
import AES
import RSA

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
    port = 6212			
    s.connect(('127.0.0.1', port))
    print("Connected to server")

    e ,d ,n = RSA.genKey(128) 
    
    s.send((str(e) + "," + str(n)).encode()) 
    # print("Public key : ",e,n)

    msg = s.recv(1024).decode()
    msg = msg.split(",")
    plaintxt_key = [int(msg[i]) for i in range(len(msg))]
    keys = RSA.decrypt(plaintxt_key,d,n)

    print("Key : ",keys)
    keys = AES.getKey(keys,128)

    msg = s.recv(1024).decode()
    cipher = []
    x = copy.copy(msg)
    for i in range(0,len(msg),2) :
        cipher.append(x[i:i+2])
    print(cipher)
    plaintxt = AES.AES_recv(128,cipher,0,keys[0],1)

    # print("here")

    print("Toriqe sent) : " + AES.hexToString(plaintxt))

    s.close()

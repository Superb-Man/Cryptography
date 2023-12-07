import socket	

from _1905104_AES import * 
from _1905104_ECC import *


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
    port = 6212			
    s.connect(('127.0.0.1', port))
    msg = s.recv(1024).decode()
    msg = msg.split(",")

    # print("Client msg : ", msg)

    [e,p,a,b,g_x,g_y,pu_ka_0,pu_ka_1] = [int(msg[i]) for i in range(len(msg))]
    pu_ka = [pu_ka_0,pu_ka_1] 
    
    pr_kb = number.getRandomRange(2,e-1) 
    pu_kb = double_and_add(g_x,g_y,pr_kb,p,a,b)

    s.send((str(pu_kb[0])+","+str(pu_kb[1])).encode())

    shared_kb = double_and_add(pu_ka[0],pu_ka[1],pr_kb,p,a,b)

    # key = getKey(str(shared_kb))
    print("Shared Secret Key : ",shared_kb[0],end = "\n\n")

    key = getKey(str(shared_kb[0]),128)
    msg = s.recv(4096).decode()
    msg = msg.split(",")
    cipher = []
    x = copy.copy(msg[0])
    for i in range(0,len(msg[0]),2) :
        cipher.append(x[i:i+2])
    plaintxt = AES_recv(128,cipher,msg[1],key[0],1)

    # print("here")

    if msg[1] == True:
        with open("decrypted_File(Sent From Alice)", 'wb') as f:
            f.write(binascii.unhexlify("".join(plaintxt)))
    else :
        print("\Server(Alice sent) : " + hexToString(plaintxt))

    s.close()

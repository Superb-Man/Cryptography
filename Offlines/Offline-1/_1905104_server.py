import socket	
from _1905104_AES import * 
from _1905104_ECC import *


if __name__ == "__main__":

    KEY_LENGTH = 128
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
    print ("Socket successfully created")

    port = 6212			
    s.bind(('', port))		
    print ("socket binded to %s" %(port))

    # put the socket into listening mode
    s.listen()	
    print ("socket is listening")
    e,p, a, b = genShared(KEY_LENGTH)
    [g_x,g_y] = genG(p,a,b)
    while True :
        client = s.accept()
        print("Request accepted from : ", client[1],end = "\n\n")
        # p ,a,b,g_x,g_y = [997,7,-19,4,5]

        pr_ka = number.getRandomRange(2,e-1)
        pu_ka = double_and_add(g_x,g_y,pr_ka,p,a,b)

        msg = str(e)+","+str(p)+","+str(a)+","+str(b)+","+str(g_x)+","+str(g_y)+","+str(pu_ka[0])+","+str(pu_ka[1]) 
        # msg = [e,p,a,b,g_x,g_y,pu_ka]


        client[0].send(msg.encode())

        msg =  client[0].recv(1024).decode()
        msg = msg.split(",") 
        pu_kb = [int(msg[i]) for i in range(len(msg))]
        shared_ka = double_and_add(pu_kb[0],pu_kb[1],pr_ka,p,a,b)

        print("Shared Secret Key : ",shared_ka[0],end = "\n\n") ;

        isFile   = bool(int(input("Enter 1 for text or 2 for file: "))-1)
        msg = ""
        if isFile :
            msg  = input("Enter file : ")
        else :
            msg  = input("Enter txt : ")
        # print("Shared key : ",key,end = " ")
        # mode     = input("Enter mode CB : ")
        key = str(shared_ka[0])
        keys , cipher = AES_send(128,msg,isFile,getKey(key,128)[0],1) 
        msg = ""
        for i in range(len(cipher)):
            msg = msg+cipher[i]
        # print(msg)
        client[0].send((msg+","+str(isFile)).encode())

        client[0].close() 

        # break
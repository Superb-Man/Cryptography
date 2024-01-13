import socket	
import os
import sys
import RSA

# path = os.getcwd() 
# path = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(path))))
# path = os.path.join(path,"Offlines/Offline-1")
# sys.path.insert(0,path)

import AES



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
    while True :
        client = s.accept()
        print("Request accepted from : ", client[1],end = "\n\n")

        print("Lara shared her public key")
        msg =  client[0].recv(1024).decode()
        msg = msg.split(",")
        public_key = [int(msg[i]) for i in range(len(msg))] 
        # print(public_key)

        keys = input("Enter key : ")
        cipherkeys = RSA.encrypt(keys,public_key[0],public_key[1])
        # print(''.join(map(lambda x: str(x), cipherkeys)))
        msg = ""
        for i in range (len(cipherkeys)) :
            if i != len(cipherkeys) - 1 :
                msg = msg+str(cipherkeys[i])+","
            else :
                msg+=str(cipherkeys[i])
        client[0].send(msg.encode())
        msg = input("Enter your text here : ")
        keys , cipher = AES.AES_send(128,msg,0,AES.getKey(keys,128)[0],1) 
        msg = ""
        print(cipher)
        for i in range(len(cipher)):
            msg = msg+cipher[i]
        # print(msg)
        client[0].send(msg.encode())

        client[0].close() 

        # break
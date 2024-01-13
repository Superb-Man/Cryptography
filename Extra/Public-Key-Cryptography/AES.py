import binascii
import time
from BitVector import *
import copy
import random
import math
import threading
from concurrent.futures import ProcessPoolExecutor
CTR_random = "a3fa6d97f4807e145b37451fc344e58c"

AES_modulus = BitVector(bitstring='100011011')
bzero = BitVector(hexstring="00")
btwo = BitVector(hexstring="02")
bsthree = BitVector(hexstring="63")

roundArrayMap = {128 : 10 , 192 : 12 , 256 : 14}
paddingmap = ["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f"]
invPaddingMap = {"01":1,"02":2,"03":3,"04":4,"05":5,"06":6,"07":7,"08":8,"09":9,"0a":10,"0b":11,"0c":12,"0d":13,"0e":14,"0f":15,"00":16}

def hexToArray(hexVal) :
    length = len(hexVal) 
    array = []
    for i in range(0,length,2) :
        array.append(hexVal[i:i+2])

    return array

def stringToHex(string):
    return hexToArray(string.encode().hex())

def hexToString(string): 
    return bytes.fromhex("".join(string)).decode("latin-1", errors="ignore")

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

mulTable = [] 

def preCalc():
    arr = {0, 1, 2, 3, 9, 11, 13, 14}
    for i in range(16):
        nrow = []
        if i in arr :
            for j in range(256):
                nrow.append(BitVector(intVal=i, size=8).gf_multiply_modular(BitVector(intVal=j, size=8), AES_modulus, 8))

        mulTable.append(nrow)
    return mulTable

def byteToMatrix(byteArray) :
    mat = []
    for k in range(4) :
        r = [BitVector(hexstring = byteArray[i]) for i in range(k,len(byteArray),4)]
        mat.append(r) ;
    return mat 

def subBytes(mat) :
    matrix2 = []
    for r in mat :
        nrow = [BitVector(intVal=Sbox[boxVal.intValue()], size=8) for boxVal in r]
        matrix2.append(nrow) 
    
    return matrix2

def invSubBytes(mat) :
    matrix2 = []
    for r in mat :
        nrow = [BitVector(intVal = InvSbox[boxVal.intValue()], size=8) for boxVal in r]
        matrix2.append(nrow) 
    
    return matrix2

def xorAdd(mat1,mat2) :
    newmat = [] 

    for r1,r2 in zip(mat1,mat2) :
        nrow = [val1 ^ val2 for val1,val2 in zip(r1,r2)]
        newmat.append(nrow)

    return newmat 

def xorAddlist(r) :
    res = bzero 
    for e in r : 
        res = res ^ e 
    
    return res 

def shiftLeft(mat) :
    newmat = [] 
    for i in range(4) :
        nrow = copy.copy(mat[i])
        for j in range (i) :
            nrow.append(nrow.pop(0)) 
        newmat.append(nrow)

    return newmat

def shiftRight(mat) :
    newmat = [] 
    for i in range(4) :
        nrow = copy.copy(mat[i])
        for j in range (i) :
            nrow.insert(0,nrow.pop()) 
        newmat.append(nrow)

    return newmat


def mul(mat1,mat2) :
    # preCalc()
    # [[sum(val1*val2 for val1,val2 in zip(r,c)) for c in zip(*mat2)] for r in mat1]
    return [[xorAddlist([mulTable[val1.intValue()][val2.intValue()] for val1, val2 in zip(r, c)]) \
        for c in zip(*mat2)] for r in mat1]


def g(r,rc) :
    nrow = copy.copy(r) 
    for i in range(1) :
        nrow.append(nrow.pop(0))
    nrow = [BitVector(intVal=Sbox[boxVal.intValue()], size=8) for boxVal in nrow]
    nrow = [(val1 ^ val2) for val1,val2 in zip(nrow,[rc,bzero,bzero,bzero])]

    return nrow
    

def schedule(key) :
    totalRound = roundArrayMap[len(key) * 8]
    col = int(len(key)/4)

    keys = [] 
    ikeys = byteToMatrix(key) 
    keys.append(ikeys) 
    round_constant = BitVector(hexstring ="01")

    for rnumber in range (1,totalRound+1) :
        r = []
        for i in range(4) :
            r.append(keys[rnumber-1][i][col-1])
        last = g(r,round_constant)
        curKey = [] 

        for j in range(col) :
            nword = [val1^val2 for val1,val2 in zip([keys[rnumber-1][i][j] for i in range(4)],last)]
            curKey.append(nword) 
            last = nword
        # transposing a matrix
        curKey = [list(rr) for rr in zip(*curKey)] 
        keys.append(curKey)
        # print("Curkey : ", [e.get_bitvector_in_hex() for col in zip(*curKey) for e in col] )
        round_constant = btwo.gf_multiply_modular(round_constant,AES_modulus,8)
    
    return keys


def encryptBlock(block , ekeys , totalRound , ivector) :
    #CBC
    # l = len(block)
    # print(l)
    # for i in range(l) :
    #     block[i] = str(BitVector(hexstring = block[i]) ^ BitVector(hexstring = ivector[i])).encode().hex()
    #     print(block[i])
    # print(ivector,end="\n\n")
    cipher = xorAdd(byteToMatrix(ivector),byteToMatrix(block))
    cipher = xorAdd(cipher,ekeys[0]) 
    for i in range(1, totalRound+1) :
        cipher = (shiftLeft(subBytes(cipher)))
        if(i < totalRound) :
            cipher = mul(Mixer,cipher)
        cipher = xorAdd(cipher,ekeys[i])
    ivector = [e.get_bitvector_in_hex() for col in zip(*cipher) for e in col] 
    #print(ivector)
    return ivector

def encryptMsg(msg,ekeys,nro) :
    res = []
    size = len(ekeys[0][0]) * 4
    ivector = ["00"] * size
    for i in range(0,len(msg),size) :
        #print(ivector)
        ivector = encryptBlock(msg[i:i+size],ekeys,nro,ivector)
        res.extend(ivector)



    return res

def decryptBlock(block , ekeys , totalRound , ivector) :
    #CBC
    #cipher = xorAdd(byteToMatrix(block),ivector)
    plaintxt = xorAdd(byteToMatrix(block),ekeys[0]) 
    for i in range(1, totalRound+1) :
        plaintxt = (shiftRight(invSubBytes(plaintxt)))
        plaintxt = xorAdd(plaintxt,ekeys[i])
        if(i < totalRound) :
            plaintxt = mul(InvMixer,plaintxt)
    plaintxt = xorAdd(plaintxt,byteToMatrix(ivector))
    return [e.get_bitvector_in_hex() for col in zip(*plaintxt) for e in col]


def decryptMsg(msg,ekeys,nro) :
    res = []
    ekeys.reverse()
    size = len(ekeys[0][0]) * 4
    ivector = ["00"] *size
    for i in range(0,len(msg),size) :
        res.extend(decryptBlock(msg[i:i+size],ekeys,nro,ivector))
        ivector = msg[i:i+size]

    return res 



def encryptBlockCTR(block , ekeys , totalRound , counter,thrd,lock,encrypt) :
    #CTR
    # lock.acquire()
    global x
    global rcver
    counter = int(counter,16) + thrd
    counter = hex(counter)
    counter = counter[2:]
    counter = hexToArray(counter)
    # print(block)
    cipher = xorAdd(byteToMatrix(counter),ekeys[0]) 
    for i in range(1, totalRound+1) :
        cipher = (shiftLeft(subBytes(cipher)))
        if(i < totalRound) :
            cipher = mul(Mixer,cipher)
        cipher = xorAdd(cipher,ekeys[i])
    cipher = xorAdd(cipher,byteToMatrix(block))
    cipher = [e.get_bitvector_in_hex() for col in zip(*cipher) for e in col]
    if int(encrypt) == 1 :
        x[thrd] = cipher
    else :
        rcver[thrd] = cipher 
    # print(cipher)
    print(thrd)
    # lock.release() 
    return cipher


def getKey(key,type) :
    hexKey = stringToHex(key)
    size = int(type/8)
    l2 = len(hexKey)
    while(l2 > size) :
        hexKey.pop()
        l2-=1
    while(l2 < size) :
        hexKey.append("20")
        l2+=1
    ekeys = schedule(copy.copy(hexKey))

    return ekeys,hexKey

def AES_send(type,msg,isFile,ekeys,mode):
    preCalc()
    print("\n\n\nAES - "+str(type)+":\n")

    msgHex = stringToHex(msg)

    if isFile:
        with open(msg,'rb') as f :
            msgHex = hexToArray(f.read().hex())
    l1 = len(msgHex)

    size = int(type/8)
    nro  = roundArrayMap[type]

    xtra = 0 
    if((l1+xtra) %16 == 0) :
        msgHex.append("00")
        xtra+=1
        while((l1+xtra) %16 != 0) :
            msgHex.append("00")
            xtra+=1
            #print('laraloveslinux')

    mod  = 16 - (l1+xtra)%16
    # print(mod)
    while((l1+xtra) %16 != 0) :
        msgHex.append(paddingmap[mod])
        xtra+=1

    print("\nPlain text/File(In hex) : ",end = " ")
    for i in range(l1+xtra):
        print(msgHex[i]+" ",end = " ")
    print("\n")
    # print(mode)
    if int(mode) == 2 :
        global CTR_random
        CTR_random = random.getrandbits(int(type))
        CTR_random = hex(CTR_random)
        CTR_random = CTR_random[2:]
        while((len(CTR_random)*4)%8 != 0) :
            CTR_random+='0'
        global x 
        no_threads = math.ceil(len(msgHex)/(type/8))  
        executor = ProcessPoolExecutor(no_threads)
        # print("Threads : ",no_threads)
        x = ["00"]*no_threads
        # lock = threading.Lock() 
        lock = 0
        sz = len(ekeys[0][0]) * 4
        j = 0 
        # tt = [0]*(no_threads)
        # print("Here")
        futures1 = []
        for i in range(no_threads) :
            future = executor.submit(encryptBlockCTR,msgHex[j:j+sz],ekeys,nro,CTR_random,i,lock,1)
            # print("HERE")
            futures1.append(future.result()) 
            # print(future.result())
            j+=sz
    
        # # start threads 
        # for i in range(no_threads) :
        #     tt[i].start()
    
        # # wait until threads finish their job 
        # for i in range(no_threads) :
        #     tt[i].join()
        # print("X is : " ,x)
        cipherHex = []
        for i in range(no_threads) :
            cipherHex.extend(futures1[i])
    else :
        cipherHex = encryptMsg(msgHex,ekeys,nro)
    cipherAscii = hexToString(cipherHex)
    # print("CipherText in ASCII : "+cipherAscii)


    return ekeys,cipherHex

def AES_recv(type,msg,isFile,key,mode) :
    preCalc()
    size = int(type/8)
    nro  = roundArrayMap[type]
    # print(msg)

    if int(mode) == 2 :
        global rcver
        global CTR_random 
        no_threads = math.ceil(len(msg)/(type/8))  
        executor1 = ProcessPoolExecutor(no_threads)
        rcver = ["00"]*no_threads
        # lock2 = threading.Lock()
        lock2 = 0 
        sz = len(key[0][0]) * 4
        j = 0 
        # t = [0]*(no_threads)
        futures = []
        for i in range(no_threads) :
            # print("here")
            future = executor1.submit(encryptBlockCTR,msg[j:j+sz],key,nro,CTR_random,i,lock2,0)
            futures.append(future.result())
            # print(future.result())
            j+=sz

        decipheredMsg = []
        for i in range(no_threads) :
            decipheredMsg.extend(futures[i])
        # print("Deciphering in CTR mode")

    else :
        decipheredMsg = decryptMsg(msg, key, nro)
    lol = copy.copy(decipheredMsg) 
    popp = 0 
    cnt = 0
    laastt =""
    while cnt != 16:
        y = lol.pop()
        # print(y)
        if y == "00" :
            popp+=1
        if cnt == 0 :
            laastt+= y 
            # print(laastt)
        cnt+=1
    if popp == 16 :
        decipheredMsg = lol
    else :
        z = invPaddingMap[laastt]
        # print(z)
        while z > 0 :
            decipheredMsg.pop()
            z-=1
    
    return decipheredMsg
    


if __name__ == "__main__": 
    isFile   = bool(int(input("Enter 1 for text or 2 for file: "))-1)
    msg = ""
    if isFile:
        msg  = input("Enter file : ")
    else :
        msg  = input("Enter txt : ")
    key      = input("Enter Key : ")
    mode     = input("Enter mode CBC/CTR : ")


    start = time.time()
    ekeys,hexKey = getKey(key,128)
    print("\nKey(In hex): ",end = " ")
    for i in range(len(hexKey)):
        print(hexKey[i],end = " ")
    print("\n")
    schedTime = time.time() - start
    
    # Send=========================================>
    start = time.time()
    [ekeys,cipher]   = AES_send(128,msg,isFile,ekeys,mode)
    print("\nCipherText(in hex) : ",end = " ")
    for i in range(len(cipher)):
        print(cipher[i],end = " ")
    print("\n")
    encryptionTime = time.time() - start
    # print(ekeys[0][0])

    
    
    
    # recive ======================================>
    startTime = time.time()
    plaintxt = AES_recv(128,cipher,isFile,ekeys,mode)
    print("\n\nDeciphered text/file contents (in hex) :", end = " ") 
    for i in range(len(plaintxt)):
        print(plaintxt[i],end = " ")
    print("\n") 
    if isFile :
        with open("decrypted_", 'wb') as f:
            f.write(binascii.unhexlify("".join(plaintxt)))
    else:
        print("\nDeciphered text(in ASCII): " + hexToString(plaintxt))


    decryptionTime = time.time()-startTime

    print("\n\nExecution time:")
    print("Key Scheduling:", schedTime*1000, "miliseconds")
    print("Encryption Time:", encryptionTime*1000, "miliseconds")
    print("Decryption Time:", decryptionTime*1000, "miliseconds")
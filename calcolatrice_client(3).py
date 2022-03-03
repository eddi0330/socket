#Myrdari Edisson
#calcolatrice client per calcoServer.py versione multithread
from threading import Thread
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=2

def genera_richieste(num,address,port):
    start_time_thread= time.time()
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #1. rimpiazzare questa parte con la generazione di operazioni e numeri random, non vogliamo inviare sempre 3+5 
    primoNumero=random.randint(0,10)
    operazione=random.choice(['+', '-', '*', '/', '%'])
    secondoNumero=random.randint(0,10)

    #2. comporre il messaggio, inviarlo come json e ricevere il risultato
    data={'primoNumero':primoNumero,'operazione':operazione,'secondoNumero':secondoNumero} 
    data=json.dumps(data)
    s.sendall(data.encode("UTF-8"))
    data=s.recv(1024)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(f"{threading.current_thread().name}: Risultato: {data.decode()}") # trasforma il vettore di byte in stringa
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()
    n=0
    # 3 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    while n<NUM_WORKERS:
        genera_richieste(NUM_WORKERS,SERVER_ADDRESS,SERVER_PORT)
        n+=1
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]

    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # ad ogni iterazione appendo il thread creato alla lista threads
    listaT=[]
    for i in range(NUM_WORKERS):
        t=Thread(target=genera_richieste,args=(NUM_WORKERS,SERVER_ADDRESS,SERVER_PORT))   #la i indica il numero delle volte che è già stato ripetuto il ciclo
        listaT.append(t)
    # 5 avvio tutti i thread
    [th.start() for th in listaT] #con questo for gli diamo il comando th.start() per ogni elemento della lista
    # 6 aspetto la fine di tutti i thread 
    [th.join() for th in listaT] #con questo for gli diamo il comando th.join() per ogni elemento della lista
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # ad ogni iterazione appendo il thread creato alla lista threads
    for i in range(NUM_WORKERS):
        p=multiprocessing.Process(target=genera_richieste,args=(NUM_WORKERS, SERVER_ADDRESS, SERVER_PORT)) #creiamo i process
        process.append(p) #aggiungiamo il process alla lista di process
    # 8 avvio tutti i processi
    [p.start() for p in process]
    # 9 aspetto la fine di tutti i processi 
    [p.join() for p in process]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)

#nome del file : pagellaClientMulti.py
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json
import pprint
from threading import Thread

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=4

#Versione 1 
def genera_richieste1(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    #   di uno studente (valori ammessi: 5 cognomi a caso tra cui il tuo cognome)
    #   di una materia (valori ammessi: Matematica, Italiano, inglese, Storia e Geografia)
    #   di un voto (valori ammessi 1 ..10)
    #   delle assenze (valori ammessi 1..5)
    
    studente=random.choice(['Myrdari', 'Cognome1', 'Cognome2', 'Cognome3', 'Cognome4'])
    materia=random.choice(['Matematica', 'Italiano', 'Inglese', 'Storia', 'Geografia'])
    voto=random.randint(1,10) 
    assenze=random.randint(1,5)
    #2. comporre il messaggio, inviarlo come json
    #   esempio: {'studente': 'Studente4', 'materia': 'Italiano', 'voto': 2, 'assenze': 3}
    data={'studente':studente,'materia':materia,'voto':voto, 'assenze':assenze} 
    data=json.dumps(data)
    s.sendall(data.encode("UTF-8"))
    #3. ricevere il risultato come json: {'studente':'Studente4','materia':'italiano','valutazione':'Gravemente insufficiente'}
    data=s.recv(1024)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        #4 stampare la valutazione ricevuta esempio: La valutazione di Studente4 in italiano è Gravemente insufficiente
        print(f"{threading.current_thread().name}: {voto} La valutazione di {studente} in {materia} è {data.decode()}")
    s.close()

#Versione 2 
def genera_richieste2(num,address,port):
  #....
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

  #   1. Generazione casuale di uno studente(valori ammessi: 5 cognomi a caso scelti da una lista)

    studente=random.choice(['Myrdari', 'Cognome1', 'Cognome2', 'Cognome3', 'Cognome4'])
    pagella=[]
    #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
    #   generazione di un voto (valori ammessi 1 ..10)
    #   e delle assenze (valori ammessi 1..5)
    materie=['Matematica', 'Italiano', 'Inglese', 'Storia', 'Geografia']
    i=0
    for m in materie:
        voto=random.randint(1,10) 
        assenze=random.randint(1,5)
        pagella.append((m,voto,assenze))
  #   esempio: pagella={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9.5,3), ("Storia",8,2), ("Geografia",8,1)]}
    data={'studente':studente,'pagella':pagella} 
    data=json.dumps(data)
    s.sendall(data.encode("UTF-8"))
    data=s.recv(1024)
    data=data.decode()
    data=json.loads(data) 
    nomeStud=data['studente']
    mediaStud=data['media']
    assenzeStud=data['assenze']
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(f"{threading.current_thread().name}: Lo studente {nomeStud} ha una media di {mediaStud} e assenze: {assenzeStud}")
    s.close()

  #2. comporre il messaggio, inviarlo come json
  #3  ricevere il risultato come json {'studente': 'Cognome1', 'media': 8.0, 'assenze': 8}
#Versione 3
def genera_richieste3(num,address,port):
    pass
  #....
  #   1. Per ognuno degli studenti ammessi: 5 cognomi a caso scelti da una lista
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
  #   e delle assenze (valori ammessi 1..5) 
  #   esempio: tabellone={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9,3), ("Storia",8,2), ("Geografia",8,1)],
  #                       "Cognome2":[("Matematica",7,2), ("Italiano",5,3), ("Inglese",4,12), ("Storia",5,2), ("Geografia",4,1)],
  #                        .....}
  #2. comporre il messaggio, inviarlo come json
  #3  ricevere il risultato come json e stampare l'output come indicato in CONSOLE CLIENT V.3

if __name__ == '__main__':
    n=0
    start_time=time.time()
    # PUNTO A) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)
    # alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    while n<NUM_WORKERS:
        #genera_richieste1(NUM_WORKERS,SERVER_ADDRESS,SERVER_PORT)
        genera_richieste2(NUM_WORKERS,SERVER_ADDRESS,SERVER_PORT)
        n+=1
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]
    # PUNTO B) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)
    listaT=[]
    for i in range(NUM_WORKERS):
        #t=Thread(target=genera_richieste1,args=(NUM_WORKERS,SERVER_ADDRESS,SERVER_PORT))
        t=Thread(target=genera_richieste2,args=(NUM_WORKERS,SERVER_ADDRESS,SERVER_PORT))   #la i indica il numero delle volte che è già stato ripetuto il ciclo
        listaT.append(t)
    # 5 avvio tutti i thread
    [th.start() for th in listaT] #con questo for gli diamo il comando th.start() per ogni elemento della lista
    # 6 aspetto la fine di tutti i thread 
    [th.join() for th in listaT] #con questo for gli diamo il comando th.join() per ogni elemento della lista
    # tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # avviare tutti i thread e attenderne la fine
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]
    # PUNTO C) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3) 
    # tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # avviare tutti i processi e attenderne la fine
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)
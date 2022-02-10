import socket
import json


HOST='127.0.0.1'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[*] In ascolto su %s:%d "%(HOST, PORT))
    clientsocket, address=s.accept()
    contatore=0
    with clientsocket as cs:
        print("Connessione da ", address)
        while True:
            data=cs.recv(1024)
            if not data: #se non riceviamo data fermiamo il programma
                break
            data=data.decode()
            data=json.loads(data)
            messaggio=data['messaggio'] #traduciamo il messaggio
            
            contatore+=1
            ris=str(contatore)+") "+messaggio #contatore dei messaggi
            ris=str(ris)
            cs.sendall(ris.encode("UTF-8"))
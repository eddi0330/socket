import socket
import json
import string
from tokenize import String

HOST="127.0.0.1"
PORT=65432
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        messaggio=input("Inserisci un messaggio (KO per interrompere il programma): ")
        if messaggio=="KO":   #se il messaggio è KO si interrompe il programmna
            break
        messaggio=str(messaggio) #trasformiamo messaggio in una stringa
        messaggio={'messaggio':messaggio} 
        messaggio=json.dumps(messaggio)  #mandiamo il messaggio attraverso il json

        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        print("Risultato: ",data.decode())
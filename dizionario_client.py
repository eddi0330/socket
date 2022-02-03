import socket
import json
import string
import pprint
pp=pprint.PrettyPrinter(indent=4)
from tokenize import String

HOST="127.0.0.1"
PORT=65432
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Comandi disponibili \n#list : per vedere i voti inseriti \n#set /nomestudente : per inserire uno studente \n#put /nomestudente/materia/voto/ore : per aggiungere i voti della materia allo studente \n#get /nomestudente : per richiedere i voti di uno studente \n#exit : per chiudere solo il client \n#close : per chiudere sia client sia server")
    while True:
        messaggio=input("Digita il comando: ")
        messaggio=str(messaggio)
        msg={'messaggio':messaggio}
        msg=json.dumps(msg)
        print(msg)
        print(type(msg))
        s.sendall(msg.encode("UTF-8"))
        data=s.recv(1024)
        dizionario= json.loads(data)
        pp.pprint(dizionario)
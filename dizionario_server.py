import socket
import json
import pprint
pp=pprint.PrettyPrinter(indent=4)

HOST='127.0.0.1'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[*] In ascolto su %s:%d "%(HOST, PORT))
    clientsocket, address=s.accept()
    pagella={"Giuseppe Gullo":[("Matematica",9,0),("Italiano",7,3),("Inglese",7.5,4),("Storia",7.5,4),("Geografia",5,7)],
         "Antonio Barbera":[("Matematica",7,0),("Italiano",7,4),("Inglese",7.5,5),("Storia",9.5,4),("Geografia",5,3)],
         "Nicola Spina":[("Matematica",7,4),("Italiano",4,4),("Inglese",7.5,8),("Storia",9.5,1),("Geografia",9,3)]}
    with clientsocket as cs:
        print("Connessione da ", address)
        while True:
            data=cs.recv(1024)
            data=data.decode()
            print(data)
            print(type(data))
            data=json.loads(data)
            print(data)
            print(type(data))
            messaggio=data['messaggio']
            if messaggio=="#list":
                dizionario = json.dumps(pagella) 
                cs.sendall(dizionario.encode("UTF-8"))
            elif messaggio=="#close":
                print("close")
            elif messaggio=="#exit":
                print("exit")
            else:
                messSplit = messaggio.split("/")
                nomeStud=messSplit[1]
                if messSplit[0]=="#set ":
                    pagella[nomeStud]=[]
                    msg="Operazione eseguita"
                    cs.sendall(msg.encode("UTF-8"))
                elif messSplit[0]=="#put ":
                    materia=messSplit[2]
                    voto=messSplit[3]
                    ore=messSplit[4]
                    pagella[nomeStud].append(materia,voto,ore)
                    msg="Operazione eseguita"
                    cs.sendall(msg.encode("UTF-8"))
                elif messSplit[0]=="#get ":
                    dizionario = json.dumps(pagella) 
                    cs.sendall(dizionario.encode("UTF-8"))

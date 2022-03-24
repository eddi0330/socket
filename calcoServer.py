import socket
from threading import Thread
SERVER_ADDRESS='127.0.0.1'
SERVER_PORT=22225

class Server():
    """
    Questa classe rappresenta un server
    """
    def __init__(self, address, port):
        self.address = address
        self.port=port
    
    def avvia_server(self):
        """
        Metodo per aprirsi e mettersi in ascolto aspettando richieste da servire
        """
        sock_listen=socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_listen.bind((self.address, self.port))
        sock_listen.listen(5)
        print("Server in ascolto su %s." % str((self.address, self.port)))
        return sock_listen

    def accetta_connessioni(self,sock_listen):
        """
        Metodo per accettare richieste di servizio ed assegnare un Thread ad ognuna di esse
        """
        while True:
            sock_service, addr_client=sock_listen.accept()
            print("\nConnessione ricevuta da "+ str(addr_client))
            print("\nCreo un thread per servire le richieste")
            try:
                Thread(target=self.ricevi_comandi,args=(sock_service,addr_client)).start()
            except:
                print("Il thread non si avvia")
                sock_listen.close()

    def ricevi_comandi(self,sock_service, addr_client):
        """
        Metodo per ricevere i comandi e servive le richieste ricevute
        """
        print("Avviato")
        while True:
            data=sock_service.recv(2048)
            if not data: 
                print("Fine dati dal client. Reset")
                break
            
            data=data.decode()
            print("Ricevuto: '%s'" % data)
            if data=='0':
                print("Chiudo la connessione con "+str(addr_client))
                break

            operazione,primoNumero,secondoNumero=data.split(";")
            ris=0
            if operazione=="+":
                ris=int(primoNumero)+int(secondoNumero)
            elif operazione=="-":
                ris=int(primoNumero)-int(secondoNumero)
            elif operazione=="*":
                ris=int(primoNumero)*int(secondoNumero)
            elif operazione=="/":
                if int(secondoNumero)==0:
                    ris="Non puoi dividere per 0"
                else:
                    ris=int(primoNumero)/int(secondoNumero)
            elif operazione=="%":
                ris=int(primoNumero)%int(secondoNumero)
            else:
                ris="Operazione non riuscita"

            data = f"Risposta a :{str(addr_client)}. Il risultato dell'operazione({primoNumero} {operazione} {secondoNumero}) è : {ris} "
            data= data.encode()
            sock_service.send(data)
        sock_service.close()

s1=Server(SERVER_ADDRESS, SERVER_PORT)
sock_lis=s1.avvia_server()
s1.accetta_connessioni(sock_lis)


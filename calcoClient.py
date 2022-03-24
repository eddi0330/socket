import socket 
from threading import Thread
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
class Client():
    """
    Questa classe rappresenta una persona che opera come client
    """
    def connessione_server(self,address,port):
        """
        Metodo per stabilire la connessione con il server
        """
        sock_service = socket.socket()
        sock_service.connect((address, port))
        print("Connesso a " + str((address, port)))
        return sock_service

    def invia_comandi(self,sock_service):
        """
        Metodo per inviare le richieste di servizio e ricevere le risposte
        """
        while True:
            try:
                primoNumero = input("Inserisci il primo numero: ")
                secondoNumero = input("Inserisci il secondo numero: ")
                operazione = input("Inserisci l'operazione da effettuare(+,-,*,/): ")
                data=f"{operazione};{primoNumero};{secondoNumero}"
            except EOFError:
                print("\nOKay. Exit")
                break 
            if not data:
                print("Non puoi inviare una stringa vuota!")
                continue 
            if data=='0':
                print("Chiudo la connessione con il server!")
                sock_service.close()
                break

            data = data.encode()
            sock_service.sendall(data)
            data = sock_service.recv(2048)
            if not data: 
                print("Server non risponde. Exit")
                break 
            data = data.decode()
            print("Ricevuto dal server:")
            print(data + '\n') 

c1=Client()
sock_serv=c1.connessione_server(SERVER_ADDRESS,SERVER_PORT)
c1.invia_comandi(sock_serv)
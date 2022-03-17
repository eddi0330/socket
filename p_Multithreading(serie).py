# 4.a DOWNLOAD PAGE - SERIAL MODE

import time
import logging
import requests
import os
paroleTot=0 #variabile globale
 
 
class WebsiteDownException(Exception):
    pass
 
 

def count_words(content,address): #con questo metodo splittiamo la stringa di parole in un array che poi utilizzeremo nel len
  parole=content.split()
  global paroleTot
  paroleTot+=len(parole)
  return(len(parole))
  #stampo il numero di parole contenute in content (home page di address)

def get_file_name(address): #con questo metodo splittiamo l'address prima dei ":" e dopo il "." e infine aggiungiamo ".txt" in modo da avere nomesito.txt
  primoSplit=address.split("//")
  secondoSplit=primoSplit[1].split(".")
  fileTxt=secondoSplit[0]+".txt"
  return(fileTxt)
  #ricavo il nome del file .txt da creare dall'indirizzo ricevuto come parametro
  #es.da http://amazon.com ottengo amazon.txt

def save_homepage(address, timeout=20):
    """
    """
    try:
        response = requests.head(address, timeout=timeout)
        r=requests.get(address) #carico il contenuto dell'home page di address
        if response.status_code>=400:
          logging.warning("Website %s returned status code= %s" & (address, response.status_code))
          raise WebsiteDownException()
        url=get_file_name(address) #lo scrivo in un file il cui nome lo ottengo chiamando la funzione get_file_name
        file=open(url,"w")
        file.write(r.text)
        file.close() #chiudo il file
        file=open(url,"r") #riapro il file in lettura
        count_words(file.read(),address)  #leggo il contenuto e conto le parole chiamando la funzione count_words
        file.close()
        os.remove(url) #cancello il file
        pass

    except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()
         
 
def notify_owner(address):
    """ 
    Simuliamo l'invio di una email di notifica all'admin del sito che non risponde
    """
    logging.info("Notifying the owner of %s website" % address)
    time.sleep(0.5)
     
 

def manage_homepage(address):
    """
    Carica l'home page del sito, crea un file, salva il contenuto, 
    ricarica il contenuto dal file, conta le parole, chiude e rimuove il file
    """
    try:
        save_homepage(address)
    except WebsiteDownException:
        notify_owner(address)



if __name__ == "__main__":
    WEBSITE_LIST = [
    'https://envato.com',
    'http://amazon.com',
    'http://facebook.com',
    'http://google.com',
    'http://google.fr',
    'http://google.es',
    'http://internet.org',
    'http://gmail.com',
    'http://stackoverflow.com',
    'http://github.com',
    'http://heroku.com',
    'http://really-cool-available-domain.com',
    'http://djangoproject.com',
    'http://rubyonrails.org',
    'http://basecamp.com',
    'http://trello.com',
    'http://yiiframework.com',
    'http://shopify.com',
    'http://another-really-interesting-domain.co',
    'http://airbnb.com',
    'http://instagram.com',
    'http://snapchat.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
    'http://live.com',
    'http://linkedin.com',
    'http://yandex.ru',
    'http://netflix.com',
    'http://wordpress.com',
    'http://bing.com',
]
    start_time = time.time()
 
    for address in WEBSITE_LIST:
        manage_homepage(address) #richiamo il metodo principale
            
    end_time = time.time()        
    
    print("Tempo di esecuzione seriale : %ssecs" % (end_time - start_time)) 
    print("Il numero di parole totali è: %s"%(paroleTot)) 
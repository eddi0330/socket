# 4.2 DOWNLOAD PAGE - THREAD MODE

import time
import logging
import requests
from queue import Queue
from threading import Thread
import os
paroleTot=0
 
class WebsiteDownException(Exception):
    """
    Eventuale gestione dell'errore dovuto al sito che non risponde     
    """
    pass   
 
def notify_owner(address):
  """ 
  Simuliamo l'invio di una email di notifica all'admin del sito che non risponde
  """
  logging.info("Notifying the owner of %s website" % address)
  time.sleep(0.5)


def count_words(content,address): #metodo usato per contare le parole di un sito
  parole=content.split()
  global paroleTot
  paroleTot+=len(parole)
  return(len(parole))

def get_file_name(address): #metodo usato per ottenere un file txt con il nome del sito
  primoSplit=address.split("//")
  secondoSplit=primoSplit[1].split(".")
  fileTxt=secondoSplit[0]+".txt"
  return(fileTxt)

def save_homepage(address, timeout=20): #metodo che serve a ottenere l'address e il contenuto della homepage in modo da creare un txt con il numero di parole dentro
    """
    Carica l'home page del sito, crea un file, salva il contenuto, 
    lo ricarica dal file, conta le parole, chiude e rimuove il file
    """
    try:
        response = requests.head(address, timeout=timeout)
        r=requests.get(address)
        if response.status_code>=400:
          logging.warning("Website %s returned status code= %s" % (address, response.status_code))
          raise WebsiteDownException()
        url=get_file_name(address)
        file=open(url,"w")
        file.write(r.text)
        file.close()
        file=open(url,"r")
        paroleFile=count_words(file.read(),address)
        file.close()
        os.remove(url)
        print("Il numero delle parole del sito %s è %d" % (address, paroleFile))
        pass
    except requests.exceptions.RequestException:
        logging.warning("Problem to get website %s" % address)
        raise WebsiteDownException()
            
 
def manage_homepage(address):
    try:
        save_homepage(address)
    except WebsiteDownException:
        notify_owner(address)

def worker():
    #creiamo un worker
    while True:
        address = task_queue.get()
        manage_homepage(address)
        # assegnamo al worker il task
        task_queue.task_done()

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
    'http://another-really-interesting-domain.com',
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

NUM_WORKERS = 4

task_queue = Queue()

start_time = time.time()

# creiamo una lista di numeri che moltiplicheremo per 2
lista1=[1,2,3,4,5,6,7]
lista2 = [elemento*2 for elemento in lista1 ]
print(lista2) 

# creiamo i thread e gli assegnamo i worker 
threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
 
# assegnamo i link dei siti alla queue
[task_queue.put(item) for item in WEBSITE_LIST]
 
# facciamo partire i thread
[thread.start() for thread in threads]
 
# facciamo il join della queue
task_queue.join()
 
         
end_time = time.time()        
 
print("Time for ThreadedSquirrel: %ssecs" % (end_time - start_time))
print("Parole totali: %s" %(paroleTot))
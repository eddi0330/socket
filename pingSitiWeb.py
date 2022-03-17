# PING SERIAL MODE
import time
import logging
import requests

class WebsiteDownException(Exception):
    """
    Definizione di un eccezione personalizzata che eredita dalla classe Exception
    """
    pass


def ping_website(address, timeout=20):
    """
    Controllo se è il sito è down. Un sito è considerato down quando 
    scade il timeout o quando lo status code restituito è >=400 
    """
    try:
        #1 imposto nell'header della richiesta il parametro timeout
        r=requests.get(address, params="",timeout=timeout)
        #2. effettuo la chiamata e controllo lo status_code se è >=400 sollevo l'eccezione per segnalare che il sito è down
        if r.status_code==400:
          
          raise WebsiteDownException()
        #3. altrimenti stampo l'indirizzo e lo status code restituito
        else:
          print(f"Status code del server {address} riportato:  {r.status_code}")
    #se la chiamata va in timeout sollevo l'eccezione per segnalare che il sito è down 
    except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()
       
         
 
def notify_owner(address):
    global listaErr
    listaErr.append(address)
    #4.gestisco una lista in cui memorizzo tutti gli url a cui mandare una notifica
    logging.info("Notifying the owner of %s website" % address)
    time.sleep(0.5)
     
 
def check_website(address):
    try:
        ping_website(address)
    except WebsiteDownException:
        notify_owner(address)

if __name__ == "__main__":
    WEBSITE_LIST = [
    'https://envato.com',
    'http://amazon.co.uk',
    'http://amazon.com',
    'http://facebook.com',
    'http://google.com',
    'http://google.fr',
    'http://google.es',
    'http://google.co.uk',
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
    listaErr=[]
    start_time = time.time()

    for address in WEBSITE_LIST:
        check_website(address)
            
    end_time = time.time()        
    print("\nTime for SERIAL PING : %s secs" % (end_time - start_time))
    print("Lista dei siti che non rispondono: %s" %(listaErr))
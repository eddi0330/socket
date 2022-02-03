from threading import Thread
import time,datetime

#definizione del thread 1 e 2
def thread1():
  print("Thread 1 iniziato")
  time.sleep(10)    #lo sleep mette in pausa per il numero specificato in secondi
  print("Thread 1 finito")

def thread2():
  print("Thread 2 iniziato")
  time.sleep(4)
  print("Thread 2 finito")

print("Main iniziato")

start_time = time.time()    #salva il tempo in una variabile
t1 = Thread(target=thread1) #assegnazione dei thread
t2 = Thread(target=thread2)
t1.start()      #inizio thread 1 e 2
t2.start()
time.sleep(2)   #sleep di 2 secondi
end_time=time.time()    #salva il tempo in una variabile

print(f"Main finito in {end_time-start_time}")
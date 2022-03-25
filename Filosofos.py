import sys 
import threading
import time 


class semaphore (object):
  def __init__(self,initial):  #Funcion de inicio
    #El self, accede a los atributos y metodos de la clase
    self.lock = threading.Condition(threading.Lock())
    self.value = initial 
    
  def up(self):   #Funcion que levanta el palillo
    with self.lock:
      self.value += 1
      self.lock.notify()
      
  def down (self):  #Funcion que deja el palillo 
    with self.lock:
      while self.value == 0:
        self.lock.wait()
      self.value -= 1
        
        
          
class ChopStick(object):
  def __init__(self,number):
    self.number=number
    self.user=-1
    self.lock = threading.Condition(threading.Lock())
    self.taken = False

  def take(self,user): #tomar el palillo
    with self.lock:
      while self.taken == True:
        self.lock.wait()
      self.user=user
      self.taken = True
      sys.stdout.write("El filosofo numero[%s] toma el palillo %s \n "% (user,self.number))
      self.lock.notifyAll()

  def drop(self,user):
    with self.lock:
      while self.taken == False:
        self.lock.wait()
      self.user = -1
      self.lock.notifyAll()
        
        
        
        
        
class philosopher (threading.Thread):  #Clase filosofo por medio de hilos 
  def __init__(self,number,left,right,butler):
    threading.Thread.__init__(self)
    self.number = number   #Numero de filosofo
    self.left = left
    self.right = right 
    self.butler = butler 
    
  def run (self):
    for i in range(1):
      self.butler.down()  #Empieza el servicio
      print("Filosofo" , self.number, "piensa" )
      time.sleep(0.1)              #Piensa
      self.left.take(self.number)  #Recoge el palillo izquierdo 
      time.sleep(0.1)
      self.right.take(self.number) #Recoge el palillo derecho 
      print ("Filosofo" , self.number , "come")
      time.sleep(0.1)
      self.right.drop(self.number) #Deja el palillo derecho
      self.left.drop (self.number) #Deja el palillo izquierdo
      self.butler.up() #Termina el servicio 
    sys.stdout.write("Filosofo[%s] Termina de pensar y comer\n" % self.number)
    
    
    
def main():
  #numero de filosos y palillos
  n=6

  butler = semaphore(n-1)

  #lista de palillos
  c = [ChopStick(i)for i in range(n)]

  #lista de filososfos

  p = [Philosofer(i,c[i],c[(i+1)%n],butler)for i in range(n)]

  for i in range(n):
   p[i].start()
if __name__ =="__main__":
  main() 

    
    
    

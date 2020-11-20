#####################################
## Becerra Mata Juan Ricardo - D02 ##
#####################################

import keyboard
import random
import os
import time

from colorama import init 
from termcolor import colored 

prod = u"\u2588"u"\u2588"

class Productor:
    pos = 0
    time = 0
    wait = False
    estado = "init" #init, durmiendo, esperando, trabajando
    estado_exp = "init"

def producir(p):
    #print("##")
    buffer[p] = prod
    return

class Consumidor:
    pos = 0
    time = 0
    wait = False
    estado = "init" #init, durmiendo, esperando, trabajando
    estado_exp = "init"

def consumir(p):
    #print("__")
    buffer[p] = "__"
    return

buffer = []
productor = Productor()
consumidor = Consumidor()

estados = ["Durmiendo", "Trabajando"]
procesos = ["Productor", "Consumidor"]

#Buffer ocupado por cualquiera de los dos
semaforo = False
wait_prod = False
wait_cons = False

def bufferClean():
    i = 0
    while i < 30:
        buffer.append("__")
        i+=1
        
def coloredNumber(i):
    if(i == productor.pos +1 and productor.pos + 1 == consumidor.pos + 1):
         return colored(i, 'grey', 'on_white')
    elif(i == productor.pos + 1):
        return colored(i, 'grey', 'on_yellow')
    elif(i == consumidor.pos + 1):
        return colored(i, 'grey', 'on_blue')
    else:
        return i
        

def printBuffer():
    i = 0
    while i<30:        
        print(buffer[i], " ", end = "")
        i+=1

    print("")

    i = 0
    space = "  "
    while i<30:
        
        if(i==9):
            space = " "
        
        print(coloredNumber(i+1), space, end = "")
        i+=1
    
    print("\n")

def checkProdAvailable():
    #Producir al menos 1 en todo el buffer
    #if("__" in buffer):
    #    return True
    #else:
    #    return False
    
    #Producir en su posicion
    if(buffer[productor.pos] == "__"):
        return True
    else:
        return False
    
def checkConsAvailable():
    #Consumir al menos 1 de todo el buffer
    #if("&&" in buffer):
    #    return True
    #else:
    #    return False
    
    #Consumir su posicion
    if(buffer[consumidor.pos] == prod):
        return True
    else:
        return False

def printSem():
    if(semaforo):
        return colored(semaforo, 'green')
    else:
        return colored(semaforo, 'red')

def printWait_Prod():
    if(wait_prod):
        return colored(wait_prod, 'green')
    else:
        return colored(wait_prod, 'red')
    
def printWait_Cons():
    if(wait_cons):
        return colored(wait_cons, 'green')
    else:
        return colored(wait_cons, 'red')

#Llena el buffer de espacios vacios "_"
bufferClean()

#Imprime el buffer actual con sus posiciones
#printBuffer()


############
# MainLoop #
############
#os.system('mode con: cols=120 lines=30')
ciclo = 0

while True:
    time.sleep(0.5)

    if(keyboard.is_pressed('ESC')):
        print("\n\nTerminando...")
        break

    #

    else:
        print("########################################################################################################################")
        print("\nCiclo: ", ciclo+1, "\n")
     
        #ESPERANDO - Proceso esperando a que el buffer este disponible, con su tiempo intancto
        #TRABAJANDO - Proceso utilizando el buffer
        #ELIGIENDO - Antes de cambiar de estado
        #INIT - Estado inicial
        #DURMIENDO - Sin hacer nada
        
        #Checar si alguno terminó 
        #if(productor.estado == "Trabajando" and productor.time == 0):
            
        
        #Si wait activo entonces proceso debe de ESPERAR
        if(wait_prod == False and productor.time > 0): #Si aun tiene tiempo y puede trabajar o dormir
            productor.time -= 1
        elif(productor.estado != "Esperando" and productor.time < 1): #Si terminó su trabajo o sueño
            productor.estado_exp = random.choice(estados)
            #wait_cons = False
            if(productor.estado == "Trabajando"):
                semaforo = False
            productor.estado = "Eligiendo"
        
        if(wait_cons == False and consumidor.time > 0):
            consumidor.time -= 1
        elif(consumidor.estado != "Esperando" and consumidor.time < 1):
            consumidor.estado_exp = random.choice(estados)
            #wait_prod = False
            if(consumidor.estado == "Trabajando"):
                semaforo = False
            consumidor.estado = "Eligiendo"
            
        #Definicion de estados
        if(semaforo == False):
            #Si hay alguien esperando tiene prioridad
            if(productor.estado == "Esperando"):
                if(checkProdAvailable()):
                    #print("productor - esp a trabaj # 150")
                    productor.estado = "Trabajando"
                    semaforo = True
                    wait_prod = False
                    #wait_cons = True
                    if(consumidor.estado_exp != "!"):
                        if(consumidor.estado_exp == "Trabajando" and checkConsAvailable()):
                            if(semaforo == False):
                                #print("Consumidor trabajando #159")
                                consumidor.estado = "Trabajando"
                                consumidor.estado_exp = "!"
                                semaforo = True
                                wait_cons = False
                                #wait_prod = True
                            else:
                                #print("Consumidor esperando #166")
                                consumidor.estado = "Esperando"
                                consumidor.estado_exp = "!"
                                wait_cons = True
                            consumidor.time = random.randrange(3, 11, 1)
                        elif(consumidor.estado_exp == "Durmiendo"):
                            #print("Consumidor Durmiendo #165")
                            consumidor.estado_exp = "!"
                            consumidor.estado = "Durmiendo"
                            consumidor.time = random.randrange(3, 11, 1)
                elif(checkProdAvailable() == False):
                    #print("Productor - sigue esperando #177")
                    if(consumidor.estado_exp != "!"):
                        if(consumidor.estado_exp == "Trabajando" and checkConsAvailable()):
                            if(semaforo == False):
                                #print("Consumidor trabajando #181")
                                consumidor.estado = "Trabajando"
                                consumidor.estado_exp = "!"
                                semaforo = True
                                wait_cons = False
                            else:
                                #print("Consumidor esperando #187")
                                consumidor.estado = "Esperando"
                                consumidor.estado_exp = "!"
                                wait_cons = True
                            consumidor.time = random.randrange(3, 11, 1)
                
            elif(consumidor.estado == "Esperando"):
                if(checkConsAvailable()):
                    #print("consumidor - esperando a trabajando #169")
                    consumidor.estado = "Trabajando"
                    semaforo = True
                    wait_cons = False
                    #wait_prod = True
                    if(productor.estado_exp != "!"):
                        if(productor.estado_exp == "Trabajando" and checkProdAvailable()):
                            if(semaforo == False):
                                #print("Productor trabajando #180")
                                productor.estado = "Trabajando"
                                productor.estado_exp = "!"
                                semaforo = True
                                wait_cons = True
                                #wait_prod = False
                            else:
                                #print("Productor esperando #187")
                                productor.estado = "Esperando"
                                productor.estado_exp = "!"
                                wait_prod = True
                            productor.time = random.randrange(3, 11, 1)
                        elif(productor.estado_exp == "Durmiendo"):
                            #print("Productor durmiendo #193")
                            productor.estado_exp = "!"
                            productor.estado = "Durmiendo"
                            productor.time = random.randrange(3, 11, 1)
                elif(checkConsAvailable() == False):
                    #print("consumidor - sigue esperando #198")
                    if(productor.estado_exp != "!"):
                        if(productor.estado_exp == "Trabajando" and checkProdAvailable()):
                            if(semaforo == False):
                                #print("Productor trabajando #202")
                                productor.estado = "Trabajando"
                                productor.estado_exp = "!"
                                semaforo = True
                                wait_cons = True
                                wait_prod = False
                            else:
                                #print("Productor esperando #209")
                                productor.estado = "Esperando"
                                productor.estado_exp = "!"
                                wait_prod = True
                            productor.time = random.randrange(3, 11, 1)
                        elif(productor.estado_exp == "Durmiendo"):
                            #print("Productor durmiendo #215")
                            productor.estado_exp = "!"
                            productor.estado = "Durmiendo"
                            productor.time = random.randrange(3, 11, 1)
                        
            #Ambos quieren trabajar
            elif(productor.estado_exp == consumidor.estado_exp == "Trabajando"): 
                #print("Sem OFF - Ambos")
                if(checkProdAvailable()): #Si puede entrar productor
                    productor.estado = "Trabajando"
                    consumidor.estado = "Esperando"
                    wait_cons = True
                    semaforo = True
                    productor.estado_exp = "!"
                    consumidor.estado_exp = "!"
                    productor.time = random.randrange(3, 11, 1)
                    consumidor.time = random.randrange(3, 11, 1)
                elif(checkConsAvailable()): #Si puede entrar consumidor
                    productor.estado = "Esperando"
                    consumidor.estado = "Trabajando"
                    wait_prod = True
                    semaforo = True
                    consumidor.estado_exp = "!"
                    productor.estado_exp = "!"
                    productor.time = random.randrange(3, 11, 1)
                    consumidor.time = random.randrange(3, 11, 1)
            
            #Uno quiere trabajar, otro dormir
            elif((productor.estado_exp == "Durmiendo" and consumidor.estado_exp == "Trabajando") or (productor.estado_exp == "Trabajando" and consumidor.estado_exp == "Durmiendo")):
                #print("Sem OFF - uno y uno")
                if(productor.estado_exp == "Trabajando"):
                    productor.estado_exp = "!"
                    consumidor.estado_exp = "!"
                    productor.estado = "Trabajando"
                    consumidor.estado = "Durmiendo"
                    #wait_cons = True
                    semaforo = True
                    productor.time = random.randrange(3, 11, 1)
                    consumidor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Trabajando"):
                    productor.estado_exp = "!"
                    consumidor.estado_exp = "!"
                    productor.estado = "Durmiendo"
                    consumidor.estado = "Trabajando"
                    #wait_prod = True
                    semaforo = True
                    productor.time = random.randrange(3, 11, 1)
                    consumidor.time = random.randrange(3, 11, 1)
                    
            #Ambos quieren dormir
            elif(productor.estado_exp == "Durmiendo" == consumidor.estado_exp):
                #print("Sem OFF - Ninguno")
                wait_cons = False
                wait_prod = False
                semaforo = False
                productor.estado_exp = "!"
                consumidor.estado_exp = "!"
                productor.estado = "Durmiendo"
                consumidor.estado = "Durmiendo"
                productor.time = random.randrange(3, 11, 1)
                consumidor.time = random.randrange(3, 11, 1)
                
            #Uno durmiendo, el otro quiere dormir
            elif(productor.estado_exp == "Durmiendo" and consumidor.estado == "Durmiendo") or (productor.estado == "Durmiendo" and consumidor.estado_exp == "Durmiendo"):
                if(productor.estado_exp == "Durmiendo"):
                    productor.estado_exp = "!"
                    productor.estado = "Durmiendo"
                    productor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Durmiendo"):
                    consumidor.estado_exp = "!"
                    consumidor.estado = "Durmiendo"
                    consumidor.time = random.randrange(3, 11, 1)
            
            #Uno durmiendo, el otro quiere trabajar
            elif(productor.estado_exp == "Trabajando" and consumidor.estado == "Durmiendo") or (productor.estado == "Durmiendo" and consumidor.estado_exp == "Trabajando"):
                if(productor.estado_exp == "Trabajando" and checkProdAvailable()):
                    productor.estado_exp = "!"
                    productor.estado = "Trabajando"
                    semaforo = True
                    productor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Trabajando" and checkConsAvailable()):
                    consumidor.estado_exp = "!"
                    consumidor.estado = "Trabajando"
                    semaforo = True
                    consumidor.time = random.randrange(3, 11, 1)
            
            #Uno Esperando, el otro quiere trabajar
            elif(productor.estado_exp == "Trabajando" and consumidor.estado == "Esperando") or (productor.estado == "Esperando" and consumidor.estado_exp == "Trabajando"):
                if(productor.estado_exp == "Trabajando" and checkProdAvailable()):
                    productor.estado_exp = "!"
                    productor.estado = "Trabajando"
                    productor.time = random.randrange(3, 11, 1)
                    semaforo = True
                elif(consumidor.estado_exp == "Trabajando" and checkConsAvailable()):
                    consumidor.estado_exp = "!"
                    consumidor.estado = "Trabajando"
                    semaforo = True
                    consumidor.time = random.randrange(3, 11, 1)
            
            #Uno Esperando, el otro quiere Dormir
            elif(productor.estado_exp == "Durmiendo" and consumidor.estado == "Esperando") or (productor.estado == "Esperando" and consumidor.estado_exp == "Durmiendo"):
                if(productor.estado_exp == "Durmiendo"):
                    productor.estado_exp = "!"
                    productor.estado = "Durmiendo"
                    productor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Durmiendo"):
                    consumidor.estado_exp = "!"
                    consumidor.estado = "Durmiendo"
                    consumidor.time = random.randrange(3, 11, 1)
            
        elif(semaforo == True):
            #Uno trabajando, el otro quiere trabajar
            #Uno trabajando, el otro quiere dormir
            if(productor.estado_exp == "Trabajando"): #Poner a esperar
                #print("Sem ON - Prod quiere trabajar #300")
                productor.estado_exp = "!"
                productor.estado = "Esperando"
                wait_prod = True
                productor.time = random.randrange(3, 11, 1)
            elif(productor.estado_exp == "Durmiendo"):
                #print("Sem ON - Prod quiere dormir #305")
                productor.estado_exp = "!"
                productor.estado = "Durmiendo"
                wait_prod = False
                productor.time = random.randrange(3, 11, 1)
                
            if(consumidor.estado_exp == "Trabajando"):
                #print("Sem ON - Cons quiere trabajar #313")
                consumidor.estado_exp = "!"
                consumidor.estado = "Esperando"
                wait_cons = True
                consumidor.time = random.randrange(3, 11, 1)
            elif(consumidor.estado_exp == "Durmiendo"):
                #print("Sem ON - Cons quiere dormir #319")
                consumidor.estado_exp = "!"
                consumidor.estado = "Durmiendo"
                wait_cons = False
                consumidor.time = random.randrange(3, 11, 1)
        
        #TRABAJANDO - PRINCIPAL
        if(productor.estado == "Trabajando" and checkProdAvailable() == True):
            producir(productor.pos)
            if(productor.pos < 29):
                productor.pos += 1
            else:
                productor.pos = 0
        elif(productor.estado == "Trabajando" and checkProdAvailable() == False):
            wait_prod = True
            wait_cons = False
            productor.estado = "Esperando"
            semaforo = False
            if(consumidor.estado == "Esperando" and checkConsAvailable()):
                consumidor.estado = "Trabajando"
                consumidor.time += 1
                semaforo = True
                
        if(consumidor.estado == "Trabajando" and checkConsAvailable() == True):
            consumir(consumidor.pos)
            if(consumidor.pos < 29):
                consumidor.pos += 1
            else:
                consumidor.pos = 0
        elif(consumidor.estado == "Trabajando" and checkConsAvailable() == False):
            wait_prod = False
            wait_cons = True
            consumidor.estado = "Esperando"
            semaforo = False
            if(productor.estado == "Esperando" and checkProdAvailable()):
                productor.estado = "Trabajando"
                productor.time += 1
                semaforo = True
        
        print("Semaforo:", printSem(), "\nwait_prod:", printWait_Prod(), "    wait_cons:", printWait_Cons(), "\n\n", colored("Productor: ", 'grey', 'on_yellow'), productor.estado, "[", productor.time,"]", " - Pos:", productor.pos+1, "\n", colored("Consumidor: ", 'grey', 'on_blue'), consumidor.estado, "[", consumidor.time, "]", "- Pos:", consumidor.pos+1,"\n")
        
        ciclo += 1 
        #Main
        printBuffer()
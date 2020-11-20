#####################################
## Becerra Mata Juan Ricardo - D02 ##
#####################################

import keyboard
import random
import os
import time

class Productor:
    pos = 0
    time = 0
    wait = False
    estado = "init" #init, durmiendo, esperando, trabajando
    estado_exp = "init"

def producir(p):
    #print("##")
    buffer[p] = "&&"
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

def printBuffer():
    i = 0
    while i<30:        
        print(buffer[i], " ", end="")
        i+=1

    print("")

    i = 0
    space = "  "
    while i<30:
        if(i==9):
            space = " "
        
        print(i+1, space, end="")
        i+=1
    
    print("\n")

def checkProdAvailable():
    #if("__" in buffer):
    #    return True
    #else:
    #    return False
    if(buffer[productor.pos] == "__"):
        return True
    else:
        return False
    
def checkConsAvailable():
    #if("&&" in buffer):
    #    return True
    #else:
    #    return False
    if(buffer[consumidor.pos] == "&&"):
        return True
    else:
        return False

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
    time.sleep(.3)

    if(keyboard.is_pressed('ESC')):
        print("\n\nTerminando...")
        break

    #

    else:
        print("########################################################################################################################")
        print("Ciclo: ", ciclo+1, "\n")
     
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
            productor.estado = "Eligiendo"
            productor.estado_exp = random.choice(estados)
            #wait_cons = False
            semaforo = False
        
        if(wait_cons == False and consumidor.time > 0):
            consumidor.time -= 1
        elif(consumidor.estado != "Esperando" and consumidor.time < 1):
            consumidor.estado = "Eligiendo"
            consumidor.estado_exp = random.choice(estados)
            #wait_prod = False
            semaforo = False
            
        #Definicion de estados
        if(semaforo == False):
            #Si hay alguien esperando tiene prioridad
            if(productor.estado == "Esperando" and checkProdAvailable()):
                productor.estado = "Trabajando"
                semaforo = True
                wait_prod = False
                wait_cons = True
                
            elif(consumidor.estado == "Esperando" and checkConsAvailable()):
                consumidor.estado = "Trabajando"
                semaforo = True
                wait_cons = False
                wait_prod = True
                        
            #Ambos quieren trabajar
            if(productor.estado_exp == consumidor.estado_exp == "Trabajando"): 
                print("Sem OFF - Ambos")
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
            if((productor.estado_exp == "Durmiendo" and consumidor.estado_exp == "Trabajando") or (productor.estado_exp == "Trabajando" and consumidor.estado_exp == "Durmiendo")):
                print("Sem OFF - uno y uno")
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
                    wait_prod = False
                    #wait_prod = True
                    semaforo = True
                    productor.time = random.randrange(3, 11, 1)
                    consumidor.time = random.randrange(3, 11, 1)
                    
            #Ambos quieren dormir
            if(productor.estado_exp == "Durmiendo" == consumidor.estado_exp):
                print("Sem OFF - Ninguno")
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
            if(productor.estado_exp == "Durmiendo" or consumidor.estado_exp == "Durmiendo"):
                if(productor.estado_exp == "Durmiendo"):
                    productor.estado_exp = "!"
                    productor.estado = "Durmiendo"
                    productor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Durmiendo"):
                    consumidor.estado_exp = "!"
                    consumidor.estado = "Durmiendo"
                    consumidor.time = random.randrange(3, 11, 1)
            
            #Uno Esperando, el otro quiere trabajar
            if(productor.estado == "Esperando" and consumidor.estado_exp == "Trabajando") or (productor.estado_exp == "Trabajando" and consumidor.estado == "Esperando"):
                if(productor.estado_exp == "Trabajando" and checkProdAvailable() == True):
                    productor.estado_exp ="!"
                    productor.estado = "Trabajando"
                    semaforo = True
                    productor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Trabajando" and checkConsAvailable() == True):
                    consumidor.estado_exp = "!"
                    consumidor.estado = "Trabajando"
                    semaforo = True
                    consumidor.time = random.randrange(3, 11, 1)
            
        elif(semaforo == True):
            #Uno trabajando, el otro quiere trabajar
            #Uno trabajando, el otro quiere dormir
            if(productor.estado_exp == "Trabajando"): #Poner a esperar
                print("Sem ON - Prod quiere trabajar")
                productor.estado_exp = "!"
                productor.estado = "Esperando"
                productor.time = random.randrange(3, 11, 1)
            elif(productor.estado_exp == "Durmiendo"):
                print("Sem ON - Prod quiere dormir")
                productor.estado_exp = "!"
                productor.estado = "Durmiendo"
                wait_prod = False
                productor.time = random.randrange(3, 11, 1)
                
            if(consumidor.estado_exp == "Trabajando"):
                print("Sem ON - Cons quiere trabajar")
                consumidor.estado_exp = "!"
                consumidor.estado = "Esperando"
                consumidor.time = random.randrange(3, 11, 1)
            elif(consumidor.estado_exp == "Durmiendo"):
                print("Sem ON - Cons quiere dormir")
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
        
        print("semaforo:", semaforo, "\nwait_prod:", wait_prod, "    wait_cons:", wait_cons, "\n\nProductor: ", productor.estado, "[", productor.time,"]", "POS: ", productor.pos, "\nConsumidor: ", consumidor.estado, "[", consumidor.time, "]", "POS: ", consumidor.pos,"\n")
        
        ciclo += 1 
        #Main
        printBuffer()
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
    return buffer[productor.pos] == "__"        
    
def checkConsAvailable():
    #if("&&" in buffer):
    #    return True
    #else:
    #    return False
    return buffer[consumidor.pos] == "&&"

#Llena el buffer de espacios vacios "_"
bufferClean()

#Imprime el buffer actual con sus posiciones
#printBuffer()


############
# MainLoop #
############
os.system('mode con: cols=120 lines=30')
ciclo = 0

while True:
    time.sleep(0.75)

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
        elif(wait_prod == False and productor.time < 1): #Si terminó su trabajo o sueño
            productor.estado = "Eligiendo"
            productor.estado_exp = random.choice(estados)
            wait_cons = False
            semaforo = False
        
        if(wait_cons == False and consumidor.time > 0):
            consumidor.time -= 1
        elif(wait_cons == False and consumidor.time < 1):
            consumidor.estado = "Eligiendo"
            consumidor.estado_exp = random.choice(estados)
            wait_prod = False
            semaforo = False
            
        #Definicion de estados
        if(semaforo == False):
            if(productor.estado_exp == consumidor.estado_exp == "Trabajando"):
                print("f")
                if(checkProdAvailable()): #Si puede entrar productor
                    productor.estado = "Trabajando"
                    consumidor.estado = "Esperando"
                    wait_cons = True
                    semaforo = True
                elif(checkConsAvailable()): #Si puede entrar consumidor
                    productor.estado = "Esperando"
                    consumidor.estado = "Trabajando"
                    wait_prod = True
                    semaforo = True
                    
                productor.time = random.randrange(3, 11, 1)
                consumidor.time = random.randrange(3, 11, 1)
        
        #TRABAJANDO - PRINCIPAL
        if(productor.estado == "Trabajando" and checkProdAvailable()):
            producir(productor.pos)
            if(productor.pos < 29):
                productor.pos += 1
            else:
                productor.pos = 0
        else:
            wait_prod = True
            wait_cons = False
            semaforo = False
                
        if(consumidor.estado == "Trabajando" and checkConsAvailable()):
            consumir(consumidor.pos)
            if(consumidor.pos < 29):
                consumidor.pos += 1
            else:
                consumidor.pos = 0
        
        print("Productor: ", productor.estado, "[", productor.time,"]", "POS: ", productor.pos, "\nConsumidor: ", consumidor.estado, "[", consumidor.time, "]", "POS: ", consumidor.pos,"\n")
        
        ciclo += 1
        #Main
        printBuffer()
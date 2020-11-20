#####################################
## Becerra Mata Juan Ricardo - D02 ##
#####################################

import keyboard
import random
import os
import time

class Productor:
    pos = 0
    time = 10
    wait = False
    estado = "Trabajando" #init, durmiendo, esperando, trabajando
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
prodOn = False
consOn = False

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
    if("__" in buffer):
        return True
    else:
        return False
    
def checkConsAvailable():
    if("&&" in buffer):
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
os.system('mode con: cols=120 lines=30')
ciclo = 0

while True:
    time.sleep(0.75)

    if(keyboard.is_pressed('ESC')):
        print("\n\nTerminando...")
        break

    else:
        print("########################################################################################################################")
        print("Ciclo: ", ciclo+1, "\n")

        #Decidir estado (Durmiendo o trabajando)
        #Verificar si tienen tiempo pendiente en el estado actual, sino cambiar
        if(productor.time < 1 and productor.wait == False):
            productor.estado_exp = random.choice(estados)
            productor.estado = "Eligiendo"
            prodOn = False
            semaforo = False
        elif(productor.estado != "Esperando" and productor.estado != "Eligiendo"):
            productor.time -= 1
            
        if(consumidor.time < 1 and consumidor.wait == False):
            consumidor.estado_exp = random.choice(estados)
            consumidor.estado = "Eligiendo"
            consOn = False
            semaforo = False
        elif(consumidor.estado != "Esperando" and consumidor.estado != "Eligiendo"):
            consumidor.time -= 1
            
        #Verificar si alguno está trabajando en este momento
        if(semaforo == False): #Ninguno trabajando
            if(consumidor.estado == "Esperando" and productor.estado == "Eligiendo" or "Esperando") or (productor.estado == "Esperando" and consumidor.estado == "Eligiendo" or "Esperando"): #Si uno estaba esperando
                if(consumidor.estado == "Esperando" and checkConsAvailable()): #El que esperaba comienza a trabajar y el otro esperaba dormir
                    consumidor.estado = "Trabajando"
                    consumidor.wait = False
                    consOn = True
                    semaforo = True
                    if(productor.estado_exp == "Durmiendo"):
                        productor.estado = "Durmiendo"
                    elif(productor.estado_exp == "Trabajando"):
                        productor.estado = "Esperando"
                        productor.time = random.randrange(3, 11, 1)
                elif(productor.estado == "Esperando" and checkProdAvailable()):
                    productor.estado = "Trabajando"
                    productor.wait = False
                    prodOn = True
                    semaforo = True
                    if(consumidor.estado_exp == "Durmiendo"):
                        consumidor.estado = "Durmiendo"
                    elif(consumidor.estado_exp == "Trabajando"):
                        consumidor.estado = "Esperando"
                        consumidor.time = random.randrange(3, 11, 1)
            
            #Decidir cual de los dos entrará primero
            elif(productor.estado_exp == consumidor.estado_exp == "Trabajando"): #Si ambos quieren trabajar
                if(random.choice(procesos) == "Productor" and checkProdAvailable()):
                    productor.estado = productor.estado_exp
                    prodOn = True
                    semaforo = True
                    productor.wait = False
                    consumidor.estado = "Esperando"
                else:
                    consumidor.estado = consumidor.estado_exp
                    consOn = True
                    semaforo = True
                    consumidor.wait = False
                    productor.estado = "Esperando"
                    
                productor.time = random.randrange(3, 11, 1)
                consumidor.time = random.randrange(3, 11, 1)
            
            elif(productor.estado_exp == "Durmiendo" and consumidor.estado_exp == "Trabajando") or (productor.estado_exp == "Trabajando" and consumidor.estado_exp == "Durmiendo"): #Si uno quiere trabajar y el otro dormir
                #print(":0")
                if(productor.estado_exp == "Trabajando" and checkProdAvailable()):
                    prodOn = True
                    semaforo = True
                    productor.wait = False
                    productor.estado = "Trabajando"
                    productor.time = random.randrange(3, 11, 1)
                    if(consumidor.time == 0):
                        consumidor.estado = "Durmiendo"
                        consumidor.time = random.randrange(3, 11, 1)
                elif(consumidor.estado_exp == "Trabajando" and checkConsAvailable()):
                    consOn = True
                    semaforo = True
                    consumidor.wait = False
                    consumidor.estado = "Trabajando"
                    consumidor.time = random.randrange(3, 11, 1)
                    if(productor.time == 0):
                        productor.estado = "Durmiendo"
                        productor.time = random.randrange(3, 11, 1)
                
            elif(productor.estado_exp == consumidor.estado_exp == "Durmiendo"): #Si ambos quieren dormir
                #print(":1")
                if(productor.estado != "Durmiendo"):
                    productor.estado = "Durmiendo"
                    productor.time = random.randrange(3, 11, 1)
                
                if(consumidor.estado != "Durmiendo"):
                    consumidor.estado = "Durmiendo"
                    consumidor.time = random.randrange(3, 11, 1)
                
        
        #print("Productor: ", productor.estado_exp, " -> ", productor.estado, "[", productor.time,"]", "POS: ", productor.pos, "\nConsumidor: ", consumidor.estado_exp, " -> ", consumidor.estado, "[", consumidor.time, "]", "POS: ", consumidor.pos,"\n")
        print("Productor: ", productor.estado, "[", productor.time,"]", "POS: ", productor.pos, "\nConsumidor: ", consumidor.estado, "[", consumidor.time, "]", "POS: ", consumidor.pos,"\n")
        
        #########
        #Trabajo#
        #########
        if(productor.estado == "Trabajando" and buffer[productor.pos] == "__" and consumidor.estado != "Trabajando"):
            p = productor.pos
            producir(p)
            consumidor.wait = False
            if(productor.pos < 29):
                productor.pos += 1
            else:
                productor.pos = 0
        else:
            productor.wait = True
            prodOn = False
            semaforo = False
            productor.estado = "Esperando"
            
        if(consumidor.estado == "Trabajando" and buffer[consumidor.pos] == "&&" and productor.estado != "Trabajando"):
            p = consumidor.pos
            consumir(p)
            productor.wait = False
            if(consumidor.pos < 29):
                consumidor.pos += 1
            else:
                consumidor.pos = 0
        else:
            consumidor.wait = True
            consOn = False
            semaforo = False
            consumidor.estado = "Esperando"

        if(productor.wait == True == consumidor.wait):
            if(buffer[consumidor.pos] == "&&"):
                consumidor.estado = "Trabajando"
                consumidor.wait = False
                consOn = True
                semaforo = True
            else:
                productor.estado = "Trabajando"
                productor.wait = False
                prodOn = True
                semaforo = True

        ciclo += 1
        #Main
        printBuffer()


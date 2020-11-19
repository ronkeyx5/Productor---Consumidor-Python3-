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
    estado = "init" #init, durmiendo, esperando, trabajando
    estado_exp = "init"

    def producir(p):
        #print("##")
        buffer[p] = "&&"
        return

class Consumidor:
    pos = 0
    time = 0
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
        if(productor.time < 1 ):
            productor.estado_exp = random.choice(estados)
        elif(productor.estado != "Esperando"):
            productor.time -= 1
            
        if(consumidor.time < 1 ):
            consumidor.estado_exp = random.choice(estados)
        elif(consumidor.estado != "Esperando"):
            consumidor.time -= 1
            
        #Verificar si alguno está trabajando en este momento
        if(semaforo == False): #Ninguno trabajando
            #Decidir cual de los dos entrará primero
            if(productor.estado_exp == consumidor.estado_exp == "Trabajando"): #Si ambos quieren trabajar
                if(random.choice(procesos) == "Productor" and checkProdAvailable()):
                    productor.estado = productor.estado_exp
                    prodOn = True
                    consumidor.estado = "Esperando"
                else:
                    consumidor.estado = consumidor.estado_exp
                    consOn = True
                    productor.estado = "Esperando"
                    
                productor.time = random.randrange(3, 11, 1)
                consumidor.time = random.randrange(3, 11, 1)
            elif(): #Si uno quiere trabajar y el otro dormir
                print(":0")
            elif(): #Si ambos quieren dormir
                print(":0")
                
        
        print("Productor: ", productor.estado_exp, " -> ", productor.estado, "[", productor.time,"]", "\nConsumidor: ", consumidor.estado_exp, " -> ", consumidor.estado, "[", consumidor.time, "]", "\n")

        ciclo += 1
        #Main
        printBuffer()


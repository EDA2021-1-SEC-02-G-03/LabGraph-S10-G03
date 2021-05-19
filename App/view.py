"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config
import time
import tracemalloc

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base:")
    print("5- Hay camino entre estacion base y estación: ")
    print("6- Ruta de costo mínimo desde la estación base y estación: ")
    print("7- Estación que sirve a mas rutas: ")
    print("0- Salir")
    print("*******************************************")


def optionTwo(cont):
    print("\nCargando información de transporte de singapur ....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))


def optionThree(cont):
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))


def optionFour(cont, initialStation):
    controller.minimumCostPaths(cont, initialStation)


def optionFive(cont, destStation):
    haspath = controller.hasPath(cont, destStation)
    print('Hay camino entre la estación base : ' +
          'y la estación: ' + destStation + ': ')
    print(haspath)


def optionSix(cont, destStation):
    path = controller.minimumCostPath(cont, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')


def optionSeven(cont):
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(cont)

        elif int(inputs[0]) == 3:
            optionThree(cont)

        elif int(inputs[0]) == 4:
            msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "

            delta_time = -1.0
            delta_memory = -1.0

            tracemalloc.start()
            start_time = controller.getTime()
            start_memory = controller.getMemory()
            
            initialStation = input(msg)

            delta_time = -1.0
            delta_memory = -1.0

            tracemalloc.start()
            start_time = controller.getTime()
            start_memory = controller.getMemory()
            #======================================
            optionFour(cont, initialStation)#'75009-10')#initialStation)
            #======================================
            stop_memory = controller.getMemory()
            stop_time = controller.getTime()
            tracemalloc.stop()

            delta_time = stop_time - start_time
            delta_memory = controller.deltaMemory(start_memory, stop_memory)
            print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")

        elif int(inputs[0]) == 5:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionFive(cont, destStation)

        elif int(inputs[0]) == 6:
            destStation = input("Estación destino (Ej: 15151-10): ")

            delta_time = -1.0
            delta_memory = -1.0

            tracemalloc.start()
            start_time = controller.getTime()
            start_memory = controller.getMemory()

            #===================================
            optionSix(cont, destStation)#'15151-10')#destStation)
            #==================================

            stop_memory = controller.getMemory()
            stop_time = controller.getTime()
            tracemalloc.stop()

            delta_time = stop_time - start_time
            delta_memory = controller.deltaMemory(start_memory, stop_memory)
            print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")

        elif int(inputs[0]) == 7:
            optionSeven(cont)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

import copy
import re
import xml.etree.ElementTree as ET
import os

class Casilla:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor
class Fila:
    def __init__(self, casillas):
        self.casillas = casillas
        self.activa = True

class Matriz:
    def __init__(self, nombre, n, m, filas, patrones_acceso, reducida):
        self.nombre = nombre
        self.n = n
        self.m = m
        self.filas = filas
        self.patrones_acceso = patrones_acceso
        self.reducida = reducida

class Nodo:
    def __init__(self, dato=None, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class ListaCircularSimpleEnlazada(object):
    def __init__(self, cabeza=None, primero=None):
        self.cabeza = cabeza
        self.primero = primero

    def append(self, matriz):
        nuevo_nodo = Nodo(matriz)
        if self.cabeza == None:
            self.cabeza = nuevo_nodo
            self.cabeza.siguiente = nuevo_nodo
            self.primero = nuevo_nodo
            return
        if self.primero != None:
            self.primero.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
            self.primero = nuevo_nodo
            return

class Main:

    contenido_archivo = ""
    ruta = ""
    lista_matrices = ListaCircularSimpleEnlazada()

    def menu(self):
        print("\n")
        print("1 Cargar archivo")
        print("2 Procesar archivo")
        print("3 Escribir archivo de salida")
        print("4 Mostrar datos del estudiante")
        print("5 Generar gráfica")
        print("6 salida" + "\n")
        entrada = input("Ingrese un numero 1-6" + "\n")
        patron = "[1-6]{1}"
        if re.search(patron, entrada):
            if entrada == "1":
                self.cargarArchivo()
                self.menu()
            elif entrada == "2":
                self.procesarArchivo()
                self.menu()
            elif entrada == "3":
                self.archivoSalida()
            elif entrada == "4":
                print("Pablo Alejandro Franco Lemus")
                print("201708993")
                print("Introducción a la programacion y Computación 2 seccion A")
                print("Ingenieria en Ciencias y Sistemas")
                print("4to Semestre")
                self.menu()
            # elif entrada == "5":
            elif entrada == "6":
                exit()
        else:
            self.menu()

    def procesarArchivo(self):
        arbol = ET.parse(self.ruta)
        raiz = arbol.getroot()
        for mat in raiz.findall('matriz'):
            nombre = mat.attrib['nombre']
            n = mat.attrib['n']
            m = mat.attrib['m']
            matriz = []
            lista = []
            contador = 1
            for d in mat:
                if d.attrib['x'] == str(contador):
                    lista.append(Casilla(d.attrib['x'], d.attrib['y'], d.text))
                else:
                    matriz.append(Fila(lista))
                    lista = []
                    contador += 1
                    lista.append(Casilla(d.attrib['x'], d.attrib['y'], d.text))
            matriz.append(Fila(lista))
            patrones_acceso = self.crearMatrizAacceso(copy.deepcopy(matriz))
            reducida = self.crearMatrizReducida(copy.deepcopy(matriz), copy.deepcopy(patrones_acceso))
            self.lista_matrices.append(Matriz(nombre, n, m, matriz, patrones_acceso, reducida))

    def crearMatrizAacceso(self, matriz_copia):
        for fila in matriz_copia:
            for casilla in fila.casillas:
                if casilla.valor != '0':
                    casilla.valor = '1'
        return matriz_copia

    def crearMatrizReducida(self,  matriz, patrones_acceso):
        patrones_iguales = self.coincidencias(matriz, copy.deepcopy(patrones_acceso))
        patrones_copia = self.coincidencias(matriz, copy.deepcopy(patrones_acceso))
        reducida = []
        x = 1
        y = 1
        while len(patrones_copia) > 0:
            conjunto_patrones = patrones_copia.pop()
            fila_temp = []
            contador1 = 0
            if len(conjunto_patrones) > 1:
                fila_a = matriz[conjunto_patrones.pop()].casillas
                while len(conjunto_patrones) > 0:
                    fila_b = matriz[conjunto_patrones.pop()].casillas
                    for celda in fila_a:
                        celda.valor = (int(celda.valor)+int(fila_b[contador1].valor))
                        contador1 += 1
                for celda in fila_a:
                    fila_temp.append(Casilla(x, y, celda.valor))
                    y += 1
                y = 1
                x += 1
                reducida.append(Fila(copy.deepcopy(fila_temp)))
                fila_temp = []
            else:
                for celda in matriz[conjunto_patrones[0]].casillas:
                    fila_temp.append(Casilla(x, y, celda.valor))
                    y += 1
                reducida.append(Fila(copy.deepcopy(fila_temp)))
                y = 1
                x += 1
                fila_temp = []
        return reducida

    def coincidencias(self, matriz, patrones_acceso):
        copia_matriz = copy.deepcopy(matriz)
        lista_coincidencias = []
        lista_temp = []
        while len(patrones_acceso) > 0:
            fila_temp = patrones_acceso.pop()
            lista_temp.append(len(patrones_acceso))
            indice_fila = 0
            for fila in patrones_acceso:
                coinciden = True
                contador = 0
                if fila.activa:
                    for celda in fila.casillas:
                        if celda.valor != fila_temp.casillas[contador].valor:
                            coinciden = False
                            break
                        contador += 1
                    if coinciden:
                        lista_temp.append(indice_fila)
                        patrones_acceso[indice_fila].activa = False
                indice_fila += 1
            if fila_temp.activa:
                lista_coincidencias.append(lista_temp)
                lista_temp = []
        return lista_coincidencias

    def cargarArchivo(self):
        ruta = input("Ingrese la ruta del archivo: ")
        dimExt = len(ruta)
        if ruta.endswith(".xml", dimExt - 4, dimExt) and os.path.exists(ruta):
            self.ruta += ruta
        else:
            print("Ingrese una ruta y extensión correcta .xml para el archivo")
            self.cargarArchivo()

    def archivoSalida(self):
        ruta = input("Escribir una ruta específica: ")

Main().menu()


import re
import xml.etree.ElementTree as ET
import os


class Casilla:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor


class Matriz:
    def __init__(self, nombre, n, m, filas):
        self.nombre = nombre
        self.n = n
        self.m = m
        self.filas = filas


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

    # def prepend(self):


class Main:

    contenido_archivo = ""
    ruta =""
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
            # elif entrada == "3":
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
                    matriz.append(lista)
                    lista = []
                    contador += 1
                    lista.append(Casilla(d.attrib['x'], d.attrib['y'], d.text))
            matriz.append(lista)
            self.lista_matrices.append(Matriz(nombre, n, m, matriz))

    def cargarArchivo(self):
        ruta = input("Ingrese la ruta del archivo: ")
        dimExt = len(ruta)
        if ruta.endswith(".xml", dimExt - 4, dimExt) and os.path.exists(ruta):
            self.ruta += ruta
        else:
            print("Ingrese una ruta y extensión correcta .xml para el archivo")
            self.cargarArchivo()


Main().menu()


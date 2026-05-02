#se usa para arrancar todo el juego, conecta todas las pantallas entre ellas
import tkinter as tk
from interfaz import PantallaInicial
from mapa import PantallaMapa
from pantalla_batalla import PantallaBatalla
from utils import Entrenador
from personaje_clase import Personaje
from personajes import leer_personajes
import random

class Juego:
    def __init__(self):
        #Se crea una ventana principal que se debe mantener durante todo el juego
        self.root = tk.Tk()
        self.root.title("Disney's Epic Adventure")
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        #Se deben definir las variables del juego como vacías en este momento
        self.jugador = None
        self.pantalla_mapa = None

        #Guardar los hollows que ya se derrotaron
        self.hollows_derrotados = []

        #Arrancar con la pantalla inicial
        self.mostrar_pantalla_inicial()
    def _limpiar_pantalla(self, widgets):
        #Se deben eliminar todos los widgets de la ventana para pasar a la siguiente ventana 
        if len(widgets) == 0:
            return
        widgets[0].destroy()
        self._limpiar_pantalla(self.root.winfo_children())

    def mostrar_pantalla_inicial(self):
        #Cuando se presione iniciar entrará el callback
        PantallaInicial(self.root, callback_iniciar=self.iniciar_juego)
    
    #Se inicia el juego después de presionar el botón iniciar, se pone un string con el nombre del jugador y un string con el avatar elegido, además el quipo muestra los personajes elegidos
    def iniciar_juego(self, nombre, avatar, equipo):
        self.jugador = Entrenador(nombre, equipo)
        self.jugador.avatar = avatar  #Guarda el avatar elegido

        #Limpiar la pantalla inicial y mostrar el mapa
        self._limpiar_pantalla(self.root.winfo_children())
        self.mostrar_mapa()

    def mostrar_mapa(self):
        self._limpiar_pantalla(self.root.winfo_children())
        self.pantalla_mapa = PantallaMapa(self.root, self.jugador, callback_batalla=self.iniciar_batalla, hollows_derrotados=self.hollows_derrotados)

    #Cuando el jugador hace click en batallar en el mapa se crea el equipo del hollow utilizando random
    def iniciar_batalla(self, nombre_hollow):
        datos = leer_personajes("personajes.txt")
        todos = self._crear_personajes(datos, 0, [])
        nombres_jugador = self._nombres_equipo(self. jugador.personajes, 0, []) #Guarda los nombres del equipo del jugador para excluirlos
        disponibles = self._filtrar_disponibles(todos, nombres_jugador, 0, [])
        equipo_hollow = self._elegir_equipo_hollow(disponibles, [], 0)
        hollow = Entrenador(nombre_hollow, equipo_hollow, es_hollow=True)
        hollow = Entrenador(nombre_hollow, equipo_hollow, es_hollow=True)

        #Limpiar pantalla y mostrar la batalla
        self._limpiar_pantalla(self.root.winfo_children())
        PantallaBatalla(self.root, self.jugador, hollow, nombre_hollow, callback_victoria=self.terminar_batalla)

    def _filtrar_disponibles(self, todos, nombres_jugador , indice, resultado):
        if indice == len(todos):
            return resultado 
        p = todos[indice]
        if p.nombre not in nombres_jugador: 
                resultado.append(p)
        return self._filtrar_disponibles(todos, nombres_jugador, indice + 1, resultado)
        
    #Cunado se termina la batalla dice el nombre del hollow derrotado o None si el jugador perdió
    def terminar_batalla(self, nombre_hollow):
        if nombre_hollow is not None: #significa que el jugador ganó
            self.hollows_derrotados.append(nombre_hollow) #Guardar que ya se han derrotado otros hollows
            self._limpiar_pantalla(self.root.winfo_children())
            self.pantalla_mapa = PantallaMapa(self.root, self.jugador, callback_batalla=self.iniciar_batalla, hollows_derrotados=self.hollows_derrotados)
            self.pantalla_mapa.hollow_derrotado(nombre_hollow)
        else:

            #Si el jugador perdió la batalla hay que volver al mapa, pero sin marcar la victoria
            self._limpiar_pantalla(self.root.winfo_children())
            self.pantalla_mapa = PantallaMapa(self.root, self.jugador, callback_batalla=self.iniciar_batalla)

    #Crear los objetos Personaje desde los datos del txt
    def _crear_personajes(self, datos, indice, resultado):
        if indice == len(datos):
            return resultado
        d = datos[indice]
        resultado.append(Personaje(d['nombre'], d['vida'], d['ataque'], d['defensa']))
        return self._crear_personajes(datos, indice + 1, resultado)

    #Elige 3 personajes aleatorios para el hollow 
    def _elegir_equipo_hollow(self, todos, elegidos, intentos):
        if len(elegidos) == 3:
            return elegidos
        indice = random.randint(0, len(todos) - 1)
        personaje = todos[indice]
        nombres = self._nombres_equipo(elegidos, 0, [])
        if personaje.nombre not in nombres:
            elegidos.append(personaje)
        return self._elegir_equipo_hollow(todos, elegidos, intentos + 1)

    #Obtener los nombres del equipo
    def _nombres_equipo(self, equipo, indice, resultado):
        if indice == len(equipo):
            return resultado
        resultado.append(equipo[indice].nombre)
        return self._nombres_equipo(equipo, indice + 1, resultado)

    #Iniciar el loop principal de Tkinter
    def arrancar(self):
        self.root.mainloop()

if __name__ == "__main__":
    juego = Juego()
    juego.arrancar()
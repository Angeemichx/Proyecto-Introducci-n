import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from utils import Entrenador
from personaje_clase import Personaje
from personajes import leer_personajes
import random

#Datos de los Hollows con sus mundos
HOLLOWS = [{"nombre": "Gargamel",  "mundo": "El Bosque Encantado"},
    {"nombre": "Jack",      "mundo": "El Caribe"},
    {"nombre": "Maléfica",  "mundo": "Reino del Mal"},
    {"nombre": "Reina",     "mundo": "El Espejo Mágico"},
    {"nombre": "Úrsula",    "mundo": "Las Profundidades"},]

class PantallaMapa:
    def __init__(self, root, jugador, callback_batalla=None, hollows_derrotados=None):
        #Se define al jugador como objeto Entrenador con sus datos
        self.root = root
        self.jugador = jugador
        self.root.title("Mapa - Disney's Epic Adventure")
        self.root.geometry("800x650")
        self.root.configure(bg="#1a1a2e")  #Fondo oscuro para el mapa
        self.root.resizable(False, False)
        self.callback_batalla = callback_batalla #Para pasar a la siguiente ventana

        #Guardar imágenes para que no las elimine Python de memoria
        self.imagenes_hollows = {}
        self.hollows_derrotados = hollows_derrotados if hollows_derrotados is not None else [] #Lista de hollows que ya fueron derrotados, si ya hay una existente usarla
        self._construir_mapa()

    def _construir_mapa(self):
        #verificar si ya derrotó a todos y ganó
        if len (self.hollows_derrotados) == 5:
            self._pantalla_victoria()
            return
        #Título del mapa
        tk.Label(self.root, text="Mapa del Reino Imaginario", font=("georgia", 22, "bold"), bg="#1a1a2e", fg="#FFE66D").pack(pady=(20, 5))

        #Ahora se debe mostrar nombre del jugador y su puntaje
        tk.Label(self.root, text=f"Guardián: {self.jugador.nombre}  |  Puntaje: {self.jugador.puntaje}", font=("Georgia", 12), bg="#1a1a2e", fg="white").pack(pady=(0, 15))
        tk.Label(self.root, text="Elige un Hollow para batallar:", font=("Georgia", 13, "italic"), bg="#1a1a2e", fg="#4ECDC4").pack(pady=(0, 10))

        #Crear frame para el cuadro de Hollows
        frame_hollows = tk.Frame(self.root, bg="#1a1a2e")
        frame_hollows.pack()

        #Se crean los botones de los hollows
        self._construir_hollows(frame_hollows, 0)

    #Función para detectar que se llegó a la victoria
    def _pantalla_victoria(self):
        #colocar un fondo
        self.root.configure(bg="#1a1a2e")
        tk.Label(self.root, text="¡¡¡VICTORIA!!!", font=("Gerorgia", 36, "bold"), bg="#1a1a1e", fg="#FFE66D").pack(pady=(80, 10))
        tk.Label(self.root, text=f"¡{self.jugador.nombre} ha derrotado a todos los Hollows!", font=("Georgia", 16), bg="#1a1a2e", fg="white").pack(pady=10)
        tk.Label(self.root, text="Todos los personajes han sido salvados\ny las historias han sido restauradas.", font=("Georgia", 13, "italic"), bg="#1a1a2e", fg="#4ECDC4").pack(pady=10)
        tk.Label(self.root, text=f"Puntaje final: {self.jugador.puntaje} personajes rescatados", font=("Georgia", 14, "bold"), bg="#1a1a2e", fg="#FF6B6B").pack(pady=20)
        tk.Button(self.root, text="Volver a jugar", font=("Georgia", 14, "bold"), bg="#FF6B6B", fg="white", relief="flat", padx=20, pady=10,cursor="hand2", activebackground="#FF6B6B", activeforeground="white", command=lambda: self.callback_batalla(None)).pack(pady=20)

    def _construir_hollows(self, frame, indice):
        if indice == len(HOLLOWS): #Caso base
            return
        hollow = HOLLOWS[indice]
        nombre = hollow["nombre"]
        mundo = hollow["mundo"]

        #Se pone la posición que tendrá el cuadro (3 en primera fila y 2 en segunda)
        col = indice % 3
        fila = indice // 3

        #Frame individual para cada Hollow
        frame_h = tk.Frame(frame, bg="#16213e", cursor="hand2", relief="solid", bd=1)
        frame_h.grid(row=fila, column=col, padx=10, pady=10)

        #Cargar imagen del Hollow
        ruta = os.path.join("imágenes", "hollows", f"{nombre}.png")
        try:
            img = Image.open(ruta).resize((120, 120))
            foto = ImageTk.PhotoImage(img)
            self.imagenes_hollows[nombre] = foto
            tk.Label(frame_h, image=foto, bg="#16213e").pack(pady=(10, 5))
        except:
            tk.Label(frame_h, text="?", font=("GEORGIA", 40), bg="#16213e").pack(pady=(10, 5))

        #Añadir nombre del Hollow
        tk.Label(frame_h, text=nombre, font=("Georgia", 12, "bold"), bg="#16213e", fg="#FF6B6B").pack()

        #Ubicar el mundo
        tk.Label(
            frame_h, text=mundo, font=("Georgia", 9, "italic"), bg="#16213e", fg="#aaaaaa").pack(pady=(0, 5))

        #Mostrar si ya fue derrotado y sino mostrar botón de batalla
        if nombre in self.hollows_derrotados:
            tk.Label(frame_h, text="Derrotado", font=("Georgia", 10, "bold"), bg="#16213e", fg="#4ECDC4").pack(pady=(0, 10))
        else:
            tk.Button(frame_h, text="Batallar", font=("Georgia", 10, "bold"), bg="#FF6B6B", fg="white", relief="flat", padx=10, pady=5, cursor="hand2", activebackground="#FF6B6B", activeforeground="white", command=lambda n=nombre: self._ir_a_batalla(n)).pack(pady=(0, 10))

        #Siguiente Hollow
        self._construir_hollows(frame, indice + 1)

    #Se llama al hacer clic en "Batallar"
    def _ir_a_batalla(self, nombre_hollow):

        #Crear el equipo del Hollow con personajes aleatorios
        datos = leer_personajes("personajes.txt")
        todos = self._crear_personajes_hollow(datos, 0, [])
        equipo_hollow = self._elegir_equipo_hollow(todos, [], 0)
        hollow = Entrenador(nombre_hollow, equipo_hollow, es_hollow=True)
        if self.callback_batalla:
            self.callback_batalla(nombre_hollow)

        #El Hollow recibe 3 personajes aleatorios
    def _elegir_equipo_hollow(self, todos, elegidos, intentos):
        if len(elegidos)==3:
            return elegidos
        indice = random.randint(0, len(todos) -1) #agrega un indice aleatorio
        personaje = todos[indice]
        if personaje.nombre not in self._nombres_equipo(elegidos, 0, []): #si ya está en el equipo no lo agrega
            elegidos.append(personaje)
        return self._elegir_equipo_hollow(todos, elegidos, intentos + 1)
    
    #Escribir los nombres del equipo
    def _nombres_equipo(self, equipo, indice, resultado):
        if indice == len(equipo):
            return resultado
        resultado.append(equipo[indice].nombre)
        return self._nombres_equipo(equipo, indice + 1, resultado)

    #Crea objetos Personaje desde los datos del txt
    def _crear_personajes_hollow(self, datos, indice, resultado):
        if indice == len(datos):
            return resultado
        d = datos[indice]
        resultado.append(Personaje(d['nombre'], d['vida'], d['ataque'], d['defensa']))
        return self._crear_personajes_hollow(datos, indice + 1, resultado)

    #Actualiza el mapa después de una batalla
    def hollow_derrotado(self, nombre_hollow):
        self.hollows_derrotados.append(nombre_hollow)
        if len(self.hollows_derrotados) == 5: #Verificar si ya derrotó a todos
            messagebox.showinfo("¡Victoria!", f"¡{self.jugador.nombre} restauró todas las historias!\n\n" f"Puntaje final: {self.jugador.puntaje}")
        self._limpiar_pantalla(self.root.winfo_children())
        self._construir_mapa()

    #Reconstruir el mapa para mostrar los cambios
    def _limpiar_pantalla(self, widgets):
        if len(widgets) == 0: # Caso base
            return
        widgets[0].destroy()
        self._limpiar_pantalla(self.root.winfo_children())
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os 
from personajes import leer_personajes
from batalla import batalla 
from utils import Entrenador
from personaje_clase import Personaje 

#Colores para la interfaz:
COLOR_FONDO = "#FFF8F0"
COLOR_BOTONES = "#FF6B6B"
COLOR_BOTONESS= "#4ECDC4"
COLOR_SELECCION = "#FFE66D"
COLOR_TEXTO = "#2C3E50"

#fuentes de texto
FUENTE_TITULO= ("georgia", 28, "bold")
FUENTE_SUBTITULO= ("georgia", 18, "bold")
FUENTE_TEXTO= ("GEORGIA", 11, "normal")
FUENTE_BOTON= ("georgia", 12, "bold")

class PantallaInicial:
    def __init__(self, root, callback_iniciar=None):
        self.root = root
        self.root.title("Pantalla Inicial")
        self.root.geometry("800x750")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)
        self.callback_iniciar = callback_iniciar 

    #cargar datos y convertirlos en objetos personaje
        datos=leer_personajes("personajes.txt")
        self.personajes_disponibles = self._crear_personajes(datos, 0, [])

    #utilizar StringVar para conectar a widgets y que se pueda actualizar la interfaz (función de tkinter)
        self.nombre_var = tk.StringVar() #con este se guarda el nombre introducido por el usuario
        self.avatar_var = tk.StringVar(value="Aladino")
        self.seleccionados = [] #para guardar los personajes que el usuario ha seleccionado
        self.botones_personajes = {} #guardar botones de personajes y cambiar color al ser seleccionados 
        self.imagenes_avatares = {} #guardar las imágenes de los avatares para mostrarlas en la interfaz
        self.imagenes_personajes = {} #guardar las imágenes de los personajes para mostrarlas en la interfaz

        self._construir_interfaz() #para crear los elementos de la interfaz

    #convertir lista de datos en objetos, se crea y se agrega a una lista de personajes disponibles para que el usuario pueda elegir, el caso base es cuando se han procesado todos los datos (cuando el indice es igual a la longitud de la lista de datos), en ese caso se devuelve la lista de personajes creados.
    def _crear_personajes(self, datos, indice, resultado):
        if indice == len(datos):
            return resultado
        d=datos[indice]
        resultado.append(Personaje(d["nombre"], d["vida"], d["ataque"], d["defensa"]))
        return  self._crear_personajes(datos, indice + 1, resultado)
    
    def _construir_interfaz(self):
        #Título principal, tk.Label muestra el tecto, pack() lo posiciona en la venta, pady agrega espacio vertical
        tk.Label(self.root, text= "Disney's Epic Adventure", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_BOTONES).pack(pady=(10,5))
        tk.Label(self.root, text= "¡Bienvenido, Conviértete en el mejor Guardián!", font=FUENTE_TEXTO, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(0,15))

    #Agregar espacio para el nombre del usuario. En tk frame es un contenedor invisible que agrupa widgets. Se pone la etiqueta y el espacio en la misma linea.
        frame_nombre = tk.Frame(self.root, bg = COLOR_FONDO)
        frame_nombre.pack(pady=5)

        #Se usa side left que coloca los elementos de forma horizontal
        tk.Label(frame_nombre, text="Tu nombre:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left", padx=5)

        #Se utiliza entry que es donde el jugador escribe y nombre_var debe actualizarse
        tk.Entry(frame_nombre, textvariable=self.nombre_var, font=FUENTE_TEXTO, width=20, relief="solid", bd=2, fg=COLOR_TEXTO).pack(side= "left", padx=5)

        #Posteriormente el jugador debe elegir su avatar 
        tk.Label(self.root, text="Selecciona tu Avatar", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(15,5))

        frame_avatares = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_avatares.pack()

        #Colocación de los avatares, recorriendo lista 
        self._construir_avatares(["Aladino", "Genio", "Jazmín"], frame_avatares, 0)

        #Selección de personajes para la batalla
        tk.Label(self.root, text= "Selecciona 3 personajes para la batalla:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(15,5))
        frame_personajes = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_personajes.pack()
        self._construir_personajes(self.personajes_disponibles, frame_personajes, 0)

        #botones
        frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_botones.pack(pady=20)

        #para iniciar el juego, se debe llamar a la función iniciar con command=self._iniciar
        tk.Button(frame_botones, text= "INICIAR", font=FUENTE_BOTON, bg=COLOR_BOTONES, fg=COLOR_FONDO, relief="flat", padx=20, pady= 8, cursor= "hand2", activebackground=COLOR_BOTONES, activeforeground=COLOR_FONDO, command=self._iniciar).pack(side="left", padx=10)
        tk.Button(frame_botones, text="ABOUT", font=FUENTE_BOTON, bg=COLOR_BOTONESS, fg=COLOR_FONDO, relief= "flat", padx=20, pady=8, cursor="hand2", activebackground=COLOR_BOTONESS, activeforeground=COLOR_FONDO, command=self._mostrar_about).pack(side="left", padx=10)

    #Ahora se construyen los botones para seleccionar el avatar (botón de selección única o radiobutton) y una imagen del personaje a seleccionar
    def _construir_avatares(self, avatares, frame, indice):
        if indice == len(avatares): #Caso base
            return
        nombre = avatares[indice]
        ruta = os.path.join("imágenes", "avatares", f"{nombre}.png")

        #debe haber un frame individual para casa personaje:
        frame_avatar = tk.Frame(frame, bg=COLOR_FONDO, cursor="hand2")
        frame_avatar.pack(side="left", padx=10)

        #Cargar la imagen, si falla se muestra "?"
        try:
            img = Image.open(ruta).resize((70,70)) #esto es para que todas las imagenes tengan el mismo tamaño
            foto = ImageTk.PhotoImage(img)

        #se debe guardar la imagen en el diccionario para que no se elimine de la memeoria
            self.imagenes_avatares[nombre] = foto
            tk.Label(frame_avatar, image=foto, bg=COLOR_FONDO).pack()
        except:
            tk.Label(frame_avatar, text="?", font=("Georgia", 30), bg=COLOR_FONDO).pack()
        
        #Debe realizarse el botón de selección del avatar, se utiliza una variable que compartan todos los personajes para que solo se pueda selección uno, value es el valor que se va a asignar a la variable cuando el usuario seleccione ese avatar
        rb = tk.Radiobutton(frame_avatar, text=nombre, variable=self.avatar_var, value=nombre, font=FUENTE_TEXTO, bg= COLOR_FONDO, fg=COLOR_TEXTO, selectcolor=COLOR_SELECCION, activebackground=COLOR_FONDO)
        rb.pack()

        #Se llama a la función para el siguiente avatar
        self._construir_avatares(avatares, frame, indice + 1)

         # Se construye un cuadro de personajes
    def _construir_personajes(self, personajes, frame, indice):

        #Caso base en el que ya construimos todos los personajes
        if indice == len(personajes):
            return
        p = personajes[indice]
        ruta = os.path.join("imágenes", "personajes", f"{p.nombre}.png")

        #Se calcula la fila y columna para el cuadro (5 personajes por fila)
        col = indice % 5
        fila = indice // 5
        frame_p = tk.Frame(frame, bg=COLOR_FONDO, cursor="hand2")

        #Se utiliza grid() para colocar el widget en una posición específica
        frame_p.grid(row=fila, column=col, padx=8, pady=5)

        try:
            img = Image.open(ruta).resize((55, 55))
            foto = ImageTk.PhotoImage(img)
            self.imagenes_personajes[p.nombre] = foto  #Guardar referencia
            tk.Label(frame_p, image=foto, bg=COLOR_FONDO).pack()
        except:
            tk.Label(frame_p, text="Batalla", font=("Georgia", 24), bg=COLOR_FONDO).pack()

        #Botón con el nombre del personaje, con lambda se guarda el nombre actual para pasarlo a _toggle_personaje sino, todos los botones pasarían el último nombre de la lista
        btn = tk.Button(
            frame_p, text=p.nombre, font=("Georgia", 9), bg="white", fg=COLOR_TEXTO, relief="solid", bd=1, padx=4, pady=2, command=lambda nombre=p.nombre: self._toggle_personaje(nombre))
        btn.pack()

        #Se guarda referencia del botón para poder cambiar su color
        self.botones_personajes[p.nombre] = btn

        #Lamada para el siguiente personaje
        self._construir_personajes(personajes, frame, indice + 1)

    # Selecciona o quita un personaje al hacer clic
    def _toggle_personaje(self, nombre):
        if nombre in self.seleccionados:

            #Si ya estaba seleccionado, lo quita y regresa el color blanco
            self.seleccionados.remove(nombre)
            self.botones_personajes[nombre].config(bg="white")
        elif len(self.seleccionados) < 3:

            #Si no estaba y hay espacio, lo agrega y lo resalta en amarillo
            self.seleccionados.append(nombre)
            self.botones_personajes[nombre].config(bg=COLOR_SELECCION)

    #Muestra una ventana emergente con la portada
    def _mostrar_about(self):
        messagebox.showinfo(
            "Información:",
            "Disney's Epic Adventure\n\n"
            "Proyecto 1 — CE1101 Introducción a la Programación\n"
            "Tecnológico de Costa Rica\n\n"
            "Estudiante: Angélica Obregón Arguedas\n"
            "Profesor: Santiago Gamboa Ramírez\n"
            "I Semestre 2026")

    #Al presionar iniciar se debe ejecutar
    def _iniciar(self):
        nombre = self.nombre_var.get().strip()  #.strip() se usa para eliminar espacios al inicio y final

        #RESTRICCIONES
        if nombre == "":
            messagebox.showwarning("¡Espera!", "Por favor ingresa tu nombre.")
            return
        if len(self.seleccionados) < 3:
            messagebox.showwarning("¡Espera!", "Debes seleccionar exactamente 3 personajes.")
            return
        equipo = self._obtener_equipo(self.personajes_disponibles, 0, [])
        self.callback_iniciar(nombre, self.avatar_var.get(), equipo)


    #Se filtra la lista completa de personajes para que queden solo con los seleccionados
    def _obtener_equipo(self, personajes, indice, resultado):
        if indice == len(personajes): #Caso Base
            return resultado
        p = personajes[indice]

        #Si el personaje fue seleccionado, lo agrega al equipo
        if p.nombre in self.seleccionados:
            resultado.append(p)
        return self._obtener_equipo(personajes, indice + 1, resultado)


#Crear la ventana y arrancar Tkinter, se utiliza mainloop() para mantener la ventana abierta esperando que el usuario responda
if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaInicial(root)
    root.mainloop()
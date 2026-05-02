import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from batalla import ciclo_turno, ejecutar_turno
from utils import Entrenador

class PantallaBatalla:
    def __init__(self, root, jugador, hollow, nombre_hollow, callback_victoria):
        #Se define root como ventana principal, juegador como el entrenador del usuario, hollow como entrnador del hollow, nombre del hollow para cargar el fondo de cada pantalla y el callback para cuando el jugador gana.
        self.root = root
        self.jugador = jugador
        self.hollow = hollow
        self.nombre_hollow = nombre_hollow
        self.callback_victoria = callback_victoria

        #Se crea lo siguiente para guardar imágenes en la memoria
        self.imagenes = {}
        self.fondo_imagen = None

        self._construir_batalla()
    def _construir_batalla(self):
        #Se utiliza canvas como una widget especial que permite poner imagen de fondo
        self.canvas = tk.Canvas(self.root, width=800, height=650)
        self.canvas.pack(fill="both", expand=True)

        #Con este, se podrá cargar la imagen de fondo según el Hollow
        ruta_fondo = os.path.join("imágenes", "mapa", f"Batalla {self.nombre_hollow}.JPG")
        try:
            img_fondo = Image.open(ruta_fondo).resize((800, 650))
            self.fondo_imagen = ImageTk.PhotoImage(img_fondo)
            self.canvas.create_image(0, 0, anchor="nw", image=self.fondo_imagen)
        except:
            self.canvas.configure(bg="#1a1a2e")

        #Frame para los puntajes
        frame_puntajes = tk.Frame(self.canvas, bg="#000000")
        self.canvas.create_window(400, 30, window=frame_puntajes)
        tk.Label(frame_puntajes, text=f"{self.jugador.nombre}: {self.jugador.puntaje} pts", font=("Georgia", 12, "bold"), bg="black", fg="#FFE66D").pack(side="left", padx=20)
        tk.Label(frame_puntajes,text=f"{self.hollow.nombre}: {self.hollow.puntaje} pts", font=("Georgia", 12, "bold"), bg="black", fg="#FF6B6B").pack(side="left", padx=20)

        #Frame del jugador a la izquierda
        frame_jugador = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(150, 250, window=frame_jugador)

        #Cargar imagen del personaje activo del jugador
        self._cargar_imagen_personaje(frame_jugador, self.jugador.activo.nombre, "jugador")

        #Nombre y HP del personaje del jugador
        self.label_nombre_jugador = tk.Label(frame_jugador, text=self.jugador.activo.nombre, font=("Georgia", 12, "bold"), bg="black", fg="white")
        self.label_nombre_jugador.pack()
        self.label_hp_jugador = tk.Label(frame_jugador, text=f"HP: {self.jugador.activo.vida_actual}/{self.jugador.activo.vida_max}", font=("Georgia", 11), bg="black", fg="#4ECDC4")
        self.label_hp_jugador.pack()

        #Frame del Hollow a la derecha
        frame_hollow = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(650, 250, window=frame_hollow)
        self._cargar_imagen_personaje(frame_hollow, self.hollow.activo.nombre, "hollow")

        #Nombre y HP del hollow
        self.label_nombre_hollow = tk.Label(frame_hollow, text=self.hollow.activo.nombre, font=("Georgia", 12, "bold"), bg="black", fg="white")
        self.label_nombre_hollow.pack()
        self.label_hp_hollow = tk.Label(frame_hollow, text=f"HP: {self.hollow.activo.vida_actual}/{self.hollow.activo.vida_max}", font=("Georgia", 11), bg="black", fg="#FF6B6B")
        self.label_hp_hollow.pack()

        #Mostrar lo que va pasando en la batalla
        frame_log = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(400, 450, window=frame_log)
        self.log = tk.Text(frame_log, width=60, height=5, font=("Georgia", 9), bg="#000000", fg="white", state="disabled", relief="flat")
        self.log.pack()

        #Frame de botones para acciones
        frame_acciones = tk.Frame(self.canvas, bg="black")
        self.canvas.create_window(400, 580, window=frame_acciones)
        tk.Button(frame_acciones, text="ATACAR", font=("Georgia", 12, "bold"), bg="#FF6B6B", fg="white", relief="flat", padx=15, pady=8, cursor="hand2", activebackground="#FF6B6B", activeforeground="white", command=self._atacar).pack(side="left", padx=10)
        tk.Button(frame_acciones, text="CAMBIAR", font=("Georgia", 12, "bold"), bg="#4ECDC4", fg="white", relief="flat", padx=15, pady=8, cursor="hand2", activebackground="#4ECDC4", activeforeground="white",command=self._mostrar_cambio).pack(side="left", padx=10)

    #Cargar la imagen del personaje activo
    def _cargar_imagen_personaje(self, frame, nombre, lado):
        ruta = os.path.join("imágenes", "personajes", f"{nombre}.png")
        try:
            img = Image.open(ruta).resize((100, 100))
            foto = ImageTk.PhotoImage(img)
            self.imagenes[f"{lado}_{nombre}"] = foto
            tk.Label(frame, image=foto, bg="black").pack(pady=5)
        except:
            tk.Label(frame, text="?", font=("Georgia", 40), bg="black").pack(pady=5)

    #Se agrega texto al log de la batalla, primero se habilita la escritura, después se agrega texto, pero hasta el final, luego baja al último estado que se agrega y vuelve a solo lectura
    def _log(self, texto):
        self.log.config(state="normal")      
        self.log.insert("end", texto + "\n") 
        self.log.see("end")                  
        self.log.config(state="disabled")    

    #Actualizar los labels de HP y nombre en pantalla
    def _actualizar_pantalla(self):
        self.label_nombre_jugador.config(text=self.jugador.activo.nombre)
        self.label_hp_jugador.config(text=f"HP: {self.jugador.activo.vida_actual}/{self.jugador.activo.vida_max}")
        self.label_nombre_hollow.config(text=self.hollow.activo.nombre)
        self.label_hp_hollow.config(
            text=f"HP: {self.hollow.activo.vida_actual}/{self.hollow.activo.vida_max}")

    #Si el jugador decide atacar
    def _atacar(self):
        #Turno del jugador
        dmg = self.jugador.activo.ataque
        dmg_real = self.hollow.activo.recibir_dmg(dmg)
        self._log(f"{self.jugador.activo.nombre} atacó a {self.hollow.activo.nombre} causando {dmg_real} de daño")

        #Verificar si el hollow cayó en KO
        if self.hollow.activo.ko:
            self._log(f"¡{self.hollow.activo.nombre} fue derrotado!")
            personaje_caido = self.hollow.activo
            self.jugador.ganar_personaje(personaje_caido)
            personaje_caido.ko = True
            siguiente = self.hollow.siguiente_vivo()
            if siguiente is not None:
                self.hollow.cambiar_activo(siguiente)
                self._log(f"{self.hollow.nombre} envió a {self.hollow.activo.nombre}")
        self._actualizar_pantalla()

        #Verificar si el hollow perdió todos sus personajes
        if not self.hollow.tener_vivos():
            self._fin_batalla(gano_jugador=True)
            return

        #Turno del Hollow
        self.root.after(800, self._turno_hollow)  #espera 800ms antes del turno del hollow
    #El Hollow actúa en su turno
    def _turno_hollow(self):
        import random
        decision = random.choice(["atacar", "cambiar"])

        if decision == "cambiar":
            siguiente = self.hollow.siguiente_vivo()
            if siguiente is not None:
                self.hollow.cambiar_activo(siguiente)
                self._log(f"{self.hollow.nombre} cambió a {self.hollow.activo.nombre}")
        else:
            dmg = self.hollow.activo.ataque
            dmg_real = self.jugador.activo.recibir_dmg(dmg)
            self._log(f"{self.hollow.activo.nombre} atacó a {self.jugador.activo.nombre} causando {dmg_real} de daño")

            if self.jugador.activo.ko:
                self._log(f"¡{self.jugador.activo.nombre} fue derrotado!")
                personaje_caido = self.jugador.activo
                self.hollow.ganar_personaje(personaje_caido)
                personaje_caido.ko = True
                siguiente = self.jugador.siguiente_vivo()
                if siguiente is not None:
                    self.jugador.cambiar_activo(siguiente)
                    self._log(f"Enviaste a {self.jugador.activo.nombre}")
        self._actualizar_pantalla()

        #Verificar si el jugador perdió todos sus personajes
        if not self.jugador.tener_vivos():
            self._fin_batalla(gano_jugador=False)

    #Muestra ventana para cambiar de personaje
    def _mostrar_cambio(self):
        #Crear ventana emergente
        ventana = tk.Toplevel(self.root)
        ventana.title("Cambia tu personaje")
        ventana.geometry("300x400")
        ventana.configure(bg="#1a1a2e")
        ventana.resizable(False, False)
        tk.Label(ventana, text="Elige un personaje:", font=("Georgia", 13, "bold"), bg="#1a1a2e", fg="white").pack(pady=15)

        # Mostrar personajes disponibles
        self._construir_opciones_cambio(ventana, self.jugador.personajes, 0)

    #Construir los botones de cambio
    def _construir_opciones_cambio(self, ventana, personajes, indice):
        if indice == len(personajes):
            return
        p = personajes[indice]

        #No mostrar el personaje activo ni los que están en KO
        if p != self.jugador.activo and not p.ko:
            estado = f"HP: {p.vida_actual}/{p.vida_max}"
            tk.Button(ventana,text=f"{p.nombre} — {estado}", font=("Georgia", 11),bg="#4ECDC4", fg="white",relief="flat", padx=10, pady=5,cursor="hand2",command=lambda nombre=p.nombre: self._cambiar_personaje(nombre, ventana)).pack(pady=5)

        self._construir_opciones_cambio(ventana, personajes, indice + 1)
    #Cambiar el personaje activo del jugador
    def _cambiar_personaje(self, nombre, ventana):
        #Buscar el personaje por su nombre
        nuevo = self._buscar_personaje(self.jugador.personajes, nombre, 0)
        if nuevo:
            self.jugador.cambiar_activo(nuevo)
            self._log(f"Cambiaste a {nuevo.nombre}")
            self._actualizar_pantalla()
        ventana.destroy()  #Cierra la ventana emergente

    #Busca un personaje en la lista
    def _buscar_personaje(self, personajes, nombre, indice):
        if indice == len(personajes):
            return None
        if personajes[indice].nombre == nombre:
            return personajes[indice]
        return self._buscar_personaje(personajes, nombre, indice + 1)

    #Fin de la batalla
    def _fin_batalla(self, gano_jugador):
        if gano_jugador:
            self._log(f"\n¡{self.jugador.nombre} venció a {self.hollow.nombre}!")
            messagebox.showinfo("¡Victoria!", f"¡Derrotaste a {self.hollow.nombre}!")
            self.callback_victoria(self.nombre_hollow)  #Para avisar al mapa
        else:
            self._log(f"\n¡{self.hollow.nombre} ganó la batalla!")
            messagebox.showinfo("Derrota", f"{self.hollow.nombre} te derrotó...")
            self.callback_victoria(None)  # None indica derrota


# Prueba
if __name__ == "__main__":
    from personaje_clase import Personaje

    p1 = Personaje("Coraje", 95, 22, 12)
    p2 = Personaje("Bob", 140, 12, 20)
    p3 = Personaje("Phineas", 110, 18, 15)

    h1 = Personaje("Raven", 115, 18, 14)
    h2 = Personaje("Starfire", 100, 29, 9)
    h3 = Personaje("Tom", 110, 17, 14)

    jugador = Entrenador("Angélica", [p1, p2, p3])
    hollow  = Entrenador("Jack", [h1, h2, h3], es_hollow=True)

    root = tk.Tk()
    root.geometry("800x650")
    app = PantallaBatalla(root, jugador, hollow, "Jack", lambda n: print(f"Batalla terminada: {n}"))
    root.mainloop()
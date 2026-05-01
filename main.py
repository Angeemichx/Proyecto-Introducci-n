#se usa para arrancar todo el juego, conecta todas las pantallas entre ellas
import tkinter as tk
from interfaz import PantallaInicial

def main():
    root = tk.Tk()
    app = PantallaInicial(root)
    root.mainloop()

if __name__ == "__main__":
    main()
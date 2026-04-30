#Se crea la función para los personajes, su vida, ataque y defensa
#Abrir archivo de texto:

def leer_personajes(nombre_archivo="personajes.txt", archivo=None, lista_personajes=None):
    # Inicialización: primera llamada
    if archivo is None:
        archivo = open(nombre_archivo, "r", encoding="utf-8")
    if lista_personajes is None:
        lista_personajes = []

    # Leer una línea
    linea = archivo.readline()

    # Caso base: no hay más líneas
    if linea == "":
        archivo.close()
        return lista_personajes

    # Ignorar líneas vacías o solo espacios
    if linea.strip() == "":
        return leer_personajes(nombre_archivo, archivo, lista_personajes)

    # Procesar la línea
    partes = linea.strip().split(',')
    lista_personajes.append({
        'nombre':   partes[0],
        'vida':     int(partes[1]),
        'ataque':   int(partes[2]),
        'defensa':  int(partes[3])
    })

    # Llamada con el archivo ya abierto
    return leer_personajes(nombre_archivo, archivo, lista_personajes)

#Función para mostrar los personajes
def imprimir_personajes(lista, indice):
    if indice == len(lista):
        return
    p = lista[indice]
    print(f"{p['nombre']} - HP:{p['vida']} ATK:{p['ataque']} DEF:{p['defensa']}")
    imprimir_personajes(lista, indice + 1)

# Leer personajes
if __name__ == "__main__":
    personajes = leer_personajes("personajes.txt")
    imprimir_personajes(personajes, 0)
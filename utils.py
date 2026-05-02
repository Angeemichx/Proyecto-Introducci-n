from personaje_clase import Personaje

class Entrenador:
    #Función para crear un entrenador con la lista de personajes que le pertenecen, el primer personaje con el que inicia y los puntos al adueñarse de otro
    def __init__(self, nombre, personajes, es_hollow=False):
        self.nombre = nombre
        self.personajes = personajes
        self.activo = personajes[0]
        self.puntaje = 0
        self.es_hollow = es_hollow

    #Verifica si el entrenador aún tiene personajes vivos recorriendo la lista, si algún personaje sigue con vida devuelve True y si no False(caso base)
    def tener_vivos(self, lista=None, indice=0):
        if lista is None:
            lista = self.personajes

        if indice == len(lista): 
            return False 
        
        if not lista [indice].ko:
            return True
        
        return self.tener_vivos(lista, indice + 1)
    
    #Se llama al siguiente personaje vivo, se busca en orden uno que no esté en ko y que tampoco sea el personaje que está activo. Si no se encuentra ningún personaje disponible sería el caso base.
    def siguiente_vivo(self, lista=None, indice=0):
        if lista is None:
            lista = self.personajes 
    
        if indice == len(lista):
            return None
        
        if not lista[indice].ko and lista[indice] != self.activo:
            return lista[indice]
        return self.siguiente_vivo(lista, indice +1)
    
    #Verifica que el nuevo personaje que se quiere utilizar no esté en ko, de verificarse cambia el personaje activo por el nuevo para que el entrenador pueda seguir en la batalla.
    def cambiar_activo(self, nuevo_personaje):
        if not nuevo_personaje.ko:
            self.activo = nuevo_personaje
            return True
        return False
    
    #Para ganar personajes, se restaura la vida tras la pelea, además se agrega el personaje a la lista de personajes del ganador y le suma puntaje. 
    def ganar_personaje(self, personaje):
        personaje.restaurar()
        self.personajes.append(personaje)
        self.puntaje += 1

    def __str__(self):
        return f"{self.nombre} / Puntaje: {self.puntaje} / Personaje activo: {self.activo.nombre}"
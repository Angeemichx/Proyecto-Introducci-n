import random
from personaje_clase import Personaje
from utils import Entrenador 

#Esta función ejecuta un turno de ataque donde el personaje va a golpear al defensor. Además, se verifica si el defensor cayó en ko.
def ejecutar_turno(atacante, defensor):
    #el atancante golpea al defensor y se obtiene el daño real que le causó
    dmg = atacante.activo.ataque 
    dmg_real = defensor.activo.recibir_dmg(dmg)

    print(f"{atacante.activo.nombre} atacó con {dmg}")
    print(f"Daño real: {dmg_real}")
    print(f"Vida restante de {defensor.activo.nombre}: {defensor.activo.vida_actual}")
    print(f"KO: {defensor.activo.ko}")

    #si el defensor cae en ko, el atacante se va a ganar al personaje que muere
    if defensor.activo.ko:
        print (f"{defensor.activo.nombre} fue derrotado!!")
        personaje_caido = defensor.activo
        atacante.ganar_personaje(personaje_caido)
        personaje_caido.ko = True

    #Si aún quedan personajes vivos, el defensor cambia al siguiente que tenga 
        siguiente = defensor.siguiente_vivo()
        if siguiente is not None:
            defensor.cambiar_activo(siguiente)

#En esta función los turnos se van alternando entre el jugador y el hollow, esto hasta que cualquier personaje activo caiga en ko.
def ciclo_turno(jugador, hollow, turno_jugador=True):
    if not jugador.tener_vivos() or not hollow.tener_vivos():
        return
    if jugador.activo.ko or hollow.activo.ko:
        return
    
    if turno_jugador:
        ejecutar_turno(jugador, hollow)
    # el hollow debe decidir de forma aleatoria si ataca o cambia de personaje, para ello se utiliza la biblioteca random:
    else:
        decision = random.choice(["atacar", "cambiar"])
        #si decide atacar, llama a la funcion siguiente_vivo para comprobar si tiene otro personaje, si no lo tiene, ataca con el unico que le queda. Si decide cambiar se llama a la función cambiar_activo y pone el siguiente personaje vivo.
        if decision == "atacar":
            siguiente = hollow.siguiente_vivo()
            if siguiente is not None:
                hollow.cambiar_activo(siguiente)
        else:
            ejecutar_turno(hollow, jugador)
    if jugador.activo.ko or hollow.activo.ko:
        return
    ciclo_turno(jugador, hollow, not turno_jugador)

#Acá se verifica si cualquier entrenador tiene personajes vivos y llama a ciclo_turno para que siga la batalla, si no los tiene vivos debe ganar el otro entrenador y muestra el resultado.
def batalla(jugador, hollow):
    if not jugador.tener_vivos():
        print (f"\n{hollow.nombre} ganó la batalla!!")
        return
    if not hollow.tener_vivos():
        print (f"\n{jugador.nombre} ganó la batalla!!")
        return
    print (f"\n---{jugador.activo.nombre} vs {hollow.activo.nombre}---")

    ciclo_turno(jugador, hollow)
    batalla(jugador, hollow)

#prueba de que funciona:
if __name__ == "__main__":
    p1 = Personaje("Coraje", 95, 22, 12)
    p2 = Personaje("Bob", 140, 12, 20)
    h1 = Personaje("Raven", 115, 18, 14)
    h2 = Personaje("Starfire", 100, 29, 9)

    jugador = Entrenador("Angélica", [p1, p2])
    hollow  = Entrenador("Hollow 1", [h1, h2], es_hollow=True)

    batalla(jugador, hollow)
    print(f"\nPuntaje - {jugador.nombre}: {jugador.puntaje} | {hollow.nombre}: {hollow.puntaje}")
    
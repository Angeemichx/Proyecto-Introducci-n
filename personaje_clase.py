class Personaje:
    #Se usa init como un constructor que al asignar valores a los atributos se ejecuta automáticamente al crear un personaje
    #Self es utilizado para referirse a la instancia actual del objeto, permite acceder a sus atributos particulares
    #En esta función se guardará el nombre, la vida original, la vida actual que baja en la batalla, los puntos de ataque, defensa y que el personaje esté vivo, todo esto, guardado en el objeto
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida_max = vida
        self.vida_actual = vida
        self.ataque = ataque
        self.defensa = defensa
        self.ko = False

#dmg es el ataque al recibir un golpe del enemigo, se resta la defensa del personaje al daño que recibe. En el caso de que el daño real sea 0 o menor a 1, se asigna que se le baje al menos 1 punto de vida.
    def recibir_dmg(self, dmg):
        dmg_real = dmg - self.defensa
        if dmg_real < 1:
            dmg_real = 1
        #A la vida actual debe restarse el daño que recibe
        self.vida_actual = self.vida_actual - dmg_real
        #Si la vida llega a 0 o menos, el personaje pasa a estar KO
        if self.vida_actual <= 0:
            self.vida_actual = 0
            self.ko = True
        return dmg_real
    
#Cuando el personaje cambie de dueño en el juego, se le restaurará su vida orginal
    def restaurar(self):
        self.vida_actual = self.vida_max
        self.ko = False #Falso porque ya no estará en KO

#El metodo __str__ se utiliza para definir la presentación para el usuario final, de esta manera se dirige a lo que esperamos ver y no a la dirección de memoria del objeto.
    def __str__(self):
        return f"{self.nombre} - HP:{self.vida_actual}/{self.vida_max} ATK:{self.ataque} DEF:{self.defensa} - {'KO' if self.ko else 'VIVO'}"
    
#prueba de funcionamiento:
if __name__ == "__main__":
    p1 = Personaje("Coraje", 95, 22, 12)
    print(p1)
    dmg_recibido = p1.recibir_dmg(30)
    print(f"Daño recibido: {dmg_recibido}")
    print(p1)
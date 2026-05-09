import pygame
import constantes

class Weapon():
    def __init__(self, image):
        self.image_original = image
        self.angulo = 0
        self.image = self.image_original
        self.forma = self.image.get_rect()
        
        # --- Variables de estado de ataque ---
        self.atacando = False
        self.angulo_ataque = 0
        self.ultimo_ataque = pygame.time.get_ticks()
        self.cooldown = 350  # Milisegundos entre cada golpe

    def update(self, personaje):
        # 1. Mantener el arma vinculada a la posición del personaje
        self.forma.center = personaje.forma.center

        # 2. Lógica de la animación de ataque
        if self.atacando:
            self.angulo_ataque += 25  
            if self.angulo_ataque >= 100:
                self.atacando = False
                self.angulo_ataque = 0
        
        # 3. Orientación y posición según hacia donde mire el personaje
        offset_mano = 18 

        if personaje.flip == False:
            self.forma.x += offset_mano
            angulo_final = self.angulo - self.angulo_ataque
            self.rotar_palo(False, angulo_final)
        else:
            self.forma.x -= offset_mano
            angulo_final = self.angulo + self.angulo_ataque
            self.rotar_palo(True, angulo_final)

    def rotar_palo(self, rotar, angulo):
        if rotar:
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
        else:
            imagen_flip = self.image_original
        
        self.image = pygame.transform.rotate(imagen_flip, angulo)
        
        centro_actual = self.forma.center
        self.forma = self.image.get_rect()
        self.forma.center = centro_actual

    def atacar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_ataque > self.cooldown:
            self.atacando = True
            self.ultimo_ataque = ahora

    # --- CORREGIDO: Ahora está dentro de la clase ---
    def dibujar(self, interfaz, scroll): 
        # 1. Calculamos la posición visual restando el scroll
        pos_x = self.forma.x - scroll[0]
        pos_y = self.forma.y - scroll[1]

        # 2. Dibujamos el arma en la posición corregida por la cámara
        interfaz.blit(self.image, (pos_x, pos_y))



''' import pygame
import weapon
import constantes
import personaje

class Weapon():
    def __init__(self, image):
        self.image_original = image
        self.angulo = 0
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.forma = self.image.get_rect()
        
    

    def atacar(self):
        if self.atacando == False:
           self.atacando = True
           self.tiempo_ataque = pygame.time.get_ticks()

    def update(self, personaje):
        self.forma.center = personaje.forma.center

    # POSICIÓN DEL PALO
        if personaje.flip == False:
           self.forma.x = self.forma.x + personaje.forma.width/2
           lado = False
        else:
           self.forma.x = self.forma.x - personaje.forma.width/2
           lado = True

    def update(self, personaje):
        self.forma.center = personaje.forma.center

        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width/2
            self.rotar_palo(False)

        if personaje.flip == True:
            self.forma.x = self.forma.x - personaje.forma.width/2
            self.rotar_palo(True)
        
    def rotar_palo(self,rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.image_original,True, False)
            self.image = pygame.transform.rotate(imagen_flip, self.angulo)

        else:
            imagen_flip = pygame.transform.flip(self.image_original, False, False)
            self.image = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.forma)
        #pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.forma, 1)

   ''' 
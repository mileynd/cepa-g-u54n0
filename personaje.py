import pygame
import constantes

class Personaje():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0

        self.image = animaciones[self.frame_index]

        self.update_time = pygame.time.get_ticks()
        self.vida = 100
        self.vivo = True
        
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)

    def movimiento(self, delta_x, delta_y, obstaculos):
        # 1. Movimiento en X y comprobación
        self.forma.x += delta_x
        for objeto in obstaculos:
            if self.forma.colliderect(objeto.forma):
                if delta_x > 0: # Choca moviéndose a la derecha
                    self.forma.right = objeto.forma.left
                if delta_x < 0: # Choca moviéndose a la izquierda
                    self.forma.left = objeto.forma.right

        # 2. Movimiento en Y y comprobación
        self.forma.y += delta_y
        for objeto in obstaculos:
            if self.forma.colliderect(objeto.forma):
                if delta_y > 0: # Choca moviéndose abajo
                    self.forma.bottom = objeto.forma.top
                if delta_y < 0: # Choca moviéndose arriba
                    self.forma.top = objeto.forma.bottom

        # Orientación (flip)
        if delta_x < 0: 
            self.flip = True
        if delta_x > 0: 
            self.flip = False
    
    def update(self):
        # Evitar que la vida baje de 0
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar(self, interfaz, scroll):
        if self.vivo:
            # 1. Calculamos la posición visual restando el scroll
            # Esto hace que Mikel se dibuje relativo a la cámara
            pos_x = self.forma.x - scroll[0]
            pos_y = self.forma.y - scroll[1]

            # 2. Creamos la imagen con el flip
            imagen_final = pygame.transform.flip(self.image, self.flip, False)
            
            # 3. Dibujamos en la posición corregida por la cámara
            interfaz.blit(imagen_final, (pos_x, pos_y))
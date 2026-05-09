import pygame
import math
import constantes

class Enemigo:
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones
        self.frame_index = 0
        self.image = self.animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.vida = 100
        self.vivo = True
        self.update_time = pygame.time.get_ticks()
        
        # Rango de detección: a esta distancia el zombi empieza a seguir a Mikel
        self.radio_deteccion = 400 

    def movimiento(self, jugador, obstaculos):
        if self.vivo:
            # 1. Calcular distancia hacia el jugador
            dist_x = jugador.forma.centerx - self.forma.centerx
            dist_y = jugador.forma.centery - self.forma.centery
            distancia = math.hypot(dist_x, dist_y)

            # 2. Solo seguir si el jugador está dentro del rango
            if distancia < self.radio_deteccion:
                dx = 0
                dy = 0
                
                if dist_x > 0: dx = 2
                if dist_x < 0: dx = -2
                if dist_y > 0: dy = 2
                if dist_y < 0: dy = -2

                # Mover en X y comprobar colisiones
                self.forma.x += dx
                for obs in obstaculos:
                    if self.forma.colliderect(obs.forma):
                        self.forma.x -= dx
                
                # Mover en Y y comprobar colisiones
                self.forma.y += dy
                for obs in obstaculos:
                    if self.forma.colliderect(obs.forma):
                        self.forma.y -= dy

    def update(self):
        if self.vivo:
            # Si su vida llega a 0, muere
            if self.vida <= 0:
                self.vivo = False
                
            # Control de la animación del zombi
            cooldown_animacion = 150 # milisegundos entre cada frame
            if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.animaciones):
                    self.frame_index = 0
                self.image = self.animaciones[self.frame_index]

    def dibujar(self, interfaz, scroll):
        if self.vivo:
            interfaz.blit(self.image, (self.forma.x - scroll[0], self.forma.y - scroll[1]))

    def dibujar_barra_vida(self, interfaz, scroll):
        if self.vivo:
            # Dibuja la barra de vida justo encima de su cabeza
            x_barra = self.forma.x - scroll[0]
            y_barra = self.forma.y - scroll[1] - 10
            
            # Fondo rojo (vida perdida)
            pygame.draw.rect(interfaz, (255, 0, 0), (x_barra, y_barra, self.forma.width, 5))
            
            # Relleno verde (vida actual)
            ancho_verde = max(0, int(self.forma.width * (self.vida / 100)))
            if ancho_verde > 0:
                pygame.draw.rect(interfaz, (0, 255, 0), (x_barra, y_barra, ancho_verde, 5))
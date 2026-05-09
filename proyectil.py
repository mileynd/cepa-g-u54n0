import pygame
import math

class Proyectil:
    def __init__(self, x, y, x_objetivo, y_objetivo, imagen):
        self.imagen = imagen
        self.forma = self.imagen.get_rect()
        self.forma.center = (x, y)
        
        # Guardamos la posición exacta como números decimales (flotantes)
        self.pos_x = float(x)
        self.pos_y = float(y)
        
        # 1. Calcular la diferencia exacta de distancia
        v_x = float(x_objetivo - x)
        v_y = float(y_objetivo - y)
        distancia = math.hypot(v_x, v_y)
        
        # Prevenir división entre cero
        if distancia == 0:
            distancia = 1
            
        # 2. Definir la velocidad exacta multiplicando el vector unitario
        # Aumentamos la velocidad a 15 para que sea más rápida y recta
        self.dx = (v_x / distancia) * 15  
        self.dy = (v_y / distancia) * 15
        
        # 3. Daño que causa al impactar (GDD)
        self.daño = 15  

    def update(self, lista_obstaculos):
        # Mover la posición exacta usando decimales
        self.pos_x += self.dx
        self.pos_y += self.dy
        
        # Actualizar la hitbox del rectángulo con la posición exacta
        self.forma.x = int(self.pos_x)
        self.forma.y = int(self.pos_y)

        # Si la piedra choca contra una pared u obstáculo, se destruye
        for obs in lista_obstaculos:
            if self.forma.colliderect(obs.forma):
                return True  
        return False

    def dibujar(self, interfaz, scroll):
        # Dibujar la piedra en pantalla aplicando la cámara
        interfaz.blit(self.imagen, (self.forma.x - scroll[0], self.forma.y - scroll[1]))
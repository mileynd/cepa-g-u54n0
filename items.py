import pygame

class Item:
    def __init__(self, x, y, animaciones, tipo="cuchara"):
        self.tipo = tipo
        self.animaciones = animaciones
        self.frame_index = 0
        self.imagen = self.animaciones[self.frame_index]
        self.forma = self.imagen.get_rect()
        self.forma.topleft = (x, y)
        
        # Variables para controlar la velocidad de la animación
        self.update_time = pygame.time.get_ticks()

    def update(self):
        # Tiempo en milisegundos entre cada frame (ej. 150ms para que no vaya tan rápido)
        cooldown_animacion = 150
        
        # Actualizar imagen según el frame actual
        self.imagen = self.animaciones[self.frame_index]
        
        # Controlar el tiempo para pasar al siguiente frame
        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        # Si llega al final de las imágenes, reinicia el ciclo
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar(self, interfaz, scroll):
        # Dibujamos la imagen actual aplicando el movimiento de la cámara
        interfaz.blit(self.imagen, (self.forma.x - scroll[0], self.forma.y - scroll[1]))
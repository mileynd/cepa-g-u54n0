import pygame

class Sobreviviente:
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones  # Lista con los 3 frames cargados
        self.frame_index = 0
        self.image = self.animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.update_time = pygame.time.get_ticks()

    def update(self):
        # Tiempo de espera entre frames (200 milisegundos)
        cooldown_animacion = 200
        
        # Cambiamos de frame según el tiempo transcurrido
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        # Si llegamos al final de la animación, volvemos al inicio
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
            
        self.image = self.animaciones[self.frame_index]

    def dibujar(self, ventana, scroll):
        # Ajustamos la posición según el scroll de la cámara
        pos_x = self.forma.x - scroll[0]
        pos_y = self.forma.y - scroll[1]
        
        ventana.blit(self.image, (pos_x, pos_y))
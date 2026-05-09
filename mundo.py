import pygame

class Obstaculo:
    def __init__(self, x, y, ancho, alto):
        # 1. Creamos el rectángulo que define el área física del obstáculo
        self.forma = pygame.Rect(x, y, ancho, alto)

    def dibujar(self, ventana, scroll):
        # Para que el obstáculo se mueva junto con la cámara (scroll)
        pos_x = self.forma.x - scroll[0]
        pos_y = self.forma.y - scroll[1]

        # Creamos un rectángulo temporal ajustado a la cámara para dibujarlo
        rect_dibujo = pygame.Rect(pos_x, pos_y, self.forma.width, self.forma.height)

        # Dibujamos el obstáculo (por ahora como un bloque gris para probar)
        pygame.draw.rect(ventana, (128, 128, 128), rect_dibujo)
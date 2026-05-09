import pygame

class Puerta:
    def __init__(self, x, y, ancho, alto):
        self.forma = pygame.Rect(x, y, ancho, alto)
        self.abierta = False

    def dibujar(self, interfaz, scroll):
        # Si está cerrada es de un color (ej. rojo), si se abre cambia a verde
        color = (0, 255, 0) if self.abierta else (139, 0, 0)
        
        # Rectángulo con el scroll de la cámara aplicado
        rect_dibujado = pygame.Rect(self.forma.x - scroll[0], self.forma.y - scroll[1], self.forma.width, self.forma.height)
        pygame.draw.rect(interfaz, color, rect_dibujado)
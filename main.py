import pygame
import sys

# --- CONFIGURACIÓN GENERAL ---
ANCHO, ALTO = 800, 600
FPS = 60
TAMANO_TILE = 40  # Cada cuadro del mapa mide 40x40 píxeles

# Colores (según tu GDD)
AZUL_SANMARQUINO = (0, 48, 87)
GRIS_PASILLO = (120, 120, 120)
CAFE_CARPETA = (101, 67, 33)   # Color madera para las carpetas
MARRON_BORDE = (60, 40, 20)    # Borde para dar profundidad
BLANCO = (255, 255, 255)
VERDE_CEPA = (57, 255, 20)

# --- DISEÑO DEL MAPA (MATRIZ) ---
# 0 = Suelo libre por donde Mikel camina
# 1 = Carpeta amontonada (Obstáculo con colisión)
# Puedes modificar los 1 y 0 para cambiar el diseño del salón
MAPA_NIVEL_1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1],
]

class Mikel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(AZUL_SANMARQUINO)
        # Posición inicial: pasillo de la izquierda
        self.rect = self.image.get_rect(topleft=(50, 50))
        self.velocidad = 5

    def update(self, obstaculos):
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        # Movimiento en 8 direcciones
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]: dx = -self.velocidad
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: dx = self.velocidad
        if teclas[pygame.K_w] or teclas[pygame.K_UP]: dy = -self.velocidad
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]: dy = self.velocidad

        # --- Sistema de Colisiones ---
        # Primero movemos en X y revisamos si chocamos
        self.rect.x += dx
        if pygame.sprite.spritecollide(self, obstaculos, False):
            self.rect.x -= dx # Si chocó, deshacemos el movimiento
        
        # Luego movemos en Y y revisamos
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, obstaculos, False):
            self.rect.y -= dy

        # Impedir que Mikel se salga de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

class Carpeta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAMANO_TILE, TAMANO_TILE))
        self.image.fill(CAFE_CARPETA)
        pygame.draw.rect(self.image, MARRON_BORDE, [0, 0, TAMANO_TILE, TAMANO_TILE], 3)
        self.rect = self.image.get_rect(topleft=(x, y))

def jugar():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Cepa G-U54N0: El Último Sanmarquino - Diseño de Nivel")
    reloj = pygame.time.Clock()

    todos_los_sprites = pygame.sprite.Group()
    grupo_carpetas = pygame.sprite.Group()

    # --- Construcción del Escenario ---
    for fila_idx, fila in enumerate(MAPA_NIVEL_1):
        for col_idx, valor in enumerate(fila):
            pos_x = col_idx * TAMANO_TILE
            pos_y = fila_idx * TAMANO_TILE
            if valor == 1:
                obj = Carpeta(pos_x, pos_y)
                grupo_carpetas.add(obj)
                todos_los_sprites.add(obj)

    mikel = Mikel()
    todos_los_sprites.add(mikel)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Lógica
        mikel.update(grupo_carpetas)

        # Dibujo
        pantalla.fill(GRIS_PASILLO)
        todos_los_sprites.draw(pantalla)
        
        # Interfaz básica
        fuente = pygame.font.SysFont("Verdana", 18)
        info = fuente.render("Fase 2: Rescata a los sobrevivientes en Matemáticas", True, BLANCO)
        pantalla.blit(info, (20, ALTO - 35))

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    jugar()

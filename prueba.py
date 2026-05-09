import pygame
import random

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cepa G-U54N0: El Último Sanmarquino")

# Cargar imagen de la Facultad (debe estar en la misma carpeta)
# Nota: Convierte tu foto a .png o .jpg primero
try:
    fondo = pygame.image.load("facultad_pixel.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
except:
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((50, 50, 50)) # Color de respaldo si no carga

# Colores
BLANCO = (255, 255, 255)
VERDE_CEPA = (57, 255, 20) # Verde radioactivo [cite: 161]

# Fuente para el título
fuente = pygame.font.SysFont("monospace", 40, bold=True)

reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # --- LÓGICA DE ANIMACIÓN (Efecto de Niebla/Corte de Luz) ---
    # Simulamos que la luz falla aleatoriamente [cite: 80]
    probabilidad_parpadeo = random.random()
    
    if probabilidad_parpadeo > 0.98: # 2% de probabilidad de oscurecerse
        pantalla.fill((0, 0, 0)) 
    else:
        pantalla.blit(fondo, (0, 0))

    # --- TEXTO DE PORTADA ---
    titulo = fuente.render("CEPA G-U54N0", True, VERDE_CEPA)
    subtitulo = fuente.render("PRESIONA ESPACIO PARA RESCATAR", True, BLANCO)
    
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
    # Efecto de parpadeo suave para el subtítulo
    if pygame.time.get_ticks() % 1000 < 500:
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, ALTO - 100))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
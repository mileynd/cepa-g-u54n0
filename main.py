import pygame
import constantes
import random
import math
import pytmx

from personaje import Personaje
from weapon import Weapon
from enemigo import Enemigo
from mundo import Obstaculo 
from sobrevivientes import Sobreviviente
from items import Item 
from puerta import Puerta 
from proyectil import Proyectil  # Import para las piedras lanzadas

# --- INICIALIZACIÓN ---
pygame.init()

# 1. Obtener la resolución nativa de tu monitor automáticamente
info = pygame.display.Info()
ANCHO_PANTALLA = info.current_w
ALTO_PANTALLA = info.current_h

# 2. Crear la ventana en Pantalla Completa con Doble Búfer (evita parpadeos)
ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption("Cepa Gusano - Sistema de Rescate")

# Actualizamos las constantes globales con el tamaño real de la pantalla
constantes.ANCHO_VENTANA = ANCHO_PANTALLA
constantes.ALTO_VENTANA = ALTO_PANTALLA

# --- VARIABLES DE CÁMARA ---
scroll = [0, 0]

# --- VARIABLES DE EFECTOS VISUALES ---
tiempo_mensaje_cura = 0

# --- VARIABLES DEL SISTEMA DE RESCATE Y PUNTUACIÓN ---
estudiantes_rescatados = 0
estudiantes_totales = 5
puntaje = 0

# --- VARIABLES DE MUNICIÓN (PIEDRAS) ---
piedras_inventario = 0  # Inicias con 3 piedras
lista_proyectiles = []

# --- FUNCIONES DE APOYO ---
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

def dibujar_interfaz():
    # 1. Dibujar Barra de Vida
    texto_vida = fuente_hud.render(f"HP: {int(jugador.vida)}", True, (255, 255, 255))
    ventana.blit(texto_vida, (20, 15))
    pygame.draw.rect(ventana, (50, 50, 50), (20, 45, 200, 15))
    ancho_rojo = int(200 * (max(0, jugador.vida) / 100))
    if ancho_rojo > 0:
        pygame.draw.rect(ventana, (255, 0, 0), (20, 45, ancho_rojo, 15))

    # 2. Dibujar Contador de Rescatados (HUD)
    texto_rescatados = fuente_hud.render(f"Rescatados: {estudiantes_rescatados} / {estudiantes_totales}", True, (255, 255, 0))
    ventana.blit(texto_rescatados, (constantes.ANCHO_VENTANA - 250, 15))

    # 3. Dibujar Puntaje (HUD)
    texto_puntaje = fuente_hud.render(f"Puntaje: {puntaje}", True, (0, 255, 0))
    ventana.blit(texto_puntaje, (constantes.ANCHO_VENTANA - 250, 45))

    # 4. Dibujar Munición de Piedras (HUD)
    texto_piedras = fuente_hud.render(f"Piedras: {piedras_inventario} / {constantes.max_piedras}", True, (200, 200, 200))
    ventana.blit(texto_piedras, (20, 75))

    # Mensaje temporal al usar Cuchara de Energía
    global tiempo_mensaje_cura
    if pygame.time.get_ticks() - tiempo_mensaje_cura < 2000:
        texto_cura = fuente_hud.render("+25 HP (Cuchara de Energía)", True, (0, 255, 0))
        ventana.blit(texto_cura, (20, 105))

# --- CARGA DE RECURSOS ---
fuente_hud = pygame.font.SysFont("Arial Black", 18)
fuente_gameover = pygame.font.SysFont("Arial Black", 60)

# Animaciones Mikel
animaciones = []
for i in range(1, 7):
    img = pygame.image.load(f"assets/images/characters/player/{i}.png")
    animaciones.append(escalar_img(img, constantes.scala_personaje))

# Animaciones Zombie
animaciones_enemigo = []
for i in range(1, 5): 
    img = pygame.image.load(f"assets/images/enemigos/enemigo_{i}.png") 
    animaciones_enemigo.append(escalar_img(img, constantes.scala_zombiee))

# Imagen Palo
imagen_palo = pygame.image.load(f"assets/images/weapons/palo.png")
imagen_palo = escalar_img(imagen_palo, constantes.scala_palo)

# Animaciones Sobreviviente
animaciones_sobreviviente = []
for i in range(1, 4):
    img = pygame.image.load(f"assets/images/sobrevivientes/sobreviviente{i}.png")
    animaciones_sobreviviente.append(escalar_img(img, constantes.scala_sobreviviente))

# Animaciones Cuchara del Comedor (4 frames)
animaciones_cuchara = []
for i in range(1, 5):
    img = pygame.image.load(f"assets/images/items/cuchara{i}.png")
    img_escalada = escalar_img(img, constantes.scala_cuchara)
    animaciones_cuchara.append(img_escalada)

# NUEVO: Animaciones de la Piedra del suelo (3 frames)
animaciones_piedra = []
for i in range(1, 4): # Toma piedra1.png, piedra2.png y piedra3.png
    img = pygame.image.load(f"assets/images/items/piedra{i}.png")
    img_escalada = escalar_img(img, constantes.scala_piedra)
    animaciones_piedra.append(img_escalada)

# Usamos el primer frame como imagen fija para cuando se lanza al aire
imagen_piedra_lanzada = animaciones_piedra[0]

# --- INSTANCIAS ---
jugador = Personaje(100, 100, animaciones)
palo = Weapon(imagen_palo)

# Puerta de salida hacia el Comedor (Ubicada al final del mapa)
puerta_salida = Puerta(1850, 400, 60, 120)

# --- GENERACIÓN ALEATORIA DE ENEMIGOS EN MAIN.PY ---
lista_enemigos = []
cantidad_zombis = 15

# --- CREACIÓN DEL MAPA ---
lista_obstaculos = [
    Obstaculo(500, 300, 100, 100),
    Obstaculo(800, 200, 50, 300),
    Obstaculo(200, 600, 400, 40),
    Obstaculo(-50, -50, 2100, 50),
    Obstaculo(-50, 2000, 2100, 50),
    Obstaculo(-50, -50, 50, 2100),
    Obstaculo(2000, -50, 50, 2100)
]


for _ in range(cantidad_zombis):
    while True:
        x_rand = random.randint(100, 1900)
        y_rand = random.randint(100, 1900)
        
        # Evitar que aparezcan muy cerca de Mikel
        dist_al_inicio = math.hypot(x_rand - 100, y_rand - 100)
        
        if dist_al_inicio > 400:
            nuevo_zombie = Enemigo(x_rand, y_rand, animaciones_enemigo)
            
            # NUEVO: Verificar que NO nazca dentro de una pared
            choca_con_muro = False
            for obs in lista_obstaculos:
                if nuevo_zombie.forma.colliderect(obs.forma):
                    choca_con_muro = True
                    break
                    
            if not choca_con_muro: # Si el lugar está libre, lo agregamos y rompemos el ciclo
                lista_enemigos.append(nuevo_zombie)
                break


# --- CREACIÓN DE SOBREVIVIENTES ---
lista_sobrevivientes = [
    Sobreviviente(150, 400, animaciones_sobreviviente),
    Sobreviviente(350, 150, animaciones_sobreviviente),
    Sobreviviente(250, 750, animaciones_sobreviviente),
    Sobreviviente(850, 120, animaciones_sobreviviente),
    Sobreviviente(1250, 800, animaciones_sobreviviente)
]

# --- CREACIÓN DE ITEMS (Cucharas y Piedras) ---
lista_items = [
    Item(550, 120, animaciones_cuchara, "cuchara"),
    Item(1000, 400, animaciones_cuchara, "cuchara"),
    Item(300, 200, animaciones_piedra, "piedra"),
    Item(1200, 600, animaciones_piedra, "piedra")
]

reloj = pygame.time.Clock()
mover_arriba = mover_abajo = mover_izquierda = mover_derecha = False

# --- BUCLE PRINCIPAL ---
run = True  
while run:
    reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_BG)

    if jugador.vivo:
        dx = dy = 0
        if mover_derecha: dx = 5
        if mover_izquierda: dx = -5
        if mover_arriba: dy = -5 
        if mover_abajo: dy = 5

        jugador.movimiento(dx, dy, lista_obstaculos)  
        jugador.update()   
        palo.update(jugador)

        # Suavizado de la cámara
        scroll[0] += (jugador.forma.centerx - scroll[0] - constantes.ANCHO_VENTANA / 2) / 15
        scroll[1] += (jugador.forma.centery - scroll[1] - constantes.ALTO_VENTANA / 2) / 15

        # ACTUALIZAR ENEMIGOS
        for zombie in lista_enemigos:
            if zombie.vivo:
                zombie.movimiento(jugador, lista_obstaculos) 
                zombie.update()

                if zombie.forma.colliderect(jugador.forma):
                    jugador.vida -= 0.3

                if palo.atacando and palo.forma.colliderect(zombie.forma):
                    zombie.vida -= 5

        # ACTUALIZAR PROYECTILES (Piedras en el aire)
        for proyectil in lista_proyectiles[:]:
            colision_muro = proyectil.update(lista_obstaculos)
            if colision_muro:
                lista_proyectiles.remove(proyectil)
                continue

            for zombie in lista_enemigos:
                if zombie.vivo and proyectil.forma.colliderect(zombie.forma):
                    zombie.vida -= proyectil.daño
                    if proyectil in lista_proyectiles:
                        lista_proyectiles.remove(proyectil)
                    break

        # ACTUALIZAR SOBREVIVIENTES
        for estudiante in lista_sobrevivientes[:]:
            estudiante.update()
            
            if jugador.forma.colliderect(estudiante.forma):
                lista_sobrevivientes.remove(estudiante)
                estudiantes_rescatados += 1
                puntaje += 100
                
            for zombie in lista_enemigos:
                if zombie.vivo and zombie.forma.colliderect(estudiante.forma):
                    if estudiante in lista_sobrevivientes:
                        lista_sobrevivientes.remove(estudiante)
                        puntaje = max(0, puntaje - 50)

        # RECOLECCIÓN DE ITEMS
        for item in lista_items[:]:
            item.update()
            if jugador.forma.colliderect(item.forma):
                if item.tipo == "cuchara":
                    jugador.vida = min(100, jugador.vida + 25)
                    lista_items.remove(item)
                    tiempo_mensaje_cura = pygame.time.get_ticks()
                
                elif item.tipo == "piedra":
                    if piedras_inventario < constantes.max_piedras:
                        piedras_inventario += 1
                        lista_items.remove(item)

        # CONTROL DE PUERTA DE SALIDA
        if estudiantes_rescatados == estudiantes_totales:
            puerta_salida.abierta = True
            
            if jugador.forma.colliderect(puerta_salida.forma):
                texto_pasar = fuente_hud.render("Cargando Nivel 2: Comedor Central...", True, (0, 255, 255))
                ventana.blit(texto_pasar, (constantes.ANCHO_VENTANA // 2 - 200, constantes.ALTO_VENTANA // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                run = False 

        if jugador.vida <= 0:
            jugador.vivo = False

    # --- 6. DIBUJAR TODO ---
    scroll_final = [int(scroll[0]), int(scroll[1])]

    # Dibujar puerta de salida
    puerta_salida.dibujar(ventana, scroll_final)

    for obs in lista_obstaculos:
        obs.dibujar(ventana, scroll_final)

    for item in lista_items:
        item.dibujar(ventana, scroll_final)

    for proyectil in lista_proyectiles:
        proyectil.dibujar(ventana, scroll_final)

    for estudiante in lista_sobrevivientes:
        estudiante.dibujar(ventana, scroll_final)

    for zombie in lista_enemigos:
        if zombie.vivo:
            zombie.dibujar(ventana, scroll_final)
            zombie.dibujar_barra_vida(ventana, scroll_final)
    
    if jugador.vivo:
        jugador.dibujar(ventana, scroll_final)
        palo.dibujar(ventana, scroll_final)
        dibujar_interfaz() 

        # --- REGLA DE FIN DE NIVEL 1 ---
        if len(lista_sobrevivientes) == 0:
            if estudiantes_rescatados == estudiantes_totales:
                texto_victoria = fuente_hud.render("¡Nivel 1 Completado! ¡Ve a la Puerta del Comedor!", True, (0, 255, 0))
                ventana.blit(texto_victoria, (constantes.ANCHO_VENTANA // 2 - 240, constantes.ALTO_VENTANA - 60))
            else:
                texto_fallo = fuente_hud.render("¡Misión Fallida! No salvaste a todos. Reiniciando...", True, (255, 0, 0))
                ventana.blit(texto_fallo, (constantes.ANCHO_VENTANA // 2 - 240, constantes.ALTO_VENTANA - 60))
                
                pygame.display.flip()
                pygame.time.wait(3000)
                
                # Reinicio completo del nivel
                estudiantes_rescatados = 0
                puntaje = 0
                piedras_inventario = 0
                jugador.vida = 100
                jugador.forma.topleft = (100, 100)
                puerta_salida.abierta = False
                lista_proyectiles = []
                
                lista_sobrevivientes = [
                    Sobreviviente(150, 400, animaciones_sobreviviente),
                    Sobreviviente(350, 150, animaciones_sobreviviente),
                    Sobreviviente(250, 750, animaciones_sobreviviente),
                    Sobreviviente(850, 120, animaciones_sobreviviente),
                    Sobreviviente(1250, 800, animaciones_sobreviviente)
                ]
                lista_enemigos = [
                    Enemigo(600, 500, animaciones_enemigo),
                    Enemigo(1100, 600, animaciones_enemigo),
                    Enemigo(1400, 250, animaciones_enemigo),
                    Enemigo(1700, 750, animaciones_enemigo)
                ]
                lista_items = [
                    Item(550, 120, animaciones_cuchara, "cuchara"),
                    Item(1000, 400, animaciones_cuchara, "cuchara"),
                    Item(300, 200, animaciones_piedra, "piedra"),
                    Item(1200, 600, animaciones_piedra, "piedra")
                ]
    else:
        texto_death = fuente_gameover.render("GAME OVER", True, (255, 0, 0))
        ventana.blit(texto_death, (constantes.ANCHO_VENTANA // 2 - 180, constantes.ALTO_VENTANA // 2 - 50))

    # --- EVENTOS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Presiona Esc para salir del juego
                run = False
            if event.key == pygame.K_a: mover_izquierda = True
            if event.key == pygame.K_d: mover_derecha = True
            if event.key == pygame.K_w: mover_arriba = True
            if event.key == pygame.K_s: mover_abajo = True
            if event.key == pygame.K_SPACE: palo.atacar()
            
            # Lanzar piedra con la tecla Q
            if event.key == pygame.K_q and piedras_inventario > 0:
                pos_mouse = pygame.mouse.get_pos()
                objetivo_x = pos_mouse[0] + scroll[0]
                objetivo_y = pos_mouse[1] + scroll[1]
                
                # Lanzamos usando la imagen fija
                nueva_piedra = Proyectil(jugador.forma.centerx, jugador.forma.centery, objetivo_x, objetivo_y, imagen_piedra_lanzada)
                lista_proyectiles.append(nueva_piedra)
                piedras_inventario -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: mover_izquierda = False
            if event.key == pygame.K_d: mover_derecha = False
            if event.key == pygame.K_w: mover_arriba = False
            if event.key == pygame.K_s: mover_abajo = False

    pygame.display.flip()  # Renderizado continuo y sin parpadeos

pygame.quit()
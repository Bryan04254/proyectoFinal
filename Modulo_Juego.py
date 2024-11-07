import pygame
import random
import sys
from Modulo_creacionDelArbol import iniciar_partida

def inicio(categoria):
    # Configuración básica de Pygame
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    # Configuración de niveles (similar al código anterior)
    niveles = [
        ["Nivel 1", 5, 5, "perro.png", "granja.png"],
        ["Nivel 2", 7, 6, "tronco.png", "bosque.png"],
        ["Nivel 3", 9, 7, "carro.png", "ciudad.png"],
        ["Nivel 4", 11, 8, "asteroide.png", "espacio.png"],
        ["Nivel 5", 13, 9, "marciano.png", "marte.png"]
    ]

    # Obtener preguntas balanceadas para la partida en la categoría seleccionada
    preguntas = iniciar_partida(categoria)
    pregunta_index = 0  # Empezar con la primera pregunta

    # Variables de juego
    contador = 0
    running = True
    while running:
        # Cargar la imagen de fondo del nivel actual
        background_image = pygame.image.load(niveles[contador][4])
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        # Reiniciar posición del jugador
        player_pos = [WIDTH // 2, HEIGHT - 40]

        # Obtener la siguiente pregunta de trivia y mostrarla en consola
        pregunta_actual = preguntas[pregunta_index]
        print("Pregunta:", pregunta_actual.texto)  # Se imprime la pregunta en la consola

        # Procesar la respuesta del jugador
        respuesta_correcta = input("¿Es correcta la respuesta? (s/n): ").strip().lower() == 's'
        pregunta_actual.registrar_respuesta(respuesta_correcta)

        # Avanzar a la siguiente pregunta si quedan más en la lista
        pregunta_index = (pregunta_index + 1) % len(preguntas)
        
        # Lógica para pasar de nivel
        contador += 1
        if contador >= len(niveles):
            print("¡Has completado todos los niveles!")
            running = False

    pygame.quit()
    sys.exit()

import pygame
import random
import sys
from Modulo_SeleccionPreguntas import iniciar_partida
from Modulo_creacionDelArbol import construir_arbol_balanceado

def iniciar_juego():
    arbol_preguntas = construir_arbol_balanceado()
    # Aquí iría la lógica del juego que utilice `arbol_preguntas` según sea necesario
    # ...


def inicio(categoria):
    # Configuración básica de Pygame
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    # Configuración de niveles
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
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Cargar la imagen de fondo del nivel actual
        try:
            background_image = pygame.image.load(niveles[contador][4])
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            screen.blit(background_image, (0, 0))
        except pygame.error:
            print(f"Error: No se pudo cargar la imagen {niveles[contador][4]}")
            running = False

        # Reiniciar posición del jugador
        player_pos = [WIDTH // 2, HEIGHT - 40]

        # Obtener la siguiente pregunta de trivia
        pregunta_actual = preguntas[pregunta_index]
        print("Pregunta:", pregunta_actual.texto)  # Se imprime la pregunta en la consola

        # Dibujar la pregunta en pantalla (simple ejemplo)
        font = pygame.font.Font(None, 36)
        pregunta_texto = font.render(pregunta_actual.texto, True, (255, 255, 255))
        screen.blit(pregunta_texto, (50, 50))

        # Procesar la respuesta del jugador (simulación de respuesta en este caso)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:  # Suponiendo que "S" es para respuesta correcta
            respuesta_correcta = True
        elif keys[pygame.K_n]:  # Suponiendo que "N" es para respuesta incorrecta
            respuesta_correcta = False
        else:
            respuesta_correcta = None

        if respuesta_correcta is not None:
            pregunta_actual.registrar_respuesta(respuesta_correcta)
            pregunta_index = (pregunta_index + 1) % len(preguntas)  # Avanza a la siguiente pregunta

            # Lógica para pasar de nivel
            contador += 1
            if contador >= len(niveles):
                print("¡Has completado todos los niveles!")
                running = False

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

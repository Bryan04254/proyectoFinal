import pygame
import random
import sys
from creacionDelArbol import Pregunta, construir_arbol_balanceado, obtener_pregunta_aleatoria

def inicio():
    # Configuración básica de Pygame
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    # Configuración de los niveles (similar al código anterior)
    niveles = [
        ["Nivel 1", 5, 5, "perro.png", "granja.png"],
        ["Nivel 2", 7, 6, "tronco.png", "bosque.png"],
        ["Nivel 3", 9, 7, "carro.png", "ciudad.png"],
        ["Nivel 4", 11, 8, "asteroide.png", "espacio.png"],
        ["Nivel 5", 13, 9, "marciano.png", "marte.png"]
    ]

    # Configurar preguntas y construir árbol balanceado
    preguntas = [
        Pregunta("¿Qué es Pygame?"),
        Pregunta("¿Cuál es la capital de Francia?"),
        Pregunta("¿Cuántos planetas hay en el sistema solar?"),
        Pregunta("¿Qué lenguaje se usa para desarrollo web?"),
        Pregunta("¿Cuál es la raíz cuadrada de 16?")
    ]
    arbol_preguntas = construir_arbol_balanceado(preguntas)

    # Variables de juego
    contador = 0
    running = True
    while running:
        # Cargar la imagen de fondo del nivel actual
        background_image = pygame.image.load(niveles[contador][4])
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        # Reiniciar la posición del jugador
        player_pos = [WIDTH // 2, HEIGHT - 40]
        
        # Obtener y mostrar una pregunta al inicio del nivel
        pregunta_actual = obtener_pregunta_aleatoria(arbol_preguntas)
        print("Pregunta:", pregunta_actual.texto)  # Se imprime la pregunta en la consola

        # Esperar respuesta del jugador
        respuesta_correcta = input("¿Es correcta la respuesta? (s/n): ").strip().lower() == 's'
        pregunta_actual.registrar_respuesta(respuesta_correcta)

        # Lógica para pasar de nivel
        # Aquí pondríamos la lógica del juego, movimientos y demás, tal como en el código anterior

        # Avanzar al siguiente nivel si el jugador ha llegado a la meta
        contador += 1
        if contador >= len(niveles):
            print("¡Has completado todos los niveles!")
            running = False

    pygame.quit()
    sys.exit()

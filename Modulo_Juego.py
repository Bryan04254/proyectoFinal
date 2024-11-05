import pygame
import random
import sys

def inicio():
    # Configuración básica
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    # Colores
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    niveles = [
        ["Nivel 1", 5, 5, "perro.png", "granja.png"],  # Velocidad: 5
        ["Nivel 2", 7, 6, "tronco.png", "bosque.png"], # Velocidad: 6
        ["Nivel 3", 9, 7, "carro.png", "ciudad.png"],  # Velocidad: 7
        ["Nivel 4", 11, 8, "asteroide.png", "espacio.png"], # Velocidad: 8
        ["Nivel 5", 13, 9, "marciano.png", "marte.png"]   # Velocidad: 9
    ]

    # Configuración del jugador
    player_size = 40
    player_pos = [WIDTH // 2, HEIGHT - player_size]
    player_speed = 10

    # Cargar la imagen del jugador
    player_image = pygame.image.load("gallina.png")
    player_image = pygame.transform.scale(player_image, (player_size, player_size))

    # Configuración de los obstáculos
    obstacle_width = 70
    obstacle_height = 40
    lanes = [100, 200, 300, 400, 500]  # Carriles en la carretera
    obstacles = []

    # Funciones del juego
    def create_obstacle(speed):
        lane = random.choice(lanes)
        obstacle_x = random.choice([-obstacle_width, WIDTH])  # Inicia desde fuera de la pantalla
        direction = 1 if obstacle_x == -obstacle_width else -1
        obstacle = {
            "pos": [obstacle_x, lane],
            "speed": speed * direction
        }
        obstacles.append(obstacle)

    def move_obstacles():
        for obstacle in obstacles:
            obstacle["pos"][0] += obstacle["speed"]
            if obstacle["pos"][0] > WIDTH + obstacle_width or obstacle["pos"][0] < -obstacle_width:
                obstacles.remove(obstacle)

    def check_collision(player_pos, obstacles):
        px, py = player_pos
        for obstacle in obstacles:
            ox, oy = obstacle["pos"]
            if (px < ox + obstacle_width and
                px + player_size > ox and
                py < oy + obstacle_height and
                py + player_size > oy):
                return True
        return False

    # Juego principal
    contador = 0
    running = True
    while running:
        # Cargar la imagen de fondo del nivel actual
        background_image = pygame.image.load(niveles[contador][4])
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        # Reiniciar el juego
        player_pos = [WIDTH // 2, HEIGHT - player_size]
        obstacles.clear()

        # Bucle para el nivel
        while True:
            obstacle_speed = niveles[contador][2]  # Actualizar la velocidad del obstáculo

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Cerrar Pygame
                    sys.exit()      # Salir del programa completamente
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_pos[1] -= player_speed
                    elif event.key == pygame.K_DOWN:
                        player_pos[1] += player_speed
                    elif event.key == pygame.K_LEFT:
                        player_pos[0] -= player_speed
                    elif event.key == pygame.K_RIGHT:
                        player_pos[0] += player_speed

            # Crear nuevos obstáculos de manera aleatoria, basado en el nivel
            num_obstacles = niveles[contador][1]  # Número de obstáculos según el nivel
            if len(obstacles) < num_obstacles:  # Limitar la cantidad de obstáculos en pantalla
                if random.randint(1, 30) == 1:
                    create_obstacle(obstacle_speed)

            # Mover obstáculos
            move_obstacles()

            # Verificar colisión
            if check_collision(player_pos, obstacles):
                print("¡Colisión! Reiniciando posición del jugador.")
                player_pos = [WIDTH // 2, HEIGHT - player_size]
                obstacles.clear()  # Opcional: puedes limpiar los obstáculos al reiniciar

            # Verificar si el jugador llegó a la meta
            if player_pos[1] < player_size:
                print("¡Ganaste! Pasando al siguiente nivel.")
                contador = contador + 1
                if contador >= len(niveles):  # Si se completaron todos los niveles
                    print("¡Has completado todos los niveles!")
                    running = False
                break  # Salir del bucle del nivel actual para avanzar

            # Dibujar
            screen.blit(background_image, (0, 0))
            pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, player_size))
            screen.blit(player_image, (player_pos[0], player_pos[1]))

            for obstacle in obstacles:
                obstacle_image = pygame.image.load(niveles[contador][3])  # Cargar imagen de obstáculo
                obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
                screen.blit(obstacle_image, (obstacle["pos"][0], obstacle["pos"][1]))

            pygame.display.flip()
            clock.tick(30)

    pygame.quit()
    sys.exit()

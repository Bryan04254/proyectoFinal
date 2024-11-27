import pygame
import random
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from Modulo_Assets import AssetManager
from Jugador import GestorJugadores
from Modulo_creacionDelArbol import construir_arbol_balanceado, Pregunta


# Definir el orden de progresión de categorías
CATEGORIA_PROGRESSION = ["granja", "bosque", "ciudad", "espacio", "marte"]

@dataclass
class GameConfig:
    """
    Configuración de parámetros del juego, definiendo pantalla, jugador y configuraciones de juego.
    
    Atributos:
        SCREEN_WIDTH (int): Ancho de la pantalla de juego.
        SCREEN_HEIGHT (int): Altura de la pantalla de juego.
        FPS (int): Cuadros por segundo del juego.
        PLAYER_SPEED (int): Velocidad de movimiento del jugador.
        INITIAL_OBSTACLE_COUNT (int): Número de obstáculos al inicio del juego.
        MAX_OBSTACLE_COUNT (int): Número máximo de obstáculos permitidos.
        OBSTACLE_SPAWN_DELAY (int): Retraso entre apariciones de obstáculos.
        BASE_OBSTACLE_SPEED (int): Velocidad inicial de los obstáculos.
        SPEED_INCREMENT (float): Tasa de incremento de velocidad.
        POINTS_TO_ADVANCE (int): Puntos necesarios para avanzar de categoría.
    """
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    FPS: int = 60
    PLAYER_SPEED: int = 5
    INITIAL_OBSTACLE_COUNT: int = 5
    MAX_OBSTACLE_COUNT: int = 10
    OBSTACLE_SPAWN_DELAY: int = 20
    BASE_OBSTACLE_SPEED: int = 5
    SPEED_INCREMENT: float = 0.5
    POINTS_TO_ADVANCE: int = 500
    
class DificultadJuego:
    """
    Representa niveles de dificultad del juego con configuraciones de velocidad asociadas.
    
    Atributos de Clase:
        MUY_BAJO (int): Nivel de dificultad muy bajo.
        BAJO (int): Nivel de dificultad bajo.
        NORMAL (int): Nivel de dificultad normal.
        INTERMEDIO (int): Nivel de dificultad intermedio.
        DIFICIL (int): Nivel de dificultad difícil.
    """
    MUY_BAJO = 1
    BAJO = 2
    NORMAL = 3
    INTERMEDIO = 4
    DIFICIL = 5

    @staticmethod
    def obtener_velocidad_base(dificultad: int) -> float:
        """
        Obtiene la velocidad base para un nivel de dificultad dado.
        
        Args:
            dificultad (int): Nivel de dificultad de 1 a 5.
        
        Returns:
            float: Velocidad base correspondiente al nivel de dificultad.
        """
        velocidades = {
            1: 3.0,  # MUY_BAJO
            2: 4.0,  # BAJO
            3: 5.0,  # NORMAL
            4: 6.0,  # INTERMEDIO
            5: 7.0   # DIFICIL
        }
        return velocidades.get(dificultad, 5.0)

class SistemaPreguntas:
    """
    Gestiona el sistema de preguntas para diferentes categorías del juego.
    
    Atributos:
        categoria (str): Categoría actual del juego.
        preguntas_por_categoria (Dict[str, List[Dict]]): Diccionario de preguntas para cada categoría.
        arbol (Optional): Árbol de preguntas balanceado para la categoría actual.
    """
    def __init__(self, categoria: str):
        """
        Inicializa el sistema de preguntas para una categoría específica.
        
        Args:
            categoria (str): La categoría del juego para inicializar las preguntas.
        """
        self.categoria = categoria
        self.preguntas_por_categoria = self._inicializar_preguntas()
        self.arbol = self._construir_arbol_inicial()
        
    def _inicializar_preguntas(self) -> Dict[str, List[Dict]]:
        """
        Inicializa y devuelve un diccionario de preguntas por categoría.
        
        Returns:
            Dict[str, List[Dict]]: Diccionario de preguntas organizadas por categoría.
        """
        return {
            "granja": [
                {"pregunta": "¿Qué alimento da la vaca?", "opciones": ["Leche", "Carne"], "correcta": "Leche", "dificultad": 1},
                {"pregunta": "¿Qué animal pone huevos?", "opciones": ["Gallina", "Perro"], "correcta": "Gallina", "dificultad": 2},
                {"pregunta":"¿Qué animal nos da lana?","opciones":["Oveja", "Cabra"],"correcta":"Oveja","dificultad": 2},
                {"pregunta":"¿Qué cultivo es típico de una granja?","opciones":["Maiz", "Helado"],"correcta":"Maiz","dificultad": 3},
                {"pregunta":"¿Qué herramienta usa un granjero para arar?","opciones":["Tractor", "Camion de transporte"],"correcta":"Tractor","dificultad": 4},
                {"pregunta":"¿Qué técnica mejora la fertilidad del suelo?","opciones":["Tractor", "Rotación de cultivos"],"correcta":"Rotación de cultivos","dificultad": 5},
            ],
            "bosque": [
                {"pregunta": "¿Qué árbol produce bellotas?", "opciones": ["Roble", "Pino"], "correcta": "Roble", "dificultad": 1},
                {"pregunta": "¿Qué animal hiberna en invierno?", "opciones": ["Oso", "Leopardo"], "correcta": "Oso", "dificultad": 2},
                {"pregunta": "¿Qué hongo crece en los bosques?", "opciones": ["Champiñón", "ascomicetos"], "correcta": "Champiñón", "dificultad": 3},
                {"pregunta": "¿Qué proceso natural renuevan los bosques?", "opciones": ["Reforestacion", "Fotosíntesis"], "correcta": "Fotosíntesis", "dificultad": 4},
                {"pregunta": "¿Qué proceso ayuda a la conservación forestal?", "opciones": ["Reforestación", "Terrestre"], "correcta": "Reforestación", "dificultad": 5},
            ],
        }

    def _construir_arbol_inicial(self):
        """
        Construye un árbol balanceado de preguntas para la categoría actual.
        
        Returns:
            Optional: Árbol balanceado de preguntas o None si no hay preguntas.
        """
        preguntas = self.preguntas_por_categoria.get(self.categoria.lower(), [])
        if not preguntas:
            return None
        return construir_arbol_balanceado([Pregunta(p["pregunta"]) for p in preguntas])

    def obtener_preguntas_categoria(self, num_preguntas: int) -> List[Dict]:
        """
        Obtiene un número específico de preguntas para la categoría actual.
        
        Args:
            num_preguntas (int): Número de preguntas a obtener.
        
        Returns:
            List[Dict]: Lista de preguntas seleccionadas aleatoriamente.
        """
        preguntas = self.preguntas_por_categoria.get(self.categoria.lower(), [])
        return random.sample(preguntas, min(len(preguntas), num_preguntas))

    def mostrar_pregunta(self, screen, pregunta_dict: Dict) -> Optional[bool]:
        """
        Muestra una pregunta en pantalla y maneja la interacción del usuario.
        
        Args:
            screen: Superficie de Pygame donde se mostrará la pregunta.
            pregunta_dict (Dict): Diccionario con los detalles de la pregunta.
        
        Returns:
            Optional[bool]: True si la respuesta es correcta, False si es incorrecta, 
                            None si no hay respuesta aún.
        """
        # Configuración de la ventana de pregunta
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 600, 400))
        pygame.draw.rect(screen, (255, 255, 255), (110, 110, 580, 380))
        
        # Renderizado del texto
        font = pygame.font.Font(None, 36)
        pregunta_texto = font.render(pregunta_dict["pregunta"], True, (0, 0, 0))
        opcion1 = font.render(f"1. {pregunta_dict['opciones'][0]}", True, (0, 0, 0))
        opcion2 = font.render(f"2. {pregunta_dict['opciones'][1]}", True, (0, 0, 0))
        
        # Posicionamiento del texto
        screen.blit(pregunta_texto, (150, 150))
        screen.blit(opcion1, (150, 250))
        screen.blit(opcion2, (150, 300))
        
        pygame.display.flip()
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return pregunta_dict['opciones'][0] == pregunta_dict['correcta']
                elif event.key == pygame.K_2:
                    return pregunta_dict['opciones'][1] == pregunta_dict['correcta']
        
        return None

class JuegoMejorado:
    """
    Clase principal que gestiona el estado del juego, interacciones del jugador y mecánicas de juego.
    
    Atributos:
        config (GameConfig): Configuración del juego.
        sistema_preguntas (SistemaPreguntas): Sistema de gestión de preguntas.
        categoria (str): Categoría actual del juego.
        score (int): Puntuación actual del jugador.
        lives (int): Vidas restantes del jugador.
        running (bool): Estado de ejecución del juego.
    """
    def __init__(self, categoria: str = "granja", nombre_jugador: str = None):
        """
        Inicializa el juego con una categoría específica y un nombre de jugador opcional.
        
        Args:
            categoria (str, opcional): Categoría inicial del juego. Por defecto "granja".
            nombre_jugador (str, opcional): Nombre del jugador para seguimiento de progreso. Por defecto None.
        """
        if pygame.get_init():
            pygame.quit()
        pygame.init()
        # Configuración inicial
        self.config = GameConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Sistema de preguntas
        self.sistema_preguntas = SistemaPreguntas(categoria)
        self.nivel_actual = 0
        self.dificultad = DificultadJuego.MUY_BAJO
        self.preguntas_respondidas = 0
        
        # Estado del juego
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Configuración de pantalla
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        
        # Jugador y estadísticas del juego
        self.categoria = categoria.lower()
        self.nombre_jugador = nombre_jugador
        self.score = 0
        self.lives = 3
        self.running = True
        
        # Determinar punto de inicio para la progresión de categorías
        self.current_categoria_index = CATEGORIA_PROGRESSION.index(self.categoria)
        
        pygame.display.set_caption(f"Dodge Obstacles - {self.categoria}")
        
        # Gestión de obstáculos
        self.obstacles = []
        self.spawn_delay_counter = 0
        self.current_obstacle_count = self.config.INITIAL_OBSTACLE_COUNT
        self.current_speed = self.config.BASE_OBSTACLE_SPEED
        
        # Sistema de gestión de jugadores
        if nombre_jugador:
            self.gestor_jugadores = GestorJugadores()
            jugador = self.gestor_jugadores.obtener_jugador(nombre_jugador)
            if jugador and self.categoria in jugador.progreso:
                ultimo_progreso = jugador.progreso[self.categoria][-1]
                self.score = ultimo_progreso.puntos
        
        # Carga de recursos
        try:
            self.assets = AssetManager(self.categoria)
            
            # Posición inicial del jugador
            player_img = self.assets.images.get("player")
            if player_img:
                player_height = player_img.get_height()
                self.player_pos = [
                    self.config.SCREEN_WIDTH // 2,
                    self.config.SCREEN_HEIGHT - player_height - 10
                ]
            else:
                self.player_pos = [
                    self.config.SCREEN_WIDTH // 2,
                    self.config.SCREEN_HEIGHT - 100
                ]
            
            # Generación inicial de obstáculos
            for _ in range(self.current_obstacle_count):
                self.spawn_obstacle(random_position=True)
                
        except Exception as e:
            print(f"Error loading assets: {e}")
            self.running = False

    def manejar_preguntas_inicio_categoria(self) -> bool:
        """
        Gestiona las preguntas al inicio de cada categoría.
        
        Presenta preguntas al jugador y ajusta la dificultad según su desempeño.
        
        Returns:
            bool: True si el juego debe continuar, False si debe terminar.
        """
        num_preguntas = 2 ** self.nivel_actual if self.nivel_actual > 0 else 1
        preguntas = self.sistema_preguntas.obtener_preguntas_categoria(num_preguntas)
        
        for pregunta in preguntas:
            respondido = False
            while not respondido and self.running:
                respuesta = self.sistema_preguntas.mostrar_pregunta(self.screen, pregunta)
                if respuesta is not None:
                    respondido = True
                    if respuesta:
                        self.dificultad = max(DificultadJuego.MUY_BAJO, self.dificultad - 1)
                    else:
                        self.dificultad = min(DificultadJuego.DIFICIL, self.dificultad + 1)

                    # Actualizar velocidad de los obstáculos basado en la dificultad
                    self.current_speed = DificultadJuego.obtener_velocidad_base(self.dificultad)
                
                # Manejar eventos de cierre de ventana
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return False
                
                self.clock.tick(self.config.FPS)
                
        return True
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        return self.running

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_pos[0] > 0:
            self.player_pos[0] -= self.config.PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.player_pos[0] < self.config.SCREEN_WIDTH - 50:
            self.player_pos[0] += self.config.PLAYER_SPEED
        if keys[pygame.K_UP] and self.player_pos[1] > 0:
            self.player_pos[1] -= self.config.PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.player_pos[1] < self.config.SCREEN_HEIGHT - 50:
            self.player_pos[1] += self.config.PLAYER_SPEED
    
    def spawn_obstacle(self, random_position=False):
        obstacle_img = self.assets.images.get("obstacle")
        if obstacle_img:
            obstacle_width = obstacle_img.get_width()
            obstacle_height = obstacle_img.get_height()
        else:
            obstacle_width = 30
            obstacle_height = 30
        
        if random_position:
            y_pos = random.randint(-200, 0)
        else:
            y_pos = -obstacle_height
            
        obstacle = pygame.Rect(
            random.randint(0, self.config.SCREEN_WIDTH - obstacle_width),
            y_pos,
            obstacle_width,
            obstacle_height
        )
        self.obstacles.append(obstacle)

    def update_obstacles(self):
        for obstacle in self.obstacles[:]:
            obstacle.y += self.current_speed
            if obstacle.y > self.config.SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
                self.score += 10
        
        # Spawn new obstacles
        if len(self.obstacles) < self.current_obstacle_count:
            self.spawn_delay_counter += 1
            if self.spawn_delay_counter >= self.config.OBSTACLE_SPAWN_DELAY:
                self.spawn_obstacle()
                self.spawn_delay_counter = 0

    def check_collisions(self):
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
        return any(obstacle.colliderect(player_rect) for obstacle in self.obstacles)
    
    def check_category_progression(self):
        """
        Check if player has reached points threshold to advance to next category
        """
        if (self.score >= self.config.POINTS_TO_ADVANCE and 
            self.current_categoria_index < len(CATEGORIA_PROGRESSION) - 1):
            
            # Advance to next category
            self.current_categoria_index += 1
            new_categoria = CATEGORIA_PROGRESSION[self.current_categoria_index]
            
            # Reset score when advancing to a new category
            self.score = 0
            
            # Reset game state for new category
            self.categoria = new_categoria
            self.current_speed = self.config.BASE_OBSTACLE_SPEED
            self.current_obstacle_count = self.config.INITIAL_OBSTACLE_COUNT
            
            # Reload assets for new category
            self.assets = AssetManager(new_categoria)
            
            # Update display caption
            pygame.display.set_caption(f"Dodge Obstacles - {new_categoria}")
            
            # Reset player position
            player_img = self.assets.images.get("player")
            if player_img:
                player_height = player_img.get_height()
                self.player_pos = [
                    self.config.SCREEN_WIDTH // 2,
                    self.config.SCREEN_HEIGHT - player_height - 10
                ]
            else:
                self.player_pos = [
                    self.config.SCREEN_WIDTH // 2,
                    self.config.SCREEN_HEIGHT - 100
                ]
            
            # Clear existing obstacles and spawn new ones
            self.obstacles.clear()
            for _ in range(self.current_obstacle_count):
                self.spawn_obstacle(random_position=True)
            
            return True
        return False

    def draw(self):
        # Draw background
        background = self.assets.images.get("background")
        if background:
            scaled_background = pygame.transform.scale(background, 
                (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            self.screen.blit(scaled_background, (0, 0))
        else:
            self.screen.fill((100, 100, 255))
        
        # Draw obstacles
        obstacle_img = self.assets.images.get("obstacle")
        if obstacle_img:
            for obs in self.obstacles:
                self.screen.blit(obstacle_img, obs)
        else:
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, (255, 0, 0), obs)
        
        # Draw player
        player_img = self.assets.images.get("player")
        if player_img:
            self.screen.blit(player_img, self.player_pos)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), 
                        pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50))
        
        # HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        category_text = font.render(f"Categoría: {self.categoria}", True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(category_text, (10, 90))
        
        pygame.display.flip()

    def guardar_progreso(self):
        if self.nombre_jugador:
            try:
                self.gestor_jugadores.actualizar_progreso(
                    nombre_jugador=self.nombre_jugador,
                    categoria=self.categoria,
                    puntos=self.score,
                    nivel=1
                )
            except Exception as e:
                print(f"Error al guardar progreso: {e}")

    def cleanup(self):
        self.guardar_progreso()
        if hasattr(self, 'assets'):
            self.assets.images.clear()
        pygame.quit()

    def run(self):
        # Iniciar con preguntas de la primera categoría
        if not self.manejar_preguntas_inicio_categoria():
            self.cleanup()
            return

        while self.running and self.lives > 0:
            self.handle_events()
            self.handle_player_movement()
            self.update_obstacles()
            
            if self.check_collisions():
                self.lives -= 1
                if self.lives <= 0:
                    break
                self.player_pos = [self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100]
            
            # Verificar progresión de categoría
            if self.check_category_progression():
                self.nivel_actual += 1
                if not self.manejar_preguntas_inicio_categoria():
                    break
            
            self.draw()
            self.clock.tick(self.config.FPS)
        
        self.cleanup()

def inicio(categoria: str = "granja", nombre_jugador: str = None):
    """Game initialization function"""
    try:
        juego = JuegoMejorado(categoria, nombre_jugador)
        juego.run()
    except Exception as e:
        print(f"Game error: {e}")
        if pygame.get_init():
            pygame.quit()

# Main execution
if __name__ == "__main__":
    inicio()
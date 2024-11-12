import pygame
import random
from typing import Dict
from dataclasses import dataclass
from Modulo_Assets import AssetManager

@dataclass
class GameConfig:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    FPS: int = 60
    PLAYER_SPEED: int = 5
    INITIAL_OBSTACLE_COUNT: int = 3  # Número inicial de obstáculos
    MAX_OBSTACLE_COUNT: int = 8      # Máximo número de obstáculos permitidos
    OBSTACLE_SPAWN_DELAY: int = 30   # Frames entre spawn de obstáculos
    
    def __post_init__(self):
        self.OBSTACLE_SPEEDS = {
            "correct": 5,
            "incorrect": 8
        }

class JuegoMejorado:
    def __init__(self, categoria: str):
        if pygame.get_init():
            pygame.quit()
        pygame.init()
        
        # Inicializar pantalla
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"Juego - {categoria}")
        
        # Configuración
        self.config = GameConfig()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado del juego
        self.categoria = categoria
        self.score = 0
        self.lives = 3
        self.level = 1
        self.current_obstacle_count = self.config.INITIAL_OBSTACLE_COUNT
        self.spawn_delay_counter = 0
        
        # Posición del jugador y ajuste según el tamaño de la imagen
        self.player_pos = [self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100]
        self.obstacles = []
        self.current_question = None
        
        # Cargar assets
        self.assets = AssetManager(categoria)
        
        # Ajustar posición inicial del jugador según el tamaño de la imagen
        if "player" in self.assets.images:
            player_height = self.assets.images["player"].get_height()
            self.player_pos[1] = self.config.SCREEN_HEIGHT - player_height - 10
        
        # Inicializar obstáculos iniciales
        for _ in range(self.current_obstacle_count):
            self.spawn_obstacle(random_position=True)
    
    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and self.current_question:
                if event.key == pygame.K_t:
                    self.handle_answer(True)
                elif event.key == pygame.K_f:
                    self.handle_answer(False)
        return True
    
    def handle_player_movement(self):
        """Maneja el movimiento del jugador"""
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
        """Crea un obstáculo en una posición aleatoria"""
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
        
    def update_obstacles(self, speed: int):
        """Actualiza la posición de los obstáculos y genera nuevos"""
        # Actualizar posición de obstáculos existentes
        for obstacle in self.obstacles[:]:
            obstacle.y += speed
            if obstacle.y > self.config.SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
                self.score += 10
                if self.score % 100 == 0:
                    self.level_up()
        
        # Verificar si necesitamos más obstáculos
        if len(self.obstacles) < self.current_obstacle_count:
            self.spawn_delay_counter += 1
            if self.spawn_delay_counter >= self.config.OBSTACLE_SPAWN_DELAY:
                self.spawn_obstacle()
                self.spawn_delay_counter = 0
    def level_up(self):
        """Aumenta la dificultad en cada nivel"""
        self.level += 1
        self.config.OBSTACLE_SPEEDS["correct"] += 1
        
        # Aumentar el número de obstáculos hasta el máximo permitido
        if self.current_obstacle_count < self.config.MAX_OBSTACLE_COUNT:
            self.current_obstacle_count += 1
        
        # Reducir el delay de spawn conforme aumenta el nivel
        if self.config.OBSTACLE_SPAWN_DELAY > 15:
            self.config.OBSTACLE_SPAWN_DELAY -= 2
        
    def check_collisions(self):
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
        return any(obstacle.colliderect(player_rect) for obstacle in self.obstacles)
    
    def draw(self):
        if not hasattr(self, 'assets') or not self.assets.images:
            self.screen.fill((0, 0, 0))
            return
        
        # Dibujar fondo adaptado a la pantalla
        background = self.assets.images.get("background")
        if background:
            # Escalar el fondo al tamaño de la pantalla si no coincide
            if background.get_size() != (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT):
                background = pygame.transform.scale(background,(self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill((100, 100, 255))
        
        # Dibujar obstáculos
        obstacle_img = self.assets.images.get("obstacle")
        if obstacle_img:
            for obs in self.obstacles:
                self.screen.blit(obstacle_img, obs)
        
        # Dibujar jugador
        player_img = self.assets.images.get("player")
        if player_img:
            self.screen.blit(player_img, self.player_pos)
        
        # HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        level_text = font.render(f"Nivel: {self.level}", True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(level_text, (10, 90))
        
        if self.current_question:
            self.show_question()
        
        pygame.display.flip()

    def cleanup(self):
        """Limpia recursos y cierra pygame"""
        if hasattr(self, 'assets'):
            self.assets.images.clear()
        pygame.quit()

    def run(self):
        """Bucle principal del juego"""
        try:
            while self.running and self.lives > 0:
                self.running = self.handle_events()
                
                if not self.current_question:
                    self.handle_player_movement()
                    self.update_obstacles(self.config.OBSTACLE_SPEEDS["correct"])
                    
                    if self.check_collisions():
                        self.lives -= 1
                        if self.lives <= 0:
                            break
                        self.player_pos = [self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100]
                
                self.draw()
                self.clock.tick(self.config.FPS)
        finally:
            self.cleanup()

def inicio(categoria: str):
    """Función de inicio del juego"""
    try:
        if pygame.get_init():
            pygame.quit()
        juego = JuegoMejorado(categoria)
        juego.run()
    except Exception as e:
        print(f"Error en el juego: {e}")
    finally:
        pygame.quit()

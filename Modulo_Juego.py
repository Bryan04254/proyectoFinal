import pygame
import random
import os
from typing import Dict
from dataclasses import dataclass
from Modulo_Assets import AssetManager
from Jugador import GestorJugadores

@dataclass
class GameConfig:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    FPS: int = 60
    PLAYER_SPEED: int = 5
    INITIAL_OBSTACLE_COUNT: int = 3
    MAX_OBSTACLE_COUNT: int = 8
    OBSTACLE_SPAWN_DELAY: int = 30
    
    def __post_init__(self):
        self.OBSTACLE_SPEEDS = {
            "correct": 5,
            "incorrect": 8
        }

class JuegoMejorado:
    def __init__(self, categoria: str = "default", nombre_jugador: str = None):
        # Asegurarnos de que pygame está inicializado correctamente
        if pygame.get_init():
            pygame.quit()
        pygame.init()
        
        # Inicializar atributos básicos
        self.running = True
        self.categoria = categoria.lower()
        self.nombre_jugador = nombre_jugador
        
        # Configuración básica
        self.config = GameConfig()
        self.clock = pygame.time.Clock()
        
        # Inicializar la pantalla
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption(f"Juego - {categoria}")
        
        # Estado del juego
        self.score = 0
        self.lives = 3
        self.level = 1
        self.current_obstacle_count = self.config.INITIAL_OBSTACLE_COUNT
        self.spawn_delay_counter = 0
        self.obstacles = []
        self.current_question = None
        
        # Sistema de jugadores
        if nombre_jugador:
            self.gestor_jugadores = GestorJugadores()
            jugador = self.gestor_jugadores.obtener_jugador(nombre_jugador)
            if jugador and self.categoria in jugador.progreso:
                ultimo_progreso = jugador.progreso[self.categoria][-1]
                self.score = ultimo_progreso.puntos
                self.level = ultimo_progreso.nivel
        
        # Asegurarse de que existe la estructura de carpetas
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, "assets", self.categoria)
        os.makedirs(assets_path, exist_ok=True)
        
        # Cargar assets
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
            
            # Crear obstáculos iniciales
            for _ in range(self.current_obstacle_count):
                self.spawn_obstacle(random_position=True)
                
        except Exception as e:
            print(f"Error al cargar assets: {e}")
            self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.current_question:
                if event.key == pygame.K_t:
                    self.handle_answer(True)
                elif event.key == pygame.K_f:
                    self.handle_answer(False)
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
            obstacle.y += self.config.OBSTACLE_SPEEDS["correct"]
            if obstacle.y > self.config.SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
                self.score += 10
                if self.score % 100 == 0:
                    self.level += 1
        
        if len(self.obstacles) < self.current_obstacle_count:
            self.spawn_delay_counter += 1
            if self.spawn_delay_counter >= self.config.OBSTACLE_SPAWN_DELAY:
                self.spawn_obstacle()
                self.spawn_delay_counter = 0

    def check_collisions(self):
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
        return any(obstacle.colliderect(player_rect) for obstacle in self.obstacles)

    def draw(self):
        # Dibujar fondo
        background = self.assets.images.get("background")
        if background:
            scaled_background = pygame.transform.scale(background, 
                (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            self.screen.blit(scaled_background, (0, 0))
        else:
            self.screen.fill((100, 100, 255))
        
        # Dibujar obstáculos
        obstacle_img = self.assets.images.get("obstacle")
        if obstacle_img:
            for obs in self.obstacles:
                self.screen.blit(obstacle_img, obs)
        else:
            for obs in self.obstacles:
                pygame.draw.rect(self.screen, (255, 0, 0), obs)
        
        # Dibujar jugador
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
        level_text = font.render(f"Nivel: {self.level}", True, (255, 255, 255))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(level_text, (10, 90))
        
        pygame.display.flip()

    def guardar_progreso(self):
        if self.nombre_jugador:
            try:
                self.gestor_jugadores.actualizar_progreso(
                    nombre_jugador=self.nombre_jugador,
                    categoria=self.categoria,
                    puntos=self.score,
                    nivel=self.level
                )
            except Exception as e:
                print(f"Error al guardar progreso: {e}")

    def cleanup(self):
        self.guardar_progreso()
        if hasattr(self, 'assets'):
            self.assets.images.clear()
        pygame.quit()

    def run(self):
        while self.running and self.lives > 0:
            self.handle_events()
            
            if not self.current_question:
                self.handle_player_movement()
                self.update_obstacles()
                
                if self.check_collisions():
                    self.lives -= 1
                    if self.lives <= 0:
                        break
                    self.player_pos = [
                        self.config.SCREEN_WIDTH // 2, 
                        self.config.SCREEN_HEIGHT - 100
                    ]
            
            self.draw()
            self.clock.tick(self.config.FPS)
        
        self.cleanup()

def inicio(categoria: str = "default", nombre_jugador: str = None):
    """Función de inicio del juego"""
    try:
        juego = JuegoMejorado(categoria, nombre_jugador)
        juego.run()
    except Exception as e:
        print(f"Error en el juego: {e}")
        if pygame.get_init():
            pygame.quit()
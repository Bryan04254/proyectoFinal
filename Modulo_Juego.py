import pygame
import random
import os
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class GameConfig:
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    FPS: int = 60
    PLAYER_SPEED: int = 5
    OBSTACLE_SPEEDS: Dict[str, int] = None
    
    def __post_init__(self):
        self.OBSTACLE_SPEEDS = {
            "correct": 5,
            "incorrect": 8
        }

class AssetManager:
    def __init__(self, categoria: str):
        self.categoria = categoria
        self.images: Dict[str, pygame.Surface] = {}
        self._load_assets()
    
    def _load_assets(self):
        """Carga las imágenes según la categoría"""
        assets_path = os.path.join("assets", self.categoria.lower())
        try:
            # Cargar imagen del jugador
            player_path = os.path.join(assets_path, "player.png")
            self.images["player"] = pygame.image.load(player_path).convert_alpha()
            
            # Cargar obstáculos
            obstacle_path = os.path.join(assets_path, "obstacle.png")
            self.images["obstacle"] = pygame.image.load(obstacle_path).convert_alpha()
            
            # Cargar fondo
            background_path = os.path.join(assets_path, "background.png")
            self.images["background"] = pygame.image.load(background_path).convert()
        except pygame.error as e:
            print(f"Error cargando imágenes: {e}")
            # Crear superficies de color como respaldo
            self.images["player"] = self._create_colored_surface((50, 50), (0, 255, 0))
            self.images["obstacle"] = self._create_colored_surface((50, 30), (255, 0, 0))
            self.images["background"] = self._create_colored_surface((800, 600), (100, 100, 255))
    
    def _create_colored_surface(self, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
        """Crea una superficie coloreada como respaldo si no hay imágenes"""
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface

class JuegoMejorado:
    def __init__(self, categoria: str):
        pygame.init()
        self.config = GameConfig()
        self.assets = AssetManager(categoria)
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado del juego
        self.categoria = categoria
        self.score = 0
        self.lives = 3
        self.player_pos = [self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100]
        self.obstacles: List[pygame.Rect] = []
        self.current_question = None
        
        # Configuración del juego
        pygame.display.set_caption(f"Juego - {categoria}")
    
    def handle_events(self) -> bool:
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and self.current_question:
                if event.key == pygame.K_t:  # True
                    self.handle_answer(True)
                elif event.key == pygame.K_f:  # False
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
    
    def create_obstacle_row(self, direction: str) -> List[pygame.Rect]:
        """Crea una fila de obstáculos"""
        obstacles = []
        num_obstacles = random.randint(3, 6)
        total_width = num_obstacles * 100  # 100 = ancho del obstáculo + espacio
        start_x = (self.config.SCREEN_WIDTH - total_width) // 2
        
        for i in range(num_obstacles):
            x = start_x + i * 100
            y = -50  # Comienzan fuera de la pantalla
            obstacle = pygame.Rect(x, y, 50, 30)
            obstacles.append(obstacle)
        
        return obstacles
    
    def update_obstacles(self, speed: int):
        """Actualiza la posición de los obstáculos"""
        for obstacle in self.obstacles[:]:
            obstacle.y += speed
            if obstacle.y > self.config.SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
    
    def check_collisions(self) -> bool:
        """Verifica colisiones entre el jugador y los obstáculos"""
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
        return any(obstacle.colliderect(player_rect) for obstacle in self.obstacles)
    
    def show_question(self):
        """Muestra una pregunta en la pantalla"""
        if not self.current_question:
            return
        
        # Dibuja un fondo semi-transparente
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Renderiza el texto de la pregunta
        font = pygame.font.Font(None, 36)
        text = font.render(self.current_question.texto, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        # Instrucciones
        instructions = font.render("Presiona T para Verdadero, F para Falso", True, (255, 255, 255))
        inst_rect = instructions.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2 + 50))
        self.screen.blit(instructions, inst_rect)
    
    def handle_answer(self, answer: bool):
        """Maneja la respuesta a una pregunta"""
        is_correct = random.choice([True, False])  # Simulado - implementar lógica real
        if is_correct:
            self.score += 1
            self.start_obstacle_challenge(True)
        else:
            self.start_obstacle_challenge(False)
        self.current_question = None
    
    def start_obstacle_challenge(self, was_correct: bool):
        """Inicia un desafío de obstáculos basado en si la respuesta fue correcta"""
        num_rows = 5 if was_correct else 10
        speed = self.config.OBSTACLE_SPEEDS["correct" if was_correct else "incorrect"]
        
        for _ in range(num_rows):
            direction = random.choice(["left", "right"])
            self.obstacles.extend(self.create_obstacle_row(direction))
    
    def draw(self):
        """Dibuja todos los elementos del juego"""
        # Dibuja el fondo
        self.screen.blit(self.assets.images["background"], (0, 0))
        
        # Dibuja el jugador
        self.screen.blit(self.assets.images["player"], self.player_pos)
        
        # Dibuja los obstáculos
        for obstacle in self.obstacles:
            self.screen.blit(self.assets.images["obstacle"], obstacle)
        
        # Dibuja el HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        # Si hay una pregunta activa, muéstrala
        if self.current_question:
            self.show_question()
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal del juego"""
        while self.running and self.lives > 0:
            self.running = self.handle_events()
            
            if not self.current_question:
                self.handle_player_movement()
                self.update_obstacles(self.config.OBSTACLE_SPEEDS["correct"])
                
                if self.check_collisions():
                    self.lives -= 1
                    if self.lives <= 0:
                        break
                    # Reinicia la posición del jugador
                    self.player_pos = [self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100]
            
            self.draw()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()

def inicio(categoria: str):
    """Función de inicio para el juego"""
    juego = JuegoMejorado(categoria)
    juego.run()
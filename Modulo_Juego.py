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

class JuegoMejorado:
    def __init__(self, categoria: str):
        # Asegurar limpieza de instancia previa
        if pygame.get_init():
            pygame.quit()
        pygame.init()
        
        # Inicializar pantalla
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"Juego - {categoria}")
        
        # Limpiar pantalla inmediatamente
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        
        # Configuración
        self.config = GameConfig()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado del juego
        self.categoria = categoria
        self.score = 0
        self.lives = 3
        self.player_pos = [self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100]
        self.obstacles = []
        self.current_question = None
        
        # Cargar assets después de la limpieza
        from Modulo_Assets import AssetManager
        self.assets = AssetManager(categoria)
    
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
    
    def update_obstacles(self, speed: int):
        for obstacle in self.obstacles[:]:
            obstacle.y += speed
            if obstacle.y > self.config.SCREEN_HEIGHT:
                self.obstacles.remove(obstacle)
    
    def check_collisions(self):
        player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
        return any(obstacle.colliderect(player_rect) for obstacle in self.obstacles)
    
    def draw(self):
        # Verificar que tenemos assets antes de dibujar
        if not hasattr(self, 'assets') or not self.assets.images:
            self.screen.fill((0, 0, 0))
            return
        
        # Dibujar fondo
        background = self.assets.images.get("background")
        if background:
            self.screen.blit(background, (0, 0))
        else:
            self.screen.fill((100, 100, 255))
        
        # Dibujar jugador
        player = self.assets.images.get("player")
        if player:
            self.screen.blit(player, self.player_pos)
        
        # Dibujar obstáculos
        obstacle = self.assets.images.get("obstacle")
        if obstacle:
            for obs in self.obstacles:
                self.screen.blit(obstacle, obs)
        
        # HUD
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
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
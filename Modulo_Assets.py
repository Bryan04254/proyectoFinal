import os
import pygame
from typing import Dict, Tuple


class AssetManager:
    def __init__(self, categoria):
        self.categoria = categoria
        self.assets_path = os.path.join("assets", categoria.lower())

    def verificar_assets(self):
        """Verifica si todos los archivos de assets existen"""
        for asset in ["player.png", "obstacle.png", "background.png"]:
            file_path = os.path.join(self.assets_path, asset)
            if not os.path.exists(file_path):
                print(f"El archivo {file_path} no existe.")
    
    def _create_asset_structure(self):
        """Crea la estructura de carpetas necesaria para los assets"""
        # Crear carpeta principal de assets si no existe
        if not os.path.exists("assets"):
            os.makedirs("assets")
            
        # Crear carpeta para cada categoría
        categorias = ["ciudad", "granja", "bosque", "espacio", "marte"]
        for cat in categorias:
            categoria_path = os.path.join("assets", cat.lower())
            if not os.path.exists(categoria_path):
                os.makedirs(categoria_path)
                
                # Crear imágenes por defecto para cada categoría
                self._create_default_images(categoria_path)
    
    def _create_default_images(self, categoria_path: str):
        """Crea imágenes por defecto para una categoría"""
        # Dimensiones por defecto
        player_size = (50, 50)
        obstacle_size = (50, 30)
        background_size = (800, 600)
        
        # Crear imagen del jugador (verde)
        self._create_colored_surface(
            os.path.join(categoria_path, "player.png"),
            player_size,
            (0, 255, 0)
        )
        
        # Crear imagen del obstáculo (rojo)
        self._create_colored_surface(
            os.path.join(categoria_path, "obstacle.png"),
            obstacle_size,
            (255, 0, 0)
        )
        
        # Crear imagen del fondo (azul claro)
        self._create_colored_surface(
            os.path.join(categoria_path, "background.png"),
            background_size,
            (100, 100, 255)
        )
    
    def _create_colored_surface(self, path: str, size: Tuple[int, int], color: Tuple[int, int, int]):
        """Crea y guarda una superficie coloreada como imagen PNG"""
        surface = pygame.Surface(size)
        surface.fill(color)
        pygame.image.save(surface, path)
    
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
            
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error cargando imágenes: {e}")
            print("Creando superficies de color por defecto...")
            
            # Crear superficies de color como respaldo
            self.images["player"] = self._create_colored_surface_memory((50, 50), (0, 255, 0))
            self.images["obstacle"] = self._create_colored_surface_memory((50, 30), (255, 0, 0))
            self.images["background"] = self._create_colored_surface_memory((800, 600), (100, 100, 255))
    
    def _create_colored_surface_memory(self, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
        """Crea una superficie coloreada en memoria"""
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface
# Inicializar pygame primero
pygame.init()

# Crear el asset manager para una categoría
asset_manager = AssetManager("ciudad")
import pygame
import os
from PIL import Image  
from typing import Dict, Tuple, Optional

class AssetManager:
     def __init__(self, categoria: str):
        self.categoria = categoria.lower()  # Aseguramos que esté en minúsculas
        self.images: Dict[str, pygame.Surface] = {}
        self.cache: Dict[str, pygame.Surface] = {}
        
        # Obtener la ruta base del script actual
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, "assets", self.categoria)
        
        # Crear estructura de carpetas si no existe
        self._create_asset_structure()
        # Cargar los assets
        self._load_assets()

     def scale_image(self, surface: pygame.Surface, new_width: Optional[int] = None, 
                new_height: Optional[int] = None, force_aspect_ratio: bool = True) -> pygame.Surface:
        """
        Escala una superficie de Pygame a nuevas dimensiones
        """
        # Convertir pygame Surface a PIL Image para mejor manejo del escalado
        temp_string = pygame.image.tostring(surface, 'RGBA')
        temp_pil_image = Image.frombytes('RGBA', surface.get_size(), temp_string)
        
        original_width, original_height = temp_pil_image.size

        if force_aspect_ratio:
            if new_width and new_height:
                width_ratio = new_width / original_width
                height_ratio = new_height / original_height
                ratio = min(width_ratio, height_ratio)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            elif new_width:
                ratio = new_width / original_width
                new_height = int(original_height * ratio)
            elif new_height:
                ratio = new_height / original_height
                new_width = int(original_width * ratio)
            else:
                return surface

        # Escalar la imagen usando PIL
        temp_pil_image = temp_pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convertir de vuelta a pygame Surface
        mode = temp_pil_image.mode
        size = temp_pil_image.size
        data = temp_pil_image.tobytes()
        
        new_surface = pygame.image.fromstring(data, size, mode)
        return new_surface

     def _load_assets(self):
        """Carga y escala las imágenes según la categoría"""
        try:
            # Cargar y escalar imagen del jugador (50x50)
            player_path = os.path.join(self.assets_path, "player.png")
            pil_image = Image.open(player_path)
            player_img = self._pil_to_pygame(pil_image)
            self.images["player"] = self.scale_image(player_img, 50, 50)

            # Cargar y escalar obstáculos (50x30)
            obstacle_path = os.path.join(self.assets_path, "obstacle.png")
            pil_image = Image.open(obstacle_path)
            obstacle_img = self._pil_to_pygame(pil_image)
            self.images["obstacle"] = self.scale_image(obstacle_img, 50, 30)

            # Cargar y escalar fondo (800x600)
            background_path = os.path.join(self.assets_path, "background.png")
            pil_image = Image.open(background_path)
            background_img = self._pil_to_pygame(pil_image)
            self.images["background"] = self.scale_image(background_img, 800, 600)

        except (pygame.error, FileNotFoundError) as e:
            print(f"Error cargando imágenes: {e}")
            print("Creando superficies de color por defecto...")
            self.images["player"] = self._create_colored_surface((50, 50), (0, 255, 0))
            self.images["obstacle"] = self._create_colored_surface((50, 30), (255, 0, 0))
            self.images["background"] = self._create_colored_surface((800, 600), (100, 100, 255))

     def _pil_to_pygame(self, pil_image: Image.Image) -> pygame.Surface:
        """Convierte una imagen PIL a superficie de Pygame"""
        if pil_image.mode in ('RGBA', 'LA') or (pil_image.mode == 'P' and 'transparency' in pil_image.info):
            pil_image = pil_image.convert('RGBA')
        else:
            pil_image = pil_image.convert('RGB')
            
        return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

     def _create_colored_surface(self, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
        """Crea una superficie coloreada como respaldo"""
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface

    
     def _create_asset_structure(self):
        """Crea la estructura de carpetas necesaria para los assets"""
        # Crear directorio principal de assets si no existe
        assets_dir = os.path.join(self.base_path, "assets")
        os.makedirs(assets_dir, exist_ok=True)

        # Crear directorios para cada categoría
        categorias = ["granja", "bosque", "ciudad", "espacio", "marte"]
        for cat in categorias:
            cat_path = os.path.join(assets_dir, cat)
            if not os.path.exists(cat_path):
                os.makedirs(cat_path)
                print(f"Creando directorio: {cat_path}")
                self._create_default_images(cat_path)
     def _create_default_images(self, categoria_path: str):
        """Crea imágenes por defecto para una categoría"""
        print(f"Creando imágenes por defecto en: {categoria_path}")
        for name, size, color in [
            ("player", (50, 50), (0, 255, 0)),      # Verde
            ("obstacle", (50, 30), (255, 0, 0)),    # Rojo
            ("background", (800, 600), (100, 100, 255))  # Azul claro
        ]:
            try:
                image_path = os.path.join(categoria_path, f"{name}.png")
                if not os.path.exists(image_path):
                    image = Image.new('RGB', size, color)
                    image.save(image_path)
                    print(f"Creada imagen: {image_path}")
            except Exception as e:
                print(f"Error creando imagen {name}: {e}")

     def get_scaled_image(self, image_name: str, scale_factor: float) -> pygame.Surface:
        """Obtiene una imagen escalada por un factor"""
        cache_key = f"{image_name}_{scale_factor}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        original = self.images.get(image_name)
        if original is None:
            raise KeyError(f"Image {image_name} not found")

        new_width = int(original.get_width() * scale_factor)
        new_height = int(original.get_height() * scale_factor)
        scaled = self.scale_image(original, new_width, new_height)
        self.cache[cache_key] = scaled
        return scaled

def inicio(categoria: str = None):
    """Función de inicio para verificar y crear assets"""
    if not pygame.get_init():
        pygame.init()
    return AssetManager(categoria.lower() if categoria else "default")
from typing import List, Dict
from typing import Optional
from dataclasses import dataclass
from Modulo_creacionDelArbol import NodoArbol, construir_arbol_balanceado, Pregunta
import random 
import json
from pathlib import Path

@dataclass
class CategoriaPreguntas:
    nombre: str
    preguntas: List[str]

PREGUNTAS_POR_CATEGORIA: Dict[str, List[str]] = {
    "Granja": [
        "¿Cuál es el animal que pone huevos?",
        "¿Qué alimento producen las vacas?",
        "¿Qué animal nos da lana?",
        # ... más preguntas de granja
    ],
    "Bosque": [
        "¿Qué árbol produce bellotas?",
        "¿Qué animal hiberna en invierno?",
        "¿Qué hongo es venenoso?",
        # ... más preguntas de bosque
    ],
    # ... otras categorías
}
def generar_arbol_por_categoria(categoria: str) -> NodoArbol:
    """Genera el árbol de preguntas para la categoría dada."""
    # Este método utiliza la función construir_arbol_balanceado
    return construir_arbol_balanceado(crear_preguntas_por_categoria(categoria))

def obtener_pregunta_por_dificultad(nodo: Optional[NodoArbol], dificultad: int) -> Optional[Pregunta]:
    """
    Obtiene una pregunta del árbol basada en el nivel de dificultad.
    
    Args:
        nodo: Nodo actual del árbol.
        dificultad: Nivel de dificultad deseado (nivel en el árbol).
        
    Returns:
        Pregunta correspondiente o None si no se encuentra.
    """
    def buscar_pregunta(nodo_actual: Optional[NodoArbol], nivel_actual: int) -> Optional[Pregunta]:
        if not nodo_actual or nivel_actual > dificultad:
            return None

        if nivel_actual == dificultad:
            return nodo_actual.pregunta

        # Intentar en ambos subárboles
        pregunta = buscar_pregunta(nodo_actual.izquierdo, nivel_actual + 1)
        if not pregunta:
            pregunta = buscar_pregunta(nodo_actual.derecho, nivel_actual + 1)
        return pregunta

    return buscar_pregunta(nodo, 1)

# Otros métodos como `construir_arbol_balanceado` y `crear_preguntas_por_categoria` se encuentran en sus respectivos módulos.

def crear_preguntas_por_categoria(categoria: str) -> List[Pregunta]:
    """
    Genera una lista de preguntas específicas para una categoría.
    
    Args:
        categoria (str): Nombre de la categoría de preguntas
        
    Returns:
        List[Pregunta]: Lista de preguntas para la categoría
        
    Raises:
        ValueError: Si la categoría no existe
    """
    if categoria not in PREGUNTAS_POR_CATEGORIA:
        raise ValueError(f"Categoría '{categoria}' no encontrada")
        
    preguntas_texto = PREGUNTAS_POR_CATEGORIA[categoria]
    preguntas = [Pregunta(texto=texto) for texto in preguntas_texto]
    random.shuffle(preguntas)
    return preguntas

def generar_arbol_por_categoria(categoria: str) -> NodoArbol:
    """
    Crea un árbol binario balanceado de preguntas para una categoría.
    
    Args:
        categoria (str): Nombre de la categoría
        
    Returns:
        NodoArbol: Raíz del árbol de preguntas
    """
    preguntas = crear_preguntas_por_categoria(categoria)
    return construir_arbol_balanceado(preguntas)
class EstadisticasCategoria:
    def __init__(self, categoria: str):
        self.categoria = categoria
        self.preguntas_respondidas = 0
        self.respuestas_correctas = 0
        self.mejor_racha = 0
        self.racha_actual = 0
        
    def registrar_respuesta(self, correcta: bool) -> None:
        """Registra una respuesta y actualiza las estadísticas."""
        self.preguntas_respondidas += 1
        if correcta:
            self.respuestas_correctas += 1
            self.racha_actual += 1
            self.mejor_racha = max(self.mejor_racha, self.racha_actual)
        else:
            self.racha_actual = 0
            
    @property
    def porcentaje_aciertos(self) -> float:
        """Calcula el porcentaje de respuestas correctas."""
        if self.preguntas_respondidas == 0:
            return 0.0
        return (self.respuestas_correctas / self.preguntas_respondidas) * 100
class GestorPreguntas:
        
    def __init__(self, categoria: str):
        self.categoria = categoria
        self.arbol = generar_arbol_por_categoria(categoria)
        self.estadisticas = EstadisticasCategoria(categoria)
        self.nivel_dificultad = 1
        
    def obtener_siguiente_pregunta(self) -> Pregunta:
        """
        Selecciona la siguiente pregunta basada en el rendimiento del jugador.
        """
        # Ajustar dificultad basada en el porcentaje de aciertos
        if self.estadisticas.porcentaje_aciertos > 80:
            self.nivel_dificultad = min(self.nivel_dificultad + 1, 3)
        elif self.estadisticas.porcentaje_aciertos < 40:
            self.nivel_dificultad = max(self.nivel_dificultad - 1, 1)
            
        # Seleccionar pregunta según nivel de dificultad
        pregunta = obtener_pregunta_por_dificultad(self.arbol, self.nivel_dificultad)
        return pregunta



def guardar_progreso(categoria: str, estadisticas: EstadisticasCategoria) -> None:
    """Guarda el progreso del jugador en un archivo JSON."""
    datos = {
        "categoria": categoria,
        "preguntas_respondidas": estadisticas.preguntas_respondidas,
        "respuestas_correctas": estadisticas.respuestas_correctas,
        "mejor_racha": estadisticas.mejor_racha
    }
    
    ruta = Path(f"progreso_{categoria.lower()}.json")
    with ruta.open("w") as f:
        json.dump(datos, f, indent=4)
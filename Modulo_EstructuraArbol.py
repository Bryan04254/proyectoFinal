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
        Pregunta("¿Qué alimento da la vaca?", "Leche", 1),
        Pregunta("¿Qué animal pone huevos?", "Gallina", 1),
        Pregunta("¿Qué animal nos da lana?", "Oveja", 2),
        Pregunta("¿Qué cultivo es típico de una granja?", "Maíz", 2),
        Pregunta("¿Qué herramienta usa un granjero para arar?", "Tractor", 3),
        Pregunta("¿Qué proceso transforma la leche?", "Pasteurización", 4),
        Pregunta("¿Qué técnica mejora la fertilidad del suelo?", "Rotación de cultivos", 5),
    ],
    "Bosque": [
        Pregunta("¿Qué árbol produce bellotas?", "Roble", 1),
        Pregunta("¿Qué animal hiberna en invierno?", "Oso", 1),
        Pregunta("¿Qué hongo crece en los bosques?", "Champiñón", 2),
        Pregunta("¿Qué ave habita en bosques?", "Búho", 2),
        Pregunta("¿Qué proceso natural renuevan los bosques?", "Fotosíntesis", 3),
        Pregunta("¿Qué tipo de ecosistema es un bosque?", "Terrestre", 4),
        Pregunta("¿Qué proceso ayuda a la conservación forestal?", "Reforestación", 5),
    ],
    "Ciudad": [
        Pregunta("¿Qué transporte público común hay?", "Autobús", 1),
        Pregunta("¿Qué profesional ayuda en emergencias?", "Policía", 1),
        Pregunta("¿Qué construcción es un servicio público?", "Hospital", 2),
        Pregunta("¿Qué infraestructura conecta ciudades?", "Carretera", 2),
        Pregunta("¿Qué sistema organiza el tráfico?", "Semáforos", 3),
        Pregunta("¿Qué proceso mejora el medio urbano?", "Reciclaje", 4),
        Pregunta("¿Qué modelo urbano reduce contaminación?", "Ciudad sostenible", 5),
    ],
    "Espacio": [
        Pregunta("¿Qué planeta está más cerca del Sol?", "Mercurio", 1),
        Pregunta("¿Qué satélite orbita la Tierra?", "Luna", 1),
        Pregunta("¿Qué estudia el universo?", "Astronomía", 2),
        Pregunta("¿Qué vehículo explora el espacio?", "Nave espacial", 2),
        Pregunta("¿Qué fenómeno crea agujeros negros?", "Gravedad extrema", 3),
        Pregunta("¿Qué permite viajar entre planetas?", "Propulsión", 4),
        Pregunta("¿Qué teoría explica el origen del universo?", "Big Bang", 5),
    ],
    "Marte": [
        Pregunta("¿De qué color es Marte?", "Rojo", 1),
        Pregunta("¿Qué planeta está antes de Marte?", "Tierra", 1),
        Pregunta("¿Qué misión exploró Marte?", "Mars Rover", 2),
        Pregunta("¿Qué elemento es esencial para vida?", "Agua", 2),
        Pregunta("¿Qué condición atmosférica tiene Marte?", "Fría", 3),
        Pregunta("¿Qué desafío tiene explorar Marte?", "Radiación", 4),
        Pregunta("¿Qué tecnología permitiría colonizar Marte?", "Terraformación", 5),
    ]
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
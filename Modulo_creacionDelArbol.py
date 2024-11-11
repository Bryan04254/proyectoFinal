import random
from typing import Optional

class Pregunta:
    """
    Representa una pregunta con su texto y estadísticas de respuestas.
    
    Attributes:
        texto (str): El texto de la pregunta
        peso (int): Peso actual de la pregunta basado en respuestas
        correctas (int): Número de respuestas correctas
        incorrectas (int): Número de respuestas incorrectas
    """
    def __init__(self, texto: str) -> None:
        self.texto = texto
        self.peso = 0
        self.correctas = 0
        self.incorrectas = 0

    def registrar_respuesta(self, correcta: bool) -> None:
        """
        Registra una respuesta y ajusta el peso de la pregunta.
        
        Args:
            correcta (bool): Si la respuesta fue correcta
        """
        if correcta:
            self.correctas += 1
            self.peso = max(0, self.peso - 1) 
        else:
            self.incorrectas += 1
            self.peso += 1  


    def __repr__(self):
        return f"Pregunta('{self.texto}', peso={self.peso})"

class NodoArbol:
    def __init__(self, pregunta: Pregunta) -> None:
        self.pregunta = pregunta
        self.izquierdo = None
        self.derecho = None
        
    def es_hoja(self) -> bool:
        """Verifica si el nodo es una hoja."""
        return self.izquierdo is None and self.derecho is None
    
    def altura(self) -> int:
        """Calcula la altura del subárbol desde este nodo."""
        altura_izq = self.izquierdo.altura() if self.izquierdo else 0
        altura_der = self.derecho.altura() if self.derecho else 0
        return max(altura_izq, altura_der) + 1


def construir_arbol_balanceado(preguntas):
    preguntas_ordenadas = sorted(preguntas, key=lambda x: x.peso)

    def construir_balanceado(inicio, fin):
        if inicio > fin:
            return None

        medio = (inicio + fin) // 2
        nodo = NodoArbol(preguntas_ordenadas[medio])

        nodo.izquierdo = construir_balanceado(inicio, medio - 1)
        nodo.derecho = construir_balanceado(medio + 1, fin)
        
        return nodo

    return construir_balanceado(0, len(preguntas_ordenadas) - 1)

def obtener_pregunta_aleatoria(nodo: Optional[NodoArbol], bias: float = 0.5) -> Optional[Pregunta]:
    """
    Selecciona una pregunta aleatoria del árbol con sesgo hacia preguntas con mayor peso.
    
    Args:
        nodo: Nodo actual del árbol
        bias: Probabilidad de seleccionar preguntas con mayor peso (0.0-1.0)
        
    Returns:
        Pregunta seleccionada o None si el árbol está vacío
    """
    if nodo is None:
        return None
    
    if random.random() < bias:
        # Favorecer preguntas con mayor peso
        if nodo.derecho is not None:
            return obtener_pregunta_aleatoria(nodo.derecho, bias)
    
    direction = random.choice(["left", "right", "stay"])
    if direction == "left" and nodo.izquierdo is not None:
        return obtener_pregunta_aleatoria(nodo.izquierdo, bias)
    elif direction == "right" and nodo.derecho is not None:
        return obtener_pregunta_aleatoria(nodo.derecho, bias)
    return nodo.pregunta
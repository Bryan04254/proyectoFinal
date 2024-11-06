import random

# Clase para representar cada pregunta con su peso
class Pregunta:
    def __init__(self, texto):
        self.texto = texto
        self.peso = 0
        self.correctas = 0
        self.incorrectas = 0

    def registrar_respuesta(self, correcta):
        """Ajusta el peso según la respuesta: aumenta si es incorrecta, disminuye si es correcta."""
        if correcta:
            self.correctas += 1
            self.peso = max(0, self.peso - 1)  # Disminuir peso, evitando que sea negativo
        else:
            self.incorrectas += 1
            self.peso += 1  # Aumenta el peso si es incorrecta

    def __repr__(self):
        return f"Pregunta('{self.texto}', peso={self.peso})"


# Clase Nodo del Árbol Binario
class NodoArbol:
    def __init__(self, pregunta):
        self.pregunta = pregunta
        self.izquierdo = None
        self.derecho = None

# Función para construir un árbol balanceado basado en los pesos de las preguntas
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

# Función para obtener una pregunta del árbol
def obtener_pregunta_aleatoria(nodo):
    """Recorre el árbol para seleccionar una pregunta aleatoria."""
    if nodo is None:
        return None

    # Elegir aleatoriamente si ir a la izquierda o derecha
    direction = random.choice(["left", "right", "stay"])
    if direction == "left" and nodo.izquierdo is not None:
        return obtener_pregunta_aleatoria(nodo.izquierdo)
    elif direction == "right" and nodo.derecho is not None:
        return obtener_pregunta_aleatoria(nodo.derecho)
    else:
        return nodo.pregunta

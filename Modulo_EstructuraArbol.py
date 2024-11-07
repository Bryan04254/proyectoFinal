import random
from Modulo_creacionDelArbol import Pregunta, NodoArbol, construir_arbol_balanceado

def crear_preguntas_por_categoria(categoria):
    """Genera una lista de 32 preguntas específicas para cada categoría."""
    preguntas = []
    for i in range(32):
        texto_pregunta = f"Pregunta {i + 1} de {categoria}"
        preguntas.append(Pregunta(texto_pregunta))
    return preguntas

def generar_arbol_por_categoria(categoria):
    """Crea un árbol binario balanceado de preguntas para una categoría dada."""
    preguntas = crear_preguntas_por_categoria(categoria)
    return construir_arbol_balanceado(preguntas)

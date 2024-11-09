import random
from Modulo_creacionDelArbol import Pregunta, NodoArbol, construir_arbol_balanceado

def crear_preguntas_por_categoria(categoria):
    """Genera una lista de 32 preguntas específicas para cada categoría."""
    preguntas = []
    for i in range(32):
        texto_pregunta = f"Pregunta {i + 1} de {categoria}"
        preguntas.append(Pregunta(texto=texto_pregunta))  # Crear una instancia de Pregunta con el texto
    random.shuffle(preguntas)  # Mezcla las preguntas para obtener aleatoriedad
    return preguntas

def generar_arbol_por_categoria(categoria):
    """Crea un árbol binario balanceado de preguntas para una categoría dada."""
    preguntas = crear_preguntas_por_categoria(categoria)
    arbol = construir_arbol_balanceado(preguntas)  # Crear el árbol balanceado con las preguntas
    return arbol


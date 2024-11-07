import random
from Modulo_EstructuraArbol import generar_arbol_por_categoria

def seleccionar_preguntas_para_partida(arbol):
    """Selecciona 5 preguntas balanceadas de diferentes niveles del árbol."""
    preguntas_seleccionadas = []

    def seleccionar_desde_nivel(nodo, nivel, max_niveles):
        """Función recursiva para seleccionar preguntas de diferentes niveles."""
        if nodo is None or len(preguntas_seleccionadas) >= 5:
            return
        
        # Nivel 1: Seleccionar la raíz
        if nivel == 1:
            preguntas_seleccionadas.append(nodo.pregunta)
        
        # Niveles siguientes: seleccionar balanceado de subárboles izquierdo y derecho
        else:
            if random.choice([True, False]):
                seleccionar_desde_nivel(nodo.izquierdo, nivel + 1, max_niveles)
            else:
                seleccionar_desde_nivel(nodo.derecho, nivel + 1, max_niveles)

        # Después de completar el subárbol, añade la raíz si aún falta para completar 5 preguntas
        if len(preguntas_seleccionadas) < 5 and nivel <= max_niveles:
            preguntas_seleccionadas.append(nodo.pregunta)

    # Iniciar la selección de preguntas desde el nivel 1 (raíz)
    seleccionar_desde_nivel(arbol, 1, 5)
    return preguntas_seleccionadas

def iniciar_partida(categoria):
    """Inicia una partida para la categoría dada, seleccionando preguntas balanceadas."""
    arbol = generar_arbol_por_categoria(categoria)
    preguntas = seleccionar_preguntas_para_partida(arbol)
    print(f"Preguntas seleccionadas para la partida en {categoria}:")
    for pregunta in preguntas:
        print(f"- {pregunta.texto}")

    return preguntas

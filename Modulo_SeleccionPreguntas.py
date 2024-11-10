from typing import List, Optional
from dataclasses import dataclass
import random
from Modulo_EstructuraArbol import generar_arbol_por_categoria, Pregunta, NodoArbol

@dataclass
class ConfiguracionPartida:
    """Configuración para una partida de preguntas."""
    num_preguntas: int = 5
    niveles_max: int = 5
    balanceo_dificultad: bool = True
    permitir_repeticion: bool = False

class SelectorPreguntas:
    """Clase para manejar la selección de preguntas en una partida."""
    
    def __init__(self, categoria: str, config: Optional[ConfiguracionPartida] = None):
        self.categoria = categoria
        self.config = config or ConfiguracionPartida()
        self.arbol = generar_arbol_por_categoria(categoria)
        self.preguntas_usadas = set()
        
    def seleccionar_preguntas(self) -> List[Pregunta]:
        """
        Selecciona preguntas para la partida según la configuración.
        
        Returns:
            List[Pregunta]: Lista de preguntas seleccionadas
        """
        preguntas = []
        niveles_por_pregunta = self._distribuir_niveles()
        
        for nivel_objetivo in niveles_por_pregunta:
            pregunta = self._seleccionar_pregunta_nivel(nivel_objetivo)
            if pregunta:
                preguntas.append(pregunta)
                
        # Si no se completó el número deseado, rellenar con preguntas aleatorias
        while len(preguntas) < self.config.num_preguntas:
            pregunta = self._seleccionar_pregunta_aleatoria()
            if pregunta and (self.config.permitir_repeticion or 
                        pregunta not in self.preguntas_usadas):
                preguntas.append(pregunta)
                
        return preguntas
    
    def _distribuir_niveles(self) -> List[int]:
        """
        Distribuye las preguntas entre diferentes niveles de dificultad.
        
        Returns:
            List[int]: Lista de niveles objetivo para cada pregunta
        """
        if not self.config.balanceo_dificultad:
            return [random.randint(1, self.config.niveles_max) 
                    for _ in range(self.config.num_preguntas)]
            
        niveles = []
        preguntas_por_nivel = self.config.num_preguntas // self.config.niveles_max
        extras = self.config.num_preguntas % self.config.niveles_max
        
        for nivel in range(1, self.config.niveles_max + 1):
            niveles.extend([nivel] * preguntas_por_nivel)
            if extras > 0:
                niveles.append(nivel)
                extras -= 1
                
        random.shuffle(niveles)
        return niveles
    
    def _seleccionar_pregunta_nivel(self, nivel_objetivo: int) -> Optional[Pregunta]:
        """
        Selecciona una pregunta del nivel especificado.
        
        Args:
            nivel_objetivo: Nivel del árbol del que se desea obtener la pregunta
            
        Returns:
            Optional[Pregunta]: Pregunta seleccionada o None si no se encuentra
        """
        def _seleccionar_rec(nodo: Optional[NodoArbol], nivel_actual: int) -> Optional[Pregunta]:
            if not nodo or nivel_actual > nivel_objetivo:
                return None
                
            if nivel_actual == nivel_objetivo:
                if (self.config.permitir_repeticion or 
                    nodo.pregunta not in self.preguntas_usadas):
                    self.preguntas_usadas.add(nodo.pregunta)
                    return nodo.pregunta
                return None
                
            # Intentar ambos subárboles
            pregunta = _seleccionar_rec(nodo.izquierdo, nivel_actual + 1)
            if not pregunta:
                pregunta = _seleccionar_rec(nodo.derecho, nivel_actual + 1)
            return pregunta
            
        return _seleccionar_rec(self.arbol, 1)
    
    def _seleccionar_pregunta_aleatoria(self) -> Optional[Pregunta]:
        """
        Selecciona una pregunta aleatoria del árbol.
        
        Returns:
            Optional[Pregunta]: Pregunta seleccionada o None si no hay disponibles
        """
        def _seleccionar_rec(nodo: Optional[NodoArbol]) -> Optional[Pregunta]:
            if not nodo:
                return None
                
            if random.random() < 0.5:
                return nodo.pregunta
                
            subpregunta = _seleccionar_rec(nodo.izquierdo)
            if not subpregunta:
                subpregunta = _seleccionar_rec(nodo.derecho)
            return subpregunta
            
        return _seleccionar_rec(self.arbol)

def iniciar_partida(categoria: str, config: Optional[ConfiguracionPartida] = None) -> List[Pregunta]:
    """
    Inicia una nueva partida para la categoría especificada.
    
    Args:
        categoria: Categoría de preguntas
        config: Configuración opcional para la partida
        
    Returns:
        List[Pregunta]: Lista de preguntas seleccionadas para la partida
    """
    selector = SelectorPreguntas(categoria, config)
    preguntas = selector.seleccionar_preguntas()
    
    print(f"\nPartida iniciada en categoría: {categoria}")
    print(f"Preguntas seleccionadas:")
    for i, pregunta in enumerate(preguntas, 1):
        print(f"{i}. {pregunta.texto}")
        
    return preguntas
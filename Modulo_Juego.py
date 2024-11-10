import pygame
import random
from Modulo_EstructuraArbol import Pregunta
from Modulo_EstructuraArbol import generar_arbol_por_categoria
from Modulo_EstructuraArbol import crear_preguntas_por_categoria

class Juego:
    def __init__(self, categoria: str):
        pygame.init()
        self.categoria = categoria
        self.vidas = 3
        self.pantalla = pygame.display.set_mode((800, 600))
        self.reloj = pygame.time.Clock()
        self.posicion_jugador = [400, 550]
        self.arbol_preguntas = generar_arbol_por_categoria(categoria)
        self.preguntas_respondidas = 0

    def iniciar_juego(self):
        """Inicia el ciclo principal del juego, alternando entre preguntas y desafíos."""
        while self.vidas > 0:
            pregunta = self._obtener_pregunta()
            respuesta_correcta = self._mostrar_pregunta(pregunta)
            self.iniciar_desafio_esquivar(respuesta_correcta)
            if self.vidas <= 0:
                print("Has perdido todas tus vidas. Juego terminado.")
                break

    def _obtener_pregunta(self) -> Pregunta:
        """Obtiene la siguiente pregunta del árbol de preguntas."""
        return self.arbol_preguntas.obtener_siguiente_pregunta()

    def _mostrar_pregunta(self, pregunta: Pregunta) -> bool:
        """Muestra una pregunta al jugador y evalúa la respuesta."""
        print(pregunta.texto)
        respuesta = input("Respuesta (verdadero/falso): ").lower()
        correcta = respuesta == "verdadero"
        self.preguntas_respondidas += 1
        return correcta

    def iniciar_desafio_esquivar(self, respuesta_correcta: bool):
        """Inicia el desafío de esquivar obstáculos según si la respuesta fue correcta o incorrecta."""
        filas_a_esquivar = 5 if respuesta_correcta else 10
        velocidad_obstaculos = 5 if respuesta_correcta else 8
        self._correr_desafio(filas_a_esquivar, velocidad_obstaculos)

    def _correr_desafio(self, filas: int, velocidad: int):
        """Ejecuta el desafío donde el jugador debe esquivar filas de obstáculos."""
        direcciones = ["izquierda", "derecha"]
        for i in range(filas):
            direccion = random.choice(direcciones)
            if not self._esquivar_fila(direccion, velocidad):
                self.vidas -= 1
                print("Perdiste una vida.")
                if self.vidas == 0:
                    print("Juego terminado.")
                    return False
        return True

    def _esquivar_fila(self, direccion: str, velocidad: int) -> bool:
        """Simula el esquivar de una fila de obstáculos."""
        obstaculos = self._crear_fila_obstaculos(direccion)
        esquivado = False
        while not esquivado:
            self.pantalla.fill((0, 0, 0))
            self._manejar_movimiento_jugador()
            for obstaculo in obstaculos:
                obstaculo['rect'].move_ip(velocidad if direccion == "derecha" else -velocidad, 0)
                pygame.draw.rect(self.pantalla, obstaculo['color'], obstaculo['rect'])
                if obstaculo['rect'].colliderect(pygame.Rect(*self.posicion_jugador, 50, 50)):
                    return False
            pygame.display.flip()
            self.reloj.tick(30)
            esquivado = all(obstaculo['rect'].x < 0 or obstaculo['rect'].x > 800 for obstaculo in obstaculos)
        return True

    def _crear_fila_obstaculos(self, direccion: str):
        """Crea una fila de obstáculos con una dirección específica."""
        obstaculos = []
        for i in range(5):
            ancho, alto = random.randint(50, 100), 30
            x_pos = random.randint(0, 700)
            color = (255, 0, 0) if self.categoria == "Ciudad" else (139, 69, 19) if self.categoria == "Bosque" else (135, 206, 250)
            obstaculos.append({'rect': pygame.Rect(x_pos, i * 100, ancho, alto), 'color': color})
        return obstaculos

    def _manejar_movimiento_jugador(self):
        """Maneja el movimiento del jugador."""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.posicion_jugador[0] > 0:
            self.posicion_jugador[0] -= 5
        if teclas[pygame.K_RIGHT] and self.posicion_jugador[0] < 750:
            self.posicion_jugador[0] += 5
        if teclas[pygame.K_UP] and self.posicion_jugador[1] > 0:
            self.posicion_jugador[1] -= 5
        if teclas[pygame.K_DOWN] and self.posicion_jugador[1] < 550:
            self.posicion_jugador[1] += 5
        pygame.draw.rect(self.pantalla, (0, 255, 0), (*self.posicion_jugador, 50, 50))

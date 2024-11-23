from dataclasses import dataclass, asdict
from typing import Dict, List
import json
from pathlib import Path
import datetime

@dataclass
class Progreso:
    categoria: str
    puntos: int
    nivel: int
    fecha: str

@dataclass
class Jugador:
    nombre: str
    edad: int
    email: str
    fecha_registro: str
    progreso: Dict[str, List[Progreso]]

class GestorJugadores:
    def __init__(self):
        self.ruta_datos = Path("datos_jugadores")
        self.ruta_datos.mkdir(exist_ok=True)
        
    def registrar_jugador(self, nombre: str, edad: int, email: str) -> Jugador:
        """Registra un nuevo jugador en el sistema"""
        jugador = Jugador(
            nombre=nombre,
            edad=edad,
            email=email,
            fecha_registro=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            progreso={}
        )
        self._guardar_jugador(jugador)
        return jugador
    
    def actualizar_progreso(self, nombre_jugador: str, categoria: str, puntos: int, nivel: int):
        """Actualiza el progreso del jugador en una categoría específica"""
        jugador = self.obtener_jugador(nombre_jugador)
        if jugador:
            progreso = Progreso(
                categoria=categoria,
                puntos=puntos,
                nivel=nivel,
                fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            if categoria not in jugador.progreso:
                jugador.progreso[categoria] = []
            jugador.progreso[categoria].append(progreso)
            self._guardar_jugador(jugador)
    
    def obtener_jugador(self, nombre: str) -> Jugador:
        """Obtiene los datos de un jugador específico"""
        ruta_archivo = self.ruta_datos / f"{nombre}.json"
        if ruta_archivo.exists():
            with ruta_archivo.open('r') as f:
                datos = json.load(f)
                return self._deserializar_jugador(datos)
        return None
    
    def _guardar_jugador(self, jugador: Jugador):
        """Guarda los datos del jugador en un archivo JSON"""
        ruta_archivo = self.ruta_datos / f"{jugador.nombre}.json"
        with ruta_archivo.open('w') as f:
            json.dump(self._serializar_jugador(jugador), f, indent=4)
    
    def _serializar_jugador(self, jugador: Jugador) -> dict:
        """Convierte un objeto Jugador a diccionario para JSON"""
        datos = asdict(jugador)
        return datos
    
    def _deserializar_jugador(self, datos: dict) -> Jugador:
        """Convierte datos JSON a objeto Jugador"""
        progreso_dict = {}
        for categoria, lista_progreso in datos['progreso'].items():
            progreso_dict[categoria] = [
                Progreso(**prog) for prog in lista_progreso
            ]
        
        return Jugador(
            nombre=datos['nombre'],
            edad=datos['edad'],
            email=datos['email'],
            fecha_registro=datos['fecha_registro'],
            progreso=progreso_dict
        )
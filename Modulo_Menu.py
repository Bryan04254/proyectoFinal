import tkinter as tk
from tkinter import messagebox
from Jugador import GestorJugadores
import Modulo_Juego as juego
import Modulo_Assets as assets

class VentanaRegistro:
    """
    Clase que representa la ventana de registro de un nuevo jugador.

    Permite al usuario registrar un nuevo jugador ingresando nombre, edad y correo electrónico.
    """
    def __init__(self, parent, callback):
        """
        Inicializa la ventana de registro.

        Args:
            parent (tk.Tk): Ventana principal o padre de esta ventana.
            callback (function): Función para actualizar el jugador actual tras el registro.
        """
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registro de Jugador")
        self.ventana.geometry("400x300")
        self.gestor_jugadores = GestorJugadores()
        self.callback = callback
        self._crear_widgets()
        
    def _crear_widgets(self):
        """Crea los elementos gráficos (widgets) de la ventana de registro."""
        frame = tk.Frame(self.ventana, padx=20, pady=20)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky='w', pady=5)
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.grid(row=0, column=1, sticky='ew', pady=5)
        
        tk.Label(frame, text="Edad:").grid(row=1, column=0, sticky='w', pady=5)
        self.edad_entry = tk.Entry(frame)
        self.edad_entry.grid(row=1, column=1, sticky='ew', pady=5)
        
        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=2, column=1, sticky='ew', pady=5)
        
        tk.Button(frame, text="Registrar", command=self._registrar).grid(row=3, column=0, columnspan=2, pady=20)
        
    def _registrar(self):
        """Maneja el evento de registro de un nuevo jugador."""
        try:
            nombre = self.nombre_entry.get().strip()
            edad = int(self.edad_entry.get().strip())
            email = self.email_entry.get().strip()
            
            if not nombre or not email:
                raise ValueError("Todos los campos son obligatorios")
                
            jugador = self.gestor_jugadores.registrar_jugador(nombre, edad, email)
            messagebox.showinfo("Éxito", "¡Registro completado con éxito!")
            self.callback(nombre)  # Llamar al callback con el nombre del jugador
            self.ventana.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")

class VentanaLogin:
    """
    Clase que representa la ventana de inicio de sesión para un jugador existente.

    Permite al usuario iniciar sesión ingresando su nombre.
    """
    def __init__(self, parent, callback):
        """
        Inicializa la ventana de inicio de sesión.

        Args:
            parent (tk.Tk): Ventana principal o padre de esta ventana.
            callback (function): Función para actualizar el jugador actual tras el inicio de sesión.
        """
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Iniciar Sesión")
        self.ventana.geometry("300x150")
        self.gestor_jugadores = GestorJugadores()
        self.callback = callback
        self._crear_widgets()
        
    def _crear_widgets(self):
        """Crea los elementos gráficos (widgets) de la ventana de inicio de sesión."""
        frame = tk.Frame(self.ventana, padx=20, pady=20)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky='w', pady=5)
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.grid(row=0, column=1, sticky='ew', pady=5)
        
        tk.Button(frame, text="Iniciar Sesión", command=self._login).grid(row=1, column=0, columnspan=2, pady=20)
        
    def _login(self):
        """Maneja el evento de inicio de sesión del jugador."""
        nombre = self.nombre_entry.get().strip()
        jugador = self.gestor_jugadores.obtener_jugador(nombre)
        
        if jugador:
            self.callback(nombre)
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "Jugador no encontrado")

def Menu_Principal():
    """
    Muestra el menú principal del juego.

    Permite al usuario registrarse, iniciar sesión, jugar o salir del programa.
    """
    global ventana, jugador_actual
    jugador_actual = None
    
    def set_jugador_actual(nombre):
        """Actualiza el nombre del jugador actual y refresca el menú."""
        global jugador_actual
        jugador_actual = nombre
        actualizar_menu()
    
    def actualizar_menu():
        """Refresca el contenido del menú principal según el estado del jugador."""
        for widget in frame_botones.winfo_children():
            widget.destroy()
            
        if jugador_actual:
            tk.Label(frame_botones, text=f"Bienvenido, {jugador_actual}!", font=("Arial", 14)).pack(pady=10)
            tk.Button(frame_botones, text="Jugar", width=50, command=lambda: Definir_Categoria()).pack(pady=5)
            tk.Button(frame_botones, text="Cerrar Sesión", width=50, command=lambda: set_jugador_actual(None)).pack(pady=5)
        else:
            tk.Button(frame_botones, text="Registrarse", width=50, command=lambda: VentanaRegistro(ventana, set_jugador_actual)).pack(pady=5)
            tk.Button(frame_botones, text="Iniciar Sesión", width=50, command=lambda: VentanaLogin(ventana, set_jugador_actual)).pack(pady=5)
        
        tk.Button(frame_botones, text="Salir", width=50, command=ventana.quit).pack(pady=5)
    
    assets.inicio()
    ventana = tk.Tk()
    ventana.title("Menú Principal - Juego de la Gallina")
    ventana.geometry("1600x900")
    
    tk.Label(ventana, text="---Juego de la Gallina---", font=("Algerian", 60)).pack(pady=10)
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(expand=True)
    
    actualizar_menu()
    ventana.protocol("WM_DELETE_WINDOW", ventana.quit)
    ventana.mainloop()

def Definir_Categoria():
    """
    Permite al usuario elegir una categoría para iniciar el juego.
    """
    global ventana
    for widget in ventana.winfo_children():
        widget.destroy()

    marco_categoria = tk.Frame(ventana)
    marco_categoria.pack(expand=True)

    tk.Label(marco_categoria, text="---Elija Una Categoria Inicial---", font=("Algerian", 60)).pack(pady=20)
    categorias = ["Granja", "Bosque", "Ciudad", "Espacio", "Marte"]
    for cat in categorias:
        tk.Button(marco_categoria, text=cat, width=50, command=lambda c=cat: elegir_y_iniciar(c)).pack(pady=10)

def elegir_y_iniciar(valor):
    """
    Inicia el juego con la categoría seleccionada.

    Args:
        valor (str): Categoría seleccionada por el usuario.
    """
    global categoria, jugador_actual, ventana
    categoria = valor
    ventana.withdraw()
    
    try:
        if jugador_actual:
            juego.inicio(categoria, jugador_actual)
        else:
            juego.inicio(categoria)
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
    finally:
        ventana.deiconify()
        Menu_Principal()

if __name__ == "__main__":
    Menu_Principal()

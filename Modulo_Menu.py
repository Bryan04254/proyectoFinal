import tkinter as tk
from tkinter import messagebox
from Jugador import GestorJugadores, Jugador
import Modulo_Juego as juego
import Modulo_Assets as assets

class VentanaRegistro:
    def __init__(self, parent, callback):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registro de Jugador")
        self.ventana.geometry("400x300")
        self.gestor_jugadores = GestorJugadores()
        self.callback = callback
        self._crear_widgets()
        
    def _crear_widgets(self):
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
    def __init__(self, parent, callback):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Iniciar Sesión")
        self.ventana.geometry("300x150")
        self.gestor_jugadores = GestorJugadores()
        self.callback = callback
        self._crear_widgets()
        
    def _crear_widgets(self):
        frame = tk.Frame(self.ventana, padx=20, pady=20)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky='w', pady=5)
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.grid(row=0, column=1, sticky='ew', pady=5)
        
        tk.Button(frame, text="Iniciar Sesión", command=self._login).grid(row=1, column=0, columnspan=2, pady=20)
        
    def _login(self):
        nombre = self.nombre_entry.get().strip()
        jugador = self.gestor_jugadores.obtener_jugador(nombre)
        
        if jugador:
            self.callback(nombre)
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "Jugador no encontrado")

def Menu_Principal():
    global ventana, jugador_actual
    jugador_actual = None
    
    def set_jugador_actual(nombre):
        global jugador_actual
        jugador_actual = nombre
        actualizar_menu()
    
    def actualizar_menu():
        # Limpiar la ventana
        for widget in frame_botones.winfo_children():
            widget.destroy()
            
        if jugador_actual:
            # Mostrar mensaje de bienvenida
            label_bienvenida = tk.Label(frame_botones, 
                                    text=f"Bienvenido, {jugador_actual}!", 
                                    font=("Arial", 14))
            label_bienvenida.pack(pady=10)
            
            # Botón para jugar
            boton_jugar = tk.Button(frame_botones, text="Jugar", width=50, 
                                command=lambda: Definir_Categoria())
            boton_jugar.pack(pady=5)
            
            # Botón para cerrar sesión
            boton_logout = tk.Button(frame_botones, text="Cerrar Sesión", width=50,
                                command=lambda: set_jugador_actual(None))
            boton_logout.pack(pady=5)
        else:
            # Botones cuando no hay sesión iniciada
            boton_registro = tk.Button(frame_botones, text="Registrarse", width=50,
                                    command=lambda: VentanaRegistro(ventana, set_jugador_actual))
            boton_registro.pack(pady=5)
            
            boton_login = tk.Button(frame_botones, text="Iniciar Sesión", width=50,
                                command=lambda: VentanaLogin(ventana, set_jugador_actual))
            boton_login.pack(pady=5)
        
        # Botón salir siempre visible
        boton_salir = tk.Button(frame_botones, text="Salir", width=50,
                            command=ventana.quit)
        boton_salir.pack(pady=5)
    
    assets.inicio()  # Agregamos los paréntesis aquí
    
    ventana = tk.Tk()
    ventana.title("Menú Principal - Juego de la Gallina")
    ventana.geometry("1600x900")
    
    # Título
    label_titulo = tk.Label(ventana, text="---Juego de la Gallina---", font=("Algerian", 60))
    label_titulo.pack(pady=10)
    
    # Frame para botones
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(expand=True)
    
    # Inicializar el menú
    actualizar_menu()
    
    ventana.protocol("WM_DELETE_WINDOW", ventana.quit)
    ventana.mainloop()

def Definir_Categoria():
    global ventana, jugador_actual

    # Limpiar la ventana para mostrar la selección de categoría
    for widget in ventana.winfo_children():
        widget.destroy()

    # Crear marco para categorías
    marco_categoria = tk.Frame(ventana)
    marco_categoria.pack(expand=True)

    # Crear título y botones de categorías
    label_titulo = tk.Label(marco_categoria, text="---Elija Una Categoria Inicial---", font=("Algerian", 60))
    label_titulo.pack(pady=20)

    categorias = ["Granja", "Bosque", "Ciudad", "Espacio", "Marte"]
    for cat in categorias:
        boton = tk.Button(marco_categoria, text=cat, width=50, 
                        command=lambda c=cat: elegir_y_iniciar(c))
        boton.pack(pady=10)

def elegir_y_iniciar(valor):
    global categoria, jugador_actual, ventana
    categoria = valor
    ventana.withdraw()  # Ocultar la ventana principal
    
    # Importar el módulo juego aquí para evitar problemas de importación circular
    
    try:
        if jugador_actual:
            # Si hay un jugador logueado, usar la versión con dos parámetros
            juego.inicio(categoria, jugador_actual)
        else:
            # Si no hay jugador logueado, usar la versión con un parámetro
            juego.inicio(categoria)
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
    finally:
        ventana.deiconify()  # Mostrar la ventana principal de nuevo
        Menu_Principal()  # Volver al menú principal

if __name__ == "__main__":
    Menu_Principal()
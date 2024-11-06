import tkinter as tk
import Modulo_Juego as juego

# Variables globales
ventana = None
categoria = ""

def Definir_Categoria():
    global ventana

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
    for categoria in categorias:
        boton = tk.Button(marco_categoria, text=categoria, width=50, command=lambda cat=categoria: elegir_y_iniciar(cat))
        boton.pack(pady=10)

def elegir_y_iniciar(valor):
    global categoria
    categoria = valor
    Iniciar_Juego()

def Iniciar_Juego():
    global ventana

    # Limpiar la ventana para iniciar el juego
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.protocol("WM_DELETE_WINDOW", ventana.quit)
    juego.inicio()  # Inicia el juego desde el módulo de juego

def Menu_Principal():
    global ventana
    ventana = tk.Tk()
    ventana.title("Menú Principal - Juego de la Gallina")
    ventana.geometry("1600x900")

    # Título y botones del menú principal
    label_titulo = tk.Label(ventana, text="---Juego de la Gallina---", font=("Algerian", 60))
    label_titulo.pack(pady=10)

    boton_creacion = tk.Button(ventana, text="Iniciar Juego", width=50, command=Definir_Categoria)
    boton_creacion.pack(pady=5)
    boton_salir = tk.Button(ventana, text="Salir", width=50, command=ventana.quit)
    boton_salir.pack(pady=5)

    ventana.protocol("WM_DELETE_WINDOW", ventana.quit)
    ventana.mainloop()

if __name__ == "__main__":
    Menu_Principal()

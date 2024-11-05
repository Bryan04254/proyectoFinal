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

    # Crear un marco para contener el título y los botones, y centrarlo en la ventana
    marco_categoria = tk.Frame(ventana)
    marco_categoria.pack(expand=True)

    # Crear título
    label_titulo = tk.Label(marco_categoria, text="---Elija Una Categoria Inicial---", font=("Algerian", 60))
    label_titulo.pack(pady=20)

    

    # Crear botones de categorías
    categorias = ["Granja", "Bosque", "Ciudad", "Espacio", "Marte"]
    for categoria in categorias:
        boton = tk.Button(marco_categoria, text=categoria, width=50, command=lambda cat=categoria: elegir_y_iniciar(cat))
        boton.pack(pady=10)
    
    
    

# Función general para asignar la categoría
def elegir_y_iniciar(valor):
    global categoria
    categoria = valor
    # Manejar el cierre de la ventana
    
    Iniciar_Juego()    
    

def Iniciar_Juego():
    global ventana

    # Limpiar la ventana para mostrar el nuevo frame del juego
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.protocol("WM_DELETE_WINDOW", ventana.quit)  # Cerrar la ventana de Tkinter        

    # Llamar a la función de inicio del módulo de juego
    juego.inicio()  # Asegúrate de que esto inicia el juego correctamente
    

def Menu_Principal():
    global ventana
    ventana = tk.Tk()
    ventana.title("Menú Principal - Juego de la Gallina")
    ventana.geometry("1600x900")  # Tamaño de la ventana

    # Crear título
    label_titulo = tk.Label(ventana, text="---Juego de la Gallina---", font=("Algerian", 60))
    label_titulo.pack(pady=10)

    # Crear botones del menú principal
    boton_creacion = tk.Button(ventana, text="Iniciar Juego", width=50, command=Definir_Categoria)
    boton_creacion.pack(pady=5)

    boton_salir = tk.Button(ventana, text="Salir", width=50, command=ventana.quit)
    boton_salir.pack(pady=5)

     # Manejar el cierre de la ventana
    ventana.protocol("WM_DELETE_WINDOW", ventana.quit)  # Cerrar la ventana de Tkinter
    
    ventana.mainloop()


# Ejecutar ventana
if __name__ == "__main__":
    Menu_Principal()

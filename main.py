from tkinter import *
from PIL import Image, ImageTk
import customtkinter

# Función para abrir la nueva ventana
def abrir_ventana_ensamblaje():
    nueva_ventana = Toplevel(window)
    nueva_ventana.title("Ensamblaje en Progreso")
    nueva_ventana.geometry("400x300")
    nueva_ventana.configure(bg="#ffffff")

    # Etiqueta en la nueva ventana
    Label(nueva_ventana, text="Ensamblaje en Progreso", font=("Arial", 20), bg="#ffffff").pack(pady=50)

    # Botón para cerrar la nueva ventana
    Button(nueva_ventana, text="Cerrar", font=("Arial", 14), command=nueva_ventana.destroy).pack(pady=20)

# Configuración de la Ventana Principal
window = Tk()
window.title("Tkinter")
window.geometry("800x350")
window.configure(bg="#ffffff")

# Cargar imagen
image_path = "labomba.jpg"  # Ruta de la imagen
image = Image.open(image_path)
image = image.resize((350, 170), Image.Resampling.LANCZOS)  # Ajustar tamaño
photo = ImageTk.PhotoImage(image)

# Etiqueta principal
Label_id10 = customtkinter.CTkLabel(
    master=window,
    text="Proceso De Ensamblaje",
    font=("Arial", 20),
    text_color="#000000",
    bg_color="#ffffff"
)
Label_id10.place(x=50, y=40)

# Etiqueta Estado
Label_id17 = customtkinter.CTkLabel(
    master=window,
    text="Estado : Conectado",
    font=("Arial", 14),
    text_color="#000000",
    bg_color="#ffffff"
)
Label_id17.place(x=630, y=20)

# Etiqueta Servidor IP
Label_id7 = customtkinter.CTkLabel(
    master=window,
    text="Servidor IP",
    font=("Arial", 18),
    text_color="#000000",
    bg_color="#ffffff"
)
Label_id7.place(x=70, y=100)

# Campo de Entrada para IP
Entry_id6 = customtkinter.CTkEntry(
    master=window,
    placeholder_text="192.168.0.1",
    placeholder_text_color="#454545",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=195,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#ffffff",
    fg_color="#F0F0F0"
)
Entry_id6.place(x=70, y=130)

# Etiqueta Servidor Port
Label_id8 = customtkinter.CTkLabel(
    master=window,
    text="Servidor Port",
    font=("Arial", 18),
    text_color="#000000",
    bg_color="#ffffff"
)
Label_id8.place(x=70, y=160)

# Campo de Entrada para Puerto
Entry_id5 = customtkinter.CTkEntry(
    master=window,
    placeholder_text="502",
    placeholder_text_color="#454545",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=195,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#ffffff",
    fg_color="#F0F0F0"
)
Entry_id5.place(x=70, y=190)

# Botón Iniciar Ensamblaje
Button_id4 = customtkinter.CTkButton(
    master=window,
    text="Iniciar Ensamblaje",
    font=("Arial", 14),
    text_color="#000000",
    hover_color="#949494",
    height=30,
    width=200,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#ffffff",
    fg_color="#F0F0F0",
    command=abrir_ventana_ensamblaje  # Asociar la función al botón
)
Button_id4.place(x=70, y=230)

# Botón Conectar
Button_id12 = customtkinter.CTkButton(
    master=window,
    text="Conectar",
    font=("Arial", 18),
    text_color="#000000",
    hover_color="#057a28",
    height=40,
    width=150,
    border_width=2,
    corner_radius=20,
    border_color="#06bc3c",
    bg_color="#ffffff",
    fg_color="#06bc3c"
)
Button_id12.place(x=420, y=240)

# Botón Desconectar
Button_id13 = customtkinter.CTkButton(
    master=window,
    text="Desconectar",
    font=("Arial", 18),
    text_color="#000000",
    hover_color="#ab0707",
    height=40,
    width=150,
    border_width=2,
    corner_radius=20,
    border_color="#f40b0b",
    bg_color="#ffffff",
    fg_color="#f40b0b"
)
Button_id13.place(x=590, y=240)

# Etiqueta para mostrar la imagen
image_label = Label(master=window, image=photo, bg="#ffffff")
image_label.image = photo  # Evitar que la imagen sea eliminada por el recolector de basura
image_label.place(x=400, y=50)  # Ajusta la posición de la imagen

# Ejecutar el bucle principal
window.mainloop()
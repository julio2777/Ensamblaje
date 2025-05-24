# Librerías necesarias para el proyecto
from tkinter import *           # Librería base para la interfaz gráfica
from tkinter import messagebox, ttk  # Messagebox para advertencias y ttk para barra de progreso
from PIL import Image, ImageTk   # Librerías para manejo de imágenes
import customtkinter             # Librería para botones personalizados (más bonitos)
import serial
from pyModbusTCP.client import ModbusClient

import time
import mysql.connector
import threading

cliente_modbus = None  # Se inicializará al conectar
paso_actual_serial = 0
puerto_serie = None  # Se inicializará al conectar
def cargar_pasos_desde_mysql():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="ensamblaje_db"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT texto, imagenes FROM pasos ORDER BY id ASC")
    datos = cursor.fetchall()
    conexion.close()

    titulos = []
    imagenes = []
    for texto, imgs in datos:
        titulos.append(texto)
        imagenes.append(imgs.split(","))
    return titulos, imagenes


titulos_pasos, imagenes_pasos = cargar_pasos_desde_mysql()
boton_por_paso = [0, 1, 4, 2, 4, 3, 4]

# Variables globales de control
estado_conexion = False              # Indica si el sistema está conectado
ventana_ensamblaje_abierta = False    # Evita abrir más de una ventana de ensamblaje al mismo tiempo

# Actualiza el estado de conexión en la pantalla principal
def actualizar_estado():
    if estado_conexion:
        Label_id17.configure(text="Estado: Conectado", text_color="#06bc3c")
    else:
        Label_id17.configure(text="Estado: Desconectado", text_color="#f40b0b")

# Función para establecer conexión con el PLC por Modbus TCP
def conectar():
    global estado_conexion, cliente_modbus
    try:
        print("[INFO] Intentando conectar al PLC...")
        cliente_modbus = ModbusClient(host='10.41.110.255', port=502, unit_id=1)
        cliente_modbus.open()
        # Intentar leer algo para confirmar la conexión
        test_lectura = cliente_modbus.read_input_registers(0, 1)
        if test_lectura:
            estado_conexion = True
            actualizar_estado()
            print("[OK] Conexión establecida con el PLC.")
            print(test_lectura)
        else:
            raise ConnectionError("No se pudo leer del PLC. ¿Está el simulador activo?")
    except Exception as e:
        print("[ERROR] No se pudo conectar al PLC:", e)
        messagebox.showerror("Error", f"No se pudo conectar al PLC:\n{e}")


# Función para desconectar
def desconectar():
    global estado_conexion
    if cliente_modbus:
        cliente_modbus.close()
    estado_conexion = False
    actualizar_estado()


def leer_modbus_continuamente(cambiar_paso_func, finalizar_func, ventana_ref):
    def loop():
        global paso_actual_serial, cliente_modbus
        while estado_conexion:
            try:
                # Leer un registro donde el PLC indica qué botón se presionó
                registros = cliente_modbus.read_input_registers(0, 1)  # Dirección 0, cantidad 1
                if registros:
                    presionado = registros[0]
                    print(f"[MODBUS] Botón leído: {presionado}")

                    esperado = boton_por_paso[paso_actual_serial]
                    print(f"[INFO] Comparando botón {presionado} con paso esperado {esperado}")
                    if presionado == esperado:
                        print("[OK] Paso correcto")
                        if paso_actual_serial == len(boton_por_paso) - 1:
                            print("[FINAL] Ensamblaje terminado")
                            # Apagar LEDs o notificar fin (escribe un valor al PLC si es necesario)
                            cliente_modbus.write_single_register(1, 0)  # Ejemplo: escribir 0 para apagar LEDs
                            finalizar_func(ventana_ref)
                        else:
                            cambiar_paso_func(1)
                    else:
                        print("[ADVERTENCIA] Paso incorrecto")
                        messagebox.showwarning("¡Error!", f"Botón incorrecto: esperábamos {esperado}, presionaste {presionado}")
                else:
                    print("[WARN] No se pudo leer del PLC")

            except Exception as e:
                print(f"[ERROR] Al leer desde Modbus: {e}")
            time.sleep(0.5)
    threading.Thread(target=loop, daemon=True).start()


# Función principal que abre la ventana del proceso de ensamblaje
def abrir_ventana_ensamblaje():
    global ventana_ensamblaje_abierta

    # Validaciones antes de abrir
    if not estado_conexion:
        messagebox.showwarning("Advertencia", "Debes conectarte antes de iniciar el ensamblaje.")
        return
    if ventana_ensamblaje_abierta:
        messagebox.showwarning("Advertencia", "Ya hay un ensamblaje en proceso.")
        return

    # Crear nueva ventana
    ventana_ensamblaje_abierta = True
    nueva_ventana = Toplevel(window)
    nueva_ventana.title("Ensamblaje en Progreso")
    nueva_ventana.geometry("900x700")
    nueva_ventana.configure(bg="#f0f2f5")
    nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(nueva_ventana))

    # Variable para controlar el paso actual
    global paso_actual
    paso_actual = IntVar(value=0)

    # Título
    titulo_label = Label(nueva_ventana, text="Proceso De Ensamblaje", font=("Helvetica", 26, "bold"), bg="#f0f2f5", fg="#263238")
    titulo_label.pack(pady=10)

    # Línea debajo del título
    Frame(nueva_ventana, bg="#b0bec5", height=2, width=700).pack(pady=(0, 20))

    # Subtítulo para paso y descripción
    paso_label = Label(nueva_ventana, text="", font=("Helvetica", 20), bg="#f0f2f5", fg="#37474f")
    paso_label.pack()

    descripcion_label = Label(nueva_ventana, text="", font=("Helvetica", 16), bg="#f0f2f5", fg="#546e7a")
    descripcion_label.pack(pady=5)

    # Frame para mostrar imágenes del paso
    frame_imagenes = Frame(nueva_ventana, bg="#f0f2f5")
    frame_imagenes.pack(pady=20)

    # Barra de progreso
    progreso = ttk.Progressbar(nueva_ventana, length=700, mode='determinate')
    progreso.pack(pady=10)

    # Frame para botones
    frame_botones = Frame(nueva_ventana, bg="#f0f2f5")
    frame_botones.pack(pady=20)

    # Botón REGRESAR
    boton_regresar = customtkinter.CTkButton(
        master=frame_botones,
        text="⬅️ Regresar",
        font=("Helvetica", 16),
        text_color="#000000",
        fg_color="#cfd8dc",
        hover_color="#90a4ae",
        border_width=2,
        border_color="#000000",
        corner_radius=20,
        width=150,
        height=40,
        command=lambda: cambiar_paso(-1)
    )
    boton_regresar.grid(row=0, column=0, padx=20)

    # Botón SIGUIENTE
    boton_siguiente = customtkinter.CTkButton(
        master=frame_botones,
        text="Siguiente ➡️",
        font=("Helvetica", 16),
        text_color="#ffffff",
        fg_color="#4CAF50",
        hover_color="#2e7d32",
        border_width=2,
        border_color="#000000",
        corner_radius=20,
        width=150,
        height=40,
        command=lambda: cambiar_paso(1)
    )
    boton_siguiente.grid(row=0, column=1, padx=20)

    # Botón FINALIZAR
    boton_finalizar = customtkinter.CTkButton(
        master=frame_botones,
        text="✔️ Finalizar",
        font=("Helvetica", 16),
        text_color="#ffffff",
        fg_color="#2196F3",
        hover_color="#1565c0",
        border_width=2,
        border_color="#000000",
        corner_radius=20,
        width=150,
        height=40,
        command=lambda: finalizar_ensamblaje(nueva_ventana)
    )
    boton_finalizar.grid(row=0, column=2, padx=20)
    boton_finalizar.grid_remove()  # Ocultar inicialmente


    # Cierra la ventana de ensamblaje
    def cerrar_ventana(ventana):
        global ventana_ensamblaje_abierta
        ventana.destroy()
        ventana_ensamblaje_abierta = False

    # Cambia el paso actual
    def cambiar_paso(direccion):
        global paso_actual_serial
        nuevo_paso = paso_actual.get() + direccion
        if 0 <= nuevo_paso < len(titulos_pasos):
            print(f"[INFO] Cambiando al paso {nuevo_paso}")
            paso_actual.set(nuevo_paso)
            paso_actual_serial = nuevo_paso
            actualizar_pantalla()

        try:
            if cliente_modbus:
                esperado = boton_por_paso[nuevo_paso]
                # Enviamos el valor del paso al PLC (por ejemplo, para encender el LED correspondiente)
                cliente_modbus.write_multiple_registers(0, [esperado, 0])  # Solo un valor, el otro puede ser relleno
                print(f"[MODBUS] Enviando al PLC que encienda LED del botón {esperado}")
        except Exception as e:
            print(f"[ERROR] No se pudo enviar paso al PLC: {e}")




    # Muestra un pequeño modal indicando que el ensamblaje fue finalizado
    def finalizar_ensamblaje(ventana):
        modal = Toplevel(ventana)
        modal.title("¡Completado!")
        modal.configure(bg="#ffffff")
        modal.transient(ventana)
        modal.grab_set()

        # Centrando el modal
        modal_width = 300
        modal_height = 150
        screen_width = modal.winfo_screenwidth()
        screen_height = modal.winfo_screenheight()
        x = (screen_width // 2) - (modal_width // 2)
        y = (screen_height // 2) - (modal_height // 2)
        modal.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        # Mensaje
        Label(modal, text="✅ Ensamblaje Finalizado", font=("Helvetica", 16), bg="#ffffff", fg="#4CAF50").pack(expand=True)

        # Después de 2 segundos, cierra todo
        ventana.after(2000, lambda: [modal.destroy(), cerrar_ventana(ventana)])

    # Actualiza la información visual de la ventana
    def actualizar_pantalla():
        actual = paso_actual.get()
        paso_label.config(text=f"Paso {actual+1}:")
        descripcion_label.config(text=titulos_pasos[actual])

        # Limpiar imágenes anteriores
        for widget in frame_imagenes.winfo_children():
            widget.destroy()

        # Mostrar imagen o imágenes correspondientes al paso actual
        #image_path = "labomba.jpg"  
        imagenes = imagenes_pasos[actual]
        if len(imagenes) == 1:
            frame_sombra = Frame(frame_imagenes, bg="#e0e0e0", padx=3, pady=3)
            frame_sombra.pack()
            img1 = Image.open(imagenes[0])
            img1 = img1.resize((350, 250), Image.Resampling.LANCZOS)
            img1 = ImageTk.PhotoImage(img1)
            label_imagen1 = Label(frame_sombra, image=img1, bg="white")
            label_imagen1.image = img1
            label_imagen1.pack()
        else:
            img1 = Image.open(imagenes[0])
            img1 = img1.resize((300, 220), Image.Resampling.LANCZOS)
            img1 = ImageTk.PhotoImage(img1)
            label_imagen1 = Label(frame_imagenes, image=img1, bg="white")
            label_imagen1.image = img1
            label_imagen1.grid(row=0, column=0, padx=10)

            img2 = Image.open(imagenes[1])
            img2 = img2.resize((300, 220), Image.Resampling.LANCZOS)
            img2 = ImageTk.PhotoImage(img2)
            label_imagen2 = Label(frame_imagenes, image=img2, bg="white")
            label_imagen2.image = img2
            label_imagen2.grid(row=0, column=1, padx=10)

        # Actualizar barra de progreso
        progreso['value'] = (actual + 1) * (100 / len(titulos_pasos))

        # Controlar visibilidad de botones
        if actual == 0:
            boton_regresar.configure(state=DISABLED)
        else:
            boton_regresar.configure(state=NORMAL)

        if actual == len(titulos_pasos) - 1:
            boton_siguiente.grid_remove()
            boton_finalizar.grid()
        else:
            boton_siguiente.grid()
            boton_finalizar.grid_remove()

    # Inicializa la pantalla
    actualizar_pantalla()

    # Enviar el LED del primer paso al ESP32
    esperado = boton_por_paso[paso_actual.get()]
    if puerto_serie and esperado is not None:
        puerto_serie.write(f"{esperado}\n".encode())
        print(f"[INICIO] LED del paso 1 enviado: botón {esperado}")


    global paso_actual_serial
    paso_actual_serial = 0

    #leer_serial_continuamente(cambiar_paso, finalizar_ensamblaje, nueva_ventana)
    leer_modbus_continuamente(cambiar_paso, finalizar_ensamblaje, nueva_ventana)


# Definición de la Ventana Principal

window = Tk()
window.title("Ensamblaje Coflex")
window.geometry("850x450")
window.configure(bg="#ffffff")

# Imagen principal 
image_path = "llave.png"
image = Image.open(image_path)
image = image.resize((300, 170), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Elementos de la pantalla principal
Label_id10 = customtkinter.CTkLabel(master=window, text="Proceso De Ensamblaje", font=("Arial", 20), text_color="#000000", bg_color="#ffffff")
Label_id10.place(x=50, y=40)

Label_id17 = customtkinter.CTkLabel(master=window, text="Estado: Desconectado", font=("Arial", 14), text_color="#f40b0b", bg_color="#ffffff")
Label_id17.place(x=630, y=20)

Label_id7 = customtkinter.CTkLabel(master=window, text="Servidor IP", font=("Arial", 18), text_color="#000000", bg_color="#ffffff")
Label_id7.place(x=70, y=100)

Entry_id6 = customtkinter.CTkEntry(master=window, placeholder_text="192.168.0.1", placeholder_text_color="#454545", font=("Arial", 14), text_color="#000000", height=30, width=195, border_width=2, corner_radius=6, border_color="#000000", bg_color="#ffffff", fg_color="#F0F0F0")
Entry_id6.place(x=70, y=130)

Label_id8 = customtkinter.CTkLabel(master=window, text="Servidor Port", font=("Arial", 18), text_color="#000000", bg_color="#ffffff")
Label_id8.place(x=70, y=160)

Entry_id5 = customtkinter.CTkEntry(master=window, placeholder_text="502", placeholder_text_color="#454545", font=("Arial", 14), text_color="#000000", height=30, width=195, border_width=2, corner_radius=6, border_color="#000000", bg_color="#ffffff", fg_color="#F0F0F0")
Entry_id5.place(x=70, y=190)

Button_id4 = customtkinter.CTkButton(master=window, text="Iniciar Ensamblaje", font=("Arial", 14), text_color="#000000", hover_color="#949494", height=30, width=200, border_width=2, corner_radius=6, border_color="#000000", bg_color="#ffffff", fg_color="#F0F0F0", command=abrir_ventana_ensamblaje)
Button_id4.place(x=70, y=230)

Button_id12 = customtkinter.CTkButton(master=window, text="Conectar", font=("Arial", 18), text_color="#000000", hover_color="#057a28", height=40, width=150, border_width=2, corner_radius=20, border_color="#06bc3c", bg_color="#ffffff", fg_color="#06bc3c", command=conectar)
Button_id12.place(x=420, y=240)

Button_id13 = customtkinter.CTkButton(master=window, text="Desconectar", font=("Arial", 18), text_color="#000000", hover_color="#ab0707", height=40, width=150, border_width=2, corner_radius=20, border_color="#f40b0b", bg_color="#ffffff", fg_color="#f40b0b", command=desconectar)
Button_id13.place(x=590, y=240)

# Imagen decorativa
image_label = Label(master=window, image=photo, bg="#ffffff")
image_label.image = photo
image_label.place(x=400, y=50)

# Lanza el programa
window.mainloop()

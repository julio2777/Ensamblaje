# 📄 README - Sistema de Ensamblaje Coflex

## 🛠 Descripción del Proyecto

Este proyecto implementa una **interfaz gráfica** en Python que guía paso a paso el **proceso de ensamblaje** de una **llave de control angular Coflex**.

Utiliza **Tkinter** y **CustomTkinter** para mostrar:
- Instrucciones claras para cada paso.
- Imágenes de las piezas o conjuntos.
- Barra de progreso para seguimiento.
- Confirmación automática al finalizar el ensamblaje.

Ideal para **prácticas de línea de producción** o **entrenamiento de operarios**.

## 🖥 Tecnologías Utilizadas

- Python 3.8+
- Tkinter (interfaz gráfica estándar de Python)
- CustomTkinter (botones y entradas modernas)
- Pillow (PIL) (para manejo de imágenes)
- ttk (para barra de progreso estilizada)

## 📋 Instrucciones para Ejecutar

1. Asegúrate de tener Python 3.8 o superior instalado.

2. Instala las dependencias necesarias:
pip install customtkinter pillow


3. Ejecuta el archivo main.py:
python main.py


4. Uso:
- Primero presiona **Conectar**.
- Luego **Iniciar Ensamblaje**.
- Sigue las instrucciones paso a paso.
- Al terminar, aparecerá un mensaje de **Ensamblaje Finalizado** y se cerrará automáticamente.

## 📈 Características Especiales

- Ventana principal simple y limpia.
- Ventana de ensamblaje con fondo suave y diseño moderno.
- Botones modernos con hover y bordes visibles.
- Progreso dinámico.
- Modal automático de éxito al finalizar.
- Código altamente documentado para fácil mantenimiento.

## 🚀 Notas Adicionales

- Actualmente el sistema muestra una imagen de prueba (labomba.jpg) en cada paso.
- Se puede adaptar fácilmente para mostrar las imágenes reales de cada pieza.
- No necesita conexión a bases de datos ni servidores externos.
- Proyecto ideal para prácticas de IoT, PLC o Automatización en líneas de producción.



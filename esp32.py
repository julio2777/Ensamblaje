from machine import Pin
import time
import sys

# Pines de entrada (ajusta si es necesario)
botones = [Pin(14, Pin.IN, Pin.PULL_UP),
           Pin(27, Pin.IN, Pin.PULL_UP),
           Pin(26, Pin.IN, Pin.PULL_UP),
           Pin(25, Pin.IN, Pin.PULL_UP)]

estado_anterior = [1, 1, 1, 1]

while True:
    for i, boton in enumerate(botones):
        actual = boton.value()
        if actual == 0 and estado_anterior[i] == 1:
            print(i)  # Enviar número de botón presionado
            sys.stdout.flush()  # Asegura que el dato se envíe por UART
            time.sleep(0.5)
        estado_anterior[i] = actual

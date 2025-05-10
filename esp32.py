from machine import Pin
import time
import sys
import select

# Entradas
botones = [Pin(14, Pin.IN, Pin.PULL_UP),  # Botón 0
           Pin(27, Pin.IN, Pin.PULL_UP),  # Botón 1
           Pin(26, Pin.IN, Pin.PULL_UP),  # Botón 2
           Pin(25, Pin.IN, Pin.PULL_UP),  # Botón 3
           Pin(33, Pin.IN, Pin.PULL_UP)]  # Botón 4 (ensamblaje)

# Salidas
leds = [Pin(4, Pin.OUT),
        Pin(19, Pin.OUT),
        Pin(18, Pin.OUT),
        Pin(5, Pin.OUT),
        Pin(32, Pin.OUT)]  # LED para ensamblaje

estado_anterior = [1, 1, 1, 1,1]
paso_actual = -1

print("ESP32 listo...")

while True:
    # Leer paso enviado desde la PC (USB)
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        recibido = sys.stdin.readline().strip()
        if recibido == "OFF":
            print("Apagando todos los LEDs...")
            for led in leds:
                led.value(0)
        else:
            try:
                paso_actual = int(recibido)
                print("Paso recibido:", paso_actual)
                for i, led in enumerate(leds):
                    led.value(1 if i == paso_actual else 0)
            except:
                print("Error al procesar dato recibido:", recibido)


    # Verificar si algún botón fue presionado
    for i, boton in enumerate(botones):
        actual = boton.value()
        if actual == 0 and estado_anterior[i] == 1:
            print(i)  # Envía el número del botón presionado
            time.sleep(0.5)
        estado_anterior[i] = actual

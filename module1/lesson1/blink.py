import board
import digitalio
import time

# Настраиваем GPIO пин для светодиода
led = digitalio.DigitalInOut(board.D18)  # GPIO18
led.direction = digitalio.Direction.OUTPUT

# Мигание светодиодом
while True:
   led.value = True  # Включить светодиод
   print("LED ON")
   time.sleep(1)
   led.value = False  # Выключить светодиод
   print("LED OFF")
   time.sleep(1)
import board
import digitalio
import time

# Настройка светодиода
led = digitalio.DigitalInOut(board.D18)  # BCM 18
led.direction = digitalio.Direction.OUTPUT

# Настройка кнопки
button = digitalio.DigitalInOut(board.D23)  # BCM 23
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

print("Нажми кнопку, чтобы включить светодиод!")

# Основной цикл
while True:
    try:
        if button.value:  # Если кнопка нажата
            led.value = True
            print("Кнопка нажата! Включаем LED.")
        else:
            led.value = False
            print("Кнопка отпущена! Выключаем LED.")

        time.sleep(0.1)  # Небольшая задержка для стабильности
    except KeyboardInterrupt:
        # Безопасное завершение при нажатии Ctrl+C
        led.value = False
        break
import board
import digitalio
import time

# Настройка пинов для RGB светодиода
red_pin = digitalio.DigitalInOut(board.D14)  # GPIO14 для красного
green_pin = digitalio.DigitalInOut(board.D15)  # GPIO15 для зеленого
blue_pin = digitalio.DigitalInOut(board.D18)  # GPIO18 для синего

# Настраиваем все пины как выходы
red_pin.direction = digitalio.Direction.OUTPUT
green_pin.direction = digitalio.Direction.OUTPUT
blue_pin.direction = digitalio.Direction.OUTPUT

# Функция для установки цвета RGB светодиода
def set_color(r, g, b):
    red_pin.value = not r
    green_pin.value = not g
    blue_pin.value = not b

# Функция для вывода информации о текущем цвете
def print_color(color_name):
    print(f"Светодиод горит цветом: {color_name}")

try:
    while True:
        # Красный
        set_color(True, False, False)
        print_color("Красный")
        time.sleep(1)

        # Зеленый
        set_color(False, True, False)
        print_color("Зеленый")
        time.sleep(1)

        # Синий
        set_color(False, False, True)
        print_color("Синий")
        time.sleep(1)

        # Желтый (Красный + Зеленый)
        set_color(True, True, False)
        print_color("Желтый")
        time.sleep(1)

        # Пурпурный (Красный + Синий)
        set_color(True, False, True)
        print_color("Пурпурный")
        time.sleep(1)

        # Голубой (Зеленый + Синий)
        set_color(False, True, True)
        print_color("Голубой")
        time.sleep(1)

        # Белый (Все цвета)
        set_color(True, True, True)
        print_color("Белый")
        time.sleep(1)

        # Выключаем все светодиоды
        set_color(False, False, False)
        print("Светодиод выключен")
        time.sleep(1)

except KeyboardInterrupt:
    # Выключаем все светодиоды при завершении
    set_color(False, False, False)
    print("\nПрограмма завершена")
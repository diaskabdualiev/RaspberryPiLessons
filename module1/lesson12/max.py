import time
import board
import busio
import digitalio
from adafruit_max7219 import matrices

# Конфигурация SPI
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)  # Chip Select (CS) на GPIO 5

# Инициализация одной матрицы MAX7219
display = matrices.Matrix8x8(spi, cs)
display.brightness(5)  # Устанавливаем яркость (0-15)

def clear_display():
    """Очистка дисплея"""
    display.fill(0)
    display.show()

def show_rectangle():
    """Отображает прямоугольник по периметру матрицы"""
    clear_display()

    # Верхняя и нижняя линии
    for x in range(8):
        display.pixel(x, 0, 1)  # Верхняя линия
        display.pixel(x, 7, 1)  # Нижняя линия

    # Левая и правая границы (без углов, чтобы не дублировать)
    for y in range(1, 7):
        display.pixel(0, y, 1)  # Левая граница
        display.pixel(7, y, 1)  # Правая граница

    display.show()

def show_heart():
    """Отображает простое сердечко на матрице"""
    clear_display()

    # Битовая карта сердечка
    heart = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    # Вывод сердечка на матрицу
    for y in range(8):
        for x in range(8):
            if heart[y][x] == 1:
                display.pixel(x, y, 1)

    display.show()

def show_animation():
    """Простая анимация: мигающее сердечко"""
    for _ in range(3):  # Повторить 3 раза
        show_heart()
        time.sleep(0.5)
        clear_display()
        time.sleep(0.5)
    show_heart()  # Оставить сердечко в конце

def show_letter(letter, delay=1):
    """Отображает одну букву из заданных шаблонов"""
    clear_display()

    # Словарь с битовыми картами букв
    letters = {
        'A': [
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'B': [
            [1, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'C': [
            [0, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    }

    # Проверяем, есть ли буква в словаре
    if letter.upper() in letters:
        bitmap = letters[letter.upper()]
        for y in range(8):
            for x in range(8):
                if bitmap[y][x] == 1:
                    display.pixel(x, y, 1)
        display.show()
        time.sleep(delay)
    else:
        print(f"Буква {letter} не найдена в словаре")

def show_letters_sequence(text="ABC", delay=1):
    """Отображает последовательность букв с заданной задержкой"""
    for letter in text:
        if letter != ' ':  # Пропускаем пробелы
            show_letter(letter, delay)

# Основная программа
try:
    print("Запуск демонстрации MAX7219")

    # Очистка дисплея
    clear_display()
    time.sleep(0.5)

    # Показываем прямоугольник
    print("1. Отображение прямоугольника")
    show_rectangle()
    time.sleep(2)

    # Показываем сердечко
    print("2. Отображение сердечка")
    show_heart()
    time.sleep(2)

    # Анимация сердечка
    print("3. Анимация мигающего сердечка")
    show_animation()
    time.sleep(1)

    # Последовательность букв
    print("4. Показ последовательности букв")
    show_letters_sequence("ABC", 1.5)

    # Очищаем дисплей в конце
    clear_display()
    print("Демонстрация завершена")

except KeyboardInterrupt:
    clear_display()
    print("\nПрограмма остановлена пользователем")
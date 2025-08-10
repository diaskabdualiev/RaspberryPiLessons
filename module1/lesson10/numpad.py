import time
import board
import digitalio
import adafruit_matrixkeypad

# Определяем пины для строк (R1-R4) и столбцов (C1-C4)
row_pins = [
    digitalio.DigitalInOut(board.D5),
    digitalio.DigitalInOut(board.D6),
    digitalio.DigitalInOut(board.D13),
    digitalio.DigitalInOut(board.D19)
]

col_pins = [
    digitalio.DigitalInOut(board.D12),
    digitalio.DigitalInOut(board.D16),
    digitalio.DigitalInOut(board.D20),
    digitalio.DigitalInOut(board.D21)
]

# Настраиваем пины строк как выходы с подтягиванием к высокому уровню
for pin in row_pins:
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = True

# Настраиваем пины столбцов как входы с подтягиванием к высокому уровню
for pin in col_pins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

# Определяем карту символов клавиатуры
keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

# Инициализируем матричную клавиатуру
keypad = adafruit_matrixkeypad.Matrix_Keypad(
    row_pins, col_pins, keys
)

# Сохраняем последнее состояние клавиатуры для определения нажатий
last_pressed = []
current_input = ""  # Строка для сохранения введенных символов

# Функция для обработки нажатий клавиш
def process_key_press(key):
    global current_input

    if key == "*":  # Если нажата звездочка, очищаем ввод
        current_input = ""
        print("Ввод очищен")
    elif key == "#":  # Если нажата решетка, обрабатываем ввод
        print(f"Вы ввели: {current_input}")
        # Здесь можно добавить логику обработки ввода
        current_input = ""
    else:  # Обычная клавиша - добавляем к текущему вводу
        current_input += key
        print(f"Нажата клавиша: {key}, Текущий ввод: {current_input}")

# Основной цикл
try:
    print("Матричная клавиатура 4x4 готова к работе!")
    print("'*' - очистить ввод, '#' - подтвердить ввод")

    while True:
        # Проверяем нажатые клавиши
        pressed = keypad.pressed_keys

        # Выводим отладочную информацию
        if pressed:
            print(f"Обнаружены нажатия: {pressed}")

        # Обрабатываем только новые нажатия (фронт сигнала)
        for key in pressed:
            if key not in last_pressed:
                process_key_press(key)

        # Обновляем состояние последних нажатых клавиш
        last_pressed = pressed.copy()

        # Небольшая задержка для стабилизации
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nПрограмма завершена.")
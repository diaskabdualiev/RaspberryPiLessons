from flask import Flask, render_template, jsonify
import time
import board
import digitalio
import adafruit_matrixkeypad
import threading

app = Flask(__name__)

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

# Глобальные переменные для хранения состояния
current_input = ""  # Текущий ввод пользователя
last_pressed = []   # Последние нажатые клавиши
keypad_history = [] # История ввода для отображения в веб-интерфейсе

# Блокировка для многопоточного доступа
lock = threading.Lock()

# Функция для обработки нажатий клавиш
def process_key_press(key):
    global current_input, keypad_history

    with lock:
        if key == "*":  # Если нажата звездочка, очищаем ввод
            keypad_history.append(f"Ввод очищен: {current_input}")
            current_input = ""
        elif key == "#":  # Если нажата решетка, обрабатываем ввод
            keypad_history.append(f"Подтверждён ввод: {current_input}")
            current_input = ""
        else:  # Обычная клавиша - добавляем к текущему вводу
            current_input += key
            keypad_history.append(f"Нажата клавиша: {key}")

        # Ограничиваем историю до последних 20 записей
        if len(keypad_history) > 20:
            keypad_history = keypad_history[-20:]

# Функция опроса клавиатуры в отдельном потоке
def keypad_polling():
    global last_pressed

    while True:
        # Проверяем нажатые клавиши
        pressed = keypad.pressed_keys

        # Обрабатываем только новые нажатия
        for key in pressed:
            if key not in last_pressed:
                process_key_press(key)

        # Обновляем состояние последних нажатых клавиш
        last_pressed = pressed.copy()

        # Небольшая задержка для стабилизации
        time.sleep(0.1)

# Роут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# API для получения текущего состояния клавиатуры
@app.route('/api/keypad-state')
def keypad_state():
    with lock:
        return jsonify({
            'current_input': current_input,
            'history': keypad_history
        })

# Запуск опроса клавиатуры в отдельном потоке
def start_keypad_thread():
    keypad_thread = threading.Thread(target=keypad_polling, daemon=True)
    keypad_thread.start()

if __name__ == '__main__':
    # Запускаем поток для опроса клавиатуры
    start_keypad_thread()

    # Запускаем веб-сервер Flask
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
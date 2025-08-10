from flask import Flask, render_template, jsonify
import time
import board
import busio
import digitalio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

app = Flask(__name__)

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация ADS1115
ads = ADS.ADS1115(i2c)

# Настройка каналов для осей X и Y джойстика
# ADS1115 имеет 4 аналоговых входа (A0-A3)
x_channel = AnalogIn(ads, ADS.P0)  # Ось X подключена к A0
y_channel = AnalogIn(ads, ADS.P1)  # Ось Y подключена к A1

# Кнопка джойстика подключена к GPIO пину
button = digitalio.DigitalInOut(board.D17)  # Кнопка на GPIO17
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Подтяжка к питанию (кнопка замыкает на GND)

# Переменные для хранения калибровочных значений
x_center = None
y_center = None
x_min = None
x_max = None
y_min = None
y_max = None

def calibrate_joystick():
    global x_center, y_center, x_min, x_max, y_min, y_max

    # Считываем несколько значений для определения центральной позиции
    x_values = []
    y_values = []

    print("Калибровка джойстика...")
    print("Пожалуйста, оставьте джойстик в центральном положении")

    for _ in range(10):
        x_values.append(x_channel.value)
        y_values.append(y_channel.value)
        time.sleep(0.1)

    # Вычисляем средние значения для определения "центра"
    x_center = sum(x_values) // len(x_values)
    y_center = sum(y_values) // len(y_values)

    # Определяем предположительные минимумы и максимумы
    x_min = x_center - 10000
    x_max = x_center + 10000
    y_min = y_center - 10000
    y_max = y_center + 10000

    print(f"Калибровка завершена: X центр = {x_center}, Y центр = {y_center}")

def map_to_percent(value, in_min, in_max):
    return int((value - in_min) * 100 / (in_max - in_min))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/joystick')
def get_joystick_data():
    global x_center, y_center, x_min, x_max, y_min, y_max

    # Проверяем, была ли проведена калибровка
    if x_center is None:
        calibrate_joystick()

    # Считываем значения с джойстика
    x_value = x_channel.value
    y_value = y_channel.value
    button_pressed = not button.value

    # Преобразуем значения в проценты от -100% до 100%
    x_percent = map_to_percent(x_value, x_min, x_max) - 50
    y_percent = map_to_percent(y_value, y_min, y_max) - 50

    # Ограничиваем значения в пределах -100% до 100%
    x_percent = max(-100, min(100, x_percent * 2))
    y_percent = max(-100, min(100, y_percent * 2))

    # Определяем направление
    direction = "Центр"
    if abs(x_percent) > 10 or abs(y_percent) > 10:  # Учитываем небольшую мертвую зону
        if abs(x_percent) > abs(y_percent):
            direction = "Вправо" if x_percent > 0 else "Влево"
        else:
            direction = "Вверх" if y_percent < 0 else "Вниз"

    return jsonify({
        'x': x_percent,
        'y': y_percent,
        'direction': direction,
        'button': button_pressed
    })

@app.route('/calibrate')
def calibrate():
    global x_center, y_center, x_min, x_max, y_min, y_max
    calibrate_joystick()
    return jsonify({
        'success': True,
        'message': 'Калибровка завершена',
        'x_center': x_center,
        'y_center': y_center
    })

if __name__ == '__main__':
    # Вызываем калибровку при запуске
    calibrate_joystick()
    app.run(host='0.0.0.0',
        port=5000,
        debug=True,        # можно оставить отладку
        use_reloader=False # но запрещаем второй запуск
        )
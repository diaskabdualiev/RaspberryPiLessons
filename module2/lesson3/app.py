import board
import digitalio
from flask import Flask, render_template, redirect, url_for

# Настройка пинов для RGB светодиода
red_pin = digitalio.DigitalInOut(board.D14)  # GPIO14 для красного
green_pin = digitalio.DigitalInOut(board.D15)  # GPIO15 для зеленого
blue_pin = digitalio.DigitalInOut(board.D18)  # GPIO18 для синего

# Настраиваем все пины как выходы
red_pin.direction = digitalio.Direction.OUTPUT
green_pin.direction = digitalio.Direction.OUTPUT
blue_pin.direction = digitalio.Direction.OUTPUT

# Инициализация Flask приложения
app = Flask(__name__)

# Глобальная переменная для отслеживания текущего цвета
current_color = "Выключен"

# Функция для установки цвета RGB светодиода
def set_color(r, g, b):
    red_pin.value = not r
    green_pin.value = not g
    blue_pin.value = not b

# Маршруты Flask
@app.route('/')
def index():
    return render_template('index.html', current_color=current_color)

@app.route('/color/<color>')
def set_led_color(color):
    global current_color

    if color == 'red':
        set_color(True, False, False)
        current_color = "Красный"
    elif color == 'green':
        set_color(False, True, False)
        current_color = "Зеленый"
    elif color == 'blue':
        set_color(False, False, True)
        current_color = "Синий"
    elif color == 'off':
        set_color(False, False, False)
        current_color = "Выключен"

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Выключаем светодиод при запуске
    set_color(False, False, False)

    # Запускаем веб-сервер
    # Используем 0.0.0.0 чтобы сервер был доступен извне
    app.run(host='0.0.0.0', port=8080)
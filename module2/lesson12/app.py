from flask import Flask, render_template, request, jsonify
import time
import board
import busio
import digitalio
from adafruit_max7219 import matrices

app = Flask(__name__)

# Конфигурация SPI
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)  # Chip Select (CS) на GPIO 5

# Инициализация одной матрицы MAX7219
display = matrices.Matrix8x8(spi, cs)
display.brightness(5)  # Устанавливаем яркость (0-15)

# Текущее состояние матрицы (0 = выключено, 1 = включено)
matrix_state = [[0 for _ in range(8)] for _ in range(8)]

def update_display():
    """Обновление состояния дисплея на основе matrix_state"""
    # Очистка дисплея
    display.fill(0)

    # Установка пикселей в соответствии с matrix_state
    for y in range(8):
        for x in range(8):
            if matrix_state[y][x] == 1:
                display.pixel(x, y, 1)

    # Отображаем изменения
    display.show()

@app.route('/')
def index():
    """Главная страница с интерфейсом для рисования"""
    return render_template('index.html')

@app.route('/api/get_matrix', methods=['GET'])
def get_matrix():
    """API для получения текущего состояния матрицы"""
    return jsonify({'matrix': matrix_state})

@app.route('/api/set_pixel', methods=['POST'])
def set_pixel():
    """API для изменения состояния одного пикселя"""
    data = request.get_json()
    x = data.get('x', 0)
    y = data.get('y', 0)
    state = data.get('state', 0)

    # Проверка валидности координат
    if 0 <= x < 8 and 0 <= y < 8:
        matrix_state[y][x] = state
        update_display()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid coordinates'})

@app.route('/api/clear', methods=['POST'])
def clear_matrix():
    """API для очистки всей матрицы"""
    global matrix_state
    matrix_state = [[0 for _ in range(8)] for _ in range(8)]
    display.fill(0)
    display.show()
    return jsonify({'success': True})

@app.route('/api/set_matrix', methods=['POST'])
def set_matrix():
    """API для установки всей матрицы сразу"""
    data = request.get_json()
    new_matrix = data.get('matrix', [])

    # Проверяем, что входящая матрица правильного размера
    if len(new_matrix) == 8 and all(len(row) == 8 for row in new_matrix):
        global matrix_state
        matrix_state = new_matrix
        update_display()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid matrix dimensions'})

@app.route('/api/set_brightness', methods=['POST'])
def set_brightness():
    """API для установки яркости дисплея"""
    data = request.get_json()
    brightness = data.get('brightness', 5)

    # Ограничиваем значение яркости
    brightness = max(0, min(15, brightness))
    display.brightness(brightness)

    return jsonify({'success': True, 'brightness': brightness})

# Предустановленные шаблоны
@app.route('/api/show_pattern', methods=['POST'])
def show_pattern():
    """Отображение предустановленного шаблона"""
    global matrix_state
    data = request.get_json()
    pattern = data.get('pattern', '')

    patterns = {
        'heart': [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'rectangle': [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
    }

    if pattern in patterns:
        matrix_state = patterns[pattern]
        update_display()
        return jsonify({'success': True, 'pattern': pattern})
    else:
        return jsonify({'success': False, 'error': 'Pattern not found'})

if __name__ == '__main__':
    # Очищаем дисплей при запуске
    display.fill(0)
    display.show()

    # Запускаем сервер на всех интерфейсах
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
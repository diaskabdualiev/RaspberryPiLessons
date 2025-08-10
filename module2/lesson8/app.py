from flask import Flask, render_template, request, jsonify
import board
import pwmio
from adafruit_motor import servo
import threading
import time

app = Flask(__name__)

# Инициализация PWM на GPIO 18
pwm = pwmio.PWMOut(board.D18, duty_cycle=2 ** 15, frequency=50)

# Создание объекта сервопривода
my_servo = servo.Servo(pwm, min_pulse=750, max_pulse=2250)

# Установка начального положения (90 градусов)
my_servo.angle = 90

# Текущий угол сервопривода
current_angle = 90

# Блокировка для безопасного доступа к сервоприводу из разных потоков
servo_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html', angle=current_angle)

@app.route('/set_angle', methods=['POST'])
def set_angle():
    global current_angle

    data = request.get_json()
    angle = int(data.get('angle', 90))

    # Ограничиваем угол от 0 до 180
    angle = max(0, min(180, angle))

    with servo_lock:
        my_servo.angle = angle
        current_angle = angle

    return jsonify({"status": "success", "angle": angle})

@app.route('/get_angle', methods=['GET'])
def get_angle():
    return jsonify({"angle": current_angle})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',
        port=5000,
        debug=True,        # можно оставить отладку
        use_reloader=False # но запрещаем второй запуск
        )
    finally:
        # При завершении программы устанавливаем сервопривод в нейтральное положение
        with servo_lock:
            my_servo.angle = 90
        # Освобождаем ресурсы
        pwm.deinit()
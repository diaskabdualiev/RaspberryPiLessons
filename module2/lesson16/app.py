from flask import Flask, render_template, request, jsonify
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

app = Flask(__name__)

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация PCA9685
pca = PCA9685(i2c)

# Установка частоты ШИМ (50 Гц для большинства сервоприводов)
pca.frequency = 50

# Создаем словарь для хранения объектов сервоприводов
# Мы инициализируем только при первом использовании
servo_dict = {}

# Максимальное количество сервоприводов на PCA9685
MAX_SERVOS = 16

# Функция для получения объекта сервопривода
def get_servo(channel):
    # Проверка валидности канала
    if channel < 0 or channel >= MAX_SERVOS:
        return None

    # Если сервопривод для этого канала уже создан, возвращаем его
    if channel in servo_dict:
        return servo_dict[channel]

    # Иначе создаем новый объект сервопривода
    try:
        servo_obj = servo.Servo(pca.channels[channel], min_pulse=500, max_pulse=2500)
        servo_dict[channel] = servo_obj
        return servo_obj
    except Exception as e:
        print(f"Ошибка при создании сервопривода для канала {channel}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html', max_servos=MAX_SERVOS)

@app.route('/set_angle', methods=['POST'])
def set_angle():
    try:
        data = request.get_json()
        channel = int(data.get('channel', 0))
        angle = float(data.get('angle', 90))

        # Получаем объект сервопривода для указанного канала
        servo_obj = get_servo(channel)

        if servo_obj is None:
            return jsonify({'status': 'error', 'message': f'Неверный канал: {channel}'}), 400

        # Ограничиваем угол в диапазоне от 0 до 180
        angle = max(0, min(180, angle))

        # Устанавливаем угол поворота
        servo_obj.angle = angle

        return jsonify({'status': 'success', 'message': f'Канал {channel} установлен на угол {angle}°'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_angle', methods=['GET'])
def get_angle():
    try:
        channel = int(request.args.get('channel', 0))

        # Получаем объект сервопривода для указанного канала
        servo_obj = get_servo(channel)

        if servo_obj is None:
            return jsonify({'status': 'error', 'message': f'Неверный канал: {channel}'}), 400

        # Получаем текущий угол
        angle = getattr(servo_obj, 'angle', 90)

        return jsonify({'status': 'success', 'angle': angle})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_servos():
    try:
        # Устанавливаем все инициализированные сервоприводы в нейтральное положение
        for channel, servo_obj in servo_dict.items():
            servo_obj.angle = 90

        return jsonify({'status': 'success', 'message': 'Все сервоприводы сброшены в нейтральное положение'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    try:
        # Запускаем веб-сервер
        app.run(host='0.0.0.0', port=5000, debug=True)

    except KeyboardInterrupt:
        # При завершении работы сбрасываем все сервоприводы в нейтральное положение
        for servo_obj in servo_dict.values():
            servo_obj.angle = 90
        print("\nПрограмма завершена.")
from flask import Flask, render_template, jsonify
import time
import board
import busio
import adafruit_mpu6050
import math

app = Flask(__name__)

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация MPU6050
mpu = adafruit_mpu6050.MPU6050(i2c)

# Установка диапазонов измерения
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_2_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_250_DPS

# Функция для расчета угла наклона из данных акселерометра
def calculate_tilt_angles(x, y, z):
    roll = math.atan2(y, z) * 180 / math.pi
    pitch = math.atan2(-x, math.sqrt(y*y + z*z)) * 180 / math.pi
    return roll, pitch

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor_data')
def get_sensor_data():
    # Считываем данные с акселерометра
    acceleration = mpu.acceleration

    # Считываем данные с гироскопа
    gyro = mpu.gyro

    # Считываем температуру
    temperature = mpu.temperature

    # Вычисляем углы наклона
    roll, pitch = calculate_tilt_angles(acceleration[0], acceleration[1], acceleration[2])

    # Формируем JSON с данными
    data = {
        'acceleration': {
            'x': round(acceleration[0], 2),
            'y': round(acceleration[1], 2),
            'z': round(acceleration[2], 2)
        },
        'gyro': {
            'x': round(gyro[0], 2),
            'y': round(gyro[1], 2),
            'z': round(gyro[2], 2)
        },
        'temperature': round(temperature, 2),
        'angles': {
            'roll': round(roll, 2),
            'pitch': round(pitch, 2)
        }
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
from flask import Flask, render_template, jsonify
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import threading

app = Flask(__name__)

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация ADS1115
ads = ADS.ADS1115(i2c)

# Настройка канала A0 для потенциометра
potentiometer = AnalogIn(ads, ADS.P0)

# Установка диапазона измерений (±4.096V)
ads.gain = 1

# Глобальные переменные для хранения текущих значений
current_value = 0
current_voltage = 0
current_percent = 0

# Блокировка для многопоточного доступа
lock = threading.Lock()

# Функция для преобразования значения в проценты
def map_to_percent(value, in_min=0, in_max=26000):
    return int((value - in_min) * 100 / (in_max - in_min))

# Функция опроса АЦП в отдельном потоке
def adc_polling():
    global current_value, current_voltage, current_percent

    try:
        while True:
            # Считываем значение с потенциометра
            raw_value = potentiometer.value
            voltage = potentiometer.voltage

            # Преобразуем в проценты
            percent = map_to_percent(raw_value)

            # Обновляем глобальные переменные
            with lock:
                current_value = raw_value
                current_voltage = voltage
                current_percent = percent

            # Задержка для стабилизации показаний
            time.sleep(0.1)

    except Exception as e:
        print(f"Ошибка в потоке опроса АЦП: {e}")

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# API для получения текущих значений
@app.route('/api/adc-state')
def adc_state():
    with lock:
        return jsonify({
            'raw_value': current_value,
            'voltage': current_voltage,
            'percent': current_percent
        })

# Запуск потока опроса АЦП
def start_adc_thread():
    adc_thread = threading.Thread(target=adc_polling, daemon=True)
    adc_thread.start()

if __name__ == '__main__':
    # Запускаем поток для опроса АЦП
    start_adc_thread()

    # Запускаем веб-сервер Flask
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
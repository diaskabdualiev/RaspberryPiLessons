import time
import board
import adafruit_dht
from flask import Flask, render_template
from datetime import datetime

# Инициализация Flask приложения
app = Flask(__name__)

# Инициализация DHT11 датчика
dht_device = adafruit_dht.DHT11(board.D18)  # DHT11 подключен к GPIO18
# Если вы используете DHT22, замените на:
# dht_device = adafruit_dht.DHT22(board.D18)

# Глобальные переменные для хранения последних показаний
temperature = 0
humidity = 0
status = "Ожидание данных..."
last_update = "Никогда"

# Функция для обновления данных с датчика
def update_sensor_data():
    global temperature, humidity, status, last_update

    try:
        # Считываем температуру и влажность
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        # Обновляем статус и время
        status = "Данные получены успешно"
        last_update = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        return True

    except RuntimeError as e:
        # Ошибки чтения датчика случаются довольно часто, особенно на DHT11
        status = f"Ошибка чтения: {e}"
        return False

    except Exception as e:
        status = f"Критическая ошибка: {e}"
        return False

# Маршруты Flask
@app.route('/')
def index():
    # Пытаемся обновить данные с датчика
    update_sensor_data()

    # Рендерим шаблон с текущими данными
    return render_template(
        'index.html',
        temperature=temperature,
        humidity=humidity,
        status=status,
        last_update=last_update
    )

# Функция для запуска фонового обновления данных
def background_update():
    while True:
        update_sensor_data()
        # DHT11 может обновлять данные только раз в 1-2 секунды
        time.sleep(2.0)

# Функция очистки при завершении
def cleanup():
    try:
        dht_device.exit()
        print("\nРесурсы датчика освобождены")
    except:
        pass
    print("Программа завершена")

if __name__ == '__main__':
    # Регистрируем функцию очистки
    import atexit
    atexit.register(cleanup)

    # Запускаем фоновое обновление данных в отдельном потоке
    import threading
    sensor_thread = threading.Thread(target=background_update, daemon=True)
    sensor_thread.start()

    try:
        # Запускаем веб-сервер
        print("Веб-сервер запущен на порту 8080. Нажмите Ctrl+C для завершения.")
        app.run(host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        cleanup()
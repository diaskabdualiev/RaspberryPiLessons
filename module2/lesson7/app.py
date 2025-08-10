import time
import board
import adafruit_hcsr04
from flask import Flask, render_template
from datetime import datetime
import threading

# Инициализация Flask приложения
app = Flask(__name__)

# Настраиваем пины для ультразвукового датчика
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D23, echo_pin=board.D24)

# Глобальные переменные для хранения данных
distance = 0
status = "Ожидание данных..."
last_update = "Никогда"

# Функция для обновления данных с датчика
def update_sensor_data():
    global distance, status, last_update

    try:
        # Получаем расстояние в сантиметрах
        distance = sonar.distance

        # Округляем до одного десятичного знака
        distance = round(distance, 1)

        # Обновляем статус и время
        status = "Данные получены успешно"
        last_update = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        return True

    except RuntimeError as e:
        # Обработка ошибок чтения
        status = "Ошибка чтения данных, проверьте подключение"
        return False

    except Exception as e:
        status = f"Критическая ошибка: {str(e)}"
        return False

# Маршруты Flask
@app.route('/')
def index():
    # Обновляем данные с датчика
    update_sensor_data()

    # Вычисляем процент для прогресс-бара (0-350 см)
    max_distance = 350  # Максимальная дальность HC-SR04 около 350-400 см

    # Ограничиваем значение в пределах 0-100%
    if distance > max_distance:
        percentage = 100
    else:
        percentage = (distance / max_distance) * 100

    # Рендерим шаблон с текущими данными
    return render_template(
        'index.html',
        distance=distance,
        percentage=percentage,
        status=status,
        last_update=last_update
    )

# Функция для запуска фонового обновления данных
def background_update():
    while True:
        update_sensor_data()
        time.sleep(0.5)  # Обновляем каждые 0.5 секунд

# Функция очистки при завершении
def cleanup():
    print("\nПрограмма остановлена")

if __name__ == '__main__':
    # Регистрируем функцию очистки
    import atexit
    atexit.register(cleanup)

    # Запускаем фоновое обновление данных в отдельном потоке
    sensor_thread = threading.Thread(target=background_update, daemon=True)
    sensor_thread.start()

    try:
        # Запускаем веб-сервер
        print("Веб-сервер запущен на порту 8080. Нажмите Ctrl+C для завершения.")
        app.run(host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        cleanup()
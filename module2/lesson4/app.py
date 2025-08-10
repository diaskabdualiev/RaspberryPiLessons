import board
import digitalio
import time
import threading
from flask import Flask, render_template, redirect, url_for

# Настройка пина для активного зуммера
buzzer_pin = digitalio.DigitalInOut(board.D18)  # GPIO18
buzzer_pin.direction = digitalio.Direction.OUTPUT

# Инициализация Flask приложения
app = Flask(__name__)

# Глобальная переменная для отслеживания статуса
status = "Ожидание"
buzzer_active = False

# Функция для подачи звукового сигнала
def beep(duration):
    global status, buzzer_active

    # Предотвращаем одновременное выполнение нескольких сигналов
    if buzzer_active:
        return

    buzzer_active = True
    buzzer_pin.value = True
    status = "Зуммер ВКЛ"
    time.sleep(duration)
    buzzer_pin.value = False
    status = "Ожидание"
    buzzer_active = False

# Функция для запуска двух сигналов
def double_beep():
    global status, buzzer_active

    if buzzer_active:
        return

    buzzer_active = True

    # Первый сигнал
    buzzer_pin.value = True
    status = "Зуммер ВКЛ (1/2)"
    time.sleep(0.2)
    buzzer_pin.value = False
    time.sleep(0.2)

    # Второй сигнал
    buzzer_pin.value = True
    status = "Зуммер ВКЛ (2/2)"
    time.sleep(0.2)
    buzzer_pin.value = False

    status = "Ожидание"
    buzzer_active = False

# Маршруты Flask
@app.route('/')
def index():
    return render_template('index.html', status=status)

@app.route('/beep/<beep_type>')
def trigger_beep(beep_type):
    thread = None

    if beep_type == 'short':
        thread = threading.Thread(target=beep, args=(0.2,))
    elif beep_type == 'double':
        thread = threading.Thread(target=double_beep)
    elif beep_type == 'long':
        thread = threading.Thread(target=beep, args=(1.0,))

    if thread:
        thread.daemon = True
        thread.start()

    return redirect(url_for('index'))

# Функция очистки при завершении
def cleanup():
    buzzer_pin.value = False
    print("\nПрограмма завершена")

if __name__ == '__main__':
    # Регистрируем функцию очистки
    import atexit
    atexit.register(cleanup)

    try:
        # Запускаем веб-сервер
        print("Веб-сервер запущен. Нажмите Ctrl+C для завершения.")
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        cleanup()
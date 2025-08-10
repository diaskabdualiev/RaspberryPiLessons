import board
import pwmio
import time
import threading
from flask import Flask, render_template, redirect, url_for

# Настройка пина для пассивного зуммера с использованием PWM
buzzer = pwmio.PWMOut(board.D18, frequency=440, duty_cycle=0)

# Инициализация Flask приложения
app = Flask(__name__)

# Глобальные переменные для управления состоянием
status = "Готов к воспроизведению"
playing = False
stop_playing = False

# Словарь нот и их частот в Гц
NOTES = {
    'C4': 262,  # До четвертой октавы
    'D4': 294,  # Ре
    'E4': 330,  # Ми
    'F4': 349,  # Фа
    'G4': 392,  # Соль
    'A4': 440,  # Ля
    'B4': 494,  # Си
    'C5': 523,  # До пятой октавы
    'REST': 0,  # Пауза
}

# Мелодия "Маленькая звездочка" (Twinkle Twinkle Little Star)
TWINKLE = [
    ('C4', 0.3), ('C4', 0.3), ('G4', 0.3), ('G4', 0.3),
    ('A4', 0.3), ('A4', 0.3), ('G4', 0.6),
    ('F4', 0.3), ('F4', 0.3), ('E4', 0.3), ('E4', 0.3),
    ('D4', 0.3), ('D4', 0.3), ('C4', 0.6),
]

# Гамма
SCALE = [
    ('C4', 0.3), ('D4', 0.3), ('E4', 0.3), ('F4', 0.3),
    ('G4', 0.3), ('A4', 0.3), ('B4', 0.3), ('C5', 0.3),
    ('C5', 0.3), ('B4', 0.3), ('A4', 0.3), ('G4', 0.3),
    ('F4', 0.3), ('E4', 0.3), ('D4', 0.3), ('C4', 0.3),
]

# Функция для проигрывания ноты заданной длительности
def play_note(note, duration):
    global status

    if note == 'REST':
        # Пауза - просто ждем
        buzzer.duty_cycle = 0
        status = f"Пауза: {duration} сек"
        time.sleep(duration)
    else:
        # Устанавливаем частоту ноты
        buzzer.frequency = NOTES[note]
        # Устанавливаем громкость (50% от максимальной)
        buzzer.duty_cycle = 32768  # 50% от 65535

        note_names = {
            'C4': 'До', 'D4': 'Ре', 'E4': 'Ми', 'F4': 'Фа',
            'G4': 'Соль', 'A4': 'Ля', 'B4': 'Си', 'C5': 'До⁵'
        }
        status = f"Играет нота: {note_names.get(note, note)}"

        # Ждем заданную длительность
        time.sleep(duration)
        # Выключаем звук
        buzzer.duty_cycle = 0
        # Небольшая пауза между нотами
        time.sleep(0.05)

# Функция для проигрывания мелодии
def play_melody(melody_name):
    global playing, stop_playing, status

    if playing:
        return  # Если уже играет мелодия, не запускаем новую

    playing = True
    stop_playing = False

    melody = []
    if melody_name == "twinkle":
        melody = TWINKLE
        status = "Играет: Маленькая звездочка"
    elif melody_name == "scale":
        melody = SCALE
        status = "Играет: Гамма"

    def play_thread():
        global playing, stop_playing, status

        try:
            while not stop_playing:
                # Проигрываем мелодию один раз
                for note, duration in melody:
                    if stop_playing:
                        break
                    play_note(note, duration)

                if stop_playing:
                    break

                # Пауза перед повторением
                time.sleep(0.5)

            buzzer.duty_cycle = 0
            status = "Воспроизведение остановлено"
            playing = False

        except Exception as e:
            buzzer.duty_cycle = 0
            status = f"Ошибка: {str(e)}"
            playing = False

    # Запускаем воспроизведение в отдельном потоке
    threading.Thread(target=play_thread, daemon=True).start()

# Маршруты Flask
@app.route('/')
def index():
    return render_template('index.html', status=status)

@app.route('/play/<melody>')
def play(melody):
    play_melody(melody)
    return redirect(url_for('index'))

@app.route('/note/<note>')
def play_single_note(note):
    global status

    if note in NOTES:
        # Остановим любое текущее воспроизведение
        stop()

        # Проигрываем отдельную ноту в отдельном потоке
        def note_thread():
            play_note(note, 0.5)  # Играем ноту 0.5 секунды
            global status
            status = "Готов к воспроизведению"

        threading.Thread(target=note_thread, daemon=True).start()

    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global stop_playing, status

    stop_playing = True
    buzzer.duty_cycle = 0
    status = "Готов к воспроизведению"

    return redirect(url_for('index'))

# Функция очистки при завершении
def cleanup():
    buzzer.duty_cycle = 0
    print("\nПрограмма завершена")

if __name__ == '__main__':
    # Регистрируем функцию очистки
    import atexit
    atexit.register(cleanup)

    try:
        # Запускаем веб-сервер
        print("Веб-сервер запущен на порту 8080. Нажмите Ctrl+C для завершения.")
        app.run(host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        cleanup()
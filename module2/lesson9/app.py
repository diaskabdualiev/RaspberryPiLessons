from flask import Flask, render_template, request, jsonify
import board
import digitalio
import threading

app = Flask(__name__)

# Инициализация пина GPIO18 как выход для управления реле
relay = digitalio.DigitalInOut(board.D18)
relay.direction = digitalio.Direction.OUTPUT

# Устанавливаем начальное состояние реле - выключено
relay.value = True  # Для реле с инверсной логикой True = выключено

# Текущее состояние реле
relay_state = False  # False = выключено, True = включено

# Блокировка для безопасного доступа к реле из разных потоков
relay_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html', state=relay_state)

@app.route('/toggle_relay', methods=['POST'])
def toggle_relay():
    global relay_state

    data = request.get_json()
    state = data.get('state', False)

    with relay_lock:
        if state:
            # Включаем реле (для инверсной логики значение FALSE)
            relay.value = False
            relay_state = True
        else:
            # Выключаем реле (для инверсной логики значение TRUE)
            relay.value = True
            relay_state = False

    return jsonify({
        "status": "success",
        "state": relay_state,
        "message": "Реле включено" if relay_state else "Реле выключено"
    })

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify({"state": relay_state})

if __name__ == '__main__':
    try:
        # Запуск Flask приложения на всех интерфейсах (0.0.0.0)
        # Чтобы можно было подключиться с других устройств в сети
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # При завершении программы отключаем реле (безопасное состояние)
        with relay_lock:
            relay.value = True  # Для реле с инверсной логикой
from flask import Flask, jsonify, render_template
import digitalio, board, threading, time

# ──────────── GPIO ────────────
PIN_A = digitalio.DigitalInOut(board.D17)
PIN_B = digitalio.DigitalInOut(board.D18)
BTN   = digitalio.DigitalInOut(board.D27)

for pin in (PIN_A, PIN_B, BTN):
    pin.direction = digitalio.Direction.INPUT
    pin.pull      = digitalio.Pull.UP      # энкодер «замыкает на GND»

# ──────────── глобальное состояние ────────────
counter = 0
direction = "—"
button_pressed = False
events = []

_lock = threading.Lock()

# ──────────── квадратурная таблица (Gray) ────────────
# transition = (prev<<2)|curr  → ±1 / 0 / error
_STEP_TAB = {
    0b0001: +1, 0b0010: -1, 0b0100: -1, 0b0111: +1,
    0b1000: +1, 0b1011: -1, 0b1101: -1, 0b1110: +1,
}

# ──────────── поток опроса ────────────
def encoder_worker():
    global counter, direction, button_pressed, events
    last_state = (PIN_A.value << 1) | PIN_B.value
    last_btn   = BTN.value
    btn_time   = time.monotonic()

    while True:
        now_state = (PIN_A.value << 1) | PIN_B.value
        transition = (last_state << 2) | now_state
        step = _STEP_TAB.get(transition, 0)
        if step:
            counter += step
            direction = "↻" if step > 0 else "↺"
            with _lock:
                events.append(f"{direction}  →  {counter}")
                events[:] = events[-12:]
        last_state = now_state

        # — антидребезг кнопки (20 мс) —
        curr_btn = BTN.value
        if curr_btn != last_btn:
            btn_time = time.monotonic()
            last_btn = curr_btn
        elif not curr_btn and (time.monotonic() - btn_time) > 0.02:
            # нажатие подтверждено
            if not button_pressed:
                button_pressed = True
                with _lock:
                    events.append(f"Кнопка: сброс счётчика ({counter}→0)")
                    counter = 0
                    events[:] = events[-12:]
        else:
            button_pressed = False

        time.sleep(0.001)   # 1 кГц опроса

# ──────────── Flask ────────────
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")      # ваш шаблон

@app.route("/api/state")
def state():
    with _lock:
        return jsonify(
            counter=counter,
            direction=direction,
            button=button_pressed,
            events=list(events),
        )

# ──────────── запуск ────────────
if __name__ == "__main__":
    threading.Thread(target=encoder_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, threaded=True)
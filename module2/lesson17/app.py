from flask import Flask, render_template, request
from RPLCD.i2c import CharLCD
import time

app = Flask(__name__)

# Создаем объект LCD
# Адрес по умолчанию 0x27, при необходимости замените на 0x3F или другой
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
            cols=16, rows=2, dotsize=8)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display_text():
    # Получаем текст из формы
    line1 = request.form['line1']
    line2 = request.form['line2']

    # Очищаем дисплей
    lcd.clear()

    # Выводим первую строку
    lcd.cursor_pos = (0, 0)  # Первая строка
    lcd.write_string(line1[:16])  # Ограничиваем 16 символами

    # Выводим вторую строку
    lcd.cursor_pos = (1, 0)  # Вторая строка
    lcd.write_string(line2[:16])  # Ограничиваем 16 символами

    return render_template('index.html',
                           message="Текст успешно отправлен на дисплей!",
                           line1=line1,
                           line2=line2)

@app.route('/clear', methods=['POST'])
def clear_display():
    # Очищаем дисплей
    lcd.clear()
    return render_template('index.html', message="Дисплей очищен!")

if __name__ == '__main__':
    try:
        # При запуске программы здороваемся
        lcd.clear()
        lcd.write_string("LCD Ready!")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Web app started")

        # Запускаем веб-сервер
        app.run(host='0.0.0.0', port=5000, debug=True)

    except KeyboardInterrupt:
        # При выходе очищаем дисплей
        lcd.clear()
        print("Программа завершена.")
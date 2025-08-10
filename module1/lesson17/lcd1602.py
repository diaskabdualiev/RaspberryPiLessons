from RPLCD.i2c import CharLCD
import time

# Параметры вашего дисплея
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,    # замените, если i2cdetect показал 0x3F
    port=1,
    cols=16,
    rows=2,
    dotsize=8
)

lcd.clear()                 # Очистка экрана
lcd.write_string('helloworld')
lcd.cursor_pos = (1, 0)     # Вторая строка, первый столбец
lcd.write_string('Raspberry Pi 5')

time.sleep(5)               # Пауза 5 с
lcd.clear()                 # Очистка перед выходом
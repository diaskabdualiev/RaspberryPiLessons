import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация ADS1115
ads = ADS.ADS1115(i2c)

# Настройка канала A0 для потенциометра
potentiometer = AnalogIn(ads, ADS.P0)

# Установка диапазона измерений (±4.096V)
ads.gain = 1

# Функция для преобразования значения в проценты
def map_to_percent(value, in_min=0, in_max=26000):
    return int((value - in_min) * 100 / (in_max - in_min))

# Функция для создания ASCII-графика
def create_ascii_bar(percent, length=50):
    filled_length = int(length * percent / 100)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}] {percent}%"

# Основной цикл
try:
    print("Модуль АЦП ADS1115 готов к работе!")
    print("Вращайте потенциометр для изменения значений")
    print("Нажмите Ctrl+C для выхода")
    print()

    # Небольшая задержка для инициализации
    time.sleep(0.5)

    while True:
        # Считываем значение с потенциометра
        raw_value = potentiometer.value
        voltage = potentiometer.voltage

        # Преобразуем в проценты
        percent = map_to_percent(raw_value)

        # Создаем визуальное представление
        bar = create_ascii_bar(percent)

        # Очищаем предыдущую строку и выводим новую информацию
        print(f"\rЗначение: {raw_value:5d} | Напряжение: {voltage:.3f}V | {bar}", end="", flush=True)

        # Задержка для стабилизации показаний
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\nПрограмма завершена.")
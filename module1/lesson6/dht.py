import time
import board
import adafruit_dht

# Инициализация DHT11 датчика с указанием пина
# Для Raspberry Pi, используем нумерацию пинов из библиотеки board
dht_device = adafruit_dht.DHT11(board.D18)  # DHT11 подключен к GPIO18

# Если вы используете DHT22, замените на:
# dht_device = adafruit_dht.DHT22(board.D18)

# Главный цикл
while True:
    try:
        # Считываем температуру и влажность
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        # Выводим показания
        print(f"Температура: {temperature:.1f}°C   Влажность: {humidity:.1f}%")

    except RuntimeError as e:
        # Ошибки чтения датчика случаются довольно часто, особенно на DHT11
        # Не паникуйте, просто попробуем снова
        print(f"Ошибка чтения: {e}")

    except Exception as e:
        # В случае критической ошибки, освобождаем ресурсы и выходим
        dht_device.exit()
        raise e

    # Ждем 2 секунды перед следующим чтением
    # DHT11 может обновлять данные только раз в 1-2 секунды
    time.sleep(2.0)
#!/usr/bin/env python3
# HC-SR04 ультразвуковой датчик на CircuitPython
# Подключение:
# - VCC к 5V
# - GND к GND
# - Trig к GPIO23 (BCM)
# - Echo к GPIO24 (BCM)

import time
import board
import digitalio
import adafruit_hcsr04

# Настраиваем пины для ультразвукового датчика
# На Raspberry Pi используйте правильные пины для вашего подключения
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D23, echo_pin=board.D24)

# Функция для вывода расстояния в консоль
def display_distance(distance):
    print(f"Расстояние: {distance:.1f} см")

    # Для визуализации можно добавить графическое представление расстояния
    if distance < 350:  # Максимальная дальность HC-SR04 около 4 метров
        bar_count = int(distance // 5)  # 1 символ на каждые 5 см
        bar = '█' * bar_count
        print(f"[{bar.ljust(70)}] {distance:.1f} см")

# Основная функция программы
def main():
    print("Мониторинг расстояния с HC-SR04")
    print("Нажмите Ctrl+C для выхода")
    print("-" * 50)

    try:
        while True:
            try:
                # Получаем расстояние в сантиметрах
                distance = sonar.distance
                display_distance(distance)
            except RuntimeError:
                # Обработка ошибок чтения
                print("Ошибка чтения данных, проверьте подключение")

            # Пауза между измерениями
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")

if __name__ == "__main__":
    main()
import time
import board
import pwmio
from adafruit_motor import servo

# Инициализация PWM на GPIO 18
pwm = pwmio.PWMOut(board.D18, duty_cycle=2 ** 15, frequency=50)

# Создание объекта сервопривода
# Параметры min_pulse и max_pulse можно регулировать для точной настройки углов
my_servo = servo.Servo(pwm, min_pulse=750, max_pulse=2250)

try:
    while True:
        print("Поворот на 0°")
        my_servo.angle = 0
        time.sleep(1)

        print("Поворот на 90°")
        my_servo.angle = 90
        time.sleep(1)

        print("Поворот на 180°")
        my_servo.angle = 180
        time.sleep(1)

        # Плавное движение от 180° к 0°
        print("Плавное движение от 180° к 0°")
        for angle in range(180, -1, -5):  # Шаг 5 градусов
            my_servo.angle = angle
            time.sleep(0.05)

        # Плавное движение от 0° к 180°
        print("Плавное движение от 0° к 180°")
        for angle in range(0, 181, 5):  # Шаг 5 градусов
            my_servo.angle = angle
            time.sleep(0.05)

except KeyboardInterrupt:
    print("\nПрограмма завершена.")
    # Устанавливаем сервопривод в нейтральное положение перед выходом
    my_servo.angle = 90
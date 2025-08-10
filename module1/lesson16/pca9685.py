import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Инициализация I2C интерфейса
i2c = busio.I2C(board.SCL, board.SDA)

# Инициализация PCA9685
pca = PCA9685(i2c)

# Установка частоты ШИМ (50 Гц для большинства сервоприводов)
pca.frequency = 50

# Создаем объекты сервоприводов
# Здесь мы используем первые 3 канала (0, 1, 2) для примера
servo0 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
servo1 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500)
servo2 = servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2500)

# Список всех сервоприводов для удобства
servos = [servo0, servo1, servo2]

# Демонстрация последовательного движения
def sequential_movement():
    print("Последовательное движение сервоприводов...")
    for i, servo_motor in enumerate(servos):
        print(f"Сервопривод {i}: поворот на 0°")
        servo_motor.angle = 0
        time.sleep(0.5)

        print(f"Сервопривод {i}: поворот на 90°")
        servo_motor.angle = 90
        time.sleep(0.5)

        print(f"Сервопривод {i}: поворот на 180°")
        servo_motor.angle = 180
        time.sleep(0.5)

        print(f"Сервопривод {i}: возврат на 90°")
        servo_motor.angle = 90
        time.sleep(0.5)

# Демонстрация одновременного движения
def synchronized_movement():
    print("Синхронное движение всех сервоприводов...")

    # Установка всех сервоприводов в начальное положение
    for servo_motor in servos:
        servo_motor.angle = 0
    time.sleep(1)

    # Плавное движение всех сервоприводов от 0° до 180°
    for angle in range(0, 181, 5):
        for servo_motor in servos:
            servo_motor.angle = angle
        print(f"Угол: {angle}°")
        time.sleep(0.05)

    # Пауза в конечном положении
    time.sleep(1)

    # Плавное движение всех сервоприводов от 180° до 0°
    for angle in range(180, -1, -5):
        for servo_motor in servos:
            servo_motor.angle = angle
        print(f"Угол: {angle}°")
        time.sleep(0.05)

# Демонстрация волнового движения
def wave_movement():
    print("Волновое движение сервоприводов...")
    for _ in range(3):  # Повторить 3 раза
        # Волна вперед
        for i in range(len(servos)):
            servos[i].angle = 150
            time.sleep(0.2)
            servos[i].angle = 30

        # Волна назад
        for i in range(len(servos) - 1, -1, -1):
            servos[i].angle = 150
            time.sleep(0.2)
            servos[i].angle = 30

# Основной цикл
try:
    print("PCA9685 готов к работе!")
    print("Демонстрация различных типов движения сервоприводов")

    # Устанавливаем все сервоприводы в нейтральное положение
    for servo_motor in servos:
        servo_motor.angle = 90
    time.sleep(1)

    # Демонстрация различных типов движения
    sequential_movement()
    time.sleep(1)

    synchronized_movement()
    time.sleep(1)

    wave_movement()
    time.sleep(1)

    # Возвращаем все сервоприводы в нейтральное положение
    print("Возврат в нейтральное положение...")
    for servo_motor in servos:
        servo_motor.angle = 90

    print("Демонстрация завершена!")

except KeyboardInterrupt:
    # Перед выходом устанавливаем все сервоприводы в безопасное положение
    for servo_motor in servos:
        servo_motor.angle = 90
    print("\nПрограмма завершена.")
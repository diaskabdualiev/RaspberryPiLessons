import time
import board
import digitalio

# Инициализация выводов энкодера
# Выходы A и B энкодера подключены к GPIO17 и GPIO18 соответственно
pin_a = digitalio.DigitalInOut(board.D17)
pin_b = digitalio.DigitalInOut(board.D18)
pin_a.direction = digitalio.Direction.INPUT
pin_b.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP  # Подтяжка к питанию
pin_b.pull = digitalio.Pull.UP  # Подтяжка к питанию

# Инициализация кнопки энкодера
button = digitalio.DigitalInOut(board.D27)  # Кнопка на GPIO27
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Подтяжка к VCC (кнопка замыкает на GND)

# Глобальные переменные
counter = 0
button_state = False
last_button_state = False
last_a_state = pin_a.value

# Главный цикл
try:
    print("Роторный энкодер: поворачивайте ручку или нажмите на нее")
    print("Нажмите Ctrl+C для выхода")

    while True:
        # Считываем текущее состояние выводов энкодера
        a_state = pin_a.value
        b_state = pin_b.value

        # Если состояние вывода A изменилось, значит произошло вращение
        if a_state != last_a_state:
            # Определяем направление вращения сравнивая состояния выводов A и B
            if b_state != a_state:
                direction = "по часовой стрелке"
                counter += 1
            else:
                direction = "против часовой стрелки"
                counter -= 1

            # Выводим информацию
            print(f"Направление: {direction}, Счетчик: {counter}")

        # Обновляем последнее состояние вывода A
        last_a_state = a_state

        # Обработка нажатия кнопки
        button_state = not button.value  # Инвертируем значение, так как кнопка подтянута к VCC

        # Проверяем изменение состояния кнопки (обнаружение фронта)
        if button_state and not last_button_state:
            print("Кнопка нажата! Сброс счетчика.")
            counter = 0

        # Обновляем последнее состояние кнопки
        last_button_state = button_state

        # Небольшая задержка для стабилизации
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nПрограмма завершена.")
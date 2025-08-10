#Уроки для набора Raspberry Pi 4

Уроки включают в себя два модуля 
Hardware
Soft+Hardware

Основной стэк это 
Hardware: CircuitPython
Software: FlaskPython

Для работы обезятельно требуется 
python enviroment
для его создания 

hostname pialash.local
login alashed
password alashed

wifi AlashElectronics
password 28071917

ssh enabled password

sudo apt update & sudo apt upgrade -y
sudo raspi-config

vnc enable
spi enable
i2c enable 
Serial Port enable
1-wire enable

reboot

git clone https://github.com/diaskabdualiev/RaspberryPiLessons.git
cd RaspberryPiLessons

pcmanfm --set-wallpaper="/home/pi/RaspberryPiLessons/AlashRaspberryPiKit.png" #для обоев

sudo apt install code установка vscode

создание ярлыка на рабочем столе

Advanced Options → Expand Filesystem.
еслт 32г образ установлен например в 64гб флешку

```bash
python3 -m venv venv
```

после его установки в директорий должна появиться папка venv

для активаций вводим команду 

```bash
source venv/bin/activate
```
после этого установливаем необходимые зависмости

```bash
pip install -r requirements.txt
```

для выхода и виртуальной среды используем команду 

```bash
deactivate
```

```bash
sudo apt update & sudo apt upgrade

sudo apt install python3-venv python3-full

pip install adafruit-blinka
pip install adafruit-circuitpython-dht
pip install adafruit-circuitpython-hcsr04
pip install adafruit-circuitpython-servokit
pip install adafruit-circuitpython-matrixkeypad
pip install adafruit-circuitpython-debouncer
pip install adafruit-circuitpython-max7219
pip install adafruit-circuitpython-ads1x15
pip install adafruit-circuitpython-mpu6050
pip install adafruit-circuitpython-pca9685
pip install RPLCD smbus2 #рабоает не корректно с adafruit
pip install adafruit-circuitpython-pn532

#для второго модуля 
pip install flask
```

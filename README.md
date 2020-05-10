# Parser
##### Syntactical analyzer

Парсер - синтаксический анализатор, преобразующий входные данные - запрос пользователя или сообщение полученное с сервера, в структурированный формат команды и последующее её выполнение.

#### Приступая к работе
Скопируйте репозиторий командой:
`$ git clone https://github.com/SmartHome-Assistance/Parser`

##### Необходимые требования

- Python 3.6.5+
- PyAudio 0.2.11+
- pygame 1.9.6
- Mosquitto
- paho-mqtt 1.5.0
- pyowm 2.10.0
- DateTime 4.3
- smbus

##### Установка компонент в Linux
- *Python*
Новая версия, Python 3.6 доступна в репозиториях universe. Поэтому достаточно просто обновить систему и установить пакет нужной версии. Для этого наберите:
`$ sudo apt update`
`$ sudo apt install python3.6`

- *PyAudio*
Для установки PyAudio, введите:
`$ sudo apt-get install python-pyaudio python3-pyaudio`

- *pygame*
Pygame - это модуль оболочки Python для библиотеки мультимедиа SDL.  Для установки, введите:
`$ pip install pygame`

- *Mosquitto*
Чтобы установить Mosquitto, введите:
`$ sudo apt-get install mosquitto mosquitto-clients`

- *paho-mqtt*
В этом документе описывается исходный код клиентской библиотеки Eclipse Paho MQTT Python, которая реализует версии 3.1 и 3.1.1 протокола MQTT. Введите команду для установки:
`$ pip install paho-mqtt`

- *pyowm*
PyOWM - это клиентская библиотека-оболочка Python для веб-API OpenWeatherMap. Для установки, введите:
`$ pip install pyowm`

- *DateTime*
Инкапсуляция значений даты / времени. Чтобы установить, введите
`$ pip install DateTime`

- *smbus*
Для установки SMBus, введите:
`$ sudo apt install python-smbus`

После установки всех компонент, убедитесь в подключении микрофона и устройства вывода, a затем просто запустите файл nomad.py

# Описание
Этот проект представляет собой инструмент командной строки для перобразования текста из входного формата (toml) в выходной (учебный конфигурационный язык)
# Установка
Для начала, убедитесь, что у вас установлен Python. Затем выполните следующие шаги:
1.Установка программы и переход в директорию
```
git clone https://github.com/skufirovan/conf-lang.git
cd ./conf-lang
```
2.Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```
3.Установите необходимые зависимости (pytest для тестов)
```
pip install pytest
```
# Запуск скрипта
Скрипт принимает текст конфигурационного файла через стандартный ввод и выводит в файле.

Пример запуска:
```
python main.py input.toml output.txt
```
Здесь:
- input.toml — файл с конфигурационными данными на языке toml.
- output.txt — файл с конфигурационными данными на учебном языке.

# Примеры входных и выходных данных:
## Пример 1
### Входные данные (TOML):
```
# Comment 1
Max_connections = 100
Timeout = 30
Ports = [80, 443, 8080]
```
### Выходные данные:
```
! Comment 1
Max_connections: 100;
Timeout: 30;
Ports: array(80, 443, 8080);
```

## Пример 2
### Входные данные (TOML):
```
# number of blades
Blades = 4
# number of speed modes
Speed_mode = 3
# rotation speed
Speed = [100, 200, 300]
```
### Выходные данные:
```
! number of blades
Blades: 4;
! number of speed modes
Speed_mode: 3;
! rotation speed
Speed: array(100, 200, 300);
```

# Тесты
Шаги запуска тестов:
1. Установить библиотеку pytest (необходимо, если не сделано ранее):
```
pip install pytest
```
2. Для запуска тестирования необходимо запустить следующий скрипт:
```
pytest -v test.py
```
## Прохождение тестов:
![image](https://github.com/skufirovan/conf-lang/blob/main/img/pytest.png?raw=true)
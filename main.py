import sys
import toml
import re

def parse_toml(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        data = {}
        comments = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('#'):
                comments.append(stripped_line.lstrip('#').strip())  # Удаляем символ # и пробелы
            else:
                comments.append(None)  # Сохраняем структуру для привязки к данным
        toml_content = "\n".join([line.split('#', 1)[0].strip() for line in lines])
        parsed_data = toml.loads(toml_content)
        return parsed_data, comments
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.", file=sys.stderr)
        sys.exit(1)
    except toml.TomlDecodeError as e:
        print(f"Ошибка разбора TOML: {e}", file=sys.stderr)
        sys.exit(1)

def is_valid_name(name):
    return bool(re.fullmatch(r"[_A-Z][_a-zA-Z0-9]*", name))

def evaluate_expression(expr, constants):
    try:
        # Заменяем ссылки на константы их значениями
        for name in constants:
            expr = expr.replace(f"^{name}", str(constants[name]))
        # Вычисляем итоговое значение
        return eval(expr)  # Используем eval для простых арифметических операций
    except Exception as e:
        raise ValueError(f"Ошибка вычисления выражения '{expr}': {e}")

def convert_to_custom_config(data, comments):
    config_lines = []
    constants = {}  # Словарь для хранения значений констант

    # Генерация списка ключей, чтобы привязывать комментарии правильно
    keys = list(data.keys())
    comment_index = 0

    def process_value(key, value):
        nonlocal comment_index
        if not is_valid_name(key):
            raise ValueError(f"Недопустимое имя переменной: {key}")

        # Обрабатываем комментарии перед текущим ключом
        while comment_index < len(comments) and comments[comment_index] is not None:
            config_lines.append(f"! {comments[comment_index]}")
            comment_index += 1

        # Переходим к следующему комментарию
        comment_index += 1

        if isinstance(value, int):
            config_lines.append(f'{key}: {value};')
            constants[key] = value  # Сохраняем константу
        elif isinstance(value, list):
            config_lines.append(f'{key}: array({", ".join(map(str, value))});')
        elif isinstance(value, str):
            # Проверяем на конструкцию вычисления ^[имя] или выражения
            if value.startswith("^"):
                resolved_value = evaluate_expression(value, constants)
                config_lines.append(f'{key}: {resolved_value};')
                constants[key] = resolved_value
            else:
                config_lines.append(f'{key}: "{value}";')
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                process_value(f"{key}_{sub_key}", sub_value)
        else:
            raise ValueError(f"Недопустимый тип значения для {key}: {type(value).__name__}")

    for key in keys:
        process_value(key, data[key])

    # Добавляем оставшиеся комментарии, если они не были связаны с данными
    while comment_index < len(comments):
        if comments[comment_index] is not None:
            config_lines.append(f"! {comments[comment_index]}")
        comment_index += 1

    return '\n'.join(config_lines)

def save_config(file_path, config_content):
    try:
        with open(file_path, 'w') as file:
            file.write(config_content)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Использование: python script.py <путь_к_входному_файлу> <путь_к_выходному_файлу>", file=sys.stderr)
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data, comments = parse_toml(input_file)
    try:
        config_content = convert_to_custom_config(data, comments)
    except ValueError as e:
        print(f"Ошибка конвертации: {e}", file=sys.stderr)
        sys.exit(1)

    save_config(output_file, config_content)

if __name__ == '__main__':
    main()
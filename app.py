#print("Hello from app.py")
import argparse
from tinydb import TinyDB, Query
import re
import json
import os
import sys

# Удаляем db.json, если он существует
if os.path.exists('db.json'):
    os.remove('db.json')

db = TinyDB('db.json')
Form = Query()

# Добавим функцию, которая будет заполнять дб если она пуста
def create_database():
    db.insert({"name": "Проба", "f_name1": "email", "f_name2": "date"})
    db.insert({"name": "Форма заказа", "customer": "text", "order_id": "text", "дата_заказа": "date", "contact": "phone"})
    db.insert({"name": "Данные пользователя", "login": "email", "tel": "phone"})

# Если db пустая, то заполняем ее
if not db.all():
    create_database()


def validate_date(date_string):
    date_patterns = [r"^\d{2}\.\d{2}\.\d{4}$", r"^\d{4}-\d{2}-\d{2}$"]
    for pattern in date_patterns:
        if re.match(pattern, date_string):
            return True
    return False

def validate_phone(phone_string):
    pattern_with_spaces = r"^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$"
    pattern_without_spaces = r"^\+7\d{3}\d{3}\d{2}\d{2}$"
    if re.match(pattern_with_spaces, phone_string) or re.match(pattern_without_spaces, phone_string):
        return True
    return False

def validate_email(email_string):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email_string):
        return True
    return False

def detect_type(value):
    print(f"Определение типа для значения: '{value}'")  # Добавили отладочную печать
    if validate_date(value):
        print("Тип: date") # Добавили отладочную печать
        return "date"
    elif validate_phone(value):
        print("Тип: phone") # Добавили отладочную печать
        return "phone"
    elif validate_email(value):
        print("Тип: email") # Добавили отладочную печать
        return "email"
    else:
        print("Тип: text") # Добавили отладочную печать
        return "text"

def find_template(params):
    template_found = None  # Добавим переменную, чтобы хранить найденный шаблон

    for item in db.all():
        print(f"Проверяем шаблон: {item}")
        template_name = item.get('name')
        template = item.copy()
        template.pop('name', None)

        # Сначала проверим, подходит ли шаблон "Проба"
        if template_name == "Проба" and len(params) == 2 and all(key in params for key in template):
            if detect_type(params["f_name1"]) == "email" and detect_type(params["f_name2"]) == "date":
                print(f"Шаблон найден: {template_name}")
                template_found = template_name
                break
            else:
                continue

        # Если это не шаблон "Проба" или параметров больше двух,
        # то проверяем соответствие по общим правилам
        if len(params) != len(template):
            continue

        match = True
        for key in template:
            if key not in params or detect_type(params[key]) != template[key]:
                match = False
                break

        if match:
            print(f"Шаблон найден: {template_name}")
            template_found = template_name
            break

    return template_found  # Возвращаем найденный шаблон (или None)


if __name__ == "__main__":
    # Проверяем, что скрипт запущен с аргументами командной строки
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Поиск шаблонов форм по параметрам.')
        parser.add_argument('command', choices=['get_tpl'], help='Команда для выполнения: get_tpl')
        parser.add_argument('--version', action='version', version='%(prog)s 0.1')
        args, unknown = parser.parse_known_args()

        params = {}
        for arg in unknown:
            if arg.startswith('--'):
                try:
                    name, value = arg[2:].split('=', 1)
                    params[name] = value
                except ValueError:
                    print(f"Неверный формат аргумента: {arg}")
                    exit()

        if args.command == 'get_tpl':
            template_name = find_template(params)
            if template_name:
                print(template_name)
            else:
                detected_types = {}
                for key, value in params.items():
                    detected_types[key] = detect_type(value)
                print(json.dumps(detected_types, indent=2, ensure_ascii=False))
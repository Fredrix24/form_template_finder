import argparse
from tinydb import TinyDB, Query
import re
import json
import os
import sys

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.json')

if os.path.exists(db_path):
    os.remove(db_path)

db = TinyDB(db_path)
Form = Query()

def create_database():
    db.insert({"name": "Проба", "f_name1": "email", "f_name2": "date"})
    db.insert({"name": "Форма заказа", "customer": "text", "order_id": "text", "дата_заказа": "date", "contact": "phone"})
    db.insert({"name": "Данные пользователя", "login": "email", "tel": "phone"})

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
    if validate_date(value):
        return "date"
    elif validate_phone(value):
        return "phone"
    elif validate_email(value):
        return "email"
    else:
        return "text"

def find_template(params):
    template_found = None

    for item in db.all():
        template_name = item.get('name')
        template = item.copy()
        template.pop('name', None)

        match = True
        for key, expected_type in template.items():
            if key not in params:
                match = False
                break
            if detect_type(params[key]) != expected_type:
                match = False
                break

        if match:
            template_found = template_name
            break

    return template_found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Поиск шаблонов форм по параметрам.')
    parser.add_argument('command', choices=['get_tpl'], help='Команда для выполнения: get_tpl')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--params_file', required=True, help='Файл с параметрами в формате JSON')

    args = parser.parse_args()

    params = {}
    if args.params_file:
        try:
            with open(args.params_file, "r", encoding="utf-8") as f:
                params = json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл {args.params_file} не найден.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Ошибка: Некорректный JSON в файле {args.params_file}.")
            sys.exit(1)

    if args.command == 'get_tpl':
        template_name = find_template(params)
        result = {}
        if template_name:
            result = template_name
        else:
            detected_types = {}
            for key, value in params.items():
                detected_types[key] = detect_type(value)
            result = detected_types

        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False)
import subprocess
import json
import os
import unittest
import locale

class TestAppRequests(unittest.TestCase):
    def run_test(self, params):
        # Создаем временные JSON-файлы
        params_file = "temp_params.json"
        result_file = "result.json"

        # Записываем параметры в JSON-файл
        with open(params_file, "w", encoding="utf-8") as f:
            json.dump(params, f, ensure_ascii=False)

        # Получаем путь к интерпретатору Python из виртуального окружения
        python_path = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

        # Запускаем app.py с указанием файла параметров
        process = subprocess.Popen(
            [python_path, "app.py", "get_tpl", "--params_file=" + params_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        # Выводим stderr, если есть
        if stderr:
            print(f"Сообщение об ошибке (stderr): {stderr.decode('utf-8', errors='ignore')}")

        # Проверяем код возврата
        if process.returncode != 0:
            print(f"Ошибка выполнения subprocess: Код возврата {process.returncode}")
            # Clean up files before returning
            if os.path.exists(params_file):
                os.remove(params_file)
            if os.path.exists(result_file):
                os.remove(result_file)
            return None

        # Читаем результат из JSON-файла
        try:
            with open(result_file, "r", encoding="utf-8") as f:
                result = json.load(f)
        except FileNotFoundError:
            print(f"Файл с результатом ({result_file}) не найден.")
            result = None

        # Удаляем временные файлы
        if os.path.exists(params_file):
            os.remove(params_file)
        if os.path.exists(result_file):
            os.remove(result_file)

        return result

    def test_find_template_proba(self):
        params = {"f_name1": "test@test.com", "f_name2": "27.05.2025"}
        result = self.run_test(params)
        self.assertEqual(result, "Проба")

    def test_find_template_user_data(self):
        params = {"login": "test@test.com", "tel": "+7 903 123 45 67"}
        result = self.run_test(params)
        self.assertEqual(result, "Данные пользователя")

    def test_find_template_no_match(self):
        params = {"tumba": "27.05.2025", "yumba": "+7 903 123 45 78"}
        result = self.run_test(params)
        self.assertEqual(result, {"tumba": "date", "yumba": "phone"})

    def test_find_template_invalid_email(self):
        params = {"f_name1": "invalid-email", "f_name2": "27.05.2025"}
        result = self.run_test(params)
        self.assertEqual(result, {"f_name1": "text", "f_name2": "date"})

if __name__ == '__main__':
    unittest.main()
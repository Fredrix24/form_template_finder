import app
import json

test_cases = [
    {
        "params": {"f_name1": "test@test.com", "f_name2": "27.05.2025"},
        "expected_output": "Проба"
    },
    {
        "params": {"tumba": "27.05.2025", "yumba": "+7 903 123 45 78"},
        "expected_output": '{"tumba": "date", "yumba": "phone"}'
    },
    {
        "params": {"login": "test@test.com", "tel": "+7 903 123 45 67"},
        "expected_output": "Данные пользователя"
    },
    {
        "params": {"f_name1": "invalid-email", "f_name2": "27.05.2025"},
        "expected_output": '{"f_name1": "text", "f_name2": "date"}'
    }
]

def run_test(params, expected_output):
    template_name = app.find_template(params)
    if template_name:
        output = template_name
    else:
        output = json.dumps({k: app.detect_type(v) for k, v in params.items()}, ensure_ascii=False, sort_keys=True)

    if output == expected_output:
        print(f"Тест пройден: {params}")
        return True
    else:
        print(f"Тест не пройден: {params}")
        print(f"  Ожидалось: {expected_output}")
        print(f"  Получено: {output}")
        return False

if __name__ == "__main__":
    all_tests_passed = True
    for test_case in test_cases:
        params = test_case["params"]
        expected_output = test_case["expected_output"]
        if not run_test(params, expected_output):
            all_tests_passed = False

    if all_tests_passed:
        print("Все тесты пройдены!")
    else:
        print("Есть непройденные тесты!")
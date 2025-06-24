from tinydb import TinyDB, Query

db = TinyDB('test.json')

# Очищаем таблицу перед добавлением новой записи
db.drop_table('_default')

db.insert({'name': 'John', 'age': 24})

User = Query()
result = db.search(User.name == 'John')

print(result)

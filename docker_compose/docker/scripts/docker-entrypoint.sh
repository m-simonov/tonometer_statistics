#!/usr/bin/env sh

set -e

# Указываем имя файла SQL-запросов
sql_file="create_db.sql"

# Указываем имя базы данных SQLite
db_name="tonometer.db"

# Проверяем, существует ли файл SQL-запросов
if [ ! -f "$sql_file" ]; then
    echo "Файл $sql_file не найден."
    touch $sql_file
    echo "Файл $sql_file создан."
    exit 1
fi

# Выполняем SQL-запросы к базе данных SQLite
sqlite3 "$db_name" < "$sql_file"

# Проверяем код возврата sqlite3
if [ $? -eq 0 ]; then
    echo "SQL-запросы успешно выполнены."
else
    echo "Ошибка выполнения SQL-запросов."
fi

exec "$@"

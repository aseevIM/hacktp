#!/bin/bash

echo "=== Обработка корпоративной почты ==="

[ ! -d "data/inbox" ] && echo "ОШИБКА: data/inbox не найдена" && exit 1
[ ! -f "data/rules/rules.json" ] && echo "ОШИБКА: rules.json не найден" && exit 1

python3 main.py

if [ $? -eq 0 ]; then
    echo "Все работает"
else
    echo "Ничего не работает"
    exit 1
fi
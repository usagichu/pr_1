@echo off

echo Тест 1: Запуск без параметров
python pr_1.py
pause

echo Тест 2: Только --vfs
python pr_1.py --vfs D:\pr_1\myvfs
pause

echo Тест 3: Только --script
python pr_1.py --commands.txt
pause

echo Тест 4: Оба параметра
python pr_1.py --vfs D:\pr_1\myvfs --script commands.txt
pause

echo Тест 5: Несуществующий скрипт
python pr_1.py --script nonexistent.txt
pause

echo Все тесты завершены.
pause
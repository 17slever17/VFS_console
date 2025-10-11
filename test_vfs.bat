@echo off

:: Тест 1: только корень VFS
python main.py --vfs-root C:\Temp\VFS

:: Тест 2: только стартовый скрипт
python main.py --start-script scripts/script.txt

:: Тест 3: оба параметра
python main.py --vfs-root C:\Temp\VFS --start-script scripts/script.txt

:: Тест 4: без параметров
python main.py

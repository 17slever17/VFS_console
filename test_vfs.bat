@echo off

:: Тест 1: минимальный
py main.py --vfs-root temp/vfs_min.xml --start-script scripts/script.txt

:: Тест 2: несколько файлов
py main.py --vfs-root temp/vfs_files.xml --start-script scripts/script.txt

:: Тест 3: 3 уровня файлов и папок
py main.py --vfs-root temp/vfs_deep.xml --start-script scripts/script.txt

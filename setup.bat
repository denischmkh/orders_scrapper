@echo off

REM Создание виртуального окружения
python -m venv venv

REM Активирование виртуального окружения
call venv\Scripts\activate

REM Установка зависимостей
pip install -r requirements.txt

echo Виртуальное окружение создано и зависимости установлены.
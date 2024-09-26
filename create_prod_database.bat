:: Установка кодовой страницы для поддержки русского языка
:: Для UTF-8 нужно `chcp 65001`, для Windows-1251 нужно `chcp 1251`
chcp 65001

:: Запрашиваем ввод пароля
set /p PGPASSWORD=Введите пароль для пользователя postgres: 

:: Установка PGUSER
set PGUSER=postgres

:: Создаем пользователя
psql -U %PGUSER% -c "CREATE USER testuser1 WITH PASSWORD '123456';"

:: Создаем базу данных
psql -U %PGUSER% -c "CREATE DATABASE sales_bot;"

:: Подключаемся к базе данных и выдаем привилегии
psql -U %PGUSER% -d sales_bot -c "GRANT ALL PRIVILEGES ON SCHEMA public TO testuser1;"

:: Очистка переменных
set PGPASSWORD=
set PGUSER=

:: pause для просмотра выполненных команд
pause
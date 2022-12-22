# Проект на фрейворке Django
## Ссылка на скачивания

- [Проект](https://github.com/Rycroft-Philostrate/project-todolist.git)

## Ссылки на документацию инструментов

- [Документация по языку Python3](https://docs.python.org/3/)
- [Документация по Django](https://docs.djangoproject.com/)

## Краткое описание инструментов

**Python** - высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Синтаксис ядра Python минималистичен. В то же время стандартная библиотека включает большой объём полезных функций.

**Django** - это высокоуровневый Python веб-фреймворк, который позволяет быстро создавать безопасные и поддерживаемые веб-сайты. Созданный опытными разработчиками, Django берёт на себя большую часть хлопот веб-разработки, поэтому вы можете сосредоточиться на написании своего веб-приложения без необходимости изобретать велосипед. Он бесплатный и с открытым исходным кодом, имеет растущее и активное сообщество, отличную документацию и множество вариантов как бесплатной, так и платной поддержки.

## Настройка и запуск приложения

1. Скачать и установить python3 версии 3.8 и выше.
2. Скачать проект и положить в любую папку.
3. Создать файл `.env` в папке приложения и указать данные environment:
   ```
   POSTGRES_USER=<login>
   POSTGRES_PASSWORD=<password>
   POSTGRES_DB=<имя БД>
   POSTGRES_PORT=<порт БД>
   POSTGRES_HOST=<адрес БД>
   ```
4. Установить зависимости, выполнив команду находясь в папку с приложением:
    ```
   pip install -r requirements.txt
   ```
5. Установить миграции, находясь в папке с приложением:
    ```
   ./manage.py makemigrations
   ./manage.py migrate
   ```
6. Запустить приложение, находясь в папке с приложением:
    ```
   ./manage.py runserver
   ```
7. Адрес и порт приложения по умолчанию: `http://127.0.0.1:8000`
8. В проекте имеются Docker файлы и action.yml для непрерывной интеграции и развертывании с помощью GitHub Actions.

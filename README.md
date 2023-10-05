# YaMDb - агрегатор оценок и отзывов пользователей

## Описание
YaMDb - сервис, который расскажет вам о любом произведнии, будь то книга, фильм или песня. Здесь можно узнать что думают об объкте искусства другие люди. Для удобства мы разделили произведения на три категории: <b>Книги, Фильмы и Музыка</b>.
В свою очередь каждая категория подразделяется на жанры.<br>
Также после регистрации на сервисе вы можно делиться своим мнением с остальным миром, оставляя оценки и отзывы. <br>
<b>Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку</b>


## Используемые технологии:

* Python
* Django
* Django REST Framework
* SQLite


## Как запустить проект
1. Склонируйте репозиторий:  
``` git clone git@github.com:VitaliiCheremisov/api_yamdb.git```    
2. Установите и активируйте виртуальное окружение:  
``` python -m venv env ```  
``` source env/Scripts/activate ``` 
3. Установите зависимости из файла requirements.txt:   
``` pip install -r requirements.txt ```
4. Перейдите в папку api_yamdb/api_yamdb.
5. Примените миграции:   
``` python manage.py migrate ```
6. Загрузите тестовые данные:  
``` python manage.py load_csv_data ```
7. Выполните команду:   
``` python manage.py runserver ```


### Документация

http://127.0.0.1:8000/redoc/


## Примеры запросов к API
- Регистрация пользователя:  
``` POST /api/v1/auth/signup/ ```  
- Получение данных своей учетной записи:  
``` GET /api/v1/users/me/ ```  
- Добавление новой категории:  
``` POST /api/v1/categories/ ```
- Удаление жанра:  
``` DELETE /api/v1/genres/{slug} ```
- Частичное обновление информации о произведении:  
``` PATCH /api/v1/titles/{titles_id} ```
- Получение списка всех отзывов:  
``` GET /api/v1/titles/{title_id}/reviews/ ```
- Добавление комментария к отзыву:  
``` POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/ ```

### Авторы проекта:

- [Виталий Черемисов](https://github.com/VitaliiCheremisov)
- [Денис Зубков](https://github.com/tokugavaieasu)
- [Александра Стеченко](https://github.com/AleksandraStechenko)

# Проект YaMDb

![example workflow]()

## Описание

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Применяемые технологии
[![Python](https://img.shields.io/badge/Python-3.7-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-2.2.16-blue?style=flat-square&logo=Django&logoColor=092E20&labelColor=d0d0d0)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.12.4-blue?style=flat-square&logo=Django&logoColor=a30000&labelColor=d0d0d0)](https://www.django-rest-framework.org/)
[![Simple JWT](https://img.shields.io/badge/Simple%20JWT%20-4.7.2-blue?style=flat-square&logo=github&logoColor=4285F4&labelColor=d0d0d0)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Установка сервиса

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AMinnigaliev/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```



## Доступ к YaMDb API

[http://localhost/api/v1/](http://localhost/api/v1/)

## Документация к YaMDb API

[http://localhost/redoc/](http://localhost/redoc/)

## Административная панель

[http://localhost/admin/](http://localhost/admin/)


## Примеры запросов к API

### Регистрация нового пользователя:
###### Доступно без токена

**POST**-запрос:

```http
http://localhost/api/v1/authhttps://github.com/signup/
```

Тело запроса:

```json
{
  "email": "new_user@test.ru",
  "username": "new_user"
}
```

Ответ:

```json
{
  "email": "new_user@test.ru",
  "username": "new_user"
}
```

Сообщение с токеном на email:
```
From: noreply@apiyamdb.ru
To: new_user@test.ru

Ваш проверочный код rH6HTs.
```

---

### Получение списка всех жанров:
###### Доступно без токена

**GET**-запрос:

```http
http://localhost/api/v1/genres/
```

Ответ:

```json
{
    "count": 15,
    "next": "http://localhost/api/v1/genres/?page=2",
    "previous": null,
    "results": [
        {
            "name": "Rock-n-roll",
            "slug": "rock-n-roll"
        },
        {
            "name": "Баллада",
            "slug": "ballad"
        },
        {
            "name": "Вестерн",
            "slug": "western"
        },
        {
            "name": "Гонзо",
            "slug": "gonzo"
        },
        {
            "name": "Детектив",
            "slug": "detective"
        },
        {
            "name": "Драма",
            "slug": "drama"
        },
        {
            "name": "Классика",
            "slug": "classical"
        },
        {
            "name": "Комедия",
            "slug": "comedy"
        },
        {
            "name": "Рок",
            "slug": "rock"
        },
        {
            "name": "Роман",
            "slug": "roman"
        }
    ]
}
```

## Авторы
1. Артём Миннигалиев (https://github.com/AMinnigaliev)
2. Алексей Иванов (https://github.com/ivanov-alexey-serg)
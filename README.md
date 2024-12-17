# Блогикум
*Социальная сеть для публикации постов позволяет делиться историями из жизни в подходящих категориях c указанием
локации, где это случилось, а также получать обратную связь в виде комментариев под своими постами и заводить новые знакомства!*

![](https://img.shields.io/badge/Python-3.9-lightblue)
![](https://img.shields.io/badge/Django-3.2-darkgreen)
![](https://img.shields.io/badge/django--bootstrap5-22.2-yellow)

<details>
  <summary>Как запустить проект локально</summary>

1. Клонировать репозиторий:

```
git clone git@github.com:ClosedEyeVisuals/blogicum.git
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

3. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python manage.py migrate
```

5. Заполнить базу данных тестовыми данными:

```
python manage.py loaddata db.json
```

6. Запустить проект:

```
python manage.py runserver
```
Проект доступен по адресу https://127.0.0.1:8000.

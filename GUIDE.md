# Магазин одежды на Django: полный гайд

Проект: сайт магазина одежды с каталогом, новинками и страницей товара.
Стек: Python, Django, SQLite, Pillow (картинки), python-dotenv (секреты), Git + GitHub.


> **Название приложения.** Приложение Django называется `magazin_odezhda` (в имени Python-модуля нельзя использовать пробелы, поэтому подчёркивание). Если у вас осталась старая база `db.sqlite3` от версии с названием `nymagaz`, удалите её и выполните `python manage.py migrate` заново: имя приложения входит в названия таблиц.

---

## 0. Что требует задание и где это реализовано

| Требование задания | Где реализовано |
|---|---|
| Каталог (карточки товаров) | `magazin_odezhda/views.py` → `product_list`, шаблон `product_list.html`, адрес `/` |
| Каталог недавних товаров (менее недели назад) | `views.py` → `new_products`, адрес `/new/` |
| Страница с описанием товара | `views.py` → `product_detail`, шаблон `product_detail.html`, адрес `/product/<id>/` |
| Оформление и дизайн | `magazin_odezhda/templates/base.html` (CSS внутри) |
| Производитель в отдельной таблице | модель `Manufacturer` + `ForeignKey` в `Product` (`models.py`) |
| Учёт наличия/отсутствия товара | поле `Product.in_stock` (галочка), вывод в шаблонах |
| Добавление товаров через админку | `magazin_odezhda/admin.py`, адрес `/admin/` |
| Сохранено в git-репозитории | разделы 3 и 4 этого гайда |

---

## 1. Структура проекта

```
magazin-odezhda/
├── manage.py                  # управляющий скрипт Django
├── requirements.txt           # список библиотек (pip freeze)
├── .env                       # секреты (создаёте сами, в git НЕ попадает)
├── .env.example               # образец для .env
├── .gitignore                 # что git игнорирует
├── GUIDE.md                   # этот файл
├── config/                    # настройки проекта
│   ├── settings.py            # настройки (SECRET_KEY берётся из .env)
│   ├── urls.py                # главные адреса (admin + магазин + media)
│   ├── wsgi.py / asgi.py
└── magazin_odezhda/                   # приложение магазина
    ├── models.py              # таблицы: Manufacturer, Product
    ├── admin.py               # настройка админки
    ├── views.py               # логика страниц
    ├── urls.py                # адреса приложения
    ├── migrations/            # история изменений базы
    └── templates/             # HTML-шаблоны
        ├── base.html          # общий каркас: шапка, стили
        ├── product_list.html  # карточки товаров
        └── product_detail.html# страница товара
```

После запуска появятся (в git не попадают): `.venv/`, `db.sqlite3`, `media/`.

---

## 2. Запуск проекта с нуля

Откройте терминал в папке, где лежит `manage.py`.

### 2.1. Виртуальное окружение и библиотеки

```bash
python -m venv .venv
source .venv/Scripts/activate       # Git Bash (как в шпаргалке)
# PowerShell:  .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
```

Если окружение создаётся с нуля без `requirements.txt`:

```bash
pip install django
pip install python-dotenv
pip install pillow
pip freeze > requirements.txt
```

### 2.2. Файл `.env`

Скопируйте `.env.example` в `.env` и впишите свой ключ:

```env
SECRET_KEY="ваш-надёжный-безопасный-ключ"
DEBUG=True
```

Сгенерировать ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

Если ключ содержит спецсимволы, оставляйте его в кавычках.
Осторожно: имя переменной именно `SECRET_KEY` (в шпаргалке в разделе «Восстановить проект» опечатка `SECERT_KEY`, из-за неё проект не запустится).

### 2.3. База данных, админ, запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Адреса:

- http://127.0.0.1:8000/ — каталог
- http://127.0.0.1:8000/new/ — новинки
- http://127.0.0.1:8000/product/1/ — страница товара
- http://127.0.0.1:8000/admin/ — админка

### 2.4. Наполнение через админку

1. Войдите в `/admin/` под суперпользователем.
2. Раздел **Производители** → добавьте производителя (например, «Samsung»).
3. Раздел **Товары** → **Добавить**: название, описание, цена, картинка (необязательно), производитель, галочка «В наличии».
4. Дата добавления проставляется автоматически, поэтому товар сразу попадёт в «Новинки».
5. Снимите галочку «В наличии», и на сайте появится надпись «Нет в наличии».

Чтобы проверить фильтр «менее недели»: отредактировать дату добавления в админке нельзя (поле `auto_now_add`). Проверка через shell:

```bash
python manage.py shell
```
```py
from datetime import timedelta
from django.utils import timezone
from magazin_odezhda.models import Product
p = Product.objects.first()
Product.objects.filter(pk=p.pk).update(created_at=timezone.now() - timedelta(days=10))
```

После этого товар исчезнет из `/new/`, но останется в каталоге.

---

## 3. Работа с Git (по шпаргалке)

### 3.1. Создание проекта

```bash
git init
```

### 3.2. Коммит

```bash
git add .
git commit -m "Текст коммита"
```

Перед первым `git add .` убедитесь, что `.gitignore` на месте, иначе `.venv`, `.env` и база уйдут в репозиторий.

Первый раз Git может попросить представиться:

```bash
git config user.name "Ваше Имя"
git config user.email "почта@пример.com"
```

### 3.3. Откатиться назад

```bash
git log --oneline                   # список коммитов с номерами
git checkout номер_коммита          # посмотреть старое состояние
git checkout main                   # вернуться обратно
```

### 3.4. Создать ветку и переключиться

```bash
git branch название
git checkout название
# одной командой: git checkout -b название
```

### 3.5. Слить ветки

```bash
git checkout main                              # куда вливаем
git merge название -m "текст коммита"          # что вливаем
```

### 3.6. Запушить

```bash
git push                      # текущая ветка (после первой привязки)
git push origin название      # отдельная ветка
```

Основной порядок работы над заданием: ветка → правки → коммит → слияние в `main` → push.

---

## 4. Привязка к вашему GitHub

### 4.1. Создайте репозиторий

1. github.com → **+** → **New repository**.
2. Имя, например `shop`.
3. **Не** отмечайте Add README, .gitignore, license (репозиторий должен быть пустым).
4. **Create repository**, скопируйте адрес `https://github.com/ВАШ_ЛОГИН/shop.git`.

### 4.2. Привяжите и отправьте

```bash
git init
git add .
git commit -m "Создание проекта"
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/shop.git
git push -u origin main
```

Проверка привязки: `git remote -v`.
Сменить адрес: `git remote set-url origin НОВЫЙ_АДРЕС`.

### 4.3. Авторизация

При `git push` вместо пароля нужен **Personal Access Token**:
GitHub → Settings → Developer settings → Personal access tokens → Generate new token (право `repo`).
Либо подтвердите вход в окне браузера, если оно откроется.

В архиве нет папки `.git`, поэтому история ваша с нуля и никаких чужих привязок нет.

---

## 5. Восстановление проекта на другом компьютере

```bash
git clone https://github.com/ВАШ_ЛОГИН/shop.git
cd shop
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Затем создайте `.env`:

```env
SECRET_KEY="......"
```

и выполните `python manage.py migrate`, `python manage.py createsuperuser`, `python manage.py runserver`.
Базы и картинок в git нет, поэтому товары придётся добавить заново.

---

## 6. Как устроен код

### 6.1. Модели (`magazin_odezhda/models.py`)

```
Manufacturer                 Product
-------------                ---------------------------
id                           id
name                         title        название
                             description  описание
                             price        цена (Decimal)
                             image        картинка (необязательно)
                             manufacturer → Manufacturer (ForeignKey)
                             in_stock     в наличии (True/False)
                             created_at   дата добавления (авто)
```

- Один производитель, много товаров (связь «один ко многим»).
- `auto_now_add=True` ставит дату один раз при создании.
- Метод `is_new()` возвращает `True`, если товару меньше 7 дней.

### 6.2. Представления (`magazin_odezhda/views.py`)

- `product_list` берёт все товары, сортирует от новых к старым (`order_by('-created_at')`).
- `new_products` фильтрует `created_at__gte = сейчас − 7 дней`.
- `product_detail` ищет товар по `pk`; если нет, показывает 404 (`get_object_or_404`).

### 6.3. Адреса

`config/urls.py` подключает админку, адреса магазина (`include('magazin_odezhda.urls')`) и раздачу картинок из `media/` (только при `DEBUG=True`).
`magazin_odezhda/urls.py` содержит три маршрута: `''`, `'new/'`, `'product/<int:pk>/'`.

### 6.4. Шаблоны

`base.html` задаёт шапку с меню и стили. `product_list.html` и `product_detail.html` наследуют его через `{% extends 'base.html' %}` и заполняют блок `content`.

### 6.5. Картинки

Загружаются в `media/products/`. Нужны `MEDIA_URL`/`MEDIA_ROOT` в `settings.py`, библиотека Pillow и маршрут для `media` в `config/urls.py`. Все три уже настроены.

### 6.6. Секреты

`settings.py` читает `.env` через `load_dotenv` и берёт `SECRET_KEY` из `os.environ`. Файл `.env` перечислен в `.gitignore`, поэтому на GitHub ключ не попадает.

---

## 7. Типичные ошибки

| Ошибка | Причина и решение |
|---|---|
| `KeyError: 'SECRET_KEY'` | нет файла `.env` или в нём опечатка в имени. Создайте `.env` рядом с `manage.py` |
| `ModuleNotFoundError: dotenv` / `django` | не активировано окружение или не выполнено `pip install -r requirements.txt` |
| `Cannot use ImageField because Pillow is not installed` | `pip install pillow` |
| Картинки не отображаются | `DEBUG=False` или нет маршрута `media`; проверьте `.env` и `config/urls.py` |
| `no such table` | не выполнен `python manage.py migrate` |
| `git push` просит пароль и отказывает | введите Personal Access Token, а не пароль |
| `remote origin already exists` | `git remote set-url origin АДРЕС` |
| `src refspec main does not match any` | не было коммита или ветка называется иначе: `git branch -M main` |
| На сайте нет новинок | товары добавлены больше недели назад или их нет совсем |
| `.env` или `db.sqlite3` оказались в git | `git rm --cached .env db.sqlite3`, проверьте `.gitignore`, сделайте коммит |

Если вы случайно закоммитили настоящий `SECRET_KEY`, удаления файла недостаточно, ключ остаётся в истории. Сгенерируйте новый.

---

## 8. Вопросы для защиты

- **Зачем `.env`?** Секретный ключ нельзя хранить в публичном репозитории.
- **Зачем `requirements.txt`?** Чтобы любой мог установить те же версии библиотек (`pip install -r`).
- **Почему производитель в отдельной таблице?** Не дублируются данные; название меняется в одном месте; можно показать все товары производителя.
- **Что делает `makemigrations` и `migrate`?** Первая создаёт файл изменений структуры, вторая применяет его к базе.
- **Как сделан фильтр новинок?** `created_at__gte` и разница `timezone.now() - timedelta(days=7)`.
- **Чем `git checkout` ветки отличается от `git merge`?** `checkout` переключает, `merge` вливает изменения другой ветки в текущую.
- **Почему `db.sqlite3` и `.venv` в `.gitignore`?** Это локальные и воспроизводимые файлы, а не исходный код.

---

## 9. Шпаргалка команд

```bash
# окружение
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pip freeze > requirements.txt

# Django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Git
git init
git add .
git commit -m "Текст коммита"
git log --oneline
git checkout номер_коммита
git branch название
git checkout название
git checkout main
git merge название -m "текст коммита"
git remote add origin АДРЕС
git push -u origin main
git push
git push origin название
```

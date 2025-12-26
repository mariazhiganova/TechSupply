# TechSupply - Система управления сетью по продаже электроники

Система для управления иерархической сетью поставщиков электроники с API-интерфейсом и админ-панелью

## Возможности

- Управление иерархической структурой поставщиков
- Отслеживание задолженностей перед поставщиками
- Фильтрация поставщиков по городу и стране
- Автоматический расчет уровня иерархии

## Технологии

- **Backend**: Django 6.0 + Django REST Framework
- **Database**: PostgreSQL
- **Auth**: JWT-аутентификация
- **API Docs**: Swagger

# Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/mariazhiganova/TechSupply.git
```

### Настройка окружения

Создайте файл .env на основе .env.example

### Установка зависимостей

```
poetry install
poetry shell
```

## Ручной запуск (без Docker)

### 1. Установите зависимости

```
poetry install
poetry shell
```

### 2. Запустите сервер

```
python manage.py migrate
python manage.py runserver
```

## Документация

Вы можете увидеть документацию API, перейдя по URL-адресу

Для Swagger:

```
http://localhost:8000/swagger/
```

## Автор

**Мария Жиганова** - Backend Developer (Python)

```
GitHub - https://github.com/mariazhiganova
```
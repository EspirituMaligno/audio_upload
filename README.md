# AudioUpload

Веб-приложение для загрузки и управления аудиофайлами, построенное на FastAPI и PostgreSQL.

## 🚀 Технологии

- FastAPI
- PostgreSQL
- Docker & Docker Compose
- Python 3.11+

## 📋 Требования

- Docker
- Docker Compose
- `.env` файл с необходимыми переменными окружения

## 🛠 Установка и запуск

1. **Клонирование репозитория**

   ```bash
   git clone https://github.com/EspirituMaligno/audio_upload.git
   cd audio_upload
   ```

2. **Настройка окружения**
   - Скопируйте `.env.example` в `.env`
   - Заполните необходимые переменные окружения

3. **Запуск приложения**

   ```bash
   cd .deployment
   docker-compose up --build
   ```

## 🌐 Доступ к приложению

- API: <http://0.0.0.0:5000>
- База данных: localhost:5433

## 🛑 Остановка приложения

```bash
docker-compose down
```

## 📝 Примечания

- База данных доступна по порту 5432
- API документация доступна по адресу http://localhost:8000/docs

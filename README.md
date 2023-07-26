# DevDynamos

### Проет, созданный для хакатона, используя FastAPI 
### FastAPI - это быстрый и современный фреймворк для создания веб-приложений на языке Python.
___
### Использовальнные библиотеки.


![Flutter](https://img.shields.io/badge/-fastapi-yellow?style=for-the-badge&logo=python) 

![Flutter](https://img.shields.io/badge/-asyncpg-yellow?style=for-the-badge&logo=python)

![Flutter](https://img.shields.io/badge/-SqlAlchemy-yellow?style=for-the-badge&logo=python)

![Flutter](https://img.shields.io/badge/-alembic-yellow?style=for-the-badge&logo=python)

![Flutter](https://img.shields.io/badge/-celery-yellow?style=for-the-badge&logo=python)

![Flutter](https://img.shields.io/badge/-passlib-yellow?style=for-the-badge&logo=python)

![Flutter](https://img.shields.io/badge/-pyjwt-yellow?style=for-the-badge&logo=python)

![Flutter](https://img.shields.io/badge/-sqladmin-yellow?style=for-the-badge&logo=python)
___
#### Для хранения данных использовалось Postgres, в качестве драйвера *asyncpg*. 
#### Для хэширования пароля использовалось *Passlib* с аутентификацией *PyJWT*.
#### Для миграции использовалось *alembic*. 
#### В качестве админки использовалось *sqladmin*.
___

### Чтобы запустить проект необходимо:

- Склонировать репозиторий.
  ```
  git clone https://github.com/sora-yuka/Div-Market.git
  ```

- Создать .env файл по примеру .env.template с ниже указынными данными.

  ```DATABASE_URL=user:password@localhost:5432/db_name```
  
  ```SECRET_KEY=secret_key```

  ```EMAIL_PASSWORD=email_password```

  ```EMAIL_HOST=your_email@gmail.com```
  
  ```ADMIN_USERNAME=your_admin```
  
  ```ADMIN_PASSWORD=your_admin_password```

  ```CELERY_BROKER_URL=...```

- Запустить docker.

  ```
  docker compose up -d --build
  ```

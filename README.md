# Ethan.AI Assignment

## Setup

build and up containers

```
docker-compose up -d --build
```

run migrations

```
docker-compose run web python3 manage.py migrate
```

create a user for admin

```
docker-compose run web python manage.py createsuperuser
```


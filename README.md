# python_django_example

This is example of the python django project. 
This code is a partial flow copy of the internal knowledge management system. In this example you can create, read, update or delete employee profile.


## Getting started

To start the project just run:
```
docker-compose up --build
```

To apply migrations:
```
docker-compose up
docker exec -it emanager_backend python manage.py makemigrations employee
docker exec -it emanager_backend python manage.py migrate
```

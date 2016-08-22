# moopy 
Simple application using Django and Semantic-UI

version : 1.0

- create database name 'moopy'
- virtualenv venv
- source /venv/bin/activate
- pip install Django==1.10
- pip install mysqlclient

- settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moopy',
        'USER': 'root',
        'PASSWORD': '12345678',
    }
}
```
- cd moopy
- python3 manage.py runserver

url home : http://localhost:8000/movies/


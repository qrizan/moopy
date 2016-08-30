# moopy 
Simple application using Django and Semantic-UI

version : 1.0

- create database name (ex:'moopy')
- virtualenv venv
- source /venv/bin/activate
- pip install -r requirements.txt

- settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moopy',
        'USER': 'root',
        'PASSWORD': '',
    }
}
```
- run migrations and create super user
- run server

url home : http://localhost:8000/movies/

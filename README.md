# Development

## How to Setup
Better using virtualenv:

```
$ mkvirtualenv calcio_spash
$ pip install -r requirements.txt
```

## How to Run
Currently we're using sqlite, no fancy-stuff 😊; First, apply migrations, then run the dev server:

```
$ python manage.py migrate
$ python manage.py runserver
```

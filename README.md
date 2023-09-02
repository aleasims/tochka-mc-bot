# tochka-mc-bot

Tochka masterclass bot

## Requirements

```bash
pip install -r requirements.txt
```

## Production run

```bash
export PYTHONPATH=.
export DJANGO_SETTINGS_MODULE=botback.settings.prod
python manage.py migrate
```

## Dev run (for dummies)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
export DJANGO_SETTINGS_MODULE=botback.settings.dev
export TG_TOKEN=YOUR_SECRET_TG_TOKEN
python3 bot/fill_courses.py
python3 bot/main.py 
```

## Run web app (locally)

```bash
python manage.py createsuperuser
python manage.py runserver
```

app: http://127.0.0.1:8000/admin


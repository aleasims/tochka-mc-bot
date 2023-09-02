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
python3 bot/main.py 
```
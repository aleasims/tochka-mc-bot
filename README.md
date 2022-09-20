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

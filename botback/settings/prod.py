import json

from .dev import *

DEBUG = False

with open("config.json") as f:
    config = json.load(f)

SECRET_KEY = config["DJANO_SECRET_KEY"]

ALLOWED_HOSTS.extend(config["ALLOWED_HOSTS"])
ALLOWED_HOSTS.append("localhost")

DATABASES = config["DATABASES"]

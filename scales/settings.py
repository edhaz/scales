from os import environ, path

BASE_PATH = path.dirname(path.abspath(__file__))
DATA_DIR = path.abspath(path.join(BASE_PATH, "data"))
DATABASE_PATH = path.join(DATA_DIR, "scales.db")

SECRET_KEY = environ.get("APP_SECRET_KEY", "not set")

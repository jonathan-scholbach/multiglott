import json
import os


with open("config.json") as config_file:
    config = json.load(config_file)

config.update(
    {
        "POSTGRES_USER": os.environ["POSTGRES_USER"],
        "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "POSTGRES_DB": os.environ["POSTGRES_DB"],
        "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
        "POSTGRES_HOST": os.environ["POSTGRES_HOST"],
        "API_SECRET_KEY": os.environ["API_SECRET_KEY"],
        "API_SECURITY_PASSWORD_SALT": os.environ["API_SECURITY_PASSWORD_SALT"],
        "API_DOMAIN": os.environ["API_DOMAIN"],
        "API_PORT": os.environ["API_PORT"],
        "API_URL": f"{os.environ['API_DOMAIN']}:{os.environ['API_PORT']}",
        "APP_NAME": os.environ["APP_NAME"],
        "SMTP_PASSWORD": os.environ["SMTP_PASSWORD"],
        "FRONTEND_DOMAIN": os.environ["FRONTEND_DOMAIN"],
        "FRONTEND_PORT": os.environ["FRONTEND_PORT"],
        "FRONTEND_URL": f"{os.environ['FRONTEND_DOMAIN']}:{os.environ['FRONTEND_PORT']}/#",
        "FRONTEND_CONFIRMED_PATH": os.environ["FRONTEND_CONFIRMED_PATH"]
    }
)

if os.environ["DATABASE_URL"]:
    config["DATABASE_URL"] = os.environ["DATABASE_URL"]

if os.environ["PORT"]:
    config["API_PORT"] = os.environ["PORT"]
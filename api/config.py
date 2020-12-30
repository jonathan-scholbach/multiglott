import os


config = {
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
    "API_VERSION": "v1",
    "SMTP_PASSWORD": os.environ["SMTP_PASSWORD"],
}

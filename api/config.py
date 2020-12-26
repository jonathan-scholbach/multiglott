import os


config = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_DB": os.environ["POSTGRES_DB"],
    "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
    "POSTGRES_HOST": os.environ["POSTGRES_HOST"],
    "SECRET_KEY": os.environ["SECRET_KEY"],
    "SECURITY_PASSWORD_SALT": os.environ["SECURITY_PASSWORD_SALT"],
}

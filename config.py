import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")  # chave default para local
    ADMIN_CPF = os.getenv("ADMIN_CPF", "")
    
    uri = os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri

    SQLALCHEMY_TRACK_MODIFICATIONS = False

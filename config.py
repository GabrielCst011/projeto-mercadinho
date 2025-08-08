import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

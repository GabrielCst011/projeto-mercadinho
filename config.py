import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:Gjwe4wYI6jHiYTL0vggfTMPHCqadGAV0@dpg-d2ajvvndiees73ds8gr0-a.oregon-postgres.render.com/db_mercadinho")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

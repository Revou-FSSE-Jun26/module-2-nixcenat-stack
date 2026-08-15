import os
from dotenv import load_dotenv

# Memuat environment variables dari file .env
load_dotenv()

class Config:
    # Mengambil string koneksi database dari file .env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    # Mematikan fitur signaling event SQLAlchemy untuk menghemat memori
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Key rahasia untuk Flask (digunakan untuk sesi/cookies)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    

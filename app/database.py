from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inisialisasi objek SQLAlchemy dan Migrate tanpa aplikasi Flask terikat dulu
db = SQLAlchemy()
migrate = Migrate()

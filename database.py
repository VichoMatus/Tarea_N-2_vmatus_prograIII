from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./vuelos.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

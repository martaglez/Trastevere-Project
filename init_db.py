from database.database import engine, Base
# IMPORTANTE: Importa aquí tus modelos para que SQLAlchemy los "vea"
from database.schema.models import User, Publication 

print("Conectando a la base de datos de Docker...")
try:
    # Este comando crea las tablas si no existen
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas con éxito en Postgres")
except Exception as e:
    print(f"Error al crear las tablas: {e}")
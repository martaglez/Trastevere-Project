from database.database import SessionLocal
from database.schema.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # Comprobamos si ya existes para no duplicar
        exists = db.query(User).filter(User.username == "admin").first()
        if exists:
            print("⚠️ El usuario 'admin' ya existe en la base de datos.")
            return

        # Creamos el objeto usuario
        new_user = User(
            username="admin",
            email="admin@trastevere.com",
            # Encriptamos la contraseña "1234"
            password_hash=generate_password_hash("1234"),
            is_premium=True
        )

        db.add(new_user)
        db.commit()
        print("✅ ¡Usuario 'admin' creado con éxito! Contraseña: 1234")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
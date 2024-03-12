from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settingsLog

# Configuración de la base de datos
DATABASE_URL = settingsLog.DATABASE_URL
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Definición de la clase Log para representar la tabla en la base de datos
class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String, index=True)

# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(bind=engine)

# Función para agregar un mensaje a la base de datos
def agregar_mensaje(mensaje):
    # Crear una instancia de la clase Log
    nuevo_log = Log(mensaje=mensaje)

    # Crear una sesión de la base de datos
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()

    try:
        # Agregar la nueva entrada a la sesión y confirmar la transacción
        db.add(nuevo_log)
        db.commit()
        db.refresh(nuevo_log)
    except Exception as e:
        # En caso de error, deshacer la transacción
        db.rollback()
        raise e
    finally:
        # Cerrar la sesión
        db.close()
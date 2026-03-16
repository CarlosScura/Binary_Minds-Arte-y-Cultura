IMPORTAR Flask
IMPORTAR la base de datos (db)
IMPORTAR todos los blueprints:
  - auth_routes
  - eventos_routes
  - usuarios_routes

# ================================
# CREAR Y CONFIGURAR LA APP
# ================================
CREAR aplicación Flask

CONFIGURAR:
  - SECRET_KEY        → texto secreto para las sesiones
  - DATABASE URI      → ruta al archivo SQLite local
  - SQLALCHEMY_TRACK_MODIFICATIONS → False

INICIALIZAR db con la app

# ================================
# REGISTRAR BLUEPRINTS
# ================================
REGISTRAR blueprint auth con prefijo "/"
REGISTRAR blueprint eventos con prefijo "/eventos"
REGISTRAR blueprint usuarios con prefijo "/usuarios"

# ================================
# CREAR TABLAS Y ARRANCAR
# ================================
AL INICIAR LA APP:
  CREAR todas las tablas si no existen

  LLAMAR a actualizar_estados_eventos()
  → esto actualiza eventos viejos cada vez que la app arranca

CORRER la aplicación en modo debug

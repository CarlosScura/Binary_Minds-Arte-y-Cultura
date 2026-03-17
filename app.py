# IMPORTAR Flask

from flask import Flask

# importar bcrypt

from models import db, bcrypt

# IMPORTAR la base de datos (db)

from models import db

# IMPORTAR todos los blueprints:
#   - auth_routes
#   - eventos_routes
#   - usuarios_routes

from auth_routes     import auth_bp
from eventos_routes  import eventos_bp, actualizar_estados_eventos
from usuarios_routes import usuarios_bp

# ================================
# CREAR Y CONFIGURAR LA APP
# ================================
# CREAR aplicación Flask

def create_app():
    app = Flask(__name__)

# CONFIGURAR:
#   - SECRET_KEY        → texto secreto para las sesiones

    app.config['SECRET_KEY']                     = 'clave-secreta-cambiar-en-produccion'

#   - DATABASE URI      → ruta al archivo SQLite local

    app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///cityevents.db'

#   - SQLALCHEMY_TRACK_MODIFICATIONS → False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INICIALIZAR db con la app

    db.init_app(app)
    bcrypt.init_app(app)

# ================================
# REGISTRAR BLUEPRINTS
# ================================
# REGISTRAR blueprint auth con prefijo "/"

    app.register_blueprint(auth_bp,     url_prefix='/')

# REGISTRAR blueprint eventos con prefijo "/eventos"

    app.register_blueprint(eventos_bp,  url_prefix='/eventos')

# REGISTRAR blueprint usuarios con prefijo "/usuarios"

    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')


# ================================
# CREAR TABLAS Y ARRANCAR
# ================================
# AL INICIAR LA APP:

    with app.app_context():

#   CREAR todas las tablas si no existen

        db.create_all()

#   LLAMAR a actualizar_estados_eventos()

        actualizar_estados_eventos()  # esto actualiza eventos viejos cada vez que la app arranca

    return app

app = create_app()

# CORRER la aplicación en modo debug

if __name__ == '__main__':
    app.run(debug=True)

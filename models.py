# IMPORTAR SQLAlchemy
# IMPORTAR datetime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt # <--- AGREGAR ESTO

# INICIALIZAR la base de datos (objeto db)

db = SQLAlchemy()
bcrypt = Bcrypt() # <--- INICIALIZAR BCrypt aquí

# ================================
# MODELO: Usuario
# ================================
# CLASE Usuario (tabla: "usuarios"):
#   - id              → número entero, clave primaria, autoincremental
#   - nombre          → texto, obligatorio
#   - email           → texto, obligatorio, único
#   - contraseña      → texto, obligatorio
#   - puntuacion_promedio → número decimal, default 0
#   - fecha_creacion  → fecha, se pone automáticamente al crear

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id                  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre              = db.Column(db.String(120), nullable=False)
    email               = db.Column(db.String(120), nullable=False, unique=True)
    contraseña          = db.Column(db.String(256), nullable=False)
    puntuacion_promedio = db.Column(db.Float, default=0.0)
    fecha_creacion      = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- AGREGAR ESTOS MÉTODOS O TU AUTH NO FUNCIONARÁ ---
    def set_password(self, password):
        """Hashea la contraseña y la guarda en el campo 'contraseña'"""
        self.contraseña = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Compara la contraseña ingresada con el hash guardado"""
        return bcrypt.check_password_hash(self.contraseña, password)
    # -----------------------------------------------------

    # Eventos que este usuario creó
    eventos_creados = db.relationship('Evento', backref='creador', lazy=True)

    # Calificaciones que RECIBIÓ (como evaluado)
    calificaciones_recibidas = db.relationship(
        'Calificacion',
        foreign_keys='Calificacion.evaluado_id',
        backref='evaluado',
        lazy=True
    )

    # Calificaciones que DIO (como evaluador)
    calificaciones_dadas = db.relationship(
        'Calificacion',
        foreign_keys='Calificacion.evaluador_id',
        backref='evaluador',
        lazy=True
    )

    def recalcular_promedio(self):
        """Recalcula el promedio en base a las calificaciones recibidas"""
        recibidas = self.calificaciones_recibidas
        if not recibidas:
            self.puntuacion_promedio = 0.0
            return
        total = sum(c.puntuacion for c in recibidas)
        self.puntuacion_promedio = round(total / len(recibidas), 2)

    def to_dict(self):
        return {
            'id':                   self.id,
            'nombre':               self.nombre,
            'email':                self.email,
            # ⚠️ nunca expongas la contraseña
            'puntuacion_promedio':  self.puntuacion_promedio,
            'fecha_creacion':       self.fecha_creacion.isoformat()
        }

# ================================
# MODELO: Evento
# ================================
# CLASE Evento (tabla: "eventos"):
#   - id               → número entero, clave primaria
#   - titulo           → texto, obligatorio
#   - descripcion      → texto largo
#   - fecha_evento     → fecha y hora, obligatorio
#   - ubicacion_texto  → texto
#   - embed_mapa       → texto largo (guarda el iframe de Google Maps)
#   - estado           → texto ("proximo" | "pasado" | "cancelado")
#   - fecha_expiracion → fecha (calculada: fecha_evento + 3 meses)
#   - creador_id       → número entero, clave foránea → apunta a Usuario.id

class Evento(db.Model):
    __tablename__ = 'eventos'

    id               = db.Column(db.Integer, primary_key=True)
    titulo           = db.Column(db.String(200), nullable=False)
    descripcion      = db.Column(db.Text)
    fecha_evento     = db.Column(db.DateTime, nullable=False)
    ubicacion_texto  = db.Column(db.String(300))
    embed_mapa       = db.Column(db.Text)   # iframe de Google Maps
    estado           = db.Column(db.String(20), default='proximo')  # proximo | pasado | cancelado
    fecha_expiracion = db.Column(db.DateTime)  # se calcula al crear: fecha_evento + 3 meses
    creador_id       = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Calificaciones asociadas a este evento
    calificaciones = db.relationship('Calificacion', backref='evento', lazy=True)

    def to_dict(self):
        return {
            'id':               self.id,
            'titulo':           self.titulo,
            'descripcion':      self.descripcion,
            'fecha_evento':     self.fecha_evento.isoformat(),
            'ubicacion_texto':  self.ubicacion_texto,
            'embed_mapa':       self.embed_mapa,
            'estado':           self.estado,
            'fecha_expiracion': self.fecha_expiracion.isoformat() if self.fecha_expiracion else None,
            'creador_id':       self.creador_id
        }

# ================================
# MODELO: Calificacion
# ================================
# CLASE Calificacion (tabla: "calificaciones"):
#   - id           → número entero, clave primaria
#   - puntuacion   → número entero (1 al 5), obligatorio
#   - evaluado_id  → número entero, clave foránea → apunta a Usuario.id
#   - evaluador_id → número entero, clave foránea → apunta a Usuario.id
#   - evento_id    → número entero, clave foránea → apunta a Evento.id

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'

    id           = db.Column(db.Integer, primary_key=True)
    puntuacion   = db.Column(db.Integer, nullable=False)  # 1 a 5
    evaluado_id  = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    evento_id    = db.Column(db.Integer, db.ForeignKey('eventos.id'),  nullable=False)

    # Restricción: un evaluador solo puede calificar una vez al mismo evaluado en el mismo evento
    __table_args__ = (
        db.UniqueConstraint('evaluador_id', 'evaluado_id', 'evento_id', name='uq_calificacion'),
    )

    def to_dict(self):
        return {
            'id':           self.id,
            'puntuacion':   self.puntuacion,
            'evaluado_id':  self.evaluado_id,
            'evaluador_id': self.evaluador_id,
            'evento_id':    self.evento_id
        }

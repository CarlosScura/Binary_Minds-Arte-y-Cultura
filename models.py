IMPORTAR SQLAlchemy
IMPORTAR datetime

INICIALIZAR la base de datos (objeto db)

# ================================
# MODELO: Usuario
# ================================
CLASE Usuario (tabla: "usuarios"):
  - id              → número entero, clave primaria, autoincremental
  - nombre          → texto, obligatorio
  - email           → texto, obligatorio, único
  - contraseña      → texto, obligatorio
  - puntuacion_promedio → número decimal, default 0
  - fecha_creacion  → fecha, se pone automáticamente al crear

# ================================
# MODELO: Evento
# ================================
CLASE Evento (tabla: "eventos"):
  - id               → número entero, clave primaria
  - titulo           → texto, obligatorio
  - descripcion      → texto largo
  - fecha_evento     → fecha y hora, obligatorio
  - ubicacion_texto  → texto
  - embed_mapa       → texto largo (guarda el iframe de Google Maps)
  - estado           → texto ("proximo" | "pasado" | "cancelado")
  - fecha_expiracion → fecha (calculada: fecha_evento + 3 meses)
  - creador_id       → número entero, clave foránea → apunta a Usuario.id

# ================================
# MODELO: Calificacion
# ================================
CLASE Calificacion (tabla: "calificaciones"):
  - id           → número entero, clave primaria
  - puntuacion   → número entero (1 al 5), obligatorio
  - evaluado_id  → número entero, clave foránea → apunta a Usuario.id
  - evaluador_id → número entero, clave foránea → apunta a Usuario.id
  - evento_id    → número entero, clave foránea → apunta a Evento.id

IMPORTAR Flask (Blueprint, request, session, redirect)
IMPORTAR modelos (Evento, Usuario)

CREAR blueprint "eventos"

# ================================
# GET /eventos
# ================================
RUTA obtener_eventos():
  RECIBIR filtro de estado desde la URL (opcional)
  
  SI hay filtro:
    BUSCAR eventos donde estado == filtro
  SI NO:
    BUSCAR todos los eventos
  
  DEVOLVER lista de eventos

# ================================
# GET /eventos/<id>
# ================================
RUTA obtener_evento(id):
  BUSCAR evento por id
  SI no existe → devolver error 404
  DEVOLVER detalle del evento (incluye embed_mapa)

# ================================
# POST /eventos/crear
# ================================
RUTA crear_evento():
  SI no hay sesión activa → redirigir a login
  SI rol del usuario NO es "organizador" → error 403

  RECIBIR datos del formulario:
    - titulo, descripcion, fecha_evento
    - ubicacion_texto, embed_mapa

  CALCULAR fecha_expiracion = fecha_evento + 3 meses

  CREAR nuevo Evento con estado "proximo"
  GUARDAR en base de datos
  REDIRIGIR al detalle del evento creado

# ================================
# POST /eventos/<id>/cancelar
# ================================
RUTA cancelar_evento(id):
  SI no hay sesión activa → redirigir a login
  
  BUSCAR evento por id
  SI el organizador_id != usuario en sesión → error 403
  
  CAMBIAR estado a "cancelado"
  GUARDAR cambios
  REDIRIGIR a lista de eventos

# ================================
# TAREA: actualizar estados viejos
# ================================
FUNCIÓN actualizar_estados_eventos():
  BUSCAR eventos donde:
    - estado == "proximo"
    - fecha_evento < fecha y hora actual
  PARA cada uno → cambiar estado a "pasado"

  BUSCAR eventos donde:
    - estado == "pasado"
    - fecha_expiracion < fecha actual
  PARA cada uno → eliminar de la base de datos

  GUARDAR todos los cambios

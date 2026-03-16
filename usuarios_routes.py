IMPORTAR Flask (Blueprint, request, session, redirect)
IMPORTAR modelos (Usuario, Calificacion)

CREAR blueprint "usuarios"

# ================================
# GET /usuarios
# ================================
RUTA obtener_usuarios():
  BUSCAR todos los usuarios
  DEVOLVER lista con nombre y puntuacion_promedio

# ================================
# GET /perfil/<id>
# ================================
RUTA obtener_perfil(id):
  BUSCAR usuario por id
  SI no existe → error 404

  BUSCAR eventos creados por este usuario
  BUSCAR calificaciones recibidas por este usuario
  DEVOLVER perfil completo + eventos + puntuacion_promedio

# ================================
# POST /calificar
# ================================
RUTA calificar():
  SI no hay sesión activa → redirigir a login

  RECIBIR datos del formulario:
    - puntuacion (1 al 5)
    - evaluado_id
    - evento_id

  BUSCAR el evento por evento_id
  SI estado del evento != "pasado" → error (no se puede calificar aún)

  VERIFICAR que el evaluador no haya calificado
  ya a esta persona en este evento → si ya calificó, error

  CREAR nueva Calificacion
  GUARDAR en base de datos

  RECALCULAR puntuacion_promedio del evaluado:
    BUSCAR todas las calificaciones donde evaluado_id == evaluado_id
    CALCULAR promedio de todas las puntuaciones
    ACTUALIZAR puntuacion_promedio del Usuario

  GUARDAR cambios
  REDIRIGIR al perfil del evaluado

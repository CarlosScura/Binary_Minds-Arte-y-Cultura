# ================================
# RESPONSABILIDAD DEL ROL INTEGRACIÓN
# ================================
# Este rol no crea archivos nuevos.
# Su trabajo es verificar que el frontend
# y el backend se comunican correctamente.

# ================================
# CHECKLIST DE CONEXIONES A VERIFICAR
# ================================

CONEXIÓN 1: Registro y Login
  VERIFICAR que registro.html envía a → POST /registro
  VERIFICAR que login.html envía a → POST /login
  VERIFICAR que después del login redirige a inicio.html
  VERIFICAR que el navbar muestra el nombre del usuario logueado

CONEXIÓN 2: Eventos
  VERIFICAR que inicio.html recibe y muestra la lista de eventos
  VERIFICAR que eventos_lista.html filtra correctamente por estado
  VERIFICAR que evento_detalle.html recibe el embed_mapa y lo renderiza
  VERIFICAR que crear_evento.html envía a → POST /eventos/crear
  VERIFICAR que cancelar evento funciona y actualiza el estado visible

CONEXIÓN 3: Perfiles y Calificaciones
  VERIFICAR que perfil_usuario.html muestra la puntuacion_promedio actualizada
  VERIFICAR que calificar.html envía a → POST /calificar
  VERIFICAR que no aparece el botón calificar si el evento no es "pasado"
  VERIFICAR que no aparece el botón calificar si no hay sesión activa

CONEXIÓN 4: Seguridad básica
  VERIFICAR que rutas protegidas redirigen a login si no hay sesión
  VERIFICAR que un usuario no puede cancelar un evento que no creó

# ================================
# DATOS DE PRUEBA
# ================================
CREAR script poblar_db.py:

  CREAR 3 usuarios de prueba con contraseñas conocidas
  CREAR 3 eventos:
    - uno con estado "proximo"
    - uno con estado "pasado"
    - uno con estado "cancelado"
  CREAR 2 calificaciones de prueba

  → Estos datos sirven para que todos puedan
    probar su parte sin depender de los demás

IMPORTAR Flask (Blueprint, request, session, redirect)
IMPORTAR modelos (Usuario)

CREAR blueprint "auth"

# ================================
# GET /registro
# ================================
RUTA mostrar_registro():
  SI hay sesión activa → redirigir a inicio
  DEVOLVER página de registro

# ================================
# POST /registro
# ================================
RUTA registrar():
  RECIBIR datos del formulario:
    - nombre, email, contraseña

  BUSCAR si ya existe un usuario con ese email
  SI existe → devolver error "el email ya está registrado"

  ENCRIPTAR la contraseña
  CREAR nuevo Usuario con los datos
  GUARDAR en base de datos

  REDIRIGIR a login

# ================================
# GET /login
# ================================
RUTA mostrar_login():
  SI hay sesión activa → redirigir a inicio
  DEVOLVER página de login

# ================================
# POST /login
# ================================
RUTA login():
  RECIBIR datos del formulario:
    - email, contraseña

  BUSCAR usuario por email
  SI no existe → error "email o contraseña incorrectos"

  VERIFICAR que la contraseña ingresada coincide con la encriptada
  SI no coincide → error "email o contraseña incorrectos"

  GUARDAR en sesión:
    - session["usuario_id"] = usuario.id
    - session["usuario_nombre"] = usuario.nombre

  REDIRIGIR a inicio

# ================================
# POST /logout
# ================================
RUTA logout():
  LIMPIAR toda la sesión
  REDIRIGIR a inicio

# ================================
# DECORADOR: login_requerido
# ================================
FUNCIÓN login_requerido():
  SI no existe session["usuario_id"]:
    → redirigir a login
  SI existe → dejar pasar, ejecutar la ruta normalmente

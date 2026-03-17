from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Usuario  # Importamos la base de datos y el modelo que hicimos
from functools import wraps

# 1. CREAR blueprint "auth"
auth_bp = Blueprint('auth', __name__)

# ================================
# GET /registro
# ================================
@auth_bp.route('/registro', methods=['GET'])
def mostrar_registro():
    # SI hay sesión activa → redirigir a inicio
    if 'usuario_id' in session:
        return redirect(url_for('inicio')) # Asumiendo que la ruta principal se llama 'inicio'
    
    # DEVOLVER página de registro
    return render_template('registro.html')

# ================================
# POST /registro
# ================================
@auth_bp.route('/registro', methods=['POST'])
def registrar():
    # RECIBIR datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')

    # BUSCAR si ya existe un usuario con ese email
    usuario_existente = Usuario.query.filter_by(email=email).first()
    
    if usuario_existente:
        # SI existe → devolver error (usamos flash para mensajes temporales)
        flash('El email ya está registrado', 'danger')
        return redirect(url_for('auth.mostrar_registro'))

    # CREAR nuevo Usuario y ENCRIPTAR (el método set_password que hicimos antes)
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    nuevo_usuario.set_password(password) # Aquí bcrypt hace su magia

    # GUARDAR en base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    # REDIRIGIR a login
    flash('Cuenta creada con éxito. ¡Ya podés iniciar sesión!', 'success')
    return redirect(url_for('auth.mostrar_login'))

# ================================
# GET /login
# ================================
@auth_bp.route('/login', methods=['GET'])
def mostrar_login():
    # SI hay sesión activa → redirigir a inicio
    if 'usuario_id' in session:
        return redirect(url_for('inicio'))
    
    return render_template('login.html')

# ================================
# POST /login
# ================================
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    usuario = Usuario.query.filter_by(email=email).first()

    # Validación simple: ¿Existe y la clave es correcta?
    if not usuario or not usuario.check_password(password):
        flash('Email o contraseña incorrectos', 'danger')
        return redirect(url_for('auth.mostrar_login'))

    # Guardamos solo lo necesario en sesión
    session["usuario_id"] = usuario.id
    session["usuario_nombre"] = usuario.nombre

    flash(f'¡Hola de nuevo, {usuario.nombre}!', 'success')
    return redirect(url_for('inicio')) # Todos van al mismo lugar

# ================================
# POST /logout
# ================================
@auth_bp.route('/logout')
def logout():
    # LIMPIAR toda la sesión
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('inicio'))

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Iniciá sesión para continuar", "warning")
            return redirect(url_for('auth.mostrar_login'))
        return f(*args, **kwargs)
    return decorada
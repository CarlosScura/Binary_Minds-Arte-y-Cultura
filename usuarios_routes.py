# IMPORTAR Flask (Blueprint, request, session, redirect)
# IMPORTAR modelos (Usuario, Calificacion)

from flask import Blueprint, request, session, redirect, url_for, jsonify
from models import Usuario, Calificacion, Evento
from models import db

# CREAR blueprint "usuarios"

usuarios_bp = Blueprint('usuarios', __name__)


# ================================
# GET /usuarios
# ================================
# RUTA obtener_usuarios():
#   BUSCAR todos los usuarios
#   DEVOLVER lista con nombre y puntuacion_promedio

@usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()

    return jsonify([
        {
            'nombre':             u.nombre,
            'puntuacion_promedio': u.puntuacion_promedio
        }
        for u in usuarios
    ]), 200

# ================================
# GET /perfil/<id>
# ================================
# RUTA obtener_perfil(id):
#   BUSCAR usuario por id
#   SI no existe → error 404

#   BUSCAR eventos creados por este usuario
#   BUSCAR calificaciones recibidas por este usuario
#   DEVOLVER perfil completo + eventos + puntuacion_promedio

@usuarios_bp.route('/perfil/<int:id>', methods=['GET'])
def obtener_perfil(id):
    # Buscar usuario, si no existe devuelve 404 automáticamente
    usuario = Usuario.query.get_or_404(id)

    # Eventos que creó este usuario
    eventos = Evento.query.filter_by(creador_id=id).all()

    # Calificaciones que recibió este usuario
    calificaciones = Calificacion.query.filter_by(evaluado_id=id).all()

    return jsonify({
        'id':                   usuario.id,
        'nombre':               usuario.nombre,
        'email':                usuario.email,
        'puntuacion_promedio':  usuario.puntuacion_promedio,
        'fecha_creacion':       usuario.fecha_creacion.isoformat(),
        'eventos': [
            {
                'id':           e.id,
                'titulo':       e.titulo,
                'fecha_evento': e.fecha_evento.isoformat(),
                'estado':       e.estado
            }
            for e in eventos
        ],
        'calificaciones_recibidas': [
            {
                'puntuacion':   c.puntuacion,
                'evaluador_id': c.evaluador_id,
                'evento_id':    c.evento_id
            }
            for c in calificaciones
        ]
    }), 200

# ================================
# POST /calificar
# ================================
# RUTA calificar():
#   SI no hay sesión activa → redirigir a login

#   RECIBIR datos del formulario:
#     - puntuacion (1 al 5)
#     - evaluado_id
#     - evento_id

#   BUSCAR el evento por evento_id
#   SI estado del evento != "pasado" → error (no se puede calificar aún)

#   VERIFICAR que el evaluador no haya calificado
#   ya a esta persona en este evento → si ya calificó, error

#   CREAR nueva Calificacion
#   GUARDAR en base de datos

#   RECALCULAR puntuacion_promedio del evaluado:
#     BUSCAR todas las calificaciones donde evaluado_id == evaluado_id
#     CALCULAR promedio de todas las puntuaciones
#     ACTUALIZAR puntuacion_promedio del Usuario

#   GUARDAR cambios
#   REDIRIGIR al perfil del evaluado

@usuarios_bp.route('/calificar', methods=['POST'])
def calificar():
    
    # Verificar sesión activa

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # ← coordiná el nombre con el módulo Auth

    # Recibir datos del formulario HTML

    evaluado_id = request.form.get('evaluado_id', type=int)
    evento_id   = request.form.get('evento_id',   type=int)
    puntuacion  = request.form.get('puntuacion',  type=int)

    # Validar que llegaron todos los campos

    if not all([evaluado_id, evento_id, puntuacion]):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    # Validar rango de puntuación

    if not (1 <= puntuacion <= 5):
        return jsonify({'error': 'La puntuación debe estar entre 1 y 5'}), 400

    # No podés calificarte a vos mismo

    if session['user_id'] == evaluado_id:
        return jsonify({'error': 'No podés calificarte a vos mismo'}), 400

    # Buscar el evento

    evento = Evento.query.get(evento_id)
    if not evento:
        return jsonify({'error': 'Evento no encontrado'}), 404

    # Solo se puede calificar si el evento ya pasó

    if evento.estado != 'pasado':
        return jsonify({'error': 'Solo podés calificar eventos que ya ocurrieron'}), 403

    # Verificar que no haya calificado antes a esta persona en este evento

    ya_califico = Calificacion.query.filter_by(
        evaluador_id = session['user_id'],
        evaluado_id  = evaluado_id,
        evento_id    = evento_id
    ).first()

    if ya_califico:
        return jsonify({'error': 'Ya calificaste a este usuario en este evento'}), 409

    # Crear y guardar la calificación

    nueva_calificacion = Calificacion(
        puntuacion   = puntuacion,
        evaluado_id  = evaluado_id,
        evaluador_id = session['user_id'],
        evento_id    = evento_id
    )
    db.session.add(nueva_calificacion)
    db.session.flush()  # flush para que la nueva calificación ya esté en memoria

    # Recalcular puntuacion_promedio del evaluado

    evaluado = Usuario.query.get(evaluado_id)

    evaluado.recalcular_promedio()

    # Guardar todo
    db.session.commit()

    # Redirigir al perfil del evaluado
    return redirect(url_for('usuarios.obtener_perfil', id=evaluado_id))

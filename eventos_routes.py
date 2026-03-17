# IMPORTAR Flask (Blueprint, request, session, redirect)

from flask import Blueprint, request, session, redirect, url_for, jsonify, abort

# IMPORTAR modelos (Evento, Usuario)

from models import db, Evento

from datetime import datetime, timedelta, timezone

# CREAR blueprint "eventos"

eventos_bp = Blueprint('eventos', __name__)


# ================================
# GET /eventos
# ================================
# RUTA obtener_eventos():
#   RECIBIR filtro de estado desde la URL (opcional)
  
#   SI hay filtro:
#     BUSCAR eventos donde estado == filtro
#   SI NO:
#     BUSCAR todos los eventos
  
#   DEVOLVER lista de eventos

@eventos_bp.route('/eventos', methods=['GET'])
def obtener_eventos():
    filtro = request.args.get('estado')

    if filtro:
        eventos = Evento.query.filter_by(estado=filtro).all()
    else:
        eventos = Evento.query.all()

    return jsonify([e.to_dict() for e in eventos])


# ================================
# GET /eventos/<id>
# ================================
# RUTA obtener_evento(id):
#   BUSCAR evento por id
#   SI no existe → error 404
#   DEVOLVER detalle del evento (incluye embed_mapa)

@eventos_bp.route('/eventos/<int:id>', methods=['GET'])
def obtener_evento(id):
    evento = Evento.query.get_or_404(id)
    return jsonify(evento.to_dict())

# ================================
# POST /eventos/crear
# ================================
# RUTA crear_evento():
#   SI no hay sesión activa → redirigir a login

#   RECIBIR datos del formulario:
#     - titulo, descripcion, fecha_evento
#     - ubicacion_texto, embed_mapa

#   CALCULAR fecha_expiracion = fecha_evento + 3 meses

#   CREAR nuevo Evento con estado "proximo"
#   ASIGNAR creador_id = usuario en sesión
#   GUARDAR en base de datos
#   REDIRIGIR al detalle del evento creado

@eventos_bp.route('/eventos/crear', methods=['POST'])
def crear_evento():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    titulo           = request.form.get('titulo')
    descripcion      = request.form.get('descripcion')
    fecha_evento_str = request.form.get('fecha_evento')
    ubicacion_texto  = request.form.get('ubicacion_texto')
    embed_mapa       = request.form.get('embed_mapa')

    fecha_evento     = datetime.fromisoformat(fecha_evento_str)
    fecha_expiracion = fecha_evento + timedelta(days=90)

    nuevo_evento = Evento(
        titulo=titulo,
        descripcion=descripcion,
        fecha_evento=fecha_evento,
        ubicacion_texto=ubicacion_texto,
        embed_mapa=embed_mapa,
        estado='proximo',
        fecha_expiracion=fecha_expiracion,
        creador_id=session['usuario_id']
    )

    db.session.add(nuevo_evento)
    db.session.commit()

    return redirect(url_for('eventos.obtener_evento', id=nuevo_evento.id))

# ================================
# POST /eventos/<id>/cancelar
# ================================
# RUTA cancelar_evento(id):
#   SI no hay sesión activa → redirigir a login
  
#   BUSCAR evento por id
#   SI el creador_id != usuario en sesión → error 403
  
#   CAMBIAR estado a "cancelado"
#   GUARDAR cambios
#   REDIRIGIR a lista de eventos

@eventos_bp.route('/eventos/<int:id>/cancelar', methods=['POST'])
def cancelar_evento(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    evento = Evento.query.get_or_404(id)

    if evento.creador_id != session['usuario_id']:
        abort(403)

    evento.estado = 'cancelado'
    db.session.commit()

    return redirect(url_for('eventos.obtener_eventos'))

# ================================
# TAREA: actualizar estados viejos
# ================================
# FUNCIÓN actualizar_estados_eventos():
#   BUSCAR eventos donde:
#     - estado == "proximo"
#     - fecha_evento < fecha y hora actual
#   PARA cada uno → cambiar estado a "pasado"

#   BUSCAR eventos donde:
#     - estado == "pasado"
#     - fecha_expiracion < fecha actual
#   PARA cada uno → eliminar de la base de datos

#   GUARDAR todos los cambios

def actualizar_estados_eventos():
    ahora = datetime.now(timezone.utc)

    proximos_vencidos = Evento.query.filter(
        Evento.estado == 'proximo',
        Evento.fecha_evento < ahora
    ).all()

    for evento in proximos_vencidos:
        evento.estado = 'pasado'

    pasados_expirados = Evento.query.filter(
        Evento.estado == 'pasado',
        Evento.fecha_expiracion < ahora
    ).all()

    for evento in pasados_expirados:
        db.session.delete(evento)

    db.session.commit()

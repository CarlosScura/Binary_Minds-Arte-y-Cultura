from flask import Blueprint, request, session, redirect, url_for, jsonify, abort, render_template

from models import db, Evento

from datetime import datetime, timedelta, timezone

eventos_bp = Blueprint('eventos', __name__)



@eventos_bp.route('/')
def inicio():
    eventos = Evento.query.filter_by(estado='proximo').all()
    return render_template('inicio.html', eventos=eventos)

@eventos_bp.route('/eventos', methods=['GET'])
def obtener_eventos():
    filtro = request.args.get('estado')

    if filtro:
        eventos = Evento.query.filter_by(estado=filtro).all()
    else:
        eventos = Evento.query.all()

    return render_template('eventos_lista.html', eventos=eventos)



@eventos_bp.route('/<int:id>', methods=['GET'])
def obtener_evento(id):
    evento = Evento.query.get_or_404(id)
    return render_template('evento_detalle.html', evento=evento)



@eventos_bp.route('/crear', methods=['GET'])
def mostrar_crear_evento():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.mostrar_login'))
    return render_template('crear_evento.html')

@eventos_bp.route('/crear', methods=['POST'])
def crear_evento():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.mostrar_login'))

    titulo           = request.form.get('titulo')
    descripcion      = request.form.get('descripcion')
    fecha_evento_str = request.form.get('fecha_evento')
    ubicacion_texto  = request.form.get('ubicacion_texto')
    embed_mapa       = request.form.get('embed_mapa')

    fecha_evento     = datetime.fromisoformat(fecha_evento_str).replace(tzinfo=timezone.utc)
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



@eventos_bp.route('/<int:id>/cancelar', methods=['POST'])
def cancelar_evento(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    evento = Evento.query.get_or_404(id)

    if evento.creador_id != session['usuario_id']:
        abort(403)

    evento.estado = 'cancelado'
    db.session.commit()

    return redirect(url_for('eventos.inicio'))



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
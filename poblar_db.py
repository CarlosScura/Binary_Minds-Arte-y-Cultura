from app import app, db
from models import Usuario, Evento
from datetime import datetime, timedelta, timezone

with app.app_context():
    ahora = datetime.now(timezone.utc)

    # Buscar usuarios existentes
    usuario1 = Usuario.query.filter_by(email='juan@correo.com').first()
    usuario2 = Usuario.query.filter_by(email='maria@correo.com').first()
    usuario3 = Usuario.query.filter_by(email='carlos@correo.com').first()

    # NUEVOS PRÓXIMOS
    evento_nuevo1 = Evento(
        titulo='Exposición de Arte Contemporáneo',
        descripcion='Muestra de obras de artistas emergentes paraguayos.',
        fecha_evento=ahora + timedelta(days=7),
        fecha_expiracion=ahora + timedelta(days=7+90),
        ubicacion_texto='Centro Cultural de la República, Asunción',
        embed_mapa='',
        estado='proximo',
        creador_id=usuario1.id
    )

    evento_nuevo2 = Evento(
        titulo='Galería Abierta: Arte Urbano',
        descripcion='Intervenciones artísticas en espacios públicos.',
        fecha_evento=ahora + timedelta(days=14),
        fecha_expiracion=ahora + timedelta(days=14+90),
        ubicacion_texto='Calle Palma, Asunción',
        embed_mapa='',
        estado='proximo',
        creador_id=usuario2.id
    )

    evento_nuevo3 = Evento(
        titulo='Festival de Música Folclórica',
        descripcion='Una noche de música tradicional paraguaya.',
        fecha_evento=ahora + timedelta(days=21),
        fecha_expiracion=ahora + timedelta(days=21+90),
        ubicacion_texto='Teatro Municipal, Asunción',
        embed_mapa='',
        estado='proximo',
        creador_id=usuario3.id
    )

    # NUEVO PASADO
    evento_nuevo4 = Evento(
        titulo='Feria de Artesanías',
        descripcion='Exposición y venta de artesanías tradicionales.',
        fecha_evento=ahora - timedelta(days=5),
        fecha_expiracion=ahora - timedelta(days=5) + timedelta(days=90),
        ubicacion_texto='Plaza Uruguaya, Asunción',
        embed_mapa='',
        estado='pasado',
        creador_id=usuario1.id
    )

    # NUEVO CANCELADO
    evento_nuevo5 = Evento(
        titulo='Taller de Pintura en Acuarela',
        descripcion='Aprende técnicas básicas y avanzadas de acuarela.',
        fecha_evento=ahora + timedelta(days=3),
        fecha_expiracion=ahora + timedelta(days=3+90),
        ubicacion_texto='Centro Cultural Paraguayo Japonés, Asunción',
        embed_mapa='',
        estado='cancelado',
        creador_id=usuario2.id
    )

    db.session.add_all([evento_nuevo1, evento_nuevo2, evento_nuevo3, evento_nuevo4, evento_nuevo5])
    db.session.commit()

    print('Eventos nuevos agregados correctamente!')

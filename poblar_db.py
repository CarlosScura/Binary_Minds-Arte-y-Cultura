# poblar_db.py
from app import app, db
from models import Usuario, Evento, Calificacion
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

with app.app_context():
    # Crear usuarios de prueba
    usuario1 = Usuario(
        nombre='Juan Pérez',
        email='juan@correo.com',
        password=generate_password_hash('123456')
    )
    usuario2 = Usuario(
        nombre='María Arroyo',
        email='maria@correo.com',
        password=generate_password_hash('123456')
    )
    usuario3 = Usuario(
        nombre='Carlos López',
        email='carlos@correo.com',
        password=generate_password_hash('123456')
    )
    db.session.add_all([usuario1, usuario2, usuario3])
    db.session.commit()

    # Crear eventos
    ahora = datetime.now()
    evento1 = Evento(
        titulo='Concierto de Rock',
        descripcion='Noche de rock con bandas Nacionales',
        fecha=ahora + timedelta(days=10),
        ubicacion='Teatro I. A. Pane',
        embed_mapa='<iframe src="https://maps.google.com/..."></iframe>',
        estado='proximo',
        creador_id=usuario1.id
    )
    evento2 = Evento(
        titulo='Feria de Artesanías',
        descripcion='Exposición y venta de artesanías',
        fecha=ahora - timedelta(days=5),
        ubicacion='Plaza Uruguaya',
        embed_mapa='',
        estado='pasado',
        creador_id=usuario2.id
    )
    evento3 = Evento(
        titulo='Taller de Pintura',
        descripcion='Aprende técnicas de acuarela',
        fecha=ahora + timedelta(days=20),
        ubicacion='Centro Cultural Paraguayo Japones',
        embed_mapa='',
        estado='cancelado',
        creador_id=usuario3.id
    )
    db.session.add_all([evento1, evento2, evento3])
    db.session.commit()

    # Crear calificaciones de prueba (para el evento pasado)
    calif1 = Calificacion(
        puntuacion=4.5,
        comentario='Muy buen organizador',
        usuario_id=usuario2.id,  # evaluado (creador del evento2)
        calificador_id=usuario1.id,
        evento_id=evento2.id
    )
    calif2 = Calificacion(
        puntuacion=5,
        comentario='Excelente evento',
        usuario_id=usuario2.id,
        calificador_id=usuario3.id,
        evento_id=evento2.id
    )
    db.session.add_all([calif1, calif2])
    db.session.commit()

    print('Gracias Por Elegirnos¡.')
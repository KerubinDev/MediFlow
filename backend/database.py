from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin se não existir
        from backend.models import Usuario
        from werkzeug.security import generate_password_hash
        
        admin = Usuario.query.filter_by(email='admin@medflow.com').first()
        if not admin:
            admin = Usuario(
                nome='Administrador',
                email='admin@medflow.com',
                senha=generate_password_hash('admin123'),
                tipo='admin'
            )
            db.session.add(admin)
            db.session.commit() 
from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from backend.config import Config
from backend.database import db
from backend.routes import api, views
from backend.auth import auth, login_manager
from werkzeug.exceptions import HTTPException
import json
import os

def criar_app(config_class=Config):
    """Cria e configura a aplicação Flask"""
    # Configura o caminho correto para templates e static
    template_dir = os.path.abspath('templates')
    static_dir = os.path.abspath('static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    app.config.from_object(config_class)
    
    # Inicializa extensões
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Registra blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(views)
    
    # Cria tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Trata erros HTTP retornando JSON"""
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_error(e):
        """Trata erros não-HTTP"""
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "description": str(e)
        }), 500

    return app

if __name__ == '__main__':
    app = criar_app()
    app.run(debug=True) 
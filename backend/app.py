"""
MediFlow - Sistema de Gestão para Clínicas Médicas
Backend principal do sistema
Desenvolvido por Kelvin Moraes (@KerubinDev)
GitHub: https://github.com/KerubinDev
Email: kelvin.moraes117@gmail.com
"""

from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from flask_login import LoginManager
from backend.config import Config
from backend.database import db, init_db
from backend.routes import api, views
from backend.auth import auth
from werkzeug.exceptions import HTTPException
import json
import os
import logging
from backend.models import Usuario

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    init_db(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registra blueprints
    app.register_blueprint(api)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(views)
    
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

    @app.errorhandler(404)
    def not_found_error(error):
        """Tratamento específico para erro 404"""
        logger.error(f"Rota não encontrada: {request.url}")
        return jsonify({
            'erro': 'Rota não encontrada',
            'url': request.url,
            'method': request.method
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        current_app.logger.error(f"Erro 500: {str(error)}")
        db.session.rollback()  # Rollback em caso de erro no banco
        return jsonify({
            'erro': 'Erro interno do servidor',
            'detalhes': str(error)
        }), 500

    @app.before_request
    def log_request_info():
        current_app.logger.debug('------------------------')
        current_app.logger.debug('Nova Requisição:')
        current_app.logger.debug(f'URL: {request.url}')
        current_app.logger.debug(f'Método: {request.method}')
        current_app.logger.debug(f'Headers: {dict(request.headers)}')
        if request.is_json:
            current_app.logger.debug(f'Dados JSON: {request.get_json()}')
        current_app.logger.debug('------------------------')

    return app

if __name__ == '__main__':
    app = criar_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000) 
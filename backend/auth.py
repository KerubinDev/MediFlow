from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from backend.models import Usuario
from backend.database import db

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def carregar_usuario(id):
    """Carrega o usuário pelo ID"""
    return Usuario.query.get(int(id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Gerencia o login de usuários"""
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        
        flash('Email ou senha inválidos')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    """Realiza o logout do usuário"""
    logout_user()
    return redirect(url_for('auth.login')) 
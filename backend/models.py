from backend.database import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    """Modelo para usuários do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # admin, medico, recepcionista
    
    def is_admin(self):
        return self.tipo == 'admin'
    
    def is_medico(self):
        return self.tipo == 'medico'
    
    def is_recepcionista(self):
        return self.tipo == 'recepcionista'
    
    # Métodos requeridos pelo Flask-Login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Paciente(db.Model):
    """Modelo para pacientes"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    endereco = db.Column(db.String(200))
    consultas = db.relationship('Consulta', backref='paciente', lazy=True)


class Medico(db.Model):
    """Modelo para médicos"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(20), unique=True, nullable=False)
    especialidade = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    horario_disponivel = db.Column(db.String(200))
    consultas = db.relationship('Consulta', backref='medico', lazy=True)
    usuario = db.relationship('Usuario', backref='medico', uselist=False)


class Consulta(db.Model):
    """Modelo para consultas"""
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='agendada')  # agendada, realizada, cancelada
    prontuario = db.relationship('Prontuario', backref='consulta', uselist=False)


class Prontuario(db.Model):
    """Modelo para prontuários"""
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    diagnostico = db.Column(db.Text)
    prescricao = db.Column(db.Text)
    exames_solicitados = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)


class Pagamento(db.Model):
    """Modelo para pagamentos"""
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, pago, cancelado
    data_pagamento = db.Column(db.DateTime)
    
    consulta = db.relationship('Consulta', backref='pagamento', uselist=False) 
from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    """Modelo para usuários do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _senha_hash = db.Column(db.String(128))
    tipo = db.Column(db.String(20), nullable=False)  # admin, medico, paciente
    
    @property
    def senha(self):
        raise AttributeError('senha não é um atributo legível')
        
    @senha.setter
    def senha(self, senha):
        self._senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self._senha_hash, senha)


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
    especialidade = db.Column(db.String(50))
    horario_disponivel = db.Column(db.String(200))
    consultas = db.relationship('Consulta', backref='medico', lazy=True)


class Consulta(db.Model):
    """Modelo para consultas"""
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'))
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='agendada')
    prontuario = db.relationship('Prontuario', backref='consulta', 
        uselist=False)


class Prontuario(db.Model):
    """Modelo para prontuários"""
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'))
    diagnostico = db.Column(db.Text)
    prescricao = db.Column(db.Text)
    exames_solicitados = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)


class Pagamento(db.Model):
    """Modelo para pagamentos"""
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'))
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)
    valor = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='pendente') 
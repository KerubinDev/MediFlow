from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from backend.models import (Usuario, Paciente, Medico, Consulta, Prontuario, 
    Pagamento)
from backend.database import db
from datetime import datetime, date

# Criação do Blueprint para as rotas da API
api = Blueprint('api', __name__)
views = Blueprint('views', __name__)


@api.route('/usuarios', methods=['GET', 'POST'])
def gerenciar_usuarios():
    """
    Gerencia operações de usuários.
    GET: Lista todos usuários
    POST: Cria novo usuário
    """
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        return jsonify([{
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
            'tipo': u.tipo
        } for u in usuarios])
    
    dados = request.get_json()
    novo_usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=dados['senha'],
        tipo=dados['tipo']
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário criado com sucesso'})


@api.route('/pacientes', methods=['GET', 'POST'])
def gerenciar_pacientes():
    """
    Gerencia operações de pacientes.
    GET: Lista todos pacientes
    POST: Cadastra novo paciente
    """
    if request.method == 'GET':
        pacientes = Paciente.query.all()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'telefone': p.telefone,
            'data_nascimento': p.data_nascimento.strftime('%Y-%m-%d'),
            'endereco': p.endereco
        } for p in pacientes])
    
    dados = request.get_json()
    novo_paciente = Paciente(
        nome=dados['nome'],
        telefone=dados['telefone'],
        data_nascimento=datetime.strptime(dados['data_nascimento'], 
            '%Y-%m-%d'),
        endereco=dados['endereco']
    )
    db.session.add(novo_paciente)
    db.session.commit()
    return jsonify({'mensagem': 'Paciente cadastrado com sucesso'})


@api.route('/medicos', methods=['GET', 'POST'])
def gerenciar_medicos():
    """
    Gerencia operações de médicos.
    GET: Lista todos médicos
    POST: Cadastra novo médico
    """
    if request.method == 'GET':
        medicos = Medico.query.all()
        return jsonify([{
            'id': m.id,
            'nome': m.nome,
            'especialidade': m.especialidade,
            'horario_disponivel': m.horario_disponivel
        } for m in medicos])
    
    dados = request.get_json()
    novo_medico = Medico(
        nome=dados['nome'],
        especialidade=dados['especialidade'],
        horario_disponivel=dados['horario_disponivel']
    )
    db.session.add(novo_medico)
    db.session.commit()
    return jsonify({'mensagem': 'Médico cadastrado com sucesso'})


@api.route('/consultas', methods=['GET', 'POST'])
def gerenciar_consultas():
    """
    Gerencia operações de consultas.
    GET: Lista todas consultas
    POST: Agenda nova consulta
    """
    if request.method == 'GET':
        consultas = Consulta.query.all()
        return jsonify([{
            'id': c.id,
            'paciente_id': c.paciente_id,
            'medico_id': c.medico_id,
            'data_hora': c.data_hora.strftime('%Y-%m-%d %H:%M'),
            'status': c.status
        } for c in consultas])
    
    dados = request.get_json()
    nova_consulta = Consulta(
        paciente_id=dados['paciente_id'],
        medico_id=dados['medico_id'],
        data_hora=datetime.strptime(dados['data_hora'], '%Y-%m-%d %H:%M'),
        status='agendada'
    )
    db.session.add(nova_consulta)
    db.session.commit()
    return jsonify({'mensagem': 'Consulta agendada com sucesso'})


@api.route('/prontuarios', methods=['GET', 'POST'])
def gerenciar_prontuarios():
    """
    Gerencia operações de prontuários.
    GET: Lista todos prontuários
    POST: Cria novo prontuário
    """
    if request.method == 'GET':
        prontuarios = Prontuario.query.all()
        return jsonify([{
            'id': p.id,
            'consulta_id': p.consulta_id,
            'diagnostico': p.diagnostico,
            'prescricao': p.prescricao,
            'exames_solicitados': p.exames_solicitados
        } for p in prontuarios])
    
    dados = request.get_json()
    novo_prontuario = Prontuario(
        consulta_id=dados['consulta_id'],
        diagnostico=dados['diagnostico'],
        prescricao=dados['prescricao'],
        exames_solicitados=dados['exames_solicitados']
    )
    db.session.add(novo_prontuario)
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário criado com sucesso'})


@api.route('/pagamentos', methods=['GET', 'POST'])
def gerenciar_pagamentos():
    """
    Gerencia operações de pagamentos.
    GET: Lista todos pagamentos
    POST: Registra novo pagamento
    """
    if request.method == 'GET':
        pagamentos = Pagamento.query.all()
        return jsonify([{
            'id': p.id,
            'paciente_id': p.paciente_id,
            'consulta_id': p.consulta_id,
            'data_pagamento': p.data_pagamento.strftime('%Y-%m-%d'),
            'valor': float(p.valor),
            'status': p.status
        } for p in pagamentos])
    
    dados = request.get_json()
    novo_pagamento = Pagamento(
        paciente_id=dados['paciente_id'],
        consulta_id=dados['consulta_id'],
        data_pagamento=datetime.now(),
        valor=dados['valor'],
        status='pago'
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify({'mensagem': 'Pagamento registrado com sucesso'})


@views.route('/dashboard')
@login_required
def dashboard():
    """Renderiza o dashboard principal"""
    stats = {
        'consultas_hoje': Consulta.query.filter(
            Consulta.data_hora.date() == date.today()
        ).count(),
        'total_pacientes': Paciente.query.count(),
        'medicos_ativos': Medico.query.count()
    }
    
    consultas = Consulta.query.filter(
        Consulta.data_hora.date() == date.today()
    ).order_by(Consulta.data_hora).all()
    
    return render_template('dashboard.html', stats=stats, consultas=consultas)

@views.route('/consultas')
@login_required
def consultas():
    """Página de gerenciamento de consultas"""
    consultas = Consulta.query.order_by(Consulta.data_hora).all()
    return render_template('consultas.html', consultas=consultas)

@views.route('/prontuarios')
@login_required
def prontuarios():
    """Página de prontuários médicos"""
    prontuarios = Prontuario.query.order_by(
        Prontuario.data_criacao.desc()
    ).all()
    return render_template('prontuario.html', prontuarios=prontuarios)

@views.route('/pacientes')
@login_required
def pacientes():
    """Página de gerenciamento de pacientes"""
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    return render_template('pacientes.html', pacientes=pacientes)

@api.route('/pacientes/<int:id>/historico')
def historico_paciente(id):
    """Retorna o histórico de consultas do paciente"""
    consultas = Consulta.query.filter_by(paciente_id=id)\
        .order_by(Consulta.data_hora.desc()).all()
    return jsonify([{
        'data_hora': c.data_hora,
        'medico': {
            'nome': c.medico.nome,
            'especialidade': c.medico.especialidade
        },
        'status': c.status
    } for c in consultas])

@api.route('/pacientes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_paciente(id):
    """Gerencia operações em um paciente específico"""
    paciente = Paciente.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'id': paciente.id,
            'nome': paciente.nome,
            'telefone': paciente.telefone,
            'data_nascimento': paciente.data_nascimento.strftime('%Y-%m-%d'),
            'endereco': paciente.endereco
        })
    
    elif request.method == 'PUT':
        dados = request.get_json()
        paciente.nome = dados['nome']
        paciente.telefone = dados['telefone']
        paciente.data_nascimento = datetime.strptime(
            dados['data_nascimento'], '%Y-%m-%d')
        paciente.endereco = dados['endereco']
        db.session.commit()
        return jsonify({'mensagem': 'Paciente atualizado com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'mensagem': 'Paciente removido com sucesso'})

@api.route('/prontuarios/<int:id>')
def obter_prontuario(id):
    """Retorna detalhes de um prontuário específico"""
    prontuario = Prontuario.query.get_or_404(id)
    return jsonify({
        'id': prontuario.id,
        'consulta': {
            'data_hora': prontuario.consulta.data_hora,
            'paciente': {
                'nome': prontuario.consulta.paciente.nome
            },
            'medico': {
                'nome': prontuario.consulta.medico.nome
            }
        },
        'diagnostico': prontuario.diagnostico,
        'prescricao': prontuario.prescricao,
        'exames_solicitados': prontuario.exames_solicitados
    })

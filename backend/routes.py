from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from backend.models import (Usuario, Paciente, Medico, Consulta, Prontuario, 
    Pagamento)
from backend.database import db
from datetime import datetime, date, timedelta
from functools import wraps
from flask import abort
from sqlalchemy import func, cast, Date

# Criação do Blueprint para as rotas da API
api = Blueprint('api', __name__)
views = Blueprint('views', __name__)


@api.route('/consultas/criar', methods=['POST'])
@login_required
def criar_consulta():
    """Cria uma nova consulta"""
    dados = request.get_json()
    
    consulta = Consulta(
        paciente_id=dados['paciente_id'],
        medico_id=dados['medico_id'],
        data_hora=datetime.fromisoformat(dados['data_hora']),
        status='agendada'
    )
    
    db.session.add(consulta)
    db.session.commit()
    
    return jsonify({'mensagem': 'Consulta criada com sucesso'})


@api.route('/consultas/<int:id>/realizar', methods=['PUT'])
@login_required
@medico_required
def realizar_consulta(id):
    """Marca uma consulta como realizada"""
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'realizada'
    db.session.commit()
    return jsonify({'mensagem': 'Consulta realizada com sucesso'})


@api.route('/consultas/<int:id>/cancelar', methods=['PUT'])
@login_required
def cancelar_consulta(id):
    """Cancela uma consulta"""
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'cancelada'
    db.session.commit()
    return jsonify({'mensagem': 'Consulta cancelada com sucesso'})


@api.route('/prontuarios/criar', methods=['POST'])
@login_required
@medico_required
def criar_prontuario():
    """Cria um novo prontuário"""
    dados = request.get_json()
    
    prontuario = Prontuario(
        consulta_id=dados['consulta_id'],
        diagnostico=dados['diagnostico'],
        prescricao=dados['prescricao'],
        exames_solicitados=dados['exames_solicitados']
    )
    
    db.session.add(prontuario)
    db.session.commit()
    
    return jsonify({'mensagem': 'Prontuário criado com sucesso'})


@api.route('/prontuarios/<int:id>/detalhes', methods=['GET'])
@login_required
@medico_required
def obter_prontuario_detalhes(id):
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


@api.route('/prontuarios/<int:id>/atualizar', methods=['PUT'])
@login_required
@medico_required
def atualizar_prontuario_dados(id):
    """Atualiza um prontuário existente"""
    prontuario = Prontuario.query.get_or_404(id)
    dados = request.get_json()
    
    prontuario.diagnostico = dados['diagnostico']
    prontuario.prescricao = dados['prescricao']
    prontuario.exames_solicitados = dados['exames_solicitados']
    
    db.session.commit()
    return jsonify({'mensagem': 'Prontuário atualizado com sucesso'})


@api.route('/prontuarios/<int:id>/imprimir', methods=['GET'])
@login_required
def imprimir_prontuario(id):
    """Gera PDF do prontuário para impressão"""
    prontuario = Prontuario.query.get_or_404(id)
    # Implementar geração de PDF
    return jsonify({'url': f'/static/prontuarios/prontuario_{id}.pdf'})


@api.route('/pacientes/criar', methods=['POST'])
@login_required
def criar_paciente():
    """Cria um novo paciente"""
    dados = request.get_json()
    
    paciente = Paciente(
        nome=dados['nome'],
        telefone=dados['telefone'],
        data_nascimento=datetime.strptime(dados['data_nascimento'], '%Y-%m-%d'),
        endereco=dados['endereco']
    )
    
    db.session.add(paciente)
    db.session.commit()
    
    return jsonify({'mensagem': 'Paciente criado com sucesso'})


@api.route('/pacientes/<int:id>/detalhes', methods=['GET'])
@login_required
def obter_paciente_detalhes(id):
    """Retorna os dados de um paciente específico"""
    paciente = Paciente.query.get_or_404(id)
    return jsonify({
        'id': paciente.id,
        'nome': paciente.nome,
        'telefone': paciente.telefone,
        'data_nascimento': paciente.data_nascimento.strftime('%Y-%m-%d'),
        'endereco': paciente.endereco
    })


@api.route('/pacientes/<int:id>/atualizar', methods=['PUT'])
@login_required
def atualizar_paciente_dados(id):
    """Atualiza um paciente existente"""
    paciente = Paciente.query.get_or_404(id)
    dados = request.get_json()
    
    paciente.nome = dados['nome']
    paciente.telefone = dados['telefone']
    paciente.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d')
    paciente.endereco = dados['endereco']
    
    db.session.commit()
    return jsonify({'mensagem': 'Paciente atualizado com sucesso'})


@api.route('/pacientes/<int:id>/excluir', methods=['DELETE'])
@login_required
def excluir_paciente_registro(id):
    """Remove um paciente"""
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({'mensagem': 'Paciente removido com sucesso'})


@api.route('/pacientes/<int:id>/historico', methods=['GET'])
@login_required
def obter_historico_paciente(id):
    """Retorna o histórico de consultas do paciente"""
    consultas = Consulta.query.filter_by(paciente_id=id).order_by(
        Consulta.data_hora.desc()
    ).all()
    
    return jsonify([{
        'id': c.id,
        'data_hora': c.data_hora.isoformat(),
        'status': c.status,
        'medico': {
            'id': c.medico.id,
            'nome': c.medico.nome
        }
    } for c in consultas])


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (
            current_user.tipo != 'admin' and 
            current_user.email != 'admin@medflow.com'
        ):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def medico_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (
            current_user.tipo != 'medico' and 
            current_user.email != 'admin@medflow.com'
        ):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def recepcionista_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (
            current_user.tipo != 'recepcionista' and 
            current_user.email != 'admin@medflow.com'
        ):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@views.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Renderiza o dashboard principal"""
    hoje = date.today()
    amanha = hoje + timedelta(days=1)
    
    stats = {
        'consultas_hoje': Consulta.query.filter(
            Consulta.data_hora >= hoje,
            Consulta.data_hora < amanha
        ).count(),
        'total_pacientes': Paciente.query.count(),
        'medicos_ativos': Medico.query.count()
    }
    
    consultas = Consulta.query.filter(
        Consulta.data_hora >= hoje,
        Consulta.data_hora < amanha
    ).order_by(Consulta.data_hora).all()
    
    return render_template('dashboard.html', stats=stats, consultas=consultas)

@views.route('/consultas')
@login_required
def consultas():
    """Página de consultas"""
    consultas = Consulta.query.order_by(Consulta.data_hora).all()
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    medicos = Medico.query.order_by(Medico.nome).all()
    return render_template('consultas.html', 
                         consultas=consultas,
                         pacientes=pacientes,
                         medicos=medicos)

@views.route('/prontuarios')
@login_required
@medico_required
def prontuarios():
    """Página de prontuários"""
    if current_user.tipo == 'medico':
        # Filtrar prontuários apenas do médico logado
        medico = Medico.query.filter_by(nome=current_user.nome).first()
        prontuarios = Prontuario.query.join(Consulta).filter(
            Consulta.medico_id == medico.id
        ).order_by(Consulta.data_hora.desc()).all()
    else:
        # Admin vê todos os prontuários
        prontuarios = Prontuario.query.join(Consulta).order_by(
            Consulta.data_hora.desc()
        ).all()
    return render_template('prontuarios.html', prontuarios=prontuarios)

@views.route('/pacientes')
@login_required
def pacientes():
    """Página de pacientes"""
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

@views.route('/')
def index():
    """Redireciona para login se não estiver autenticado ou para a página apropriada se estiver"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('views.dashboard'))
        elif current_user.is_medico():
            return redirect(url_for('views.consultas'))
        elif current_user.is_recepcionista():
            return redirect(url_for('views.pacientes'))
    return redirect(url_for('auth.login'))

@views.route('/usuarios')
@login_required
@admin_required
def usuarios():
    """Página de gerenciamento de usuários"""
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template('usuarios.html', usuarios=usuarios)

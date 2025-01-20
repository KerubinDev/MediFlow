from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from backend.models import (Usuario, Paciente, Medico, Consulta, Prontuario, 
    Pagamento)
from backend.database import db
from datetime import datetime, date, timedelta
from functools import wraps
from flask import abort
from sqlalchemy import func, cast, Date

# Criação do Blueprint para as rotas da API
api = Blueprint('api', __name__, url_prefix='/api')
views = Blueprint('views', __name__)

# Definição dos decoradores de permissão
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

# Rotas da API
@api.route('/consultas', methods=['GET'])
@login_required
def listar_consultas():
    try:
        current_app.logger.debug("Iniciando listagem de consultas")
        consultas = Consulta.query.all()
        current_app.logger.debug(f"Encontradas {len(consultas)} consultas")
        
        resultado = [{
            'id': c.id,
            'paciente_id': c.paciente_id,
            'medico_id': c.medico_id,
            'data_hora': c.data_hora.isoformat(),
            'status': c.status,
            'paciente': {'nome': c.paciente.nome},
            'medico': {'nome': c.medico.nome}
        } for c in consultas]
        
        return jsonify(resultado)
    except Exception as e:
        current_app.logger.error(f"Erro ao listar consultas: {str(e)}")
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@api.route('/consultas', methods=['POST'])
@login_required
def criar_consulta():
    try:
        dados = request.get_json()
        current_app.logger.debug(f"Dados recebidos para criar consulta: {dados}")
        
        # Validar dados
        if not all(k in dados for k in ['paciente_id', 'medico_id', 'data_hora']):
            return jsonify({'erro': 'Dados incompletos'}), 400
            
        # Converter string para datetime
        try:
            data_hora = datetime.fromisoformat(dados['data_hora'])
        except ValueError as e:
            return jsonify({'erro': f'Formato de data inválido: {str(e)}'}), 400
        
        consulta = Consulta(
            paciente_id=dados['paciente_id'],
            medico_id=dados['medico_id'],
            data_hora=data_hora,
            status='agendada'
        )
        
        db.session.add(consulta)
        db.session.commit()
        
        current_app.logger.info(f"Consulta criada com sucesso: ID {consulta.id}")
        return jsonify({
            'mensagem': 'Consulta criada com sucesso',
            'id': consulta.id
        })
    except Exception as e:
        current_app.logger.error(f"Erro ao criar consulta: {str(e)}")
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@api.route('/consultas/<int:id>', methods=['GET'])
@login_required
def obter_consulta(id):
    try:
        current_app.logger.debug(f"Obtendo consulta {id}")
        
        consulta = Consulta.query.get(id)
        if not consulta:
            current_app.logger.error(f"Consulta {id} não encontrada")
            return jsonify({'erro': f'Consulta {id} não encontrada'}), 404
            
        if not consulta.paciente:
            current_app.logger.error(f"Paciente não encontrado para consulta {id}")
            return jsonify({'erro': 'Paciente não encontrado para esta consulta'}), 400
            
        if not consulta.medico:
            current_app.logger.error(f"Médico não encontrado para consulta {id}")
            return jsonify({'erro': 'Médico não encontrado para esta consulta'}), 400
            
        dados = {
            'id': consulta.id,
            'paciente_id': consulta.paciente_id,
            'medico_id': consulta.medico_id,
            'data_hora': consulta.data_hora.isoformat(),
            'status': consulta.status,
            'paciente': {
                'id': consulta.paciente.id,
                'nome': consulta.paciente.nome
            },
            'medico': {
                'id': consulta.medico.id,
                'nome': consulta.medico.nome
            }
        }
        
        current_app.logger.debug(f"Dados da consulta: {dados}")
        return jsonify(dados)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter consulta {id}: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@api.route('/consultas/<int:id>', methods=['PUT'])
@login_required
def atualizar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    dados = request.get_json()
    consulta.paciente_id = dados['paciente_id']
    consulta.medico_id = dados['medico_id']
    consulta.data_hora = datetime.fromisoformat(dados['data_hora'])
    db.session.commit()
    return jsonify({'mensagem': 'Consulta atualizada com sucesso'})

@api.route('/consultas/<int:id>/realizar', methods=['PUT'])
@login_required
@medico_required
def realizar_consulta(id):
    try:
        current_app.logger.debug(f"Realizando consulta {id}")
        
        consulta = Consulta.query.get(id)
        if not consulta:
            current_app.logger.error(f"Consulta {id} não encontrada")
            return jsonify({'erro': f'Consulta {id} não encontrada'}), 404
            
        if consulta.status == 'realizada':
            return jsonify({'erro': 'Consulta já foi realizada'}), 400
            
        if consulta.status == 'cancelada':
            return jsonify({'erro': 'Não é possível realizar uma consulta cancelada'}), 400
            
        consulta.status = 'realizada'
        db.session.commit()
        
        current_app.logger.info(f"Consulta {id} realizada com sucesso")
        return jsonify({'mensagem': 'Consulta realizada com sucesso'})
    except Exception as e:
        current_app.logger.error(f"Erro ao realizar consulta {id}: {str(e)}")
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@api.route('/consultas/<int:id>/cancelar', methods=['PUT'])
@login_required
def cancelar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'cancelada'
    db.session.commit()
    return jsonify({'mensagem': 'Consulta cancelada com sucesso'})

@api.route('/prontuarios', methods=['POST'])
@login_required
@medico_required
def criar_prontuario():
    try:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@api.route('/consultas/<int:id>/detalhes', methods=['GET'])
@login_required
def obter_consulta_detalhes(id):
    """Retorna detalhes de uma consulta específica"""
    consulta = Consulta.query.get_or_404(id)
    return jsonify({
        'id': consulta.id,
        'paciente_id': consulta.paciente_id,
        'medico_id': consulta.medico_id,
        'data_hora': consulta.data_hora.isoformat(),
        'status': consulta.status,
        'paciente': {
            'nome': consulta.paciente.nome
        },
        'medico': {
            'nome': consulta.medico.nome
        }
    })

@api.route('/prontuarios/<int:id>/detalhes', methods=['GET'])
@login_required
@medico_required
def obter_prontuario_detalhes(id):
    """Retorna detalhes de um prontuário específico"""
    try:
        print(f"Buscando prontuário com ID: {id}")
        prontuario = Prontuario.query.get_or_404(id)
        print(f"Prontuário encontrado: {prontuario.id}")
        
        if not prontuario.consulta:
            print("Consulta não encontrada")
            return jsonify({'erro': 'Consulta não encontrada para este prontuário'}), 404
            
        print(f"Consulta encontrada: {prontuario.consulta.id}")
        
        if not prontuario.consulta.paciente:
            print("Paciente não encontrado")
            return jsonify({'erro': 'Paciente não encontrado para esta consulta'}), 404
            
        if not prontuario.consulta.medico:
            print("Médico não encontrado")
            return jsonify({'erro': 'Médico não encontrado para esta consulta'}), 404
        
        dados = {
            'id': prontuario.id,
            'consulta': {
                'id': prontuario.consulta.id,
                'data_hora': prontuario.consulta.data_hora.isoformat(),
                'paciente': {
                    'id': prontuario.consulta.paciente.id,
                    'nome': prontuario.consulta.paciente.nome
                },
                'medico': {
                    'id': prontuario.consulta.medico.id,
                    'nome': prontuario.consulta.medico.nome
                }
            },
            'diagnostico': prontuario.diagnostico,
            'prescricao': prontuario.prescricao,
            'exames_solicitados': prontuario.exames_solicitados
        }
        print(f"Dados do prontuário: {dados}")
        return jsonify(dados)
    except Exception as e:
        print(f"Erro ao obter prontuário: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'erro': f'Erro ao carregar dados do prontuário: {str(e)}'}), 500

@api.route('/prontuarios/<int:id>/atualizar', methods=['PUT'])
@login_required
@medico_required
def atualizar_prontuario(id):
    """Atualiza um prontuário existente"""
    try:
        print(f"Atualizando prontuário {id}")
        prontuario = Prontuario.query.get_or_404(id)
        dados = request.get_json()
        
        print(f"Dados recebidos: {dados}")
        
        prontuario.diagnostico = dados.get('diagnostico')
        prontuario.prescricao = dados.get('prescricao')
        prontuario.exames_solicitados = dados.get('exames_solicitados')
        
        db.session.commit()
        print("Prontuário atualizado com sucesso")
        
        return jsonify({'mensagem': 'Prontuário atualizado com sucesso'})
    except Exception as e:
        print(f"Erro ao atualizar prontuário: {str(e)}")
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@api.route('/prontuarios/<int:id>/imprimir', methods=['GET'])
@login_required
def imprimir_prontuario(id):
    """Gera PDF do prontuário para impressão"""
    try:
        print(f"Gerando impressão do prontuário {id}")
        prontuario = Prontuario.query.get_or_404(id)
        
        dados = {
            'paciente': prontuario.consulta.paciente.nome,
            'medico': prontuario.consulta.medico.nome,
            'data': prontuario.consulta.data_hora.strftime('%d/%m/%Y'),
            'diagnostico': prontuario.diagnostico,
            'prescricao': prontuario.prescricao,
            'exames': prontuario.exames_solicitados
        }
        
        print(f"Dados para impressão: {dados}")
        return jsonify(dados)
    except Exception as e:
        print(f"Erro ao gerar impressão: {str(e)}")
        return jsonify({'erro': str(e)}), 500

@api.route('/pacientes/criar', methods=['POST'])
@login_required
def criar_paciente():
    """Cria um novo paciente"""
    try:
        dados = request.get_json()
        current_app.logger.debug(f"Dados recebidos para criar paciente: {dados}")
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'telefone', 'data_nascimento', 'endereco']
        if not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({
                'erro': 'Dados incompletos. Todos os campos são obrigatórios.'
            }), 400
        
        # Validar formato da data
        try:
            data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'erro': 'Formato de data inválido. Use YYYY-MM-DD'
            }), 400
        
        # Criar o paciente
        paciente = Paciente(
            nome=dados['nome'],
            telefone=dados['telefone'],
            data_nascimento=data_nascimento,
            endereco=dados['endereco']
        )
        
        db.session.add(paciente)
        db.session.commit()
        
        current_app.logger.info(f"Paciente criado com sucesso: ID {paciente.id}")
        return jsonify({
            'mensagem': 'Paciente criado com sucesso',
            'id': paciente.id
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao criar paciente: {str(e)}")
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

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
    """Retorna o histórico detalhado de consultas do paciente"""
    consultas = Consulta.query.filter_by(paciente_id=id)\
        .order_by(Consulta.data_hora.desc()).all()
    
    return jsonify([{
        'id': c.id,
        'data_hora': c.data_hora.isoformat(),
        'status': c.status,
        'medico': {
            'id': c.medico.id,
            'nome': c.medico.nome,
            'especialidade': c.medico.especialidade
        },
        'prontuario': {
            'id': c.prontuario.id if c.prontuario else None,
            'diagnostico': c.prontuario.diagnostico if c.prontuario else None
        } if c.status == 'realizada' else None
    } for c in consultas])

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

from backend.models import Usuario, Paciente, Medico, Consulta, Prontuario, Pagamento
from backend.database import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def criar_usuarios_padrao():
    """Cria usuários padrão do sistema"""
    usuarios = [
        {
            'nome': 'Administrador',
            'email': 'admin@medflow.com',
            'senha': 'admin123',
            'tipo': 'admin'
        },
        {
            'nome': 'Dr. João Silva',
            'email': 'medico@medflow.com',
            'senha': 'medico123',
            'tipo': 'medico'
        },
        {
            'nome': 'Maria Recepção',
            'email': 'recepcao@medflow.com',
            'senha': 'recepcao123',
            'tipo': 'recepcionista'
        }
    ]
    
    for u in usuarios:
        if not Usuario.query.filter_by(email=u['email']).first():
            usuario = Usuario(
                nome=u['nome'],
                email=u['email'],
                tipo=u['tipo']
            )
            usuario.senha = u['senha']
            db.session.add(usuario)

def criar_dados_exemplo():
    """Cria dados de exemplo para o sistema"""
    # Criar médicos
    medico = Medico(
        nome='Dr. João Silva',
        especialidade='Clínico Geral',
        horario_disponivel='08:00-18:00'
    )
    db.session.add(medico)
    
    # Criar pacientes
    pacientes = [
        {
            'nome': 'Ana Santos',
            'telefone': '(11) 99999-1111',
            'data_nascimento': datetime(1990, 5, 15),
            'endereco': 'Rua A, 123'
        },
        {
            'nome': 'Carlos Oliveira',
            'telefone': '(11) 99999-2222',
            'data_nascimento': datetime(1985, 8, 20),
            'endereco': 'Rua B, 456'
        }
    ]
    
    for p in pacientes:
        paciente = Paciente(**p)
        db.session.add(paciente)
        db.session.flush()  # Para obter o ID do paciente
        
        # Criar consultas para cada paciente
        consulta = Consulta(
            paciente_id=paciente.id,
            medico_id=medico.id,
            data_hora=datetime.now() + timedelta(days=1),
            status='agendada'
        )
        db.session.add(consulta)
        db.session.flush()
        
        # Criar prontuário
        prontuario = Prontuario(
            consulta_id=consulta.id,
            diagnostico='Exemplo de diagnóstico',
            prescricao='Exemplo de prescrição',
            exames_solicitados='Exemplo de exames'
        )
        db.session.add(prontuario)
        
        # Criar pagamento
        pagamento = Pagamento(
            paciente_id=paciente.id,
            consulta_id=consulta.id,
            valor=150.00,
            status='pendente'
        )
        db.session.add(pagamento)
    
    db.session.commit()

def inicializar_banco():
    """Inicializa o banco de dados com dados padrão"""
    db.create_all()
    criar_usuarios_padrao()
    criar_dados_exemplo() 
from backend.models import Usuario, Paciente, Medico, Consulta, Prontuario, Pagamento
from backend.database import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def banco_ja_inicializado():
    """Verifica se o banco já foi inicializado"""
    return (
        Usuario.query.first() is not None and
        Medico.query.first() is not None and
        Paciente.query.first() is not None
    )

def criar_usuarios_padrao():
    """Cria usuários padrão do sistema se não existirem"""
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
    
    db.session.commit()

def criar_dados_exemplo():
    """Cria dados de exemplo no banco de dados"""
    
    # Criar usuários
    usuarios = [
        Usuario(
            nome='Admin',
            email='admin@medflow.com',
            senha=generate_password_hash('admin123'),
            tipo='admin'
        ),
        Usuario(
            nome='Dr. João Silva',
            email='joao.silva@medflow.com',
            senha=generate_password_hash('medico123'),
            tipo='medico'
        ),
        Usuario(
            nome='Maria Recepcionista',
            email='maria@medflow.com',
            senha=generate_password_hash('recep123'),
            tipo='recepcionista'
        )
    ]
    
    for usuario in usuarios:
        db.session.add(usuario)
    
    db.session.flush()  # Para obter os IDs dos usuários
    
    # Criar médicos
    medicos = [
        Medico(
            nome='Dr. João Silva',
            crm='12345-SP',  # Adicionado CRM
            especialidade='Clínico Geral',
            usuario_id=usuarios[1].id,  # Associar ao usuário médico
            horario_disponivel='08:00-18:00'
        ),
        Medico(
            nome='Dra. Ana Santos',
            crm='54321-SP',  # Adicionado CRM
            especialidade='Pediatra',
            usuario_id=usuarios[1].id,  # Você pode criar outro usuário médico se preferir
            horario_disponivel='09:00-17:00'
        )
    ]
    
    for medico in medicos:
        db.session.add(medico)
    
    db.session.flush()  # Para obter os IDs dos médicos
    
    # Criar pacientes
    pacientes = [
        Paciente(
            nome='Carlos Oliveira',
            telefone='(11) 99999-2222',
            data_nascimento=datetime(1985, 8, 20),
            endereco='Rua B, 456'
        ),
        Paciente(
            nome='Ana Santos',
            telefone='(11) 99999-1111',
            data_nascimento=datetime(1990, 5, 15),
            endereco='Rua A, 123'
        )
    ]
    
    for paciente in pacientes:
        db.session.add(paciente)
    
    db.session.flush()  # Para obter os IDs dos pacientes
    
    # Criar consultas
    hoje = datetime.now()
    consultas = [
        Consulta(
            paciente_id=pacientes[0].id,
            medico_id=medicos[0].id,
            data_hora=hoje + timedelta(days=1, hours=10),
            status='agendada'
        ),
        Consulta(
            paciente_id=pacientes[1].id,
            medico_id=medicos[1].id,
            data_hora=hoje + timedelta(days=2, hours=14),
            status='agendada'
        )
    ]
    
    for consulta in consultas:
        db.session.add(consulta)
    
    # Criar prontuários para consultas realizadas
    consulta_realizada = Consulta(
        paciente_id=pacientes[0].id,
        medico_id=medicos[0].id,
        data_hora=hoje - timedelta(days=5),
        status='realizada'
    )
    db.session.add(consulta_realizada)
    db.session.flush()
    
    prontuario = Prontuario(
        consulta_id=consulta_realizada.id,
        diagnostico='Gripe comum',
        prescricao='Repouso e hidratação',
        exames_solicitados='Hemograma completo'
    )
    db.session.add(prontuario)
    
    try:
        db.session.commit()
        print("Dados de exemplo criados com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar dados de exemplo: {str(e)}")
        raise

def inicializar_banco():
    """Inicializa o banco de dados com dados de exemplo"""
    db.drop_all()  # Limpa o banco existente
    db.create_all()  # Cria as tabelas
    criar_dados_exemplo()  # Popula com dados de exemplo

if __name__ == '__main__':
    inicializar_banco() 
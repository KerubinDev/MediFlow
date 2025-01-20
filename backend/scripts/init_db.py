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
    try:
        print("Iniciando criação de dados de exemplo...")
        
        # Criar usuário médico
        usuario_medico = Usuario(
            nome='Dr. João Silva',
            email='joao.silva@medflow.com',
            senha=generate_password_hash('medico123'),
            tipo='medico'
        )
        db.session.add(usuario_medico)
        db.session.flush()
        print(f"Usuário médico criado com ID: {usuario_medico.id}")
        
        # Criar médico
        medico = Medico(
            nome='Dr. João Silva',
            crm='12345-SP',
            especialidade='Clínico Geral',
            usuario_id=usuario_medico.id,
            horario_disponivel='08:00-18:00'
        )
        db.session.add(medico)
        db.session.flush()
        print(f"Médico criado com ID: {medico.id}")
        
        # Criar paciente
        paciente = Paciente(
            nome='Ana Santos',
            telefone='(11) 99999-1111',
            data_nascimento=datetime(1990, 5, 15),
            endereco='Rua A, 123'
        )
        db.session.add(paciente)
        db.session.flush()
        print(f"Paciente criado com ID: {paciente.id}")
        
        # Criar consulta realizada
        consulta = Consulta(
            paciente_id=paciente.id,
            medico_id=medico.id,
            data_hora=datetime.now() - timedelta(days=1),
            status='realizada'
        )
        db.session.add(consulta)
        db.session.flush()
        print(f"Consulta criada com ID: {consulta.id}")
        
        # Criar prontuário
        prontuario = Prontuario(
            consulta_id=consulta.id,
            diagnostico='Gripe comum',
            prescricao='Repouso e hidratação',
            exames_solicitados='Hemograma completo'
        )
        db.session.add(prontuario)
        db.session.flush()
        print(f"Prontuário criado com ID: {prontuario.id}")
        
        # Commit final
        db.session.commit()
        print("Dados de exemplo criados com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar dados de exemplo: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def inicializar_banco():
    """Inicializa o banco de dados com dados de exemplo"""
    print("Iniciando inicialização do banco...")
    db.drop_all()
    print("Tabelas antigas removidas")
    db.create_all()
    print("Novas tabelas criadas")
    criar_dados_exemplo()

if __name__ == '__main__':
    inicializar_banco() 
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

def limpar_banco():
    """Limpa todas as tabelas do banco de dados"""
    try:
        Pagamento.query.delete()
        Prontuario.query.delete()
        Consulta.query.delete()
        Medico.query.delete()
        Paciente.query.delete()
        Usuario.query.delete()
        db.session.commit()
        print("Banco de dados limpo com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao limpar banco: {str(e)}")
        raise

def inicializar_banco():
    """
    Inicializa o banco de dados com usuários padrão e dados de exemplo.
    """
    try:
        # Cria as tabelas se não existirem
        db.create_all()
        
        # Limpa os dados existentes
        limpar_banco()

        # Lista de usuários padrão
        usuarios_padrao = [
            {
                'nome': 'Administrador',
                'email': 'admin@medflow.com',
                'senha': 'admin123',
                'tipo': 'admin'
            },
            {
                'nome': 'Dr. Silva',
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

        # Adiciona cada usuário
        usuarios_criados = {}
        for usuario in usuarios_padrao:
            novo_usuario = Usuario(
                nome=usuario['nome'],
                email=usuario['email'],
                tipo=usuario['tipo']
            )
            novo_usuario.set_senha(usuario['senha'])
            db.session.add(novo_usuario)
            db.session.flush()
            usuarios_criados[usuario['email']] = novo_usuario
            print(f"Usuário criado: {usuario['email']}")

        # Criar médicos de exemplo
        medicos_exemplo = [
            {
                'nome': 'Dr. Silva',
                'crm': '12345-SP',
                'especialidade': 'Clínico Geral',
                'horario_disponivel': '08:00-18:00',
                'email_usuario': 'medico@medflow.com'
            },
            {
                'nome': 'Dra. Santos',
                'crm': '54321-SP',
                'especialidade': 'Pediatra',
                'horario_disponivel': '09:00-17:00',
                'email_usuario': 'medico@medflow.com'
            }
        ]

        medicos_criados = []
        for med in medicos_exemplo:
            usuario = usuarios_criados.get(med['email_usuario'])
            if usuario:
                medico = Medico(
                    nome=med['nome'],
                    crm=med['crm'],
                    especialidade=med['especialidade'],
                    horario_disponivel=med['horario_disponivel'],
                    usuario_id=usuario.id
                )
                db.session.add(medico)
                db.session.flush()
                medicos_criados.append(medico)
                print(f"Médico criado: {med['nome']}")

        # Criar pacientes de exemplo
        pacientes_exemplo = [
            {
                'nome': 'João da Silva',
                'telefone': '(11) 99999-1111',
                'data_nascimento': datetime(1990, 5, 15),
                'endereco': 'Rua das Flores, 123'
            },
            {
                'nome': 'Maria Oliveira',
                'telefone': '(11) 99999-2222',
                'data_nascimento': datetime(1985, 8, 20),
                'endereco': 'Av. Principal, 456'
            }
        ]

        pacientes_criados = []
        for pac in pacientes_exemplo:
            paciente = Paciente(**pac)
            db.session.add(paciente)
            db.session.flush()
            pacientes_criados.append(paciente)
            print(f"Paciente criado: {pac['nome']}")

        # Criar consultas e prontuários de exemplo
        for i, paciente in enumerate(pacientes_criados):
            for medico in medicos_criados:
                # Consulta passada
                data_passada = datetime.now() - timedelta(days=i+1)
                consulta_passada = Consulta(
                    paciente_id=paciente.id,
                    medico_id=medico.id,
                    data_hora=data_passada,
                    status='realizada'
                )
                db.session.add(consulta_passada)
                db.session.flush()

                # Prontuário para consulta passada
                prontuario = Prontuario(
                    consulta_id=consulta_passada.id,
                    diagnostico=f'Diagnóstico de exemplo {i+1}',
                    prescricao='Medicamento A, Medicamento B',
                    exames_solicitados='Hemograma, Raio-X',
                    data_criacao=data_passada
                )
                db.session.add(prontuario)

                # Pagamento para consulta passada
                pagamento = Pagamento(
                    consulta_id=consulta_passada.id,
                    valor=150.00,
                    status='pago',
                    data_pagamento=data_passada
                )
                db.session.add(pagamento)

                # Consulta futura
                consulta_futura = Consulta(
                    paciente_id=paciente.id,
                    medico_id=medico.id,
                    data_hora=datetime.now() + timedelta(days=i+1),
                    status='agendada'
                )
                db.session.add(consulta_futura)
                print(f"Consultas criadas para {paciente.nome} com Dr(a). {medico.nome}")

        # Commit final
        db.session.commit()
        print("\nBanco de dados inicializado com sucesso!")
        print("\nDados criados:")
        print(f"- {len(usuarios_padrao)} usuários")
        print(f"- {len(medicos_criados)} médicos")
        print(f"- {len(pacientes_criados)} pacientes")
        print(f"- {len(pacientes_criados) * len(medicos_criados) * 2} consultas")
        print(f"- {len(pacientes_criados) * len(medicos_criados)} prontuários")
        print(f"- {len(pacientes_criados) * len(medicos_criados)} pagamentos")

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao inicializar o banco de dados: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    inicializar_banco() 
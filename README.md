# MediFlow

<div align="center">
  <h1>MediFlow</h1>
  <p>Sistema de Gestão para Clínicas Médicas</p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/License-GPL%20v3-blue.svg" alt="License">
    <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask Version">
  </p>
</div>

## 📋 Sobre

MediFlow é um sistema web completo para gestão de clínicas médicas, desenvolvido com Flask e SQLAlchemy. O sistema oferece funcionalidades para gerenciamento de consultas, prontuários eletrônicos, pacientes e usuários, com foco em usabilidade e segurança.

## 🚀 Funcionalidades

- **Gestão de Consultas**
  - Agendamento e reagendamento
  - Confirmação de presença
  - Cancelamento
  - Histórico completo
  - Status de consulta em tempo real

- **Prontuário Eletrônico**
  - Registro de diagnósticos
  - Prescrições médicas
  - Solicitação de exames
  - Impressão de prontuários
  - Histórico médico completo

- **Gestão de Pacientes**
  - Cadastro completo
  - Histórico médico
  - Busca avançada
  - Atualização de dados
  - Visualização de consultas anteriores

- **Controle de Usuários**
  - Níveis de acesso (Admin, Médico, Recepcionista)
  - Gerenciamento de permissões
  - Segurança e autenticação
  - Logs de atividades

## 🛠️ Tecnologias

- **Backend**
  - Python 3.8+
  - Flask (Framework Web)
  - SQLAlchemy (ORM)
  - Flask-Login (Autenticação)
  - Werkzeug (Segurança)

- **Frontend**
  - Bootstrap 5 (Framework CSS)
  - JavaScript
  - HTML5/CSS3
  - Fetch API

- **Banco de Dados**
  - SQLite

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/KerubinDev/MediFlow.git
cd MediFlow
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute o sistema:
```bash
python run.py
```

## 🔑 Credenciais Padrão

Após iniciar o sistema, você terá acesso aos seguintes usuários:

**Admin:**
- Email: admin@medflow.com
- Senha: admin123

**Médico:**
- Email: medico@medflow.com
- Senha: medico123

**Recepcionista:**
- Email: recepcao@medflow.com
- Senha: recepcao123

## 🔒 Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure as seguintes variáveis:

- `FLASK_APP`: Nome do aplicativo Flask
- `FLASK_ENV`: Ambiente (development/production)
- `SECRET_KEY`: Chave secreta para sessões
- `DATABASE_URL`: URL do banco de dados

## 📁 Estrutura do Projeto

```
mediflow/
├── backend/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── app.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

## 👥 Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença GNU GPL v3. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Kelvin Moraes**
- Email: kelvin.moraes117@gmail.com
- GitHub: [@KerubinDev](https://github.com/KerubinDev)

---
<div align="center">
  <sub>Built with ❤️ by Kelvin Moraes</sub>
</div>
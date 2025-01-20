"""
MediFlow - Sistema de Gestão para Clínicas Médicas
Desenvolvido por Kelvin Moraes (@KerubinDev)
GitHub: https://github.com/KerubinDev
Email: kelvin.moraes117@gmail.com
"""

from backend.app import criar_app
from backend.scripts.init_db import inicializar_banco
import os
from colorama import init, Fore, Style

# Inicializa o colorama para cores no terminal
init()

app = criar_app()

# Inicializa o banco de dados com dados de exemplo
with app.app_context():
    inicializar_banco()
    
    # Mostra os logins disponíveis
    print("\n=== Logins Disponíveis ===")
    print("\nAdmin Geral:")
    print("Email: admin@medflow.com")
    print("Senha: admin123")
    
    print("\nMédico:")
    print("Email: medico@medflow.com")
    print("Senha: medico123")
    
    print("\nRecepcionista:")
    print("Email: recepcao@medflow.com")
    print("Senha: recepcao123")
    
    print("\nServidor iniciando...\n")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 
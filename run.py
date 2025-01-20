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
    print(f"\n{Fore.GREEN}=== Logins Disponíveis ==={Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Admin Geral:{Style.RESET_ALL}")
    print("Email: admin@medflow.com")
    print("Senha: admin123")
    
    print(f"\n{Fore.YELLOW}Médico:{Style.RESET_ALL}")
    print("Email: medico@medflow.com")
    print("Senha: medico123")
    
    print(f"\n{Fore.YELLOW}Recepcionista:{Style.RESET_ALL}")
    print("Email: recepcao@medflow.com")
    print("Senha: recepcao123")
    
    print(f"\n{Fore.GREEN}Servidor iniciando...{Style.RESET_ALL}\n")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 
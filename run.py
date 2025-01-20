from backend.app import criar_app
from backend.scripts.init_db import inicializar_banco
import os

app = criar_app()

# Inicializa o banco de dados com dados de exemplo
with app.app_context():
    inicializar_banco()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 
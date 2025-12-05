import os
import sys

# Garante que o diretório corrente (onde está wsgi.py) esteja no sys.path
sys.path.append(os.path.dirname(__file__))

# Importa a fábrica de app e cria uma instância
try:
	from app import create_app
except Exception:
	# Tenta importar como pacote absoluto se o caminho acima falhar
	from transporte.app import create_app

# Cria a instância da aplicação e expõe a variável WSGI esperada
app = create_app()
application = app

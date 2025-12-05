import os
import sys

# Garante que o diretório corrente (onde está wsgi.py) esteja no sys.path
sys.path.append(os.path.dirname(__file__))

# Importa o objeto Flask 'app' do seu módulo principal
from app import app

# Alguns provedores esperam a variável 'application'
application = app

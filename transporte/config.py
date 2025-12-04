# logistica_app/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

class Config:
    # Supabase Connection Details (Usar variáveis de ambiente!)
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY_ANON = os.environ.get("SUPABASE_KEY_ANON", "")
    SUPABASE_KEY_SERVICE_ROLE = os.environ.get("SUPABASE_KEY_SERVICE_ROLE", "")

    # Configuração do banco NoSQL (ex: MongoDB, S3 para storage, etc.)
    NOSQL_STORAGE_URL = os.environ.get("NOSQL_STORAGE_URL", "")

    # Outras configurações do Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
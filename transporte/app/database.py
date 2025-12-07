# logistica_app/app/database.py

from supabase import create_client, Client
from flask import current_app, g

def get_supabase_client() -> Client:
    """Obtém e armazena o cliente Supabase no contexto da aplicação (g)."""
    if 'supabase_client' not in g:
        # Usa as configurações carregadas do app/config.py
        url: str = current_app.config["SUPABASE_URL"]
        key: str = current_app.config["SUPABASE_KEY_ANON"] # Usamos ANON para a maioria das operações de front-end
        
        # O cliente 'service_role' é para operações de back-end mais sensíveis (ex: criação de usuário, deleção)
        # O ideal é usar o key Anon + RLS (Row Level Security) do Supabase.
        g.supabase_client = create_client(url, key)
    
    return g.supabase_client

# Função para inicializar o cliente no contexto da aplicação Flask
def init_app(app):
    # Aqui podemos adicionar funções para fechar a conexão no final do request, se usarmos um pool mais tradicional.
    pass


def get_safe_supabase_client() -> Client:
    """Compatibilidade: função auxiliar usada em várias partes do código.
    Retorna o cliente Supabase, mas encapsula erros comuns e fornece uma mensagem
    de erro mais clara caso as configurações não estejam presentes.
    """
    try:
        return get_supabase_client()
    except Exception as e:
        # Relevante durante import-time se current_app não estiver disponível
        raise RuntimeError(f"Não foi possível inicializar o cliente Supabase: {e}")
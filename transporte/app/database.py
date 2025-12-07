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
    Retorna o cliente Supabase, mas faz checagens explícitas nas configurações
    para fornecer mensagens de erro claras quando variáveis de ambiente
    estiverem faltando ou o contexto da app não estiver disponível.
    """
    # Verifica se as configurações básicas estão presentes para dar mensagens claras
    try:
        url = current_app.config.get('SUPABASE_URL', '')
        anon = current_app.config.get('SUPABASE_KEY_ANON', '')
    except RuntimeError:
        # current_app not available
        raise RuntimeError('Supabase não inicializado: `current_app` não disponível no contexto atual.')

    if not url:
        raise RuntimeError('Variável de ambiente SUPABASE_URL não encontrada. Defina SUPABASE_URL.')
    if not anon:
        raise RuntimeError('Variável de ambiente SUPABASE_KEY_ANON não encontrada. Defina SUPABASE_KEY_ANON (ou SUPABASE_KEY_SERVICE_ROLE para operações de teste).')

    try:
        return get_supabase_client()
    except Exception as e:
        raise RuntimeError(f"Não foi possível inicializar o cliente Supabase: {e}")
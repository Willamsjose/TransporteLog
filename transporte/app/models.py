# logistica_app/app/models.py

from flask_login import UserMixin
from .database import get_supabase_client
from typing import Optional, Dict, Any

class User(UserMixin):
    """
    Modelo de Usuário para integração com Flask-Login, baseado na tabela 'Usuario'.
    """
    def __init__(self, id_usuario: str, id_empresa: str, email: str, nome: str, cargo: str, senha_hash: Optional[str] = None):
        # 'id' é obrigatório para o UserMixin
        self.id = id_usuario
        self.id_empresa = id_empresa
        self.email = email
        self.nome = nome
        self.cargo = cargo
        self.senha_hash = senha_hash
        
    @staticmethod
    def _create_user_from_data(user_data: Dict[str, Any]) -> 'User':
        """Função auxiliar para criar um objeto User a partir dos dados do Supabase."""
        return User(
            id_usuario=user_data.get('id'),
            id_empresa=user_data.get('id_empresa'),
            email=user_data.get('email'),
            nome=user_data.get('nome'),
            cargo=user_data.get('cargo'),
            senha_hash=user_data.get('senha_hash')
        )

    @staticmethod
    def get(user_id: str) -> Optional['User']:
        """Busca um usuário pelo ID (usado pelo Flask-Login para recarregar a sessão)."""
        supabase = get_supabase_client()
        # Busca o usuário pelo ID
        response = supabase.table('Usuario').select('*').eq('id', user_id).limit(1).execute()

        if response.data:
            return User._create_user_from_data(response.data[0])
        return None

    @staticmethod
    def get_by_email(email: str) -> Optional['User']:
        """Busca um usuário pelo email (usado no login para autenticação)."""
        supabase = get_supabase_client()
        # Busca o usuário pelo email
        response = supabase.table('Usuario').select('*').eq('email', email).limit(1).execute()

        if response.data:
            return User._create_user_from_data(response.data[0])
        return None
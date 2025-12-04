# logistica_app/app/utils/data_access.py (Novo Arquivo)

from ..database import get_supabase_client
from flask_login import current_user # Acesso ao usuário logado
from typing import List, Dict, Any
from typing import List, Dict, Any, Tuple

# Esta função DEVE ser chamada APÓS o login
def get_safe_supabase_client():
    """Retorna o cliente Supabase, garantindo que o usuário está logado."""
    if not current_user.is_authenticated:
        # Em um cenário real, você levantaria uma exceção aqui
        raise PermissionError("Usuário não autenticado. Acesso negado.")
    
    # Retorna o cliente ANON, confiando que o RLS está implementado (ou que o Flask vai filtrar)
    return get_supabase_client()


def get_veiculos_por_empresa() -> List[Dict[str, Any]]:
    """Busca todos os veículos APENAS da empresa logada."""
    supabase = get_safe_supabase_client()
    id_empresa = current_user.id_empresa # Chave de segurança!
    
    try:
        # Filtra rigorosamente pelo ID da empresa logada
        response = supabase.table('Veiculo').select('*').eq('id_empresa', id_empresa).execute()
        
        # O Supabase retorna a lista de dados na chave 'data'
        return response.data
    except Exception as e:
        print(f"Erro ao buscar veículos: {e}")
        return []

# Exemplo de Inserção Segura
def add_abastecimento(dados_abastecimento: Dict[str, Any]) -> bool:
    """Insere um novo registro de abastecimento para a empresa logada."""
    supabase = get_safe_supabase_client()
    
    # Injeta a chave de segurança ID_EMPRESA no dicionário de dados
    dados_abastecimento['id_empresa'] = current_user.id_empresa 
    
    try:
        supabase.table('Abastecimento').insert([dados_abastecimento]).execute()
        return True
    except Exception as e:
        print(f"Erro ao inserir abastecimento: {e}")
        return False
    
def get_vehicles_for_select() -> List[Tuple[str, str]]:
    """Busca veículos da empresa logada no formato (id, placa - modelo) para SelectField."""
    supabase = get_safe_supabase_client()
    id_empresa = current_user.id_empresa
    choices = [('', 'Selecione o Veículo...')]

    try:
        response = supabase.table('Veiculo').select('id, placa, modelo').eq('id_empresa', id_empresa).execute()
        
        # Cria tuplas (valor, label)
        for v in response.data:
            choices.append((str(v['id']), f"{v['placa']} - {v['modelo']}"))
            
    except Exception as e:
        print(f"Erro ao buscar veículos para o formulário: {e}")
        
    return choices

def get_last_km(vehicle_id: int) -> int:
    """Busca a última KM registrada para um veículo específico."""
    supabase = get_safe_supabase_client()
    id_empresa = current_user.id_empresa
    
    # Tenta buscar o último KM de Abastecimento (prioridade)
    try:
        response = supabase.table('Abastecimento').select('km_registro').eq('id_empresa', id_empresa).eq('id_veiculo', vehicle_id).order('data_abastecimento', desc=True).limit(1).execute()
        if response.data:
            return response.data[0]['km_registro']
    except Exception as e:
        print(f"Erro ao buscar último KM de abastecimento: {e}")
        
    # Se falhar, busca o KM atual na tabela Veiculo
    try:
        response = supabase.table('Veiculo').select('km_atual').eq('id_empresa', id_empresa).eq('id', vehicle_id).limit(1).execute()
        if response.data:
            return response.data[0]['km_atual']
    except Exception as e:
        print(f"Erro ao buscar KM do veículo: {e}")
        
    return 0
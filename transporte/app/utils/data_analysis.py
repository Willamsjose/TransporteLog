# logistica_app/app/utils/data_analysis.py (Novo Arquivo)

from ..database import get_safe_supabase_client
from flask_login import current_user
from typing import List, Dict, Any, Union

def get_fueling_costs_summary() -> Dict[str, Any]:
    """
    Calcula o custo total de abastecimento por veículo e na frota.
    Retorna também a média de Km/L por veículo.
    """
    supabase = get_safe_supabase_client()
    id_empresa = current_user.id_empresa
    
    # 1. Obter todos os abastecimentos e veículos da empresa
    # O Supabase permite fazer JOINs simples com a sintaxe 'select(*, tabela_externa(*))'
    try:
        # Busca Abastecimentos e dados do Veículo relacionados
        response = supabase.table('Abastecimento').select(
            'litros, valor_litro, km_registro, id_veiculo, Veiculo(placa, km_atual)'
        ).eq('id_empresa', id_empresa).order('id_veiculo', desc=False).order('km_registro', desc=False).execute()
        
        fueling_data = response.data
    except Exception as e:
        print(f"Erro ao buscar dados de abastecimento: {e}")
        return {"total_frota": 0.00, "veiculos": {}}

    # 2. Processamento e Agregação em Python (Melhor que SQL para cálculos complexos)
    
    veiculos_summary: Dict[str, Dict[str, Union[float, int, List[Dict]]]] = {}
    custo_total_frota = 0.0
    
    for item in fueling_data:
        # Key: ID do Veículo
        vehicle_id = str(item['id_veiculo'])
        
        if vehicle_id not in veiculos_summary:
            # Inicializa a estrutura do veículo
            veiculos_summary[vehicle_id] = {
                "placa": item['Veiculo']['placa'],
                "custo_total": 0.0,
                "total_litros": 0.0,
                "consumo_km_l": [], # Para armazenar os Km/L e calcular a média
                "registros": []     # Para guardar a ordem e KM
            }
        
        # Custo do abastecimento atual
        custo_abastecimento = float(item['litros'] * item['valor_litro'])
        
        # Acumula totais
        veiculos_summary[vehicle_id]['custo_total'] += custo_abastecimento
        veiculos_summary[vehicle_id]['total_litros'] += float(item['litros'])
        custo_total_frota += custo_abastecimento
        
        # Armazena registro para cálculo de Km/L posterior (em ordem reversa para processamento)
        veiculos_summary[vehicle_id]['registros'].insert(0, {
            'km': item['km_registro'],
            'litros': float(item['litros'])
        })

    # 3. Cálculo de Consumo (Km/L)
    for vehicle_id, summary in veiculos_summary.items():
        registros = summary['registros']
        km_l_list = []
        
        # Itera sobre os registros, exceto o primeiro (que não tem anterior)
        for i in range(1, len(registros)):
            current = registros[i]
            previous = registros[i-1]
            
            # Condição para cálculo de Km/L (Deve ser tanque cheio no registro anterior)
            # Como não salvamos a informação de 'tanque cheio' no BD, assumiremos para este cálculo
            # que a diferença entre KMs representa a distância percorrida no último abastecimento.
            
            distancia = current['km'] - previous['km']
            litros = current['litros']
            
            if distancia > 0 and litros > 0:
                km_l = round(distancia / litros, 2)
                km_l_list.append(km_l)
                
        # Calcula a média de Km/L
        summary['media_km_l'] = round(sum(km_l_list) / len(km_l_list), 2) if km_l_list else 0.0
        
        # Remove registros internos
        del summary['registros']
        del summary['consumo_km_l']
        
    return {
        "total_frota": round(custo_total_frota, 2),
        "veiculos": veiculos_summary
    }

def get_maintenance_costs_summary() -> Dict[str, Any]:
    """
    Calcula o custo total de manutenção por veículo e na frota.
    """
    supabase = get_safe_supabase_client()
    id_empresa = current_user.id_empresa
    
    try:
        # Busca todas as manutenções realizadas e seus custos
        response = supabase.table('Manutencao_Realizada').select(
            'custo_total, id_veiculo, Veiculo(placa)'
        ).eq('id_empresa', id_empresa).execute()
        
        maintenance_data = response.data
    except Exception as e:
        print(f"Erro ao buscar dados de manutenção: {e}")
        return {"total_frota": 0.00, "veiculos": {}}

    veiculos_summary: Dict[str, Dict[str, float]] = {}
    custo_total_frota = 0.0
    
    for item in maintenance_data:
        vehicle_id = str(item['id_veiculo'])
        custo = float(item['custo_total'])
        
        if vehicle_id not in veiculos_summary:
            veiculos_summary[vehicle_id] = {
                "placa": item['Veiculo']['placa'],
                "custo_total": 0.0,
                "num_manutencoes": 0
            }
        
        veiculos_summary[vehicle_id]['custo_total'] += custo
        veiculos_summary[vehicle_id]['num_manutencoes'] += 1
        custo_total_frota += custo
        
    return {
        "total_frota": round(custo_total_frota, 2),
        "veiculos": veiculos_summary
    }
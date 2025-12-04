# logistica_app/app/blueprints/dashboard/routes.py

from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required
# Importa as novas funções de análise
from ...utils.data_analysis import get_fueling_costs_summary, get_maintenance_costs_summary
from ...utils.data_access import get_safe_supabase_client # Para alertas (opcional)
from ..Maintenance.routes import check_maintenance_alerts # Reutiliza a função de alertas

# Define o Blueprint 'dashboard'
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def main_dashboard():
    
    # 1. Custo de Abastecimento
    fueling_summary = get_fueling_costs_summary()
    
    # 2. Custo de Manutenção
    maintenance_summary = get_maintenance_costs_summary()
    
    # 3. Alertas de Manutenção (Reutilizando a função)
    supabase = get_safe_supabase_client()
    alerts = check_maintenance_alerts(current_user.id_empresa, supabase)
    
    if alerts:
        flash(f"⚠️ **ATENÇÃO:** Você tem {len(alerts)} manutenções que precisam de sua atenção!", 'warning')
        
    # 4. Cálculo do Custo Total da Frota
    custo_total_geral = fueling_summary['total_frota'] + maintenance_summary['total_frota']
    
    # 5. Mesclar dados por veículo para exibição unificada
    # Cria uma lista de veículos únicos para exibição
    veiculos_data = {}
    for vid, data in fueling_summary['veiculos'].items():
        veiculos_data[vid] = {
            "placa": data['placa'],
            "custo_abastecimento": round(data['custo_total'], 2),
            "media_km_l": data['media_km_l'],
            "custo_manutencao": 0.00
        }
        
    for vid, data in maintenance_summary['veiculos'].items():
        if vid in veiculos_data:
            veiculos_data[vid]['custo_manutencao'] = round(data['custo_total'], 2)
        else:
             # Caso um veículo tenha só manutenção e não abastecimento
             veiculos_data[vid] = {
                "placa": data['placa'],
                "custo_abastecimento": 0.00,
                "media_km_l": 0.00,
                "custo_manutencao": round(data['custo_total'], 2)
            }


    return render_template('main_dashboard.html', 
                           title='Dashboard de Custos Logísticos',
                           fueling_summary=fueling_summary,
                           maintenance_summary=maintenance_summary,
                           custo_total_geral=round(custo_total_geral, 2),
                           veiculos_data=veiculos_data.values(),
                           alerts=alerts)
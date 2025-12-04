from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import date, timedelta, datetime
from .forms import PredictiveMaintenanceForm, RealizedMaintenanceForm
from ...utils.data_access import get_safe_supabase_client, get_vehicles_for_select, get_last_km

# Define o Blueprint 'maintenance'
maintenance_bp = Blueprint('maintenance', __name__, template_folder='templates', url_prefix='/manutencao')

# -----------------
# FUNÇÃO AUXILIAR: VERIFICA ALERTAS PREDITIVOS
# -----------------
def check_maintenance_alerts(id_empresa: str, supabase):
    """Verifica e retorna manutenções agendadas que estão perto de vencer por KM ou Data."""
    
    # 1. Busca todas as manutenções Preditivas AGENDADAS
    response = supabase.table('Manutencao_Preditiva').select(
        '*, Veiculo(placa, km_atual)' 
    ).eq('id_empresa', id_empresa).eq('status', 'Agendada').execute()
    
    alerts = []
    today = date.today()

    for item in response.data:
        veiculo_km_atual = item['Veiculo']['km_atual']
        intervalo_alerta = item['intervalo_alerta']
        
        # Alerta por KM
        if item['km_agendado'] and item['km_agendado'] > 0:
            km_restante = item['km_agendado'] - veiculo_km_atual
            
            if km_restante <= intervalo_alerta:
                alerts.append({
                    'type': 'km',
                    'id': item['id'],
                    'descricao': item['descricao'],
                    'veiculo': item['Veiculo']['placa'],
                    'urgency': f"{km_restante} KM restantes (Alerta: {intervalo_alerta} KM)"
                })
        
        # Alerta por Data
        if item['data_agendada']:
            data_agendada = date.fromisoformat(item['data_agendada'])
            dias_restantes = (data_agendada - today).days
            
            if dias_restantes <= intervalo_alerta and dias_restantes >= 0:
                alerts.append({
                    'type': 'data',
                    'id': item['id'],
                    'descricao': item['descricao'],
                    'veiculo': item['Veiculo']['placa'],
                    'urgency': f"{dias_restantes} dias restantes (Alerta: {intervalo_alerta} dias)"
                })

    return alerts

# -----------------
# ROTA PRINCIPAL (EXIBE ALERTAS)
# -----------------
@maintenance_bp.route('/')
@login_required
def index():
    supabase = get_safe_supabase_client()
    alerts = check_maintenance_alerts(current_user.id_empresa, supabase)
    
    if alerts:
        flash(f"⚠️ **ATENÇÃO:** Você tem {len(alerts)} manutenções que precisam ser revisadas!", 'warning')
    
    # Você pode buscar a lista de todos os agendamentos aqui também, se desejar.
    
    return render_template('maintenance_index.html', 
                           title='Gestão de Manutenção', 
                           alerts=alerts)

# -----------------
# 1. ROTA DE AGENDAMENTO PREDITIVO
# -----------------
@maintenance_bp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_maintenance():
    form = PredictiveMaintenanceForm()
    form.id_veiculo.choices = get_vehicles_for_select()
    
    if form.validate_on_submit():
        supabase = get_safe_supabase_client()
        
        # Validação: Pelo menos KM ou Data deve ser fornecido (Opcional no form, mas necessário aqui)
        if not form.km_agendado.data and not form.data_agendada.data:
            flash("É necessário agendar por KM ou por Data.", 'danger')
            return render_template('schedule_maintenance.html', form=form)

        schedule_data = {
            "id_empresa": current_user.id_empresa,
            "id_veiculo": form.id_veiculo.data,
            "descricao": form.descricao.data,
            "tipo_manutencao": form.tipo_manutencao.data,
            "km_agendado": form.km_agendado.data or None,
            "data_agendada": form.data_agendada.data.isoformat() if form.data_agendada.data else None,
            "intervalo_alerta": form.intervalo_alerta.data,
            "status": "Agendada"
        }
        
        try:
            supabase.table('Manutencao_Preditiva').insert(schedule_data).execute()
            flash('Manutenção agendada com sucesso! Os alertas serão gerados automaticamente.', 'success')
            return redirect(url_for('maintenance.index'))
        except Exception as e:
            flash(f'Erro ao agendar manutenção: {e.args[0] if e.args else str(e)}', 'danger')

    return render_template('schedule_maintenance.html', title='Agendar Manutenção Preditiva', form=form)

# -----------------
# 2. ROTA DE REGISTRO DE MANUTENÇÃO REALIZADA
# -----------------
@maintenance_bp.route('/perform', methods=['GET', 'POST'])
@login_required
def perform_maintenance():
    form = RealizedMaintenanceForm()
    form.id_veiculo.choices = get_vehicles_for_select()
    
    # Tenta pegar um id de agendamento na query (se veio de um alerta)
    id_preditivo = request.args.get('preditivo', type=int) 
    
    if form.validate_on_submit():
        supabase = get_safe_supabase_client()
        
        # 1. UPLOAD DA NOTA FISCAL (Simulação do Storage)
        url_nota_fiscal = None
        file = request.files.get('nota_fiscal_file')
        
        if file and file.filename:
            file_name = f"nf_manutencao_{current_user.id_empresa}_{form.id_veiculo.data}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            url_nota_fiscal = f"/storage/notas_manutencao/{file_name}.{file.filename.split('.')[-1]}"
            flash("O upload da nota fiscal de manutenção foi simulado. A URL será salva no BD.", 'warning')

        # 2. PREPARAÇÃO DOS DADOS
        maintenance_data = {
            "id_empresa": current_user.id_empresa,
            "id_veiculo": form.id_veiculo.data,
            "id_manutencao_preditiva": id_preditivo, # Salva o ID do agendamento, se houver
            "data_realizacao": form.data_realizacao.data.isoformat(),
            "descricao_servico": form.descricao_servico.data,
            "custo_total": form.custo_total.data,
            "oficina_responsavel": form.oficina_responsavel.data,
            "id_usuario_registro": current_user.id,
            "url_nota_fiscal": url_nota_fiscal
        }
        
        try:
            # Insere o registro de manutenção realizada
            supabase.table('Manutencao_Realizada').insert(maintenance_data).execute()
            
            # 3. ATUALIZA STATUS DO AGENDAMENTO (Se for o caso)
            if id_preditivo:
                supabase.table('Manutencao_Preditiva').update({'status': 'Realizada'}).eq('id', id_preditivo).execute()
                flash('Manutenção realizada e agendamento preditivo atualizado!', 'success')
            else:
                flash('Manutenção avulsa registrada com sucesso!', 'success')
                
            return redirect(url_for('maintenance.index'))

        except Exception as e:
            flash(f'Erro ao registrar manutenção: {e.args[0] if e.args else str(e)}', 'danger')

    return render_template('perform_maintenance.html', title='Registrar Manutenção Realizada', form=form, id_preditivo=id_preditivo)
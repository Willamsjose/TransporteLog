# logistica_app/app/blueprints/fueling/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from .forms import FuelingForm
from ...utils.data_access import get_safe_supabase_client, get_vehicles_for_select, get_last_km

# Define o Blueprint 'fueling'
fueling_bp = Blueprint('fueling', __name__, template_folder='templates', url_prefix='/abastecimento')

# -----------------
# FUNÇÃO DE CÁLCULO DE CONSUMO
# -----------------
def calculate_consumption(current_km: int, previous_km: int, liters: float) -> float:
    """Calcula o consumo Km/L."""
    if previous_km >= current_km or liters <= 0:
        return 0.0
    distance = current_km - previous_km
    return round(distance / liters, 2)

# -----------------
# ROTA DE CADASTRO DE ABASTECIMENTO
# -----------------
@fueling_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_fueling():
    form = FuelingForm()
    
    # Popula o SelectField de Veículos dinamicamente
    form.id_veiculo.choices = get_vehicles_for_select()
    
    if form.validate_on_submit():
        supabase = get_safe_supabase_client()
        
        vehicle_id = form.id_veiculo.data
        current_km = form.km_registro.data
        liters = form.litros.data
        
        # 1. VALIDAÇÃO DE KM E OBTENÇÃO DO REGISTRO ANTERIOR
        previous_km = get_last_km(vehicle_id)
        
        if current_km <= previous_km:
            flash(f"A KM ({current_km}) deve ser maior que a última KM registrada ({previous_km}).", 'danger')
            return render_template('register_fueling.html', title='Registrar Abastecimento', form=form)

        # 2. CÁLCULO DE CONSUMO (Só se for Tanque Cheio)
        calculated_consumption = None
        if form.is_tanque_cheio.data == 'True':
            calculated_consumption = calculate_consumption(current_km, previous_km, liters)
            if calculated_consumption > 0:
                flash(f"Consumo calculado desde o último registro: **{calculated_consumption} Km/L**.", 'info')

        # 3. UPLOAD DA NOTA FISCAL (Integração NoSQL/Storage Simulada)
        url_nota_fiscal = None
        file = request.files.get('nota_fiscal_file')
        
        if file and file.filename:
            # Em produção, este é o ponto onde você chamaria o Supabase Storage SDK
            # para fazer o upload e obter a URL segura.
            file_name = f"nf_{current_user.id_empresa}_{vehicle_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            url_nota_fiscal = f"/storage/notas_abastecimento/{file_name}.{file.filename.split('.')[-1]}"
            flash("O upload da nota fiscal foi simulado. A URL será salva no BD.", 'warning')


        # 4. PREPARAÇÃO E INSERÇÃO NO BANCO DE DADOS
        abastecimento_data = {
            "id_empresa": current_user.id_empresa, # RLS KEY
            "id_veiculo": vehicle_id,
            "data_abastecimento": form.data_abastecimento.data.strftime('%Y-%m-%d %H:%M:%S%z'),
            "litros": liters,
            "valor_litro": form.valor_litro.data,
            "km_registro": current_km,
            "local_abastecimento": form.local_abastecimento.data,
            "id_usuario_registro": current_user.id,
            "url_nota_fiscal": url_nota_fiscal, # URL para o Storage
        }
        
        try:
            # Inserção na tabela Abastecimento
            supabase.table('Abastecimento').insert(abastecimento_data).execute()
            
            # Atualiza a KM atual do veículo na tabela Veiculo
            supabase.table('Veiculo').update({'km_atual': current_km}).eq('id', vehicle_id).execute()
            
            flash('Abastecimento registrado e KM do veículo atualizada com sucesso!', 'success')
            return redirect(url_for('fueling.register_fueling'))

        except Exception as e:
            flash(f'Erro ao registrar abastecimento: {e.args[0] if e.args else str(e)}', 'danger')

    return render_template('register_fueling.html', 
                           title='Registrar Abastecimento', 
                           form=form,
                           previous_km=previous_km if 'previous_km' in locals() else 0)
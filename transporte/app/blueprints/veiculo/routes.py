# logistica_app/app/blueprints/vehicle/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import VehicleForm
from ...utils.data_access import get_safe_supabase_client

# Define o Blueprint 'vehicle'
vehicle_bp = Blueprint('vehicle', __name__, template_folder='templates', url_prefix='/veiculos')

# -----------------
# 1. CADASTRO DE VEÍCULO
# -----------------
@vehicle_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_vehicle():
    form = VehicleForm()
    
    if form.validate_on_submit():
        supabase = get_safe_supabase_client()
        
        # Coleta os dados do formulário
        vehicle_data = {
            "id_empresa": current_user.id_empresa, # CHAVE DE SEGURANÇA MULTI-EMPRESA
            "placa": form.placa.data.upper(),
            "marca": form.marca.data,
            "modelo": form.modelo.data,
            "ano": form.ano.data,
            "tipo_combustivel": form.tipo_combustivel.data,
            "km_atual": form.km_atual.data,
        }
        
        try:
            # Insere os dados na tabela Veiculo
            supabase.table('Veiculo').insert(vehicle_data).execute()
            
            flash('Veículo cadastrado com sucesso!', 'success')
            return redirect(url_for('vehicle.list_vehicles'))

        except Exception as e:
            # Erro comum: Placa duplicada (UNIQUE constraint)
            flash(f'Erro ao cadastrar veículo. Verifique se a placa já existe. Detalhe: {e.args[0]}', 'danger')

    return render_template('register_vehicle.html', title='Cadastrar Veículo', form=form)

# -----------------
# 2. LISTAGEM DE VEÍCULOS
# -----------------
@vehicle_bp.route('/list')
@login_required
def list_vehicles():
    supabase = get_safe_supabase_client()
    id_empresa = current_user.id_empresa
    veiculos = []

    try:
        # Busca apenas os veículos da empresa logada
        response = supabase.table('Veiculo').select('*').eq('id_empresa', id_empresa).order('placa').execute()
        veiculos = response.data
    except Exception as e:
        flash(f'Erro ao carregar lista de veículos: {e}', 'danger')

    return render_template('vehicle_list.html', title='Frota', veiculos=veiculos)
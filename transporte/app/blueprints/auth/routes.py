# app/blueprints/auth/routes.py - Versão corrigida

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import EmpresaRegisterForm, LoginForm
from ...utils.data_access import get_safe_supabase_client

# Define o Blueprint 'auth'
auth_bp = Blueprint('auth', __name__, template_folder='templantes', url_prefix='/auth')

# -----------------
# 1. ROTA DE CADASTRO DE EMPRESA
# -----------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register_empresa():
    """Registra uma nova empresa"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.main_dashboard'))
    
    form = EmpresaRegisterForm()
    
    if form.validate_on_submit():
        try:
            supabase = get_safe_supabase_client()
            
            # Verificar se email já existe
            response = supabase.table('Empresa').select('id').eq('email', form.email.data).execute()
            if response.data:
                flash('Este email já está registrado.', 'danger')
                return render_template('register_empresa.html', title='Cadastro de Empresa', form=form)
            
            # Criar novo registro de empresa
            empresa_data = {
                'nome': form.nome.data,
                'email': form.email.data,
                'senha_hash': generate_password_hash(form.senha.data),
                'cnpj': form.cnpj.data or None,
                'telefone': form.telefone.data or None,
            }
            
            response = supabase.table('Empresa').insert(empresa_data).execute()
            
            if response.data:
                flash('Empresa cadastrada com sucesso! Faça login para continuar.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Erro ao cadastrar empresa. Tente novamente.', 'danger')
                
        except Exception as e:
            flash(f'Erro ao processar registro: {str(e)}', 'danger')
    
    return render_template('register_empresa.html', title='Cadastro de Empresa', form=form)

# -----------------
# 2. ROTA DE LOGIN
# -----------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Realiza login de usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.main_dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            supabase = get_safe_supabase_client()
            
            # Buscar usuário por email
            response = supabase.table('Empresa').select('*').eq('email', form.email.data).execute()
            
            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                
                # Verificar senha
                if check_password_hash(user_data.get('senha_hash', ''), form.senha.data):
                    # Criar sessão do usuário
                    from ...models import User
                    user = User(
                        id=user_data['id'],
                        nome=user_data['nome'],
                        email=user_data['email'],
                        id_empresa=user_data['id']
                    )
                    login_user(user, remember=form.lembrar_me.data)
                    flash(f'Bem-vindo(a), {user.nome}!', 'success')
                    
                    next_page = request.args.get('next')
                    if next_page and next_page.startswith('/'):
                        return redirect(next_page)
                    return redirect(url_for('dashboard.main_dashboard'))
                else:
                    flash('Email ou senha inválidos.', 'danger')
            else:
                flash('Email ou senha inválidos.', 'danger')
                
        except Exception as e:
            flash(f'Erro ao realizar login: {str(e)}', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# -----------------
# 3. ROTA DE LOGOUT
# -----------------
@auth_bp.route('/logout')
@login_required
def logout():
    """Realiza logout do usuário"""
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

# -----------------
# 4. ROTA DE DASHBOARD (TEMPORÁRIA)
# -----------------
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard temporário (redireciona para novo dashboard)"""
    return redirect(url_for('dashboard.main_dashboard'))

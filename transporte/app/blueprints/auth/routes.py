# app/blueprints/auth/routes.py - Versão corrigida

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import EmpresaRegisterForm, LoginForm
from ...utils.data_access import get_safe_supabase_client
from flask import current_app
from supabase import create_client

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

            # Preferir usar service_role client para checagens/escritas server-side quando disponível
            service_key = current_app.config.get('SUPABASE_KEY_SERVICE_ROLE')
            if service_key:
                svc = create_client(current_app.config.get('SUPABASE_URL'), service_key)
            else:
                svc = supabase

            # Verificar se email já existe (procurar na tabela 'usuario')
            response = svc.table('usuario').select('id').eq('email', form.email.data).execute()
            if response.data:
                flash('Este email já está registrado.', 'danger')
                return render_template('register_empresa.html', title='Cadastro de Empresa', form=form)
            
            # Criar novo registro de empresa (somente campos existentes na tabela 'empresa')
            empresa_data = {
                'nome': form.nome.data,
                'cnpj': form.cnpj.data or None,
            }

            # Use the previously created svc (service or anon) for insert
            resp_insert = svc.table('empresa').insert(empresa_data).execute()

            if getattr(resp_insert, 'error', None):
                flash('Erro ao cadastrar empresa. Tente novamente.', 'danger')
                return render_template('register_empresa.html', title='Cadastro de Empresa', form=form)

            # Tentar recuperar o id criado pelo insert: preferir cnpj quando disponível
            try:
                if empresa_data.get('cnpj'):
                    resp_id = svc.table('empresa').select('id').eq('cnpj', empresa_data['cnpj']).limit(1).execute()
                else:
                    # fallback: procurar por nome
                        resp_id = svc.table('empresa').select('id').eq('nome', empresa_data['nome']).limit(1).execute()

                if not getattr(resp_id, 'data', None):
                    flash('Empresa criada, mas não foi possível recuperar o ID.', 'warning')
                    return render_template('register_empresa.html', title='Cadastro de Empresa', form=form)
                empresa_id = resp_id.data[0].get('id')
            except Exception:
                flash('Empresa criada, mas falha ao recuperar o ID.', 'warning')
                return render_template('register_empresa.html', title='Cadastro de Empresa', form=form)

            # Agora criar o usuário administrador em 'usuario' se a tabela suportar essas colunas
            usuario_data = {
                'nome': f"{form.nome.data} (admin)",
                'email': form.email.data,
                'senha_hash': generate_password_hash(form.senha.data),
                'id_empresa': empresa_id,
            }

            try:
                if service_key:
                    resp_user = svc.table('usuario').insert(usuario_data).execute()
                else:
                    resp_user = supabase.table('usuario').insert(usuario_data).execute()

                if getattr(resp_user, 'error', None) or not getattr(resp_user, 'data', None):
                    flash('Empresa criada mas falha ao criar usuário admin. Verifique o banco.', 'warning')
                else:
                    flash('Empresa e usuário admin cadastrados com sucesso! Faça login para continuar.', 'success')
                    return redirect(url_for('auth.login'))
            except Exception as e:
                flash(f'Empresa cadastrada mas erro ao criar usuário admin: {e}', 'warning')
                
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
            
            # Buscar usuário por email na tabela 'usuario'
            response = supabase.table('usuario').select('*').eq('email', form.email.data).execute()
            
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

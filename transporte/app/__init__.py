# logistica_app/app/__init__.py (Atualizado)

from flask import Flask, url_for
from config import Config
from flask_login import LoginManager # NOVO IMPORT
from . import database 
from .models import User # NOVO IMPORT

# 1. Instanciar o Flask-Login
login_manager = LoginManager() 

@login_manager.user_loader
def load_user(user_id):
    """Função obrigatória para recarregar o objeto User a partir do ID da sessão."""
    # Chama o método que criamos na classe User
    return User.get(user_id) 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ...
    
    database.init_app(app)
    
    # 2. Inicializar o Flask-Login com a aplicação
    login_manager.init_app(app) 
    
    # Configurações de rotas de login
    login_manager.login_view = 'auth.login' # Rota para onde redirecionar quando o login é exigido
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'

    # 3. REGISTRO DOS BLUEPRINTS
    from .blueprints.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.veiculo.routes import vehicle_bp
    app.register_blueprint(vehicle_bp) # Rotas começarão em /veiculos/

    # Registro do Blueprint de Abastecimento
    from .blueprints.Fueling.routes import fueling_bp
    app.register_blueprint(fueling_bp) # Rotas começarão em /abastecimento/

    # Registro do Blueprint de Dashboard
    from .blueprints.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    # Atualiza a rota inicial para dar opções
    @app.route('/')
    def index():
        """Página inicial simples com links para cadastro/login."""
        # O endpoint de registro foi nomeado como 'register_empresa' nas rotas
        register_url = url_for('auth.register_empresa')
        login_url = url_for('auth.login')
        return (
            f"<html><head><meta charset='utf-8'><title>Transporte</title></head>"
            f"<body style='font-family:Segoe UI,Calibri,Arial;margin:20px'>"
            f"<h2>Aplicação de Logística rodando!</h2>"
            f"<p>Acesse:<br><a href=\"{register_url}\">Cadastrar empresa</a> — ou — <a href=\"{login_url}\">Entrar (login)</a></p>"
            f"</body></html>"
        )
        
    return app
# logistica_app/app/blueprints/auth/forms.py (Atualizado)

from flask_wtf import FlaskForm
# Adiciona BooleanField para o checkbox 'Lembrar de mim'
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

# ... (EmpresaRegisterForm continua igual) ...

# NOVO FORMULÁRIO
class LoginForm(FlaskForm):
    """
    Formulário para login do Usuário.
    """
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')
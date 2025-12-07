# logistica_app/app/blueprints/auth/forms.py (Atualizado)

from flask_wtf import FlaskForm
# Adiciona BooleanField para o checkbox 'Lembrar de mim'
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class EmpresaRegisterForm(FlaskForm):
    """
    Formulário para registro de uma nova Empresa.
    Campos esperados pelas rotas: nome, email, senha, cnpj, telefone
    """
    nome = StringField('Nome da Empresa', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=128)])
    confirmar_senha = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem coincidir')])
    cnpj = StringField('CNPJ', validators=[Length(max=20)], description='Opcional')
    telefone = StringField('Telefone', validators=[Length(max=30)], description='Opcional')
    submit = SubmitField('Cadastrar Empresa')

# NOVO FORMULÁRIO
class LoginForm(FlaskForm):
    """
    Formulário para login do Usuário.
    """
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')
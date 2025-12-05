# logistica_app/app/blueprints/auth/forms.py (Atualizado)

from flask_wtf import FlaskForm
# Adiciona BooleanField para o checkbox 'Lembrar de mim'
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class EmpresaRegisterForm(FlaskForm):
    """
    Formulário para cadastro de empresa.
    Campos básicos: nome, email, senha, confirmar senha, cnpj e telefone.
    """
    nome = StringField('Nome', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem coincidir')])
    cnpj = StringField('CNPJ', validators=[Length(max=20)], default='')
    telefone = StringField('Telefone', validators=[Length(max=20)], default='')
    submit = SubmitField('Cadastrar')

# NOVO FORMULÁRIO
class LoginForm(FlaskForm):
    """
    Formulário para login do Usuário.
    """
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')
# logistica_app/app/blueprints/vehicle/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp

class VehicleForm(FlaskForm):
    """
    Formulário para cadastro e edição de veículos.
    """
    placa = StringField('Placa', validators=[
        DataRequired(),
        Length(min=7, max=10),
        Regexp(r'^[A-Z0-9-]{7,10}$', message="Formato de placa inválido.")
    ])
    
    marca = StringField('Marca', validators=[DataRequired(), Length(max=50)])
    
    modelo = StringField('Modelo', validators=[DataRequired(), Length(max=50)])
    
    ano = IntegerField('Ano', validators=[
        DataRequired(),
        NumberRange(min=1900, max=2100, message="Ano inválido.")
    ])
    
    # Opções de combustível (pode ser carregado dinamicamente do BD no futuro)
    tipo_combustivel = SelectField('Combustível', choices=[
        ('Diesel', 'Diesel'),
        ('Gasolina', 'Gasolina'),
        ('Etanol', 'Etanol'),
        ('GNV', 'GNV'),
        ('Eletrico', 'Elétrico')
    ], validators=[DataRequired()])
    
    km_atual = IntegerField('Quilometragem Atual (KM)', validators=[
        DataRequired(),
        NumberRange(min=0, message="A KM não pode ser negativa.")
    ])
    
    submit = SubmitField('Salvar Veículo')
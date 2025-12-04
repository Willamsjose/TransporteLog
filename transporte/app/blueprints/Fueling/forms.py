# logistica_app/app/blueprints/fueling/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, IntegerField, StringField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Optional, Length
from flask_wtf.file import FileField, FileAllowed # Para lidar com uploads
from datetime import datetime

class FuelingForm(FlaskForm):
    
    id_veiculo = SelectField('Veículo (Placa - Modelo)', validators=[DataRequired()], coerce=int)
    
    data_abastecimento = DateTimeLocalField('Data e Hora', 
                                            format='%Y-%m-%dT%H:%M', 
                                            default=datetime.now(),
                                            validators=[InputRequired()])
    
    litros = DecimalField('Litros Abastecidos', places=2, validators=[
        DataRequired(),
        NumberRange(min=0.01, message="Deve ser um valor positivo.")
    ])
    
    valor_litro = DecimalField('Valor por Litro (R$)', places=2, validators=[
        DataRequired(),
        NumberRange(min=0.01, message="Deve ser um valor positivo.")
    ])
    
    km_registro = IntegerField('KM no Abastecimento (Odômetro)', validators=[
        DataRequired(),
        NumberRange(min=1, message="A KM deve ser maior que 0.")
    ])
    
    local_abastecimento = StringField('Local do Abastecimento', validators=[Length(max=255), Optional()])
    
    # Campo para cálculo de consumo: só calcula se for tanque cheio
    is_tanque_cheio = SelectField('Tanque Cheio?', choices=[
        ('True', 'Sim'),
        ('False', 'Não')
    ], validators=[DataRequired()], default='True')
    
    # Campo para upload (Integração NoSQL/Storage)
    nota_fiscal_file = FileField('Nota Fiscal (Opcional)', validators=[
        FileAllowed(['jpg', 'png', 'pdf'], 'Apenas imagens (JPG, PNG) ou PDF são permitidos.')
    ])
    
    submit = SubmitField('Registrar Abastecimento')
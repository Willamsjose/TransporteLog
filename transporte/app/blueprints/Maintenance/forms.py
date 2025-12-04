# logistica_app/app/blueprints/maintenance/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, InputRequired
from flask_wtf.file import FileField, FileAllowed
from datetime import date

# ----------------
# 1. FORMULÁRIO DE AGENDAMENTO PREDITIVO
# ----------------
class PredictiveMaintenanceForm(FlaskForm):
    """
    Formulário para agendar manutenção preditiva baseada em KM ou Data.
    """
    id_veiculo = SelectField('Veículo (Placa - Modelo)', validators=[DataRequired()], coerce=int)
    
    descricao = StringField('Descrição do Serviço', validators=[DataRequired(), Length(max=255)])
    
    tipo_manutencao = SelectField('Tipo', choices=[
        ('Preventiva', 'Preventiva (Troca de Óleo, Filtros, Pneus)'),
        ('Corretiva', 'Corretiva (Reparos de Falhas)'),
        ('Preditiva', 'Preditiva (Análise de Condição)')
    ], validators=[DataRequired()])
    
    # Campo para agendamento por KM
    km_agendado = IntegerField('KM Prevista para o Serviço', validators=[
        NumberRange(min=1, message="A KM deve ser positiva."),
        Optional() # Permite que seja agendado por data
    ])
    
    # Campo para agendamento por Data
    data_agendada = DateField('Data Prevista para o Serviço', 
                              format='%Y-%m-%d', 
                              default=date.today(),
                              validators=[Optional()])
    
    # Campo para o ALERTA (km ou dias antes)
    intervalo_alerta = IntegerField('Dias/KM de Alerta', validators=[
        DataRequired(),
        NumberRange(min=1, message="Defina um intervalo positivo para o alerta.")
    ], description="Se for por KM, o alerta será dado 'X' KM antes. Se for por data, 'X' dias antes.")

    submit = SubmitField('Agendar Manutenção')


# ----------------
# 2. FORMULÁRIO DE REGISTRO DE MANUTENÇÃO REALIZADA
# ----------------
class RealizedMaintenanceForm(FlaskForm):
    """
    Formulário para registrar uma manutenção que ocorreu (pode ser de um agendamento ou não).
    """
    # Se este formulário for carregado a partir de um alerta, o id_manutencao_preditiva virá na URL
    
    id_veiculo = SelectField('Veículo (Placa - Modelo)', validators=[DataRequired()], coerce=int)
    
    data_realizacao = DateField('Data da Realização', format='%Y-%m-%d', validators=[InputRequired()])
    
    descricao_servico = StringField('Serviço Detalhado', validators=[DataRequired()])
    
    custo_total = DecimalField('Custo Total (R$)', places=2, validators=[
        DataRequired(),
        NumberRange(min=0.01, message="O custo deve ser positivo.")
    ])
    
    oficina_responsavel = StringField('Oficina/Prestador de Serviço', validators=[Length(max=255), Optional()])
    
    # Campo para upload (Integração NoSQL/Storage)
    nota_fiscal_file = FileField('Nota Fiscal (Opcional)', validators=[
        FileAllowed(['jpg', 'png', 'pdf'], 'Apenas imagens (JPG, PNG) ou PDF são permitidos.')
    ])
    
    submit = SubmitField('Registrar Manutenção Realizada')
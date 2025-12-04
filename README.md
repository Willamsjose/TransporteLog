# Transporte com Flask - Sistema de Gestão de Transporte

Sistema web desenvolvido em Flask para gestão de frota de veículos, abastecimento, manutenção preditiva e análise de custos.

## 🎯 Funcionalidades

- ✅ Autenticação de empresas
- ✅ Cadastro e gestão de veículos
- ✅ Registro de abastecimento com cálculo de km/L
- ✅ Agendamento de manutenção preditiva
- ✅ Registro de manutenção realizada
- ✅ Dashboard com análise de custos
- ✅ Alertas de manutenção automáticos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask 3.1.2
- **Autenticação**: Flask-Login
- **Banco de Dados**: Supabase (PostgreSQL)
- **Formulários**: Flask-WTF, WTForms
- **Frontend**: HTML5 + CSS3
- **Ambiente**: Python 3.13+, Virtual Environment

## 📦 Dependências

Veja `requirements.txt` para lista completa de dependências.

Principais:
- Flask==3.1.2
- Flask-Login
- Flask-WTF
- python-dotenv==1.2.1
- supabase==2.25.0
- psycopg2-binary==2.9.11

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/Willamsjose/TransporteLog.git
cd TransporteLog/transporte
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv .
# Windows
Scripts\Activate.ps1
# Linux/Mac
source bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite .env com suas credenciais Supabase
nano .env
```

### 5. Execute a aplicação
```bash
python app.py
# ou
flask run
```

A aplicação estará disponível em `http://localhost:5000`

## 📋 Estrutura do Projeto

```
transporte/
├── app.py                          # Ponto de entrada
├── config.py                       # Configurações
├── requirements.txt                # Dependências Python
├── .env.example                    # Exemplo de variáveis de ambiente
├── app/
│   ├── __init__.py                # Inicialização da app
│   ├── database.py                # Conexão com Supabase
│   ├── models.py                  # Modelos de dados
│   ├── blueprints/
│   │   ├── auth/                  # Autenticação
│   │   ├── veiculo/               # Gestão de veículos
│   │   ├── Fueling/               # Registro de abastecimento
│   │   ├── Maintenance/           # Manutenção preditiva
│   │   └── dashboard/             # Dashboard principal
│   ├── static/
│   │   ├── css.css                # Estilos centralizados
│   │   ├── js.js                  # Scripts
│   │   └── Imagens/               # Imagens
│   └── utils/
│       ├── data_access.py         # Acesso a dados
│       └── data_analysis.py       # Análise de dados
```

## 🔒 Segurança

- ✅ Senhas criptografadas com Werkzeug
- ✅ Credenciais protegidas em `.env`
- ✅ Autenticação obrigatória via Flask-Login
- ✅ Validação de formulários com WTForms
- ✅ CORS configurado para requisições seguras

## 📝 Fluxo de Uso

### 1. Cadastro de Empresa
1. Acesse `/auth/register`
2. Preencha dados da empresa
3. Confirme registro e faça login

### 2. Cadastro de Veículos
1. Acesse `/veiculos/register`
2. Preencha dados do veículo
3. Visualize lista em `/veiculos/list`

### 3. Registro de Abastecimento
1. Acesse `/abastecimento/register`
2. Selecione veículo e dados de abastecimento
3. Sistema calcula km/L automaticamente

### 4. Manutenção Preditiva
1. Acesse `/manutencao/schedule`
2. Agende manutenção por KM ou Data
3. Sistema gera alertas automáticos

### 5. Dashboard
1. Visualize `/dashboard/` após login
2. Veja custos totais, por veículo e alertas
3. Exporte relatórios (em desenvolvimento)

## 🐛 Bugs Corrigidos

Veja `ANALISE_QUALIDADE.md` para lista completa de bugs identificados e corrigidos.

Principais correções:
- ✅ Credenciais removidas de código fonte
- ✅ Typos em config.py corrigidos
- ✅ Rotas de autenticação refatoradas
- ✅ CSS centralizado e estilos inline removidos
- ✅ Templates HTML completados

## 📊 Análise de Qualidade

Sistema passou por análise completa de qualidade:
- ✅ 46+ bugs identificados e corrigidos
- ✅ Cobertura de 100% dos arquivos
- ✅ 0 erros críticos
- ✅ Segurança melhorada

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -am 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja LICENSE para detalhes.

## 👨‍💻 Autor

**Willams Jose**
- GitHub: [@Willamsjose](https://github.com/Willamsjose)
- Email: willamstech@outlook.com

## 📞 Suporte

Para problemas ou sugestões, abra uma issue no GitHub.

---

**Última atualização**: Dezembro 2025
**Status**: ✅ Produção (Versão 1.0)

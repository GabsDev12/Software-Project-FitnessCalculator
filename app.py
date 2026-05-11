from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configura SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para armazenar IMCs
class IMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    imc_valor = db.Column(db.Float, nullable=False)
    imc_classificacao = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<IMC {self.nome}: {self.imc_valor}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imc', methods=['GET', 'POST'])
def imc():
    resultado = None
    if request.method == 'POST':
        nome = request.form['nome']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        
        imc_valor = round(peso / (altura ** 2), 2)
        imc_classificacao = ""

        if imc_valor < 18.5:
            imc_classificacao = "Magreza"

        elif 18.5 <= imc_valor <= 24.9:
            imc_classificacao = "Normal"

        elif 25.0 <= imc_valor <= 29.9:
            imc_classificacao = "Sobrepeso(I)"
        
        elif 30.0 <= imc_valor <= 39.9:
            imc_classificacao = "Obesidade(II)"
        
        else:
            imc_classificacao = "Obesidade Grave(III)"

        resultado = f'{imc_valor} - {imc_classificacao}'

        # Salva no banco de dados
        novo = IMC(nome=nome, peso=peso, altura=altura, imc_valor=imc_valor, imc_classificacao=imc_classificacao)
        db.session.add(novo)
        db.session.commit()
    
    return render_template('imc.html', resultado=resultado)

# Tabela armazenas TMB

class TMB(db.Model):

    __tablename__ = "tmb"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.String(40), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    tmb_valor = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<TMB {self.nome}: {self.tmb_valor}>'
    
@app.route('/tmb', methods=['GET', 'POST'])
def tmb():

    tmb_valor = None
    ft_sedentario = None
    ft_leve = None
    ft_moderado = None
    ft_muito_ativo = None
    ft_extremo_ativo = None

    if request.method == 'POST':
        nome = request.form['nome']
        sexo = request.form['sexo']
        peso = float(request.form['peso'])
        altura = int(request.form['altura'])
        idade = int(request.form['idade'])
    
        if sexo == 'masculino':
            tmb_valor = (10 * peso) + (6.25 * altura) - (5 * idade) + 5

        elif sexo == 'feminino':
            tmb_valor = (10 * peso) + (6.25 * altura) - (5 * idade) - 161
    
        else:
            tmb_valor = None

        novo = TMB(nome=nome, sexo=sexo, idade=idade, peso=peso, altura=altura, tmb_valor=tmb_valor)
        db.session.add(novo)
        db.session.commit()

        ft_sedentario = round(tmb_valor * 1.2)
        ft_leve = round(tmb_valor * 1.375)
        ft_moderado = round(tmb_valor * 1.55)
        ft_muito_ativo = round(tmb_valor * 1.725)
        ft_extremo_ativo = round(tmb_valor * 1.9)

    return render_template('tmb.html', tmb_valor=tmb_valor, ft_sedentario=ft_sedentario, ft_leve=ft_leve, ft_moderado=ft_moderado, ft_muito_ativo=ft_muito_ativo, ft_extremo_ativo=ft_extremo_ativo)

class Agua(db.Model):

    __tablename__ = "Table_agua"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.String(40), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    fator_atividade = db.Column(db.String(40), nullable=False)
    fator_climatico = db.Column(db.String(40), nullable=False)
    consumo_agua = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Consumo Agua {self.nome}: {self.consumo_agua}>'

@app.route('/agua', methods=['GET', 'POST'])
def agua():

    # Definindo váriáveis
    copos_agua = None
    consumo_agua = None

    peso = None

    fator_atividade = None

    fator_climatico = None

    idade = None
    fator_idade = None

    sexo = None
    fator_sexo = None

    # Associando valores do formulário às variáveis

    if request.method == 'POST':
        nome = request.form['nome']
        sexo = request.form['sexo']
        peso = float(request.form['peso'])
        idade = int(request.form['idade'])
        fator_atividade = request.form['fator_atividade']
        fator_climatico = request.form['fator_climatico']

        # Definindo fator de Atividade

        if fator_atividade == "sedentario":
            fator_atividade = 0.90
        elif fator_atividade == "levemente_ativo":
            fator_atividade = 1
        elif fator_atividade == "moderadamente_ativo":
            fator_atividade = 1.15
        elif fator_atividade == "muito_ativo":
            fator_atividade = 1.30
        elif fator_atividade == "atleta_intenso":
            fator_atividade = 1.50

        # Definindo fator Climático

        if fator_climatico == "frio_intenso":
            fator_climatico = 0.90
        elif fator_climatico == "frio":
            fator_climatico = 0.95
        elif fator_climatico == "moderado":
            fator_climatico = 1
        elif fator_climatico == "calor":
            fator_climatico = 1.08
        elif fator_climatico == "calor_intenso":
            fator_climatico = 1.15

        # Definindo fator Idade

        if idade <= 13:
            fator_idade = 1.10
        elif 14 <= idade <= 55:
            fator_idade = 1.00
        elif 56 <= idade <= 75:
            fator_idade = 0.95
        else:
            fator_idade = 0.90

        # Definindo fator Sexo

        if sexo == "masculino":
            fator_sexo = 1
        else:
            fator_sexo = 0.9

        consumo_agua = peso * 35 * fator_atividade * fator_climatico * fator_idade * fator_sexo
        consumo_agua = round(consumo_agua, 2)

        copos_agua = round(consumo_agua / 250)

        novo = Agua(nome=nome, sexo=sexo, peso=peso, idade=idade, fator_atividade=fator_atividade, fator_climatico=fator_climatico, consumo_agua=consumo_agua)
        db.session.add(novo)
        db.session.commit()

    return render_template('agua.html', consumo_agua=consumo_agua, copos_agua=copos_agua)

# Cria o banco se não existir
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
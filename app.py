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

    return render_template('tmb.html', tmb_valor=tmb_valor)

# Cria o banco se não existir
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
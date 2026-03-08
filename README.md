# O que é o FitnessCalculator?

O FitnessCalculator é uma aplicação web desenvolvida para calcular métricas relacionadas à saúde e condicionamento físico de acordo com os dados do usuário, como: 
- ⚖️ | IMC (Peso adequado em relação a altura)
- 🔥 | TMB com ou sem atividade física (Gasto calórico diário)
- 💧 | Estimativa de consumo de água
- 🍗 | Consumo de macronutrientes

# Estruturação do projeto 📁

Será utilizado o framework Flask para a implementação do projeto. A aplicação será estruturada de forma organizada, separando os arquivos responsáveis pela lógica do sistema, interface do usuário e recursos estáticos. A estrutura inicial do projeto será definida da seguinte maneira:
```text
FitnessCalculator
│
├── README.md
├── app.py
├── requirements.txt
│
├── templates
│   ├── base.html
│   ├── index.html
│   └── cadastro.html
│
└── static
    ├── css
    │   └── style.css
    │
    └── js
        └── script.js
```

O arquivo app.py será responsável pela lógica principal da aplicação, incluindo a definição das rotas e o processamento dos dados recebidos do usuário. O arquivo requirements.txt conterá as dependências necessárias para a execução do projeto.

A pasta templates armazenará os arquivos HTML responsáveis pela interface da aplicação, utilizando o sistema de templates do Flask para renderização dinâmica das páginas.

Por fim, a pasta static conterá os recursos estáticos da aplicação, como arquivos de estilização em CSS e scripts em JavaScript, utilizados para melhorar a apresentação e interatividade da interface.

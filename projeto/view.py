# o que o usuário vai ver
from flask import render_template, request, redirect, url_for, flash
import logging
from app import app, mongo
from model import User, Receita
from control import login_user

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info('Solicitação recebida na rota /login')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificando se o usuário existe e se a senha é correspondente
        if login_user(username=username, password=password):
            return redirect(url_for('home'))
        #Login falho
        else:
            flash('Login inválido. Tente novamente por favor.')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    app.logger.info('Solicitação recebida na rota /cadastro')
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # Verificando se o usuário já existe
        existing_user = mongo.db.users.find_one({'username': username})

        if existing_user:
            # Se o usuário já existe
            flash('O nome de usuário já está sendo utilizado, tente novamente por favor.')
        else:
            # Criando um novo usuário
            new_user = User(username, password)
            mongo.db.users.insert_one(new_user.__dict__)

            # Redirecionando para página de login
            return redirect(url_for('login'))
        
    return render_template('cadastro.html')

@app.route('/cadreceitas', methods=['GET', 'POST'])
def cadreceitas():
    app.logger.info('Solicitação recebida na rota /cadreceitas')
    if request.method == 'POST':
        # Obtenha os dados do formulário de cadastro de notas de alunos
        titulo = request.form['titulo']
        tags = request.form['tags']
        conteudo = request.form['conteudo_receita']
        # Certifique-se de associar a nota ao aluno que a está recebendo
        # Substitua 'user_id' pelo ID do usuário autenticado
        user_id = 'user_id'  # Substitua pelo ID do usuário autenticado
        new_receita = Receita(userid=user_id, titulo=titulo, tags=tags, conteudo=conteudo)
        mongo.db.receitas.insert_one(new_receita.__dict__)

        flash('Receita cadastrada com sucesso!', 'success')

    return render_template('cadreceitas.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    app.logger.info('Solicitação recebida na rota /home')
    
    # Obtenha o filtro de tag da URL
    selected_tag = request.args.get('tag', default='', type=str)
    
    # Consulta no banco de dados
    query = {}
    if selected_tag:
        query['tags'] = {'$regex': selected_tag, '$options': 'i'}
    
    receitas = mongo.db.receitas.find(query)
    
    # Obtenha uma lista de todas as tags disponíveis no banco de dados
    all_tags = [receita['tags'] for receita in mongo.db.receitas.find()]
    
    return render_template('home.html', receitas=receitas, selected_tag=selected_tag, all_tags=all_tags)

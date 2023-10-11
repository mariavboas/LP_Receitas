from app import mongo
def login_user(username, password):
    # Lógica para verificar o login do usuário no banco de dados
    user = mongo.db.users.find_one({'username': username, 'password': password})
    if user:
        return True
    else:
        return False
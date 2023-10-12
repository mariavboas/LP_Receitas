from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://admin:adminadmin@receitaslp.a7sx0qh.mongodb.net/receitaslp'
app.config['SECRET_KEY'] = '823857g9fe0g0jj;.;.pl[ork9kh0jr98jr]'
mongo = PyMongo(app)

from view import *

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import logging
from flask_cors import CORS
from flask_login import current_user
app = Flask(__name__, static_url_path='/static')
CORS(app, origins='*')  
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
logging.basicConfig(level=logging.ERROR)
from Agenda.models.tables import Usuario

@login_manager.user_loader
def load_user(idusuario):
    return Usuario.query.get(int(idusuario))

@app.before_request
def before_request():
    g.user = current_user

# Exemplo de rota que recupera dados do usuário autenticado
@app.route('/dados_do_usuario')
def dados_do_usuario():
    if g.user.is_authenticated:
        user_id = g.user.id  # Obtém o ID do usuário autenticado
        user_data = Usuario.query.get(user_id)  # Recupera os dados do usuário do banco de dados

        return jsonify({'username': user_data.username})
    else:
        return jsonify({'error': 'Usuário não autenticado'})

# Importe os controllers no final para evitar importação circular
from Agenda.controllers import default


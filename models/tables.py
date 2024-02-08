from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from Agenda import db
from datetime import date, datetime
import json
import weakref
from sqlalchemy.orm import class_mapper
login_manager = LoginManager()

# Tabelas de associação


# Modelo de Usuário
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario" 
    idusuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    materias = db.relationship('Materias', backref='usuario', lazy=True)


    def __init__(self, nome, email, senha,):
        self.nome = nome
        self.email = email
        self.senha = senha

    def __repr__(self):
        return f" Usuario {self.nome}"

    def get_id(self):
        return str(self.idusuario)

# Fora da classe Usuario
@login_manager.user_loader
def load_user(idusuario):
    return Usuario.query.get(int(idusuario))

# Modelos Materias, Provas, Tarefas
class Materias(db.Model):
    __tablename__ = "materias" 
    idmaterias = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    professor = db.Column(db.String(45), nullable=False)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)

    def __init__(self, nome, data, hora, professor, idusuario):
        self.nome = nome
        self.data = data
        self.hora = hora
        self.professor = professor
        self.idusuario = idusuario
    def __repr__(self):
        return f"Matéria de {self.nome}"
    def to_dict(self):
        return {
            'idmaterias': self.idmaterias,
            'title': f"{self.nome} Professor: {self.professor}",
            'start': self.data.isoformat(),
            'extendedProps': {
                'materia': {
                    'nome': self.nome,
                    'professor': self.professor,
                }
            }
        }

    def toJSON(self):
        return json.dumps(self.to_dict(), default=str, indent=4)
class Provas(db.Model):
    __tablename__ = "provas" 
    idprovas = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    valor = db.Column(db.DECIMAL(4, 2), nullable=False)
    desc = db.Column(db.Text(1000), nullable=False)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    idmaterias = db.Column(db.Integer, db.ForeignKey('materias.idmaterias'), nullable=False)
    materia = db.relationship('Materias', backref=db.backref('provas', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('provas', lazy=True))
    
    def __init__(self, data, hora, valor, desc, idmaterias, idusuario):
        self.data = data
        self.hora = hora
        self.valor = valor
        self.desc = desc
        self.idusuario = idusuario
        self.idmaterias = idmaterias

    def __repr__(self):
        return f"Prova de {self.prova.desc}: {self.desc}"
    def to_dict(self):
        return {
            'idprovas': self.idprovas,
            'title': f"{self.desc} Valor: {self.valor} Matéria: {self.materia.nome}",
            'start': self.data.isoformat(),
            'extendedProps': {
                'prova': {
                    'descrição': self.desc,
                    'valor': self.valor,
                    'hora': self.hora.isoformat(),
                    'materia': self.materia.to_dict(),  # Incluindo as informações da matéria
                }
            }
        }

    def toJSON(self):
        return json.dumps(self.to_dict(), default=str, indent=4)


class Tarefas(db.Model):
    __tablename__ = "tarefas" 
    idtarefas = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    valor = db.Column(db.DECIMAL(4, 2), nullable=False)
    desc = db.Column(db.Text(1000), nullable=False)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    idmaterias = db.Column(db.Integer, db.ForeignKey('materias.idmaterias'), nullable=False)
    materia = db.relationship('Materias', backref=db.backref('tarefas', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('tarefas', lazy=True))
    
    
    def __init__(self, data, hora, valor, desc, idmaterias, idusuario):
        self.data = data
        self.hora = hora
        self.valor = valor
        self.desc = desc
        self.idusuario = idusuario
        self.idmaterias = idmaterias

    def __repr__(self):
        return f"<Tarefa de {self.tarefa.desc}: {self.desc}>"
    def to_dict(self):
        return {
            'idtarefas': self.idtarefas,
            'title': f"{self.desc} Valor: {self.valor} Matéria: {self.materia.nome}",
            'start': self.data.isoformat(),
            'extendedProps': {
                'tarefa': {
                    'descrição': self.desc,
                    'valor': self.valor,
                    'hora': self.hora.isoformat(),
                    'materia': self.materia.to_dict(),  # Incluindo as informações da matéria
                }
            }
        }

    def toJSON(self):
        return json.dumps(self.to_dict(), default=str, indent=4)

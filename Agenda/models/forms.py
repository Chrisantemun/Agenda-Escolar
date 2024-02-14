from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, SelectField, HiddenField
from wtforms.validators import InputRequired, Email, DataRequired       
from wtforms import DateField
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired("Por favor, digite seu e-mail."), Email("Insira um e-mail válido.")])
    password = PasswordField('Senha', validators=[DataRequired("Por favor, digite sua senha.")])
    remember_me = BooleanField('Lembrar-me')

class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired("Por favor, digite seu e-mail."), Email("Insira um e-mail válido.")])
    password = PasswordField('Senha', validators=[DataRequired("Por favor, digite sua senha.")])
    remember_me = BooleanField('Lembrar-me')
    
    

class MateriasForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[InputRequired()])
    hora = StringField('Hora', validators=[InputRequired()])
    professor = StringField('Professor', validators=[InputRequired()])
    idusuario = HiddenField('Usuario', default=None)


class ProvasForm(FlaskForm):
    data = DateField('Data', format='%Y-%m-%d', validators=[InputRequired()])
    hora = StringField('Hora', validators=[InputRequired()])
    valor = FloatField('Valor', validators=[InputRequired()])
    desc =  StringField('Descrição', validators=[InputRequired()])
    idmaterias = SelectField('Materia', coerce=int, validators=[InputRequired()])
    idusuario = HiddenField('Usuario', default=None)

class TarefasForm(FlaskForm):
    data = DateField('Data', format='%Y-%m-%d', validators=[InputRequired()])
    hora = StringField('Hora', validators=[InputRequired()])
    valor = FloatField('Valor', validators=[InputRequired()])
    desc =  StringField('Descrição', validators=[InputRequired()])
    idmaterias = SelectField('Materia', coerce=int, validators=[InputRequired()])
    idusuario = HiddenField('Usuario', default=None)
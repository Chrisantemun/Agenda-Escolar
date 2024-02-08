from flask_login import UserMixin, logout_user
from Agenda import db # Importe 'db' localmente onde necessário
from flask import flash
from flask import render_template, request
from Agenda import app
from Agenda.models.forms import LoginForm
from Agenda.models.forms import UsuarioForm
from Agenda.models.forms import ProvasForm
from Agenda.models.forms import MateriasForm
from Agenda.models.forms import TarefasForm
from flask import jsonify
from flask import Flask,redirect, url_for
from Agenda.models.tables import Usuario, Materias, Provas, Tarefas
from flask_login import current_user, login_required, login_user
from sqlalchemy.orm import joinedload
from flask_wtf.csrf import CSRFProtect
from flask import current_app
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
csrf = CSRFProtect(app)


@app.route("/index")
def index():
    return render_template('index.html')



@app.route("/usuario", methods=["GET", "POST"])
def usuario():
   
    form = UsuarioForm()
   

    if form.validate_on_submit():
       
        try:
           
            novo_usuario = Usuario(nome=form.nome.data, email=form.email.data, senha=form.password.data)
            db.session.add(novo_usuario)
           
            db.session.commit()
          

            
            login_user(novo_usuario)
            
            
            flash("Cadastro bem-sucedido. Redirecionando para matérias.", "success")
            
            
            return redirect(url_for('perfil'))
           
        except Exception as e:
           
            print(f"Erro ao cadastrar usuário: {str(e)}")
        
            db.session.rollback()
         
            flash("Erro ao cadastrar usuário.", "danger")
            

    return render_template('usuario.html', form=form)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.password.data
        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            login_user(usuario)

            # Redireciona para a página de perfil após o login bem-sucedido
            next_url = request.args.get('next')

            if next_url:
                
                return redirect(next_url)
            else:
                
                return redirect(url_for('perfil'))
        else:
            
            form.email.errors.append("Credenciais inválidas")

    return render_template('login.html', form=form)

    


@app.route("/materias", methods=["GET", "POST"])
def materias():
    form = MateriasForm()
    
    if current_user.is_authenticated and not form.is_submitted():
        form.idusuario.default = current_user.idusuario
        form.process()
    if form.validate_on_submit():
        
        
        
        try:
            
            nova_materia = Materias(nome=form.nome.data, data=form.data.data, hora=form.hora.data, professor=form.professor.data, idusuario=form.idusuario.data)
            
            db.session.add(nova_materia)
          
            current_user.materias.append(nova_materia)
            
            db.session.commit()
            
            
            flash("Cadastro bem-sucedido. Redirecionando para listar matérias.", "success")
            
            return redirect(url_for('listarmaterias'))
            
        except Exception as e:
           
            db.session.rollback()
           
            flash("Erro ao cadastrar materia", "danger")
            
    else:
        
        print(form.errors)
   
    return render_template('materias.html', form=form)


  



@app.route("/provas", methods = ["GET", "POST"])
def provas():
    form = ProvasForm()
    form.idmaterias.choices = [(m.idmaterias, m.nome) for m in Materias.query.filter_by(usuario=current_user).all()]
    if current_user.is_authenticated and not form.is_submitted():
        form.idusuario.default = current_user.idusuario
        form.process() 
    if form.validate_on_submit():
        try:
            print("4")
            nova_prova = Provas(data=form.data.data, hora=form.hora.data, valor=form.valor.data, desc = form.desc.data, idmaterias = form.idmaterias.data, idusuario = form.idusuario.data)
            print("5")
            db.session.add(nova_prova)
            print("6")
            db.session.commit()
            print("7")
            print("8")
            flash("Cadastro bem-sucedido. Redirecionando para listar provas.", "success")
            print("9")
            return redirect(url_for('listarprovas'))
            print("10")
        except Exception as e:
            print("11")
            print(f"Erro ao cadastrar prova: {str(e)}")
            print("12")
            db.session.rollback()
            print("13")
            flash("Erro ao cadastrar prova", "danger")
            print("14")
    return render_template('provas.html', form=form)
    print("15")

@app.route("/tarefas", methods = ["GET", "POST"])
def tarefas():
    form = TarefasForm()
    form.idmaterias.choices = [(m.idmaterias, m.nome) for m in Materias.query.filter_by(usuario=current_user).all()]  
    if current_user.is_authenticated and not form.is_submitted():
        form.idusuario.default = current_user.idusuario
        form.process() 
    if form.validate_on_submit():
        try:
            print("4")
            nova_tarefa = Tarefas(data=form.data.data, hora=form.hora.data, valor=form.valor.data, desc = form.desc.data, idmaterias = form.idmaterias.data, idusuario = form.idusuario.data)
            print("5")
            db.session.add(nova_tarefa)
            print("6")
            db.session.commit()
            print("7")
            print("8")
            flash("Cadastro bem-sucedido. Redirecionando para listar tarefas.", "success")
            print("9")
            return redirect(url_for('listartarefas'))
            print("10")
        except Exception as e:
            print("11")
            print(f"Erro ao cadastrar tarefa: {str(e)}")
            print("12")
            db.session.rollback()
            print("13")
            flash("Erro ao cadastrar tarefa", "danger")
            print("14")
    return render_template('tarefas.html', form=form)
    print("15")



@app.route('/redirecionar_para_cadastro', methods=['POST'])
def redirecionar_para_cadastro():
    # Lógica adicional, se necessário, antes do redirecionamento
    # ...

    # Redireciona para a página de cadastro
    return redirect(url_for("usuario"))

@app.route('/redirecionar_para_login', methods=['POST'])
def redirecionar_para_login():
    # Lógica adicional, se necessário, antes do redirecionamento
    # ...

    # Redireciona para a página de cadastro
    return redirect(url_for("login"))


@app.route('/calendario')
def calendario():
    return render_template('calendario.html')




def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                # this will fail on non-encodable values, like other classes
                json.dumps(data)
                fields[field] = data
            except TypeError:
                # replace original with a serializable type
                fields[field] = None
        # a json-encodable dict
        return fields

def serialize_object(obj):
    if hasattr(obj, 'toJSON'):
        return json.loads(obj.toJSON())
    else:
        return alchemy_encoder(obj)

# ...

@app.route('/eventos_calendario')
def eventos_calendario():
    try:
        materias_from_db = Materias.query.filter_by(usuario=current_user).all()
        provas_from_db = Provas.query.filter_by(usuario=current_user).all()
        tarefas_from_db = Tarefas.query.filter_by(usuario=current_user).all()

        eventos_materias = [
            {
                'title': f"{materia.nome} Professor: {materia.professor} - \nHora:{materia.hora}",
                'start': materia.data.strftime('%Y-%m-%d'),
                'materia': serialize_object(materia),
            }
            for materia in materias_from_db
        ]

        eventos_provas = [
            {
                'title': f"{prova.desc} \nValor: {prova.valor} - \nMatéria: {prova.materia} - \nHora:{prova.hora}",
                'start': prova.data.strftime('%Y-%m-%d'),
                'prova': serialize_object(prova),
            }
            for prova in provas_from_db
        ]

        eventos_tarefas = [
            {
                'title': f"{tarefa.desc}\n"
                         f"Valor: {tarefa.valor} -\n"
                         f"Matéria: {tarefa.materia} - \nHora:{tarefa.hora}",
                'start': tarefa.data.strftime('%Y-%m-%d'),
                'tarefa': serialize_object(tarefa),
            }
            for tarefa in tarefas_from_db
        ]

        eventos = eventos_materias + eventos_provas + eventos_tarefas
        print('Eventos:', eventos)
        return jsonify(eventos)

    except Exception as e:
        print(f"Erro ao obter eventos do calendário: {str(e)}")
        return jsonify({'error': str(e)}), 500






@app.route('/deletar_materias/<int:idmaterias>', methods=['POST'])
def deletar_materias(idmaterias):
    try:
        if not current_user.is_authenticated:
            current_app.logger.error('Usuário não autenticado')
            return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 401

        materia = Materias.query.get(idmaterias)
        if not materia:
            return jsonify({'success': False, 'error': 'Matéria não encontrada'}), 404

        if materia.usuario != current_user:
            return jsonify({'success': False, 'error': 'Matéria não pertence ao usuário'}), 403

        # Remova a matéria associada ao usuário autenticado
        db.session.delete(materia)
        db.session.commit()

        current_app.logger.info(f'Matéria com ID {idmaterias} foi deletada com sucesso!')

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro durante a deleção da matéria com ID {idmaterias}: {str(e)}')
        print(e)  # Isso imprime no console
        current_app.logger.error(str(e))  # Isso registra no sistema de log do Flask
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/deletar_provas/<int:idprovas>', methods=['POST'])
def deletar_provas(idprovas):
    try:
        if not current_user.is_authenticated:
            current_app.logger.error('Usuário não autenticado')
            return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 401

        prova = Provas.query.get(idprovas)
        if not prova:
            return jsonify({'success': False, 'error': 'Prova não encontrada'}), 404

        

        # Remova a matéria associada ao usuário autenticado
        db.session.delete(prova)
        db.session.commit()

        current_app.logger.info(f'Prova com ID {idprovas} foi deletada com sucesso!')

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro durante a deleção da prova com ID {idprovas}: {str(e)}')
        print(e)  # Isso imprime no console
        current_app.logger.error(str(e))  # Isso registra no sistema de log do Flask
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/deletar_tarefas/<int:idtarefas>', methods=['POST'])
def deletar_tarefas(idtarefas):
    try:
        if not current_user.is_authenticated:
            current_app.logger.error('Usuário não autenticado')
            return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 401

        tarefa = Tarefas.query.get(idtarefas)
        if not tarefa:
            return jsonify({'success': False, 'error': 'Tarefa não encontrada'}), 404

        

        # Remova a matéria associada ao usuário autenticado
        db.session.delete(tarefa)
        db.session.commit()

        current_app.logger.info(f'Tarefa com ID {idtarefas} foi deletada com sucesso!')

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro durante a deleção da tarefa com ID {idtarefas}: {str(e)}')
        print(e)  # Isso imprime no console
        current_app.logger.error(str(e))  # Isso registra no sistema de log do Flask
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/atualizar_materia/<int:idmaterias>", methods=["GET", "POST"])
def atualizar_materia(idmaterias):
    # Lógica para carregar a matéria existente do banco de dados
    materia = Materias.query.get(idmaterias)

    # Verifique se a matéria existe
    if not materia:
        flash("Matéria não encontrada.", "danger")
        return redirect(url_for('listarmaterias'))

    # Crie um formulário preenchido com os detalhes atuais da matéria
    form = MateriasForm(obj=materia)

    if form.validate_on_submit():
        # Atualize os campos da matéria com os dados do formulário
        form.populate_obj(materia)

        # Realize o commit para salvar as alterações no banco de dados
        db.session.commit()

        flash("Matéria atualizada com sucesso.", "success")
        return redirect(url_for('listarmaterias'))

    return render_template('atualizarmateria.html', form=form, materia=materia)

@app.route("/atualizar_prova/<int:idprovas>", methods=["GET", "POST"])
def atualizar_prova(idprovas):
    # Lógica para carregar a prova existente do banco de dados
    prova = Provas.query.get(idprovas)

    # Verifique se a prova existe
    if not prova:
        flash("Prova não encontrada.", "danger")
        return redirect(url_for('listarprovas'))

    # Crie um formulário preenchido com os detalhes atuais da prova
    form = ProvasForm(obj=prova)

    # Preencha as opções do SelectField com as matérias disponíveis
    form.idmaterias.choices = [(materia.idmaterias, materia.nome) for materia in Materias.query.all()]

    if form.validate_on_submit():
        # Atualize os campos da prova com os dados do formulário
        form.populate_obj(prova)

        # Realize o commit para salvar as alterações no banco de dados
        db.session.commit()

        flash("Prova atualizada com sucesso.", "success")
        return redirect(url_for('listarprovas'))

    return render_template('atualizarprova.html', form=form, prova=prova)

@app.route("/atualizar_tarefa/<int:idtarefas>", methods=["GET", "POST"])
def atualizar_tarefa(idtarefas):
    # Lógica para carregar a prova existente do banco de dados
    tarefa = Tarefas.query.get(idtarefas)

    # Verifique se a prova existe
    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for('listartarefas'))

    # Crie um formulário preenchido com os detalhes atuais da prova
    form = TarefasForm(obj=tarefa)

    # Preencha as opções do SelectField com as matérias disponíveis
    form.idmaterias.choices = [(materia.idmaterias, materia.nome) for materia in Materias.query.all()]

    if form.validate_on_submit():
        # Atualize os campos da prova com os dados do formulário
        form.populate_obj(tarefa)

        # Realize o commit para salvar as alterações no banco de dados
        db.session.commit()

        flash("Tarefa atualizada com sucesso.", "success")
        return redirect(url_for('listartarefas'))

    return render_template('atualizartarefa.html', form=form, tarefa=tarefa)



@app.route('/listarmaterias')
@login_required
def listarmaterias():
    materias = Materias.query.filter_by(usuario=current_user).all()
    return render_template('listarmaterias.html', materias=materias)

@app.route('/listarprovas')
@login_required
def listarprovas():
    provas = Provas.query.filter_by(usuario=current_user).all()
    return render_template('listarprovas.html', provas=provas)




@app.route('/listartarefas')
@login_required
def listartarefas():
    tarefas = Tarefas.query.filter_by(usuario=current_user).all()
    return render_template('listartarefas.html', tarefas=tarefas)






@app.route('/perfil', methods=["GET", "POST"])
@login_required
def perfil():
    if current_user.is_authenticated:
        dados_do_usuario = {"nome": current_user.nome, "email": current_user.email}
        return render_template('perfil.html', usuario=dados_do_usuario)
    else:
        # Tratar o caso em que o usuário não está autenticado
        # Você pode redirecionar para a página de login ou mostrar uma mensagem de erro
        return redirect(url_for('login')) 

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))  


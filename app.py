# Flask para aplicacion web
from flask import Flask, render_template, request, redirect, url_for
# SQLAlchemy como ORM
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

########### Para crear la Base de Datos ###########
# En consola : 
# sqlite3 database/task.db
# *Ya tener el directorio /database

# Instancia la base de datos - /// -> Para que use el lenguak¿je de sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/task.db'
db = SQLAlchemy(app)

# Modelo ed la base de datos
class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    content     = db.Column(db.String(200))
    done        = db.Column(db.Boolean)

# Para renderizar la vista
@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html',tasks = tasks)

# POST para escribir - GET para leer
@app.route('/create-task', methods=['POST'])
def create():
    #task en un objeto tipo Task
        # El id lo asigna el ORM
        # content lo lee del input del HTML
    task = Task(content = request.form['content'], done=False)
    db.session.add(task)
    db.session.commit() # Para que lo guarde/ejecute
    return redirect(url_for('home'))
    

@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done) # Si esta en True pasa a False
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    # task = Task.query.filter_by(id=int(id)).first() -- Devuelve el primer id que coincida
    task = Task.query.filter_by(id=int(id)).delete() # Elimina el primer id que coincida
    db.session.commit()
    return redirect(url_for('home'))

    ########## Crear las tablas en la base de datos ##########
    # En python : 
    # > python
    # > from app import db
    # > db.create_all()

    

if __name__ == '__main__':
    app.run(debug=True)


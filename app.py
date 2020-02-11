# http://127.0.0.1:5000/
# FLASK_APP=app.py FLASK_DEBUG=true flask run

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://evolkvolk@localhost:5432/todoapp'

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


db.create_all()


@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
    })


@app.route('/')
def index():

    # return all rows as a JSON array of objects
    all_todos = json.dumps([{r.id:r.description} for r in Todo.query.all()])
    print(all_todos)
    return render_template('index.html', data=all_todos)

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ram@localhost:5432/todoapp'
    app.config['SQLALCHEMY_ECHO'] = True
   
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)

def __repr__(self):
       return f'<Todo {self.id}, description {self.description}, list {self.list_id}>'


class TodoList(db.Model):
   __tablename__ = 'todolists'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(), nullable=False)
   todos = db.relationship('Todo', backref='list', lazy=True)

def __repr__(self):
    return f'<TodoList ID: {self.id}, name: {self.name}, todos: {self.todos}>'

with app.app_context():
    db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    body = {}
    try:
        j = request.get_json()
        description = j['description']
        list_id = j['list_id']
        todo = Todo(description=description, list_id=list_id, completed=False)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
    except:
        db.session.rollback()
        print(sys.exc_info())
        return jsonify({ 'success': False })
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({ 'success': False })
    finally:
        db.session.close()
    return jsonify({ 'success': True })


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
       # Todo.query.filter_by(id=todo_id).delete()
    #edited in last change
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)

        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({ 'success': False })
    finally:
        db.session.close()
    return jsonify({ 'success': True })


# operation for lists

@app.route('/lists/create', methods=['POST'])
def create_list():
    body = {}
    try:
        j = request.get_json()
        name = j['name']
        #todolist = TodoList(name=name)
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['id'] = todolist.id
        body['name'] = todolist.name
    except:
        db.session.rollback()
        print(sys.exc_info())
        return jsonify({ 'success': False })
    finally:
        db.session.close()
    return jsonify({ 'success': True })



@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def set_completed_list(list_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        list = List.query.get(list_id)
        list.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({ 'success': False })
    finally:
        db.session.close()
    return jsonify({ 'success': True })


@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    try:
       # Todo.query.filter_by(id=todo_id).delete()
    #edited in last change
        list = List.query.get(list_id)
        db.session.delete(list)

        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({ 'success': False })
    finally:
        db.session.close()
    return jsonify({ 'success': True })


# routes

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))



@app.route('/lists/<list_id>')
def get_list_todos(list_id):
   return render_template('index.html', 
   lists=TodoList.query.all(),
   active_list=TodoList.query.get(list_id),
   todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

   return render_template('index.html', todos=todos, lists=lists, active_list=active_list)



if __name__ == '__main__':
    
    app.run(debug=True)
   
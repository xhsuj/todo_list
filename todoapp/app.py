from flask import Flask, render_template,request,redirect,url_for,jsonify,abort,json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://yhb@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db) #no need to use db.create_all() to sink our models, instead we use versions and migrations

order_items=db.Table('order_items',db.Column('order_id',db.Integer,db.ForeignKey('order.id'),primary_key=True),
db.Column('product_id',db.Integer,db.ForeignKey('product.id'),primary_key=True)
)
class Todo(db.Model):
    __tablename__='todos'
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(), nullable=False)
    completed=db.Column(db.Boolean, nullable=False,default=False)
    list_id=db.Column(db.Integer, db.ForeignKey('todolists.id',ondelete='CASCADE'),nullable=False)
    lists = db.relationship('TodoList')
    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed} {self.list_id}>'
class TodoList(db.Model):
    __tablename__='todolists'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    completed=db.Column(db.Boolean, nullable=False,default=False)
    todos=db.relationship('Todo',backref='todo',lazy=True, cascade='all,delete,delete-orphan')

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'

class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    status=db.Column(db.String(),nullable=False)
    products=db.relationship('Product',secondary=order_items,backref=db.backref('orders',lazy=True))

class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)

#db.create_all() # ensure that the table would be created as models define


#def create_todo():
#    description=request.form.get('description','')
#    todo=Todo(description=description)
#    db.session.add(todo)
#    db.session.commit()
#    return redirect(url_for('index')) #index is the name of the route handeler def index()

@app.route('/lists/<list_id>/list-completed', methods=['POST'])
def set_list_completed_todo(list_id):
    try:
        body={}
        error=False
        completed=request.get_json()['completed']
        counte=request.get_json()['count']
        list=TodoList.query.get(list_id)
        list.completed=completed
        count=0
        for item in list.todos:
            if(item.completed):
                count=count+1
        if (count==len(list.todos) and completed==False) or (count<len(list.todos) and completed==True):
            for item in list.todos:
                item.completed=completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error=False
    body={}
    try:
        description=request.get_json()['description'] # get json fetches the json body
        list_id=request.get_json()['id']
        todo=Todo(description=description,list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['description']=todo.description
        body['id']=todo.list_id
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    if not error:
        return jsonify(body)

@app.route('/todolists/create', methods=['POST'])
def create_todolist():
    error=False
    body={}
    try:
        name=request.get_json()['name']
        todolist=TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['name']=todolist.name
        body['id']=todolist.id
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    if not error:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        error=False
        completed=request.get_json()['completed']
        count=request.get_json()['count']
        todo=Todo.query.get(todo_id)
        todo.completed=completed
        list_id=todo.list_id
        list=TodoList.query.get(list_id)
        if count==len(list.todos) and completed==True:
            list.completed=True
        if count<len(list.todos) and completed==False:
            list.completed=False
        db.session.commit()
    except:
        db.session.rollback()
        error=True
    finally:
        db.session.close()
    if error:
        abort(500)
    return '',200

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def set_deleted_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})

@app.route('/todolists/<list_id>/delete', methods=['DELETE'])
def set_deleted_todolist(list_id):
    try:
        dele_list=TodoList.query.get(list_id)
        dele_list.todos
        db.session.delete(dele_list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
    lists=TodoList.query.order_by('id').all(),
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    ) #specify which html file we will use for the application

@app.route('/')
def index():
    return redirect(url_for('get_list_todos',list_id=1))

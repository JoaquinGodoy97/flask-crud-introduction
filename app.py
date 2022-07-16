from asyncio import tasks
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model): # por que tengo que crear una clase? para poder tener Models por default?
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) 
    completed = db.Column(db.Integer, default=0) #ignore this is never used // said the guy from the video
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #any time, to entre created, auto set to the time'

    def __repr__(self):
        return '<Task %r>' % self.id #everytime we make a task would return the id which it was created with
# index route/dont immediately 404

@app.route('/', methods=['POST', 'GET']) #we specify not just get by default but also get
def index():

    if request.method == 'POST':
        task_content = request.form['content'] # passing the id of the input which was content
        new_task = Todo(content=task_content)

        # #what is try
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'
    else:
        tasksCreated = Todo.query.order_by(Todo.date_created).all() # giving them back in the order they were created
        return render_template('index.html', tasks_html = tasksCreated) #what is tasks replacing? I think I got it

@app.route('/delete/<int:id>') # int for interger
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)#if it doesnt exists 404

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except: 
        return 'There was a problem deleting the task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] # passing the id of the input which was content
        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task = task)

if __name__ == '__main__':
    app.run(debug=True)
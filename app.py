from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    if due_date:
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
    new_task = Task(title=title, description=description, priority=priority, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update(task_id):
    task = Task.query.get(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

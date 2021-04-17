from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

#----Get Year (for copyright)----#
now = dt.datetime.now()
year = now.year

#----Create Tables----#
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(250), nullable=False)
    task = db.Column(db.String(), nullable=False)

#----Comment Out After Database and Tables are Created----#
db.create_all()

#----Create Forms----#
class TaskForm(FlaskForm):
    cat = SelectField(label = 'Category', choices = ['To Do','In Progress', 'Procrastinate', 'Complete'], validators=[DataRequired()])
    task = StringField(label='Task', validators=[DataRequired()])
    submit = SubmitField("Submit")

#----Create Routes----#

@app.route("/")
def home():
    task_data =Task.query.all()
    db.session.commit()
    return render_template("index.html", year = year, tasks = task_data)

@app.route("/add/<cat>", methods = ['GET', 'POST'])
def add(cat):
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            cat=form.cat.data,
            task=form.task.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", year = year, form=form, cat = cat)

@app.route("/edit/<task_id>", methods = ['GET', 'POST'] )
def edit(task_id):
    task_to_update = Task.query.filter_by(id=task_id).first()
    form = TaskForm(
        cat=task_to_update.cat,
        task=task_to_update.task
    )
    if form.validate_on_submit():
        task_to_update.cat = form.cat.data
        task_to_update.task = form.task.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", year=year, form=form, is_edit=True, task_id=task_id)

@app.route("/delete/<task_id>", methods = ['GET', 'POST'] )
def delete(task_id):
    task_to_delete = Task.query.filter_by(id=task_id).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SubmitField, BooleanField
from wtforms import validators
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
import random
import os
import random
from datetime import datetime


app = Flask(__name__)

# Create random secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


# TODO TABLE Configuration
class ToDo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True, nullable=False)
    date_added = db.Column(db.String(250), nullable=False)
    date_started = db.Column(db.String(250), nullable=True)
    date_completed = db.Column(db.String(250), nullable=True)


# db.create_all()


class ToDoForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Submit")


class ToDoEdit(FlaskForm):
    date_started = BooleanField('date_started')
    date_completed = BooleanField('date_completed')
    submit = SubmitField("Submit")


@app.route('/')
def all_todos():
    todos = db.session.query(ToDo).all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST', 'GET'])
def add_todo():
    form = ToDoForm()
    if form.validate_on_submit():
        new_todo = ToDo(
            name=request.form.get('name'),
            date_added=datetime.now().strftime("%m/%d/%Y, %H:%M"),
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('all_todos'))
    return render_template('add.html', form=form)


@app.route('/edit/<int:todo_id>', methods=['POST', 'GET'])
def edit_todo(todo_id):
    todo_to_edit = ToDo.query.get(todo_id)
    form = ToDoEdit()
    if form.validate_on_submit():
        mod_todo = ToDo(
            date_started=request.form.get('date_started'),
            date_completed=request.form.get('date_completed')
            )
        if mod_todo.date_started == 'y':
            todo_to_edit.date_started = datetime.now().strftime("%m/%d/%Y, %H:%M")
        if mod_todo.date_completed == 'y':
            todo_to_edit.date_completed = datetime.now().strftime("%m/%d/%Y, %H:%M")
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form)


@app.route("/delete/<int:todo_id>", methods=["DELETE", "GET", "POST"])
def delete_todo(todo_id):
    todo_to_delete = ToDo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('all_todos'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000)

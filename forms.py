from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField, EmailField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField(label="Email:",validators=[DataRequired()])
    password = PasswordField(label="Password:",validators=[DataRequired()])
    submit = SubmitField(label="LOGIN",validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField(label="Username:", validators=[DataRequired()])
    email = EmailField(label="Email:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="LOGIN", validators=[DataRequired()])

class ToDoForm(FlaskForm):
    name = StringField(label="Enter List Name:", validators=[DataRequired()])
    task = StringField(label="Todo:",validators=[DataRequired()],render_kw={"placeholder":"Enter the first task and press ENTER"})
    submit = SubmitField(label="DONE", validators=[DataRequired()])

class NextTaskForm(FlaskForm):
    task = StringField(label="Todo:",validators=[DataRequired()],render_kw={"placeholder":"Enter the next task and press ENTER"})
    submit = SubmitField(label="DONE", validators=[DataRequired()])
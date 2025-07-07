from flask import Flask,render_template, redirect, url_for,flash
from flask_bootstrap import Bootstrap5
from forms import LoginForm,RegisterForm, ToDoForm, NextTaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from sqlalchemy import Integer,Float,String,Text
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
import os


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email:Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password:Mapped[str] = mapped_column(String(100), nullable=False)

class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    task: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    user: Mapped[str] = mapped_column(String(250), nullable=False)

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///database.db")
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"   "for local use this"
db.init_app(app=app)
login_manager.init_app(app=app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

with app.app_context():
    db.create_all()

bootstrap = Bootstrap5(app=app)

@app.route("/")
def home():
    if current_user.is_authenticated:
        tasks = db.session.execute(db.select(Task).where(Task.user == current_user.name)).scalars().all()
        return render_template("home.html",tasks=tasks)
    else:
        return render_template("index.html")

@app.route("/login", methods=['GET','POST'])
def login():
    my_form = LoginForm()
    if my_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == my_form.email.data)).scalar()
        if user:
            if user.password == my_form.password.data:
                login_user(user)
                return redirect("/")
            else:
                flash("Password is incorrect")
                return redirect("/login")
        else:
            flash("This Email don't exist, please try another email or do register")
            return redirect("/login")
    return render_template("login.html", form=my_form)

@app.route("/register", methods=['GET','POST'])
def register():
    my_form = RegisterForm()
    if my_form.validate_on_submit():
        if db.session.execute(db.select(User).where(User.name == my_form.name.data)).scalar():
            flash("This Username is used, try another name.")
        if db.session.execute(db.select(User).where(User.email == my_form.email.data)).scalar():
            flash("This is email is used, please try another email or do login")
        user = User(
            name = my_form.name.data,
            email = my_form.email.data,
            password = my_form.password.data
        )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            pass
        else:
            login_user(user)
            return redirect("/")

    return render_template("register.html", form=my_form)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/task", methods=["GET","POST"])
@login_required
def add_task_list():
    task_form = ToDoForm()
    tasks = db.session.execute(db.select(Task).where(Task.user == current_user.name)).scalars().all()
    if task_form.validate_on_submit():
        task_list = Task(
            title = task_form.name.data,
            task = task_form.task.data,
            date = "2",
            user = current_user.name
        )
        db.session.add(task_list)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_task.html", form=task_form,tasks=tasks)

@app.route("/task/<task_name>", methods=["GET","POST"])
def task(task_name):
    task_form = NextTaskForm()
    task = db.session.execute(db.select(Task).where(Task.title == task_name)).scalar()
    tasks = db.session.execute(db.select(Task).where(Task.user == current_user.name)).scalars().all()
    if task_form.validate_on_submit():
        task.task = f"{task.task}#@{task_form.task.data}"
        db.session.commit()
        return redirect(url_for('task', task_name=task_name))
    else:
        todos = task.task.split("#@")
        return render_template("task.html", form=task_form, task=task,todos=todos,tasks=tasks)

@app.route("/delete_list/<task_name>")
def delete_list(task_name):
    list = db.session.execute(db.select(Task).where(Task.title == task_name)).scalar()
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_task/<task_name>/<task_todo>")
def delete_task(task_name,task_todo):
    list = db.session.execute(db.select(Task).where(Task.title == task_name)).scalar()
    list.task = list.task.replace(task_todo, "")
    db.session.commit()
    return redirect(url_for("task", task_name=task_name))

if __name__ == "__main__":
    app.run(debug=False)

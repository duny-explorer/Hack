from flask_restful import Api, Resource, reqparse
from flask import jsonify, make_response, render_template, request, session, flash
from requests import delete, post, put
from werkzeug.utils import redirect, secure_filename
from DBManager import *
from forms import *
from flask_bootstrap import Bootstrap

api = Api(app)
bootstrap = Bootstrap(app)
UPLOAD_FOLDER = '/static'
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PROPAGATE_EXCEPTIONS'] = True
categories = ["книги", "наука", "люди"]

"""
db.session.add(DBUsers(
                username="admin",
                password='password',
                name='Дарья',
                email='duny.explorer@yandex.ru',
                surname='Денисова',
                admin=True
            ))
db.session.commit()
"""

delete_task = []


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if 'username' in session:
        return redirect('/')

    if request.method == "GET":
        return render_template('login.html', form=form, version=1)
    elif request.method == "POST":
        user_name = form.username.data
        password = form.password.data
        user = DBUsers.query.filter_by(username=user_name).first()

        if not user:
            flash('Такого пользователя нет')
        elif user.password != password:
            flash('Неправильный пароль')
        else:
            session['username'] = user_name
            session['user_id'] = user.id
            session['user_admin'] = user.admin
            return redirect("/")

        return redirect("/login")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/')


@app.route('/register', methods=["POST", "GET"])
def add_user():
    form = RegistrationForm()
    if request.method == "GET":
        return render_template('login.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            db.session.add(DBUsers(
                username=username,
                password=form.password.data,
                name=form.name.data,
                email=form.email.data,
                surname=form.surname.data,
                admin=False
            ))

            db.session.commit()
            return redirect('/login')
        return render_template('login.html', form=form)


@app.route('/add-task', methods=["POST", "GET"])
def add_task():
    if 'username' not in session:
        return redirect('/')
    form = AddTask()
    if request.method == "GET":
        form = AddTask()
        if session["1"]:
            form.text.data = session['text']
            form.name.data = session['name']
            form.year.data = session['data']
        return render_template('login.html', form=form, version=2)
    elif request.method == "POST":
        if form.validate_on_submit():
            print(session['1'])
            if session["1"]:
                user = DBTask.query.get(session['1'])
                user.text = form.text.data
                user.name = form.name.data
                user.time_end = form.year.data
                db.session.commit()
            else:
                user = DBUsers.query.get(session['user_id'])
                task = DBTask(
                    name=form.name.data,
                    text=form.text.data,
                    category=form.category.data,
                    time_end=form.year.data
                )
                user.News.append(task)
                db.session.commit()
            return redirect('/')

        return render_template('login.html', form=form, version=2)


@app.route('/', methods=["GET", "POST"])
def index():
    session["1"] = 0
    if request.method == "GET":
        if 'username' not in session:
            return render_template('index.html', version=1)

        data = None
        if not session["user_admin"]:
            data = DBTask.query.filter_by(user_id=session["user_id"]).all()
            for i in enumerate(sorted(delete_task)):
                data.pop(i[1] - i[0] - 1)
            form = None
        else:
            data = DBTask.query.all()
            form = SerchAutor()

        return render_template('index.html', len=len(data),
                               data=data, version=0, form=form)

    elif request.method == "POST":
        form = SerchAutor()
        if form.autor:
            if DBUsers.query.filter_by(username=form.autor.text):
                data = DBTask.query.filter_by(
                    user_id=DBUsers.query.filter_by(username=form.autor.text).first().id)
            else:
                data = []
        else:
            data = DBTask.query.all()

    return render_template('index.html', len=len(data),
                           data=data, version=0, form=form)


@app.route('/change/<int:task>')
def change(task):
    task1 = DBTask.query.get(task)

    if task1.user_id != session['user_id']:
        return redirect('/')

    print(task1.text)
    session['text'] = task1.text
    session["name"] = task1.name
    session["data"] = task1.time_end
    session['1'] = task

    return redirect('/add-task')


@app.route('/delete/<int:task>')
def delete(task):
    delete_task.append(task)
    return redirect('/')


@app.route('/info_task/<int:task>')
def info_task(task):
    if 'username' not in session:
        return redirect('/')

    return render_template("preview_task.html", task=DBTask.query.get(task))


@app.route('/admin')
def admin():
    data = DBUsers.query.all()
    data.pop(session['user_id'] - 1)
    return render_template("admin.html", data=data)


@app.route('/new_admin/<int:user>')
def new_admin(user):
    user = DBUsers.query.get(user)

    user.admin = not user.admin
    db.session.commit()

    return redirect("/admin")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField, SelectField, RadioField, \
    DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from DBManager import *


def exist_login(form, field):
    if DBUsers.query.filter_by(username=field.data).all():
        raise ValidationError("Такой пользователь уже существует")


def exist_email(form, field):
    if DBUsers.query.filter_by(email=field.data).all():
        raise ValidationError("Пользователь с такой почтой существует")


def data(form, field):
    if field.data.count('.') != 2:
        raise ValidationError("Неправильный формат")

    try:
        date = list(map(int, field.data.split(".")))

        if date[0] > 31 or date[1] > 13:
            raise ValidationError("Неправильный формат")
    except:
        raise ValidationError("Неправильный формат")


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=4, max=20,
                                                                 message="Слишком маленькая или большая строка")])
    surname = StringField('Фамилия', validators=[DataRequired(),
                                                 Length(min=4, max=50, message="Слишком маленькая или большая строка")])
    username = StringField('Логин', validators=[DataRequired(),
                                                Length(min=4, max=25, message="Слишком маленькая или большая строка"),
                                                exist_login])
    password = PasswordField('Пароль',
                             validators=[DataRequired(),
                                         Length(min=4, max=30, message="Слишком маленькая или большая строка"),
                                         EqualTo("confirm", message="Пароли не совпадают"),
                                         exist_email])
    confirm = PasswordField('Повторите пароль')
    email = StringField('Почта', validators=[Email("Неправильный почтовый адрес"), Length(max=120), exist_email])
    submit = SubmitField('Зарегистрироваться')


class AddTask(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(min=4, max=20,
                                                                 message="Слишком маленькая или большая строка")])
    text = TextAreaField('Описание', validators=[DataRequired(), Length(min=4, max=20,
                                                 message="Слишком маленькая или большая строка")])
    year = StringField("Крайние сроки выполния", validators=[DataRequired(), data])
    category = StringField('Категория')
    submit = SubmitField('Добавить')
"""
class CommunicationForm(FlaskForm):
    choice = RadioField(choices=list(zip(DBUsers.query.all(), list(map(DBUsers.query.all(), lambda x: x.name)))))
"""


class SerchAutor(FlaskForm):
    name = StringField('Автор', validators=[Length(max=20, message="Слишком маленькая или большая строка")])
    submit = SubmitField('Поиск')



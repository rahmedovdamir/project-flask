from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, FileField,BooleanField, SelectField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError,InputRequired , Regexp
from .models.user import User




class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=2,max=100)])
    login=StringField('Логин', validators=[DataRequired(),Length(min=2,max=20)])
    group=StringField('Группа', validators=[DataRequired(),Length(min=2,max=20)])
    avatar = FileField('Фото', validators=[FileAllowed(['jpg','png'])])
    status = SelectField("Должность",choices=[("default", "Выберите должность"), ("student", "Студент"), ("teacher", "Преподаватель")])
    password=PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль',validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Зарегестрироваться')

    def validate_login(self,login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данные имя пользователя уже заняты')

class LoginForm(FlaskForm):
    login=StringField('Логин', validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class AuthForm(FlaskForm):
    tg_id = StringField('Telegram ID', validators=[DataRequired(message="Введите Telegram ID"), Regexp('^[0-9]+$', message="ID должен содержать только цифры")])
    submit = SubmitField('Отправить')

class StudentForm(FlaskForm):
    student = SelectField('student', choices=["Выберите должность"],render_kw = {'class':'from-control'})

class TeacherForm(FlaskForm):
    teacher = SelectField('teacher', choices=[],render_kw = {'class':'from-control'})
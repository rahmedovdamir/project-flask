from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, FileField,BooleanField, SelectField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models.user import User

class RegistrationForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired(), Length(min=2,max=100)])
    login=StringField('Логин', validators=[DataRequired(),Length(min=2,max=20)])
    avatar = FileField('Фото', validators=[FileAllowed(['jpg','png'])])
    password=PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегаться')

    def validate_login(self,login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данные имя пользователя уже заняты')

class LoginForm(FlaskForm):
    login=StringField('Логин', validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')



class StudentForm(FlaskForm):
    student = SelectField('student', choices=[],render_kw = {'class':'from-control'})

class TeacherForm(FlaskForm):
    teacher = SelectField('teacher', choices=[],render_kw = {'class':'from-control'})
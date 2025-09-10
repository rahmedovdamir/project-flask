from flask import Blueprint,render_template,redirect, flash , url_for , request 
from ..extensions import db , bcrypt
from ..models.user import User
from ..forms import RegistrationForm, LoginForm, AuthForm
from ..functions import save_picture
from flask_login import login_user, logout_user , current_user
user = Blueprint('user', __name__)

@user.route('/user/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        try:
            avatar_filename = save_picture(form.avatar.data)
        except Exception as e:
            flash(f"Выберите фото!", "danger")
            return redirect(url_for('user.register'))
        user = User(name = form.name.data, login = form.login.data, avatar = avatar_filename,group = form.group.data, password = hashed_password, status = form.status.data)
        if user.status == "default":
            flash(f"Выберите правильную должность!", "danger")
            redirect(url_for('user.register'))
        else:    
            try:
                db.session.add(user)
                db.session.commit()
                flash(f"Вы успешно зарегестрировались, {form.login.data} !", "success")
                return redirect(url_for('user.login')) #todo: если не добавил файл - вылезает ошибка
            except Exception as e:
                print(str(e))
                flash(f"При регистрации произошла ошибка!", "danger")
    return render_template('user/register.html', form=form)

@user.route('/user/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login = form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f"Вы успешно авторизованы, {form.login.data} !", "success")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash(f"Ошибка входа. Проверьте логин или пароль", "danger")
    return render_template('user/login.html', form=form)

@user.route('/user/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('post.all'))

@user.route('/user/info', methods=['POST','GET'])
def info():
    return render_template('user/info.html')

@user.route('/tgauth', methods=['POST','GET'])
def auth():
    form = AuthForm()
    if form.validate_on_submit():
        tg = form.tg_id.data
        id_user = current_user.id
        user = User.query.get(id_user)
        if user:
            user.tgid = tg
            db.session.commit()
            flash(f"Вы успешно привязали тг, {current_user.login} !", "success")
        else:
            flash(f"Ошибка привязки", "danger")
    return render_template('user/auth.html', form=form)


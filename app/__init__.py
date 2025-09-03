from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config
from .routes.user import user
from .routes.post import post
#from .routes.schedule import schedule

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(post)
    #app.register_blueprint(schedule)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    #LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Вы не можете получить доступ, сначала войдите!'
    login_manager.login_message_category = 'info'

    with app.app_context():
        db.create_all()



    return app

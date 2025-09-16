import os

class Config(object):
    APPNAME  = 'app'
    ROOT = os.path.abspath(APPNAME) 
    UPLOAD_PATH = '/static/upload/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    USER = os.environ.get('POSTGRES_USER', 'damir')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD','Rahmedov17!')
    HOST = os.environ.get('POSTGRES_HOST', 'postgres')  
    PORT = os.environ.get('POSTGRES_PORT','5432')
    DB = os.environ.get('POSTGRES_DB','db1')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    
    SECRET_KEY = 'awrsdtfygh23uojnkb123hvgc123'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
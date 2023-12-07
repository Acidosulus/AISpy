import os
basedir = os.path.abspath(os.path.dirname(__file__))
import configparser  # импортируем библиотеку
import urllib

class Config:
    config = configparser.ConfigParser()
    config.read("settings.ini", encoding='UTF-8')  

    SECRET_KEY = 'a really really really really long secret key' #os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{urllib.parse.quote_plus("КАЗАКОВЦЕВ_НМ")}:{urllib.parse.quote_plus("1")}@{urllib.parse.quote_plus("10.19.50.11:1433")}/{urllib.parse.quote_plus("atom_khk_ul_test.stack")}'

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
       # 'sqlite:///' + os.path.join(basedir, 'app.db')
    #MAIL_SERVER = os.environ.get('MAIL_SERVER')
    #MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #ADMINS = ['your-email@example.com']
    #POSTS_PER_PAGE = 25

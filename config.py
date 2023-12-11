import os
basedir = os.path.abspath(os.path.dirname(__file__))
import configparser  # импортируем библиотеку
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    config = configparser.ConfigParser()
    config.read("settings.ini", encoding='UTF-8')  

    SECRET_KEY = 'a really really really really long secret key' #os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ##SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:321@185.112.225.153:35432/start_dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    ##SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    
    ###   really working connection to STEK
    ## SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{urllib.parse.quote_plus("КАЗАКОВЦЕВ_НМ")}:{urllib.parse.quote_plus("1")}@{urllib.parse.quote_plus("10.19.50.11:1433")}/{urllib.parse.quote_plus("atom_khk_ul_test.stack")}'


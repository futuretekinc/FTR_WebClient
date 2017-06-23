# Statement for enabling the development environment
DEBUG = True

import os
from datetime import timedelta
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

APP_SALT= b'$2b$05$112yJd.fV8zeGjNk4MVJO'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

MYSQL_OPER='mysql+pymysql://root:4rnekd9wkd@ftr-app.japanwest.cloudapp.azure.com/ftr_app_db?charset=utf8'
MYSQL_DB='mysql+pymysql://ftrdb:#4rnekd9wkd@ftrdb.japanwest.cloudapp.azure.com/ftrapp?charset=utf8'
SQLALCHEMY_DATABASE_URI = MYSQL_DB
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_TIMEOUT = 1000
SQLALCHEMY_POOL_RECYCLE = 500

DATABASE_CONNECT_OPTIONS = {}

#THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

WTF_CSRF_ENABLED = True

# Secret key for signing cookies
# SECRET_KEY = "secret"
SECRET_KEY = '#2kajsd91j3kd93911-2023'
SESSION_COOKIE_NAME='futuretek_cookies'
PERMANENT_SESSION_LIFETIME=timedelta(31) # 31days

KAFKA_HOST = 'ftr-app.japanwest.cloudapp.azure.com:9092'


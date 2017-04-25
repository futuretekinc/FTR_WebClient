# -*- coding:utf-8 -*-
import os
import sys
import json
import time
import pickle
import logging
import pyodbc
from uuid import uuid4
from datetime import datetime

from flask import *
from flask.sessions import SessionInterface, SessionMixin
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
from flask_marshmallow import Marshmallow
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy

from kafka.client import KafkaClient
from kafka import KafkaConsumer,KafkaProducer,SimpleProducer
from kafka import KafkaProducer

from sqlalchemy import MetaData, create_engine

from flask_apscheduler import APScheduler

import numpy as np
import pandas as pd

def create_db(app,metadata):
    db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit':False},use_native_unicode=True)
    return db

def init_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.debug_log_format = "%(levelname)s in %(module)s [%(lineno)d]: %(message)s"
    metadata = MetaData()
    db = create_db(app,metadata)
    ma = Marshmallow(app)
    return app, metadata,db, ma

app, metadata, db, ma = init_app()

KAFKA_HOST = app.config.get('KAFKA_HOST')

@app.before_first_request
def before_first_request_handler():
    pass

@app.before_request
def before_request_handler():
    pass
    
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404    

@app.errorhandler(500)
def server_error(error):
#     app.logger.error(error)
    return render_template('500.html'), 500    

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()



   
from app.client.controllers import client
app.register_blueprint(client)

@app.route('/')
def index():
#     return render_template('layout/main.html')
    return redirect(url_for('client.dashboard'))

db.create_all() 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 





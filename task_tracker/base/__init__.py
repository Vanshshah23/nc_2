from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import warnings
from datetime import timedelta

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app=Flask(__name__)
app.secret_key='task_tracker'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['TESTING']=True
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
app.config['SQLALCHEMY_ECHO']= False
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:9429@localhost:5432/python_db'
app.config['SQLALCHEMY_MAX_OVERFLOW']=0
db=SQLAlchemy(app)
app.app_context().push()
import base.com.controller
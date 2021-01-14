import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join('./', 'audio_tasks_new.db')

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tasks.db'

db = SQLAlchemy(app)
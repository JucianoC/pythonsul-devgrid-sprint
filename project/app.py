from __future__ import absolute_import, unicode_literals
from flask import Flask, jsonify
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from views import *

app.config.from_pyfile('config.py')

celery = make_celery(app)

db = SQLAlchemy(app)
class Event(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)

if __name__ == "__main__":
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host='0.0.0.0', port=5000, debug=True)
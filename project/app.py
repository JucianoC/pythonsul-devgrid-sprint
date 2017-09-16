# from __future__ import absolute_import, unicode_literals
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from project.flask_celery import make_celery

app = Flask(__name__)
app.config.from_pyfile('config.py')
celery = make_celery(app)
db = SQLAlchemy(app)

class ClusterServer(Server):
    def __call__(self, app, *args, **kwargs):
        # custom_call()
        #Hint: Here you could manipulate app
        return Server.__call__(self, app, *args, **kwargs)

app = Flask(__name__)
manager = Manager(app)
manager.add_command('runserver', ClusterServer())

from project.views import *

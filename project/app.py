# from __future__ import absolute_import, unicode_literals
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from project.flask_celery import make_celery
import click

app = Flask(__name__)
app.config.from_pyfile('config.py')
celery = make_celery(app)
db = SQLAlchemy(app)

from project.views import *

@app.cli.command('start_cluster', with_appcontext=True)
def start_cluster():
    """Initialize the cluster service."""
    from project.cluster import ClusterFactory
    ClusterFactory(db).run()
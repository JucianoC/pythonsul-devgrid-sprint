from __future__ import absolute_import, unicode_literals
from flask import Flask, jsonify
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = "amqp://localhost//"
app.config['CELERY_BACKEND'] = "mysql+mysqlconnector://root:root@localhost/devgrid"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost/devgrid"

celery = make_celery(app)

db = SQLAlchemy(app)
class Event(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)

@app.route('/receiver')
def receiver():
    return jsonify({'success': True}), 200

@celery.task(name='project.parse')
def parse(event_string):
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
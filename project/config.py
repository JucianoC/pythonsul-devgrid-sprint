import project
import os
path = os.path.abspath(os.path.dirname(project.__file__))

DEBUG = True
SECRET_KEY = 'devgrid'
CELERY_BROKER_URL = "amqp://localhost//"
# CELERY_BACKEND = "db+sqlite:///{}/database.db".format(path)
SQLALCHEMY_DATABASE_URI = "sqlite:////{}/database.db".format(path)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = "localhost:5000"

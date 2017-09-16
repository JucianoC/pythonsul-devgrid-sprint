import sys

DEBUG = True
SECRET_KEY = 'devgrid'
CELERY_BROKER_URL = "amqp://localhost//"
# CELERY_BACKEND = "db+sqlite:///{}/database.db".format(sys.path[0])
SQLALCHEMY_DATABASE_URI = "sqlite:////{}/database.db".format(sys.path[0])
SQLALCHEMY_TRACK_MODIFICATIONS = False

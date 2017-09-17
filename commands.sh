
#run flask and cluster
export FLASK_APP=project/app.py
flask run #to run flask
flask start_cluster #to run cluster

#run celery
celery -A project.app.celery worker --loglevel=info
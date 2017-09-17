This project has been developed for the Devgrid PythonSul Sprint.

To run this code you will need the follow:

* RabbitMQ
* A MySQL database
* Python 3

After that do this:

1. Create a virtual enviroment:
    ```
    python3 -m venv myvenv
    cd myvenv
    source bin/activate
    ```
2. Inside your virtual environment, clone this repository:
    ```
    git clone https://github.com/JucianoC/pythonsul-devgrid-sprint.git devgrid
    cd devgrid
    ```
3. Install the python libraries:
    ```
    pip install -r requirements.txt
    ``
4. Configure the connection with the MySQL in project/config.py
5. Now you can run the flask app:
    ```
    export FLASK_APP=project/app.py
    flask run
    ```
6. Now in a different terminal in the same directory and virtual environment, start the Celery:
    ```
    celery -A project.app.celery worker --loglevel=info
    ```
7. In the repository folder (running your virtual environment) run the following commands to start the service that run the clustering algorithm periodically.
    ```
    export FLASK_APP=project/app.py
    flask start_cluster
    ```
8. This three services (Flask, Cluster and Celery) must be running.

After that the flask are enabled to receive the messages by POST, in http://localhost:5000/receiver by default.

When the number of unclustered events brings 1000 the cluster service collect them and apply the algorithm, a report of the clusters already executed can be viewed at http://localhost:5000/report.
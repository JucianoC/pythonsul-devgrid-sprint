from __future__ import absolute_import, unicode_literals
from project.app import app, celery, db
from flask import request, jsonify, render_template
from project.models import Cluster
import numpy

@app.route('/receiver', methods=['POST'])
def receiver():
    event_string = str(request.data)
    save.delay(event_string)
    return jsonify({'success': True}), 200

@app.route('/report', methods=['GET'])
def report():
    database_data = db.session.query(Cluster).all()
    clusters = [
        dict(
            id = cluster.id,
            number_events = len(cluster.event),
            power_active_avg = round(numpy.mean([evt.power_active for evt in cluster.event]), 3)
        ) for cluster in database_data
    ]
    return render_template('report.html', clusters=clusters)

@celery.task(name='project.save')
def save(event_string):
    from project.event import EventFactory
    event = EventFactory.event_from_string(event_string)
    return event.save(db)
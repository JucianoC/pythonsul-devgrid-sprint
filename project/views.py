from app import app, celery
from flask import request

from event import EventFactory

@app.route('/receiver')
def receiver():
    event_string = request.data
    save.delay(event_string)
    return jsonify({'success': True}), 200

@celery.task(name='project.parse')
def save(event_string):
    event = EventFactory.get_event(event_string)
    event.save()
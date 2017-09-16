from __future__ import absolute_import, unicode_literals
from project.app import app, celery, db
from flask import request, jsonify

@app.route('/receiver', methods=['POST'])
def receiver():
    event_string = str(request.data)
    save.delay(event_string)
    return jsonify({'success': True}), 200

@celery.task(name='project.save')
def save(event_string):
    from project.event import EventFactory
    event = EventFactory.event_from_string(event_string)
    event.save(db)
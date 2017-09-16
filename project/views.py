from __future__ import absolute_import, unicode_literals
from project.app import app, celery, db
from flask import request

@app.route('/receiver', methods=['POST'])
def receiver():
    event_string = request.data
    save.delay(event_string, db)
    return jsonify({'success': True}), 200

@celery.task(name='project.parse')
def save(event_string, db):
    from project.event import EventFactory
    event = EventFactory.event_from_string(event_string)
    event.save(db)
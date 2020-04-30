import models
import datetime
Event = models.Event

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

events = Blueprint('events', 'events')

@events.route('/', methods=['GET', 'POST'])
def event():
  if request.method == 'POST':
    if not current_user.is_authenticated:
      return jsonify(
        data={ 'error': '403 Forbidden'},
        message="You need to be logged!",
        status=403
      ), 403
    else:
      payload = request.get_json()
      new_event = Event.create(
        category=payload['category'],
        title=payload['title'],
        description=payload['description'],
        date=datetime.date.today(),
        user=current_user.id
      )

      event = model_to_dict(new_event)
      event['user'].pop('password')

      return jsonify(
        data=event,
        message=f"Successfully created event for {event['user']} on {event['date']}",
        status=201
      ), 201

  if request.method == 'GET':
    if not current_user.is_authenticated:
      return jsonify(
        data={ 'error': '403 Forbidden'},
        message="You need to be logged!",
        status=403
      ), 403
    else:
      events = [model_to_dict(event) for event in current_user.events]
      for event_dict in events:
        (event_dict['user']).pop('password')

      return jsonify(
        data=events,
        message=f'You have found {len(events)} events',
        status=200
      ), 200
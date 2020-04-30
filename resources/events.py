import models
from datetime import *
Event = models.Event

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

events = Blueprint('events', 'events')

@events.route('/', methods=['GET', 'POST'])
def event_index():
  if not current_user.is_authenticated:
    return jsonify(
      data={ 'error': '403 Forbidden'},
      message="You need to be logged!",
      status=403
    ), 403
  else:
    if request.method == 'POST':
      payload = request.get_json()
      new_event = Event.create(
        category=payload['category'],
        title=payload['title'],
        description=payload['description'],
        date=date(payload['year'], payload['month'], payload['day']),
        user=current_user.id
      )

      event = model_to_dict(new_event)
      event['user'].pop('password')

      return jsonify(
        data=event,
        message=f"Successfully created event for {event['user']['username']} on {event['date']}",
        status=201
      ), 201

    # need to implement query to select specfic dates and days
    if request.method == 'GET':
      year = request.args.get('year')
      month = request.args.get('month')
      day = request.args.get('day')
      if not year or not month or not day:
        week = (date.today().toordinal()) // 7  
        start_date = date.fromordinal(week * 7)
        
      else:
        year, month, day = int(year), int(month), int(day)
        week = (date(year, month, day).toordinal()) // 7  
        start_date = date.fromordinal(week * 7)
      
      days = int(request.args.get('days', default=7))
      end_date = start_date + timedelta(days=days)

      events = Event.select().where( Event.date >= start_date
        ).where( Event.date <= end_date
        ).where( Event.user_id == current_user.id)
      events = [model_to_dict(event) for event in events]
      for event in events:
        (event['user']).pop('password')

      return jsonify(
        data=events,
        message=f'You have found {len(events)} events',
        status=200
      ), 200

@events.route('/<id>', methods=['GET', 'DELETE', 'PATCH'])
def event_id(id):
  if not current_user.is_authenticated:
    return jsonify(
      data={ 'error': '403 Forbidden'},
      message="You need to be logged!",
      status=403
    ), 403
  else:
    if request.method == 'GET':
      try:
        event = model_to_dict(Event.get_by_id(id))
        if event['user']['id'] != current_user.id:
          return jsonify(
            data={},
            message="Invalid event id or user does not have the event",
            status=403
          ), 403
        else:
          event['user'].pop('password')
          return jsonify(
            data=event,
            message=f"Found event with id {id}",
            status=200
          ), 200
      except models.DoesNotExist:
        return jsonify(
          data={},
          message="Invalid event id or user does not have the event",
          status=403
        ), 403

    if request.method == 'DELETE':
      try:
        event_to_delete = Event.get_by_id(id)
        if event_to_delete.user.id != current_user.id:
          return jsonify(
            data={},
            message="Invalid event id or user does not have the event",
            status=403
          ), 403
        else:
          event_to_delete.delete_instance()
          return jsonify(
            data={},
            message=f"Deleted event with id {id}",
            status=200
          ), 200
      except models.DoesNotExist:
        return jsonify(
          data={},
          message="Invalid event id or user does not have the event",
          status=403
        ), 403
    
    if request.method == 'PATCH':
      try:
        event = Event.get_by_id(id)
        if event.user.id != current_user.id:
          return jsonify(
            data={},
            message="user does not have the event",
            status=403
          ), 403
        else:
          payload = request.get_json()
          query = Event.update({
            Event.category: payload['category'],
            Event.title: payload['title'],
            Event.description: payload['description'],
            Event.date: date(payload['year'], payload['month'], payload['day'])
          }).where(Event.id == id)
          query.execute()
          return jsonify(
            data={},
            message=f"updated event with id {id}",
            status=200
          ), 200
      except models.DoesNotExist:
        return jsonify(
          data={},
          message="Invalid event id or user does not have the event",
          status=403
        ), 403


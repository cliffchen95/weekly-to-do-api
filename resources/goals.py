import models
from datetime import *
Goal = models.Goal

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

goals = Blueprint('goals', 'goals')

@goals.route('/', methods=['GET', 'POST'])
def goal():
  if not current_user.is_authenticated:
    return jsonify(
      data={ 'error': '403 Forbidden'},
      message="You need to be logged!",
      status=403
    ), 403

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

  if request.method == 'POST':
    payload = request.get_json()
    try:
      goal = Goal.get(
        Goal.start_date == start_date,
        Goal.user_id == current_user.id
      )
      return jsonify(
        data={},
        message="Goal already existed",
        status=403
      ), 403

    except models.DoesNotExist:
      new_goal = Goal.create(
        goal=payload['goal'],
        user=current_user.id,
        start_date=start_date 
      )
      goal = model_to_dict(new_goal)
      goal['user'].pop('password')
      return jsonify(
        data=goal,
        message=f"Successfully created new goal for the week starting {goal['start_date']}",
        status=200
      ), 200

  if request.method == 'GET':
    try:
      goal = Goal.get(
        Goal.start_date == start_date,
        Goal.user_id == current_user.id
      )
      goal = model_to_dict(goal)
      goal['user'].pop('password')
      return jsonify(
        data={"goal": goal, "start_date": start_date},
        message="Goal has been found",
        status=200
      ), 200
    except models.DoesNotExist: 
      return jsonify(
        data={},
        message="Goal does not exist",
        status=404
      ), 404



@goals.route('/<id>', methods=['PATCH'])
def goal_id(id):
  if not current_user.is_authenticated:
    return jsonify(
      data={ 'error': '403 Forbidden'},
      message="You need to be logged!",
      status=403
    ), 403

  payload = request.get_json()
  try:
    goal = Goal.get(
      Goal.id == id,
      Goal.user_id == current_user.id
    )
    goal.goal = payload['goal']
    goal.save()
    goal = model_to_dict(goal)
    goal['user'].pop('password')
    return jsonify(
      data=goal,
      message=f"Successfully updated goal with id {id}",
      status=200
    ), 200
  except models.DoesNotExist:
    return jsonify(
      data={},
      message="The goal does not exist or user not authorized",
      status=403
    ), 403
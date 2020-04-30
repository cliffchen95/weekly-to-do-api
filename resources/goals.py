import models
from datetime import *
Goal = models.Goal

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

goals = Blueprint('goals', 'goals')

@goals.route('/', methods=['GET', 'POST'])
def goal():
  year = request.args.get('year')
  month = request.args.get('month')
  day = request.args.get('day')
  if not year or not month or not day:
    week = (date.today().toordinal()) // 7  
    start_date = date.fromordinal(week * 7)
    print(start_date)
  else:
    year, month, day = int(year), int(month), int(day)
    week = (date(year, month, day).toordinal()) // 7  
    start_date = date.fromordinal(week * 7)
    print(start_date)

  if request.method == 'POST':
    payload = request.get_json()
    try:
      goal = Goal.get(Goal.start_date == start_date)
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
  return "check teriminal"
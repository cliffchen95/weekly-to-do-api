import models
from datetime import *
Goal = models.Goal

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

goals = Blueprint('goals', 'goals')

@goals.route('/', methods=['GET'])
def goal():
  year = request.args.get('year')
  month = request.args.get('month')
  day = request.args.get('day')
  return f"{year} - {month} - {day}"
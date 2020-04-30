import models
from datetime import *
Goal = models.Goal

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

goals = Blueprint('goals', 'goals')

@goals.route('/', methods=['GET'])
def goal():
  return "goal Blueprint!"
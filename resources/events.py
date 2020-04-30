import models

Event = models.Event

from flask import Blueprint, request, jsonify
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

events = Blueprint('events', 'events')

@events.route('/', methods=['POST'])
def event():
  if request.method == 'POST':
    return "hit creation route"


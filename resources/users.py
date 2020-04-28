import models

User = models.User

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from flask_login import login_user

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

# create and delete user
@users.route('/', methods=['POST', 'DELETE'])
def user():
  if request.method == 'POST':
    payload = request.get_json()
    payload['username'] = payload['username'].lower()

    try:
      User.get(User.username == payload['username'])
      return jsonify(
        data={},
        message=f"A user with username {payload['username']} already exists",
        status=401
      ), 401
    except models.DoesNotExist:
      pw_hash = generate_password_hash(payload['password'])

      created_user = User.create(
        username=payload['username'],
        password=pw_hash
      )

      login_user(created_user)

      created_user_dict = model_to_dict(created_user)
      created_user_dict.pop('password')

      return jsonify(
        data=created_user_dict,
        message=f"Successfully registered user {created_user_dict['username']}",
        status=201
      ), 201

  if request.method == 'DELETE':
    return "you hit delete route"

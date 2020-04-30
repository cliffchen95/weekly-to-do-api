import models

User = models.User

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

# create and delete user
@users.route('/', methods=['GET', 'POST', 'DELETE'])
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


@users.route('/login', methods=['POST'])
def login():
  if not current_user.is_authenticated:
    payload = request.get_json()
    payload['username'] = payload['username'].lower()

    try:
      user = User.get(User.username == payload['username'])
      user_dict = model_to_dict(user)
      if check_password_hash(user_dict['password'], payload['password']):
        
        login_user(user)

        user_dict.pop('password')
        return jsonify(
          data=user_dict,
          message=f"Successfully logged in {user_dict['username']}",
          status=200
        ), 200
      else:
        return jsonify(
          data={},
          message='Username does not exist or incorrect password',
          status=401
        ), 401

    except models.DoesNotExist:
      return jsonify(
        data={},
        message='Username does not exist or incorrect password',
        status=401
      ), 401
  else:
    user = model_to_dict(current_user)
    user.pop('password')
    return jsonify(
      data=user,
      message=f"You are currently logged in as {user['username']}",
      status=200
    ), 200

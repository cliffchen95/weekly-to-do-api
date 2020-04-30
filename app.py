from flask import Flask
from flask_login import LoginManager

import models
from resources.users import users
from resources.events import events
from resources.goals import goals

DEBUG=True
PORT=8000

app = Flask(__name__)

app.secret_key = "somekey"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    print("loading the following user")
    user = models.User.get_by_id(user_id)
    return user
  except models.DoesNotExist:
    return None

@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': 'User not logged in'
    },
    message="You must be logged in",
    status=401
  ), 401

  
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(events, url_prefix='/api/v1/events')
app.register_blueprint(goals, url_prefix='/api/v1/goals')

@app.route('/')
def hello():
  return 'Server running'

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)

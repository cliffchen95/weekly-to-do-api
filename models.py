from peewee import *
from flask_login import UserMixin


DATABASE = SqliteDatabase('todo.sqlite')

class User(UserMixin, Model):
  username=CharField(unique=True)
  password=CharField()

  class Meta:
    database = DATABASE

class Event(Model):
  title=TextField()
  category=TextField()
  description=TextField()
  date=DateField(formats=['%Y-%m-%d'])
  user=ForeignKeyField(User, backref='events')

  class Meta:
    database = DATABASE

class Goal(Model):
  goal=TextField()
  start_date=DateField(formats=['%Y-%m-%d'])
  user=ForeignKeyField(User, backref='goals')

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Event, Goal], safe=True)
  print('connected to database')

  DATABASE.close()
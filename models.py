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
  date=DateField()
  user=ForeignKeyField(User, backref='events')

  class Meta:
    database = DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Event], safe=True)
  print('connected to database')

  DATABASE.close()
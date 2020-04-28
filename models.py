from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('todo.sqlite')

class User(UserMixin, Model):
  username=CharField(unique=True)
  password=CharField()

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User], safe=True)
  print('connected to database')

  DATABASE.close()
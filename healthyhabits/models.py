import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db

class UserRecord(db.Model):
  user_id = db.StringProperty()
  name = db.StringProperty()
  
class DayRecord(db.Model):
  sleepAmount = db.BooleanProperty(default=False)
  sleepTimes = db.BooleanProperty(default=False)
  nap = db.BooleanProperty(default=False)
  exercise = db.BooleanProperty(default=False)
  veggies = db.BooleanProperty(default=False)
  healthyMeals = db.BooleanProperty(default=False)
  mealTimes = db.BooleanProperty(default=False)
  junkFood = db.BooleanProperty(default=False)
  relax = db.BooleanProperty(default=False)
  water = db.BooleanProperty(default=False)
  total = db.IntegerProperty(default=0)

class WeekRecord(db.Model):
  week = db.IntegerProperty()
  user = db.ReferenceProperty(UserRecord)
  mon = db.ReferenceProperty(DayRecord, collection_name="mon")
  tues = db.ReferenceProperty(DayRecord, collection_name="tues")
  wed = db.ReferenceProperty(DayRecord, collection_name="wed")
  thurs = db.ReferenceProperty(DayRecord, collection_name="thurs")
  fri = db.ReferenceProperty(DayRecord, collection_name="fri")
  sat = db.ReferenceProperty(DayRecord, collection_name="sat")
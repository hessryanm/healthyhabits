import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db

class User(db.Model):
  user_id = db.IntegerProperty()
  name = db.StringProperty()
  
class Day(db.Model):
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
  total = db.IntegerProperty()

class Week(db.Model):
  start = db.DateProperty()
  end = db.DateProperty()
  user = db.ReferenceProperty(User)
  mon = db.ReferenceProperty(Day)
  tues = db.ReferenceProperty(Day)
  wed = db.ReferenceProperty(Day)
  thurs = db.ReferenceProperty(Day)
  fri = db.ReferenceProperty(Day)
  sat = db.ReferenceProperty(Day)
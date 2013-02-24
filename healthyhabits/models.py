# import cgi
# import datetime
# import urllib
# import webapp2

# from google.appengine.ext import db

# class UserRecord(db.Model):
#   user_id = db.IntegerProperty()
#   name = db.StringProperty()
  
# class DayRecord(db.Model):
#   sleepAmount = db.BooleanProperty(default=False)
#   sleepTimes = db.BooleanProperty(default=False)
#   nap = db.BooleanProperty(default=False)
#   exercise = db.BooleanProperty(default=False)
#   veggies = db.BooleanProperty(default=False)
#   healthyMeals = db.BooleanProperty(default=False)
#   mealTimes = db.BooleanProperty(default=False)
#   junkFood = db.BooleanProperty(default=False)
#   relax = db.BooleanProperty(default=False)
#   water = db.BooleanProperty(default=False)
#   total = db.IntegerProperty()

# class WeekRecord(db.Model):
#   start = db.DateProperty()
#   end = db.DateProperty()
#   user = db.ReferenceProperty(UserRecord)
#   mon = db.ReferenceProperty(DayRecord)
#   tues = db.ReferenceProperty(DayRecord)
#   wed = db.ReferenceProperty(DayRecord)
#   thurs = db.ReferenceProperty(DayRecord)
#   fri = db.ReferenceProperty(DayRecord)
#   sat = db.ReferenceProperty(DayRecord)
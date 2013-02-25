import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *
import datetime
import copy

def get_day_dict(current_week, day):
  day = getattr(current_week, day)
  if day is None:
    return {
      'sleepAmount': False,
      'sleepTimes': False,
      'nap': False,
      'exercise': False,
      'veggies': False,
      'healthyMeals': False,
      'mealTimes': False,
      'junkFood': False,
      'relax': False,
      'water': False
    }
  else:
    return {
      'sleepAmount': day.sleepAmount,
      'sleepTimes': day.sleepTimes,
      'nap': day.nap,
      'exercise': day.exercise,
      'veggies': day.veggies,
      'healthyMeals': day.healthyMeals,
      'mealTimes': day.mealTimes,
      'junkFood': day.junkFood,
      'relax': day.relax,
      'water': day.water
    }

class MainPage(webapp2.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    user = UserRecord.gql("WHERE user_id = :1", google_user.user_id())
    user = user.get()
    if user is None:
      user = UserRecord()
      user.user_id = google_user.user_id()
      user.name = google_user.nickname()
      user.put()
      
    week_num = datetime.datetime.now().isocalendar()[1]
    current_week = WeekRecord.gql("WHERE week = :1 AND user = :2", week_num, user)
    current_week = current_week.get()
    if current_week is None:
      current_week = WeekRecord()
      current_week.week = week_num
      current_week.user = user
      current_week.put()
    
    q = WeekRecord.gql("WHERE week = :1 ORDER BY user.name", week_num)
    all_users = []
    for p in q.run():
      person = {}
      person['name'] = p.user.name
      person['mon'] = p.mon.total
      person['tues'] = p.tues.total
      person['wed'] = p.wed.total
      person['thurs'] = p.thurs.total
      person['fri'] = p.fri.total
      person['sat'] = p.sat.total
      all_users.append(copy.copy(person))
      
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render("templates/home.html", {'uname': user.name, 'users': all_users}))
    
class SubmitPage(webapp2.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    user = UserRecord.gql("WHERE user_id = :1", google_user.user_id())
    user = user.get()
    if user is None:
      user = UserRecord()
      user.user_id = google_user.user_id()
      user.name = google_user.nickname()
      user.put()
      
    week_num = datetime.datetime.now().isocalendar()[1]
    current_week = WeekRecord.gql("WHERE week = :1 AND user = :2", week_num, user)
    current_week = current_week.get()
    if current_week is None:
      current_week = WeekRecord()
      current_week.week = week_num
      current_week.user = user
      current_week.put()
      
    data = {}
    data['mon'] = get_day_dict(current_week, 'mon')
    data['tues'] = get_day_dict(current_week, 'tues')
    data['wed'] = get_day_dict(current_week, 'wed')
    data['thurs'] = get_day_dict(current_week, 'thurs')
    data['fri'] = get_day_dict(current_week, 'fri')
    data['sat'] = get_day_dict(current_week, 'sat')
    
    self.response.out.write(template.render("templates/submit.html", data))
    
  def post(self):
    google_user = users.get_current_user()
    user = UserRecord.gql("WHERE user_id = :1", google_user.user_id())
    user = user.get()
    if user is None:
      user = UserRecord()
      user.user_id = google_user.user_id()
      user.name = google_user.nickname()
      user.put()
      
    week_num = datetime.datetime.now().isocalendar()[1]
    current_week = WeekRecord.gql("WHERE week = :1 AND user = :2", week_num, user)
    current_week = current_week.get()
    if current_week is None:
      current_week = WeekRecord()
      current_week.week = week_num
      current_week.user = user
      current_week.put()
      
    day = getattr(current_week, self.request.params['day'])
    if day is None:
      day = DayRecord()
      # setattr(current_week, self.request.params['day'], db.Key(day.key())
      # current_week.put()
    
    total = 0
    if 'sleepAmount' in self.request.params:
      day.sleepAmount = True
      total += 1
    else:
      day.sleepAmount = False
    if 'sleepTimes' in self.request.params:
      day.sleepTimes = True
      total += 1
    else:
      day.sleepTimes = False
    if 'nap' in self.request.params:
      day.nap = True
      total += 1
    else:
      day.nap = False
    if 'exercise' in self.request.params:
      day.exercise = True
      total += 1
    else:
      day.exercise = False
    if 'veggies' in self.request.params:
      day.veggies = True
      total += 1
    else:
      day.veggies = False
    if 'healthyMeals' in self.request.params:
      day.healthyMeals = True
      total += 1
    else:
      day.healthyMeals = False
    if 'mealTimes' in self.request.params:
      day.mealTimes = True
      total += 1
    else:
      day.mealTimes = False
    if 'junkFood' in self.request.params:
      day.junkFood = True
      total += 1
    else:
      day.junkFood = False
    if 'relax' in self.request.params:
      day.relax = True
      total += 1
    else:
      day.relax = False
    if 'water' in self.request.params:
      day.water = True
      total += 1
    else:
      day.water = False
      
    day.total = total
    
    day.put()
    setattr(current_week, self.request.params['day'], day)
    self.redirect("/")
    
app = webapp2.WSGIApplication([
  ('/', MainPage), 
  ('/submit', SubmitPage)], 
debug=True)
    
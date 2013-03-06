import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *
import datetime
import copy
import json
from timezone import USTimeZone

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
    
def get_day_total(current_week, day):
  day = getattr(current_week, day)
  if day is None:
    return 0
  else:
    return day.total
    
def get_date(request):
  mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
  time = datetime.datetime.now(mountain)
  iso = time.isocalendar()
  date = {}
  date['week_num'] = iso[1]
  date['year'] = iso[0]
  date['now'] = True
  date['day'] = iso[2]
  
  if 'week' in request.params and request.params['week'] != "":
    date['week_num'] = int(request.params['week'])
    date['now'] = False
    
  if 'year' in request.params and request.params['year'] != "":
    date['year'] = int(request.params['year'])
    date['now'] = False
    
  return date
  
def get_user():
  google_user = users.get_current_user()
  user = UserRecord.gql("WHERE user_id = :1", google_user.user_id())
  user = user.get()
  if user is None:
    user = UserRecord()
    user.user_id = google_user.user_id()
    user.name = google_user.nickname()
    user.put()
  return user  
  
def get_current_week(date, user):
  current_week = WeekRecord.gql("WHERE week = :1 AND year = :2 AND user = :3", date['week_num'], date['year'], user)
  current_week = current_week.get()
  
  if current_week is None:
    current_week = WeekRecord.gql("WHERE week = :1 AND user = :2", date['week_num'], user)
    current_week = current_week.get()
    
    if current_week is not None:
      current_week.year = date['year']
      current_week.put()
      
    else:
      current_week = WeekRecord()
      current_week.week = date['week_num']
      current_week.year = date['year']
      current_week.user = user
      current_week.put()
    
  return current_week

class MainPage(webapp2.RequestHandler):
  def get(self):
    
    user = get_user()
      
    date = get_date(self.request)
    
    current_week = get_current_week(date, user)
    
    q = db.GqlQuery("SELECT * FROM WeekRecord WHERE week = :1 AND year=:2", date['week_num'], date['year'])
    all_users = []
    for p in q:
      person = {}
      person['name'] = p.user.name
      total = 0
      person['mon'] = get_day_total(p, 'mon')
      total += person['mon']
      person['tues'] = get_day_total(p, 'tues')
      total += person['tues']
      person['wed'] = get_day_total(p, 'wed')
      total += person['wed']
      person['thurs'] = get_day_total(p, 'thurs')
      total += person['thurs']
      person['fri'] = get_day_total(p, 'fri')
      total += person['fri']
      person['sat'] = get_day_total(p, 'sat')
      total += person['sat']
      person['total'] = total
      all_users.append(copy.copy(person))
      
      if p.year is None:
        p.year = date['year']
        p.put()
      
    self.response.headers['Content-Type'] = 'text/html'
    prev_week = date['week_num'] - 1
    if prev_week <= 0:
      prev_week = 52
      prev_year = date['year'] - 1
    else:
      prev_year = date['year']
    self.response.out.write(template.render("templates/home.html", {'uname': user.name, 'users': all_users, 'logout_url':users.create_logout_url("/"), 'prev_week_num':prev_week, 'prev_year_num':prev_year, 'this_week':date['now'], 'queries': self.request.query_string}))
    
  def post(self):
    user = get_user()
      
    if "name" in self.request.params:
      user.name = self.request.params['name']
      user.put()
    
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(dict(result="true")))
    
class SubmitPage(webapp2.RequestHandler):
  def get(self):
    user = get_user()
      
    date = get_date(self.request)
    
    current_week = get_current_week(date, user)
      
    data = {}
    data['mon'] = get_day_dict(current_week, 'mon')
    data['tues'] = get_day_dict(current_week, 'tues')
    data['wed'] = get_day_dict(current_week, 'wed')
    data['thurs'] = get_day_dict(current_week, 'thurs')
    data['fri'] = get_day_dict(current_week, 'fri')
    data['sat'] = get_day_dict(current_week, 'sat')
    data['this_week'] = date['now']
    data['day_num'] = date['day']
    
    self.response.out.write(template.render("templates/submit.html", data))
    
  def post(self):
    user = get_user()
      
    date = get_date(self.request)
    
    current_week = get_current_week(date, user)
      
    day = getattr(current_week, self.request.params['day'])
    if day is None:
      day = DayRecord()
    
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
    current_week.put()
    self.redirect("/?"+self.request.query_string)
    
app = webapp2.WSGIApplication([
  ('/', MainPage), 
  ('/submit', SubmitPage)], 
debug=True)
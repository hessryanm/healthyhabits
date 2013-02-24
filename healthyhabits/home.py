import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *
import datetime
import copy

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
    self.response.out.write(template.render("templates/submit.html", {}))
    
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
      
    print(self.request.params)
    
app = webapp2.WSGIApplication([
  ('/', MainPage), 
  ('/submit', SubmitPage)], 
debug=True)
    
import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *
import datetime

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
    q = UserRecord.all()
    q.order("name")
    all_users = []
    for p in q.run():
      person = {}
      person['name'] = p.name
      print(datetime.datetime.now().date())
      week = WeekRecord.gql("WHERE start < :1 AND end > :1", datetime.datetime.now().date())
      week = week.get()
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render("templates/home.html", {'uname': user.name}))
    
class SubmitPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(template.render("templates/submit.html", {}))
    
app = webapp2.WSGIApplication([
  ('/', MainPage), 
  ('/submit', SubmitPage)], 
debug=True)
    
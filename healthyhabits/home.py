import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
# from models import *

class MainPage(webapp2.RequestHandler):
  def get(self):
    google_user = users.get_current_user()
    #user = User.gql("WHERE user_id IS :1 LIMIT 1", google_user.user_id())
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render("templates/home.html", {'id': google_user.user_id(), 'uname': google_user.nickname()}))
    
class SubmitPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(template.render("templates/submit.html", {}))
    
app = webapp2.WSGIApplication([
  ('/', MainPage), 
  ('/submit', SubmitPage)], 
debug=True)
    
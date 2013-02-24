import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user();
    
    if user:
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(template.render("templates/home.html", {'lname': "Hess", 'uname': user.nickname()}))
    else:
      self.redirect(users.create_login_url(self.request.uri));
    
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
    
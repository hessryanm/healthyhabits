import webapp2
import os
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(template.render("templates/home.html", {'lname': "Hess", 'uname': 'noobile'}))
    
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
    

import webapp2
from google.appengine.ext import ndb    

class HandleForm(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        self.response.write('Hello %s!'%name)
        saveForm(self)

class Form(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    age = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

def saveForm(self):    
    age = int(self.request.get('age'))
    name = self.request.get('name')
    email = self.request.get('email')        
    if email:
        # use email as key name
        form = Form(key=ndb.Key('Form', email), name=name,age=age)
    else:
        form = Form(name=name,age=age)        
    form.put()    
    
    self.response.write('<br>Your form is saved')
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello!<br>')
        self.response.write('Start your <a href="/start">form</a>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', HandleForm)
], debug=True)

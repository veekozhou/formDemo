import webapp2
from google.appengine.ext import ndb    

# import users api
from google.appengine.api import users
import os

# import module for templates
import jinja2
# for logging message to server log
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# use the email as the key name
# Add the appropriate property based on the form in Assigment 1
class Form(ndb.Model):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

# Learn how handle input and create error response
class SubmitForm(webapp2.RequestHandler):
    def post(self):
        # get the data
        age = int(self.request.get('age'))
        name = self.request.get('name')
        
        # get the current user
        user = users.get_current_user()
        
        if not user:
            # Error: user's login time out or logged out
            self.error(401)
            # you can send a error message as well
            self.response.out.write("Error: no login")
            return
        
        # get the email from user object
        email = user.email()
        
        # USE EMAIL AS KEY NAME
        form = Form(key=ndb.Key('Form', email), name=name,age=age)
        # update db
        form.put()
    
        self.response.write('<br>Your form is saved')
        
        # HTTP STATUS CODE 200 is always sent automatically
   
# In the last demo, the previous form is only a static html, it is not useful in real applications
# Now the form is rendered as a template
class EditForm(webapp2.RequestHandler):
    def get(self):        
        
        user = users.get_current_user()
        if user:
            # redirect "/" after user has logged out
            logout_url = users.create_logout_url('/')
        else:
            # direct to login and redirect back to this page after login
            self.redirect(users.create_login_url(self.request.uri))
            # return will stop loading code below
            return
        
        # these are logging functions
        # useful when debugging your app
        logging.info(user.email())
        logging.info(user.user_id())
        
        ###################
        # Assignment Hint:
        # look up the datastore for the "Form" data of the current users
        # add the form data to the template_values and displayed in the html file 
        ###################
        
        # check if the current user is admin
        # When app is uploaded to GAE server, admins are Google Accounts with access to the application code
        isAdmin = users.is_current_user_admin()
        
        # these values are for the template
        template_values = {
            # pass an object
            'user': user,
            # pass an entity
            # 'form': form,
            # pass a string
            'logout_url': logout_url,
            'isAdmin' : isAdmin
        }
        
        # finally render the template, the template is the form2.html in the templates folder
        template = JINJA_ENVIRONMENT.get_template('templates/form2.html')
        self.response.write(template.render(template_values))
    
# this is the "/" page, do not modify. This page is not part of the assignment
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello!<br>')
        self.response.write('Start your <a href="/edit/form">form</a>')        
        
app = webapp2.WSGIApplication([    
    ('/', MainHandler),  
    ('/edit/form', EditForm),  # show the form in a template
    ('/submit/form', SubmitForm), # submit and save form data
    ('*.', MainHandler)
    ], debug=True)

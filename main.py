import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from snippets import MyUser
from add import Add


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html' #We define how the response is going to be

        url='' #the variable to store the URL link that will be created
        url_string='' #Tells something about the name of the URL
        user = users.get_current_user() # we get the current user information
        welcome = 'Welcome back' #used for displaying particular messages based on the user

        if user: #if we have a current user
            url=users.create_logout_url(self.request.uri) #we will create a logout_url for the user
            url_string='Logout' #we will tell that this is a logout url

            myuser_key = ndb.Key('MyUser',user.user_id()) #we will generate a key object for the user of type 'MyUser' and will have the information of user_id()
            myuser =myuser_key.get() # get the user value from the data store using the key that was generated

            if myuser == None: #if we don't find the user in the datastore
                welcome = 'Welcome to the application' #we display a simple welcome message in the window
                myuser=MyUser(id=user.user_id()) #
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'

        template_values = {
            'url': url ,
            'url_string': url_string ,
            'user': user ,
            'welcome': welcome
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage), ('/add', Add)], debug = True)
# ,('/details', Details)

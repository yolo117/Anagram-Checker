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
    def split(self, word):
        return [char for char in word]
    def merge(self, word):
        new=''
        for x in word:
            new += x
        return new
    def sort(self, word):
        split_data =self.split(word)
        # print(split_data)
        sorted_alphabets = sorted(split_data)
        # print(sorted_alphabets)
        merged_word = self.merge(sorted_alphabets)
        return merged_word

    # def substring(self, str):
    #     list = self.split(str)
    #     new_word_list=[]
    #     for i in range(len(list)):
    #         x = list[i]
    #         xs = list[i + 1:]

    def substring(self, str):
        List=self.split(str)
        randomList=[]
        # print list(enumerate(List))
        i=0
        for count, element in enumerate(List):
            if count!=i:
                randomList.append((element))
                # print(randomList)
                i=i+1
        # print(self.merge(randomList))
        return(self.merge(randomList))
        self.substring(self.merge(randomList))




    def get(self):
        self.response.headers['Content-Type'] = 'text/html' #We define how the response is going to be

        url='' #the variable to store the URL link that will be created
        url_string='' #Tells something about the name of the URL
        user = users.get_current_user() # we get the current user information
        welcome = 'Welcome' #used for displaying particular messages based on the user

        subanagram_action= self.request.get('button_search_subanagram')

        # self.substringcreator('aerl')
        action= self.request.get('search_button')

        message = ''
        Anagram = ''
        subanagram=''

        if user: #if we have a current user
            url=users.create_logout_url(self.request.uri) #we will create a logout_url for the user
            url_string='Logout' #we will tell that this is a logout url

            myuser_key = ndb.Key('MyUser',user.user_id()) #we will generate a key object for the user of type 'MyUser' and will have the information of user_id()
            myuser =myuser_key.get() # get the user value from the data store using the key that was generated

            searched_string=self.request.get('search_word')
            lex_word = self.sort(searched_string.lower())
            key_word=user.user_id() + lex_word
            word_key= ndb.Key('Words', key_word)
            word=word_key.get()
            if word == None:
                message= 'Anagram not found'
            else:
                message=''
                Anagram = word.wordsList

            if myuser == None: #if we don't find the user in the datastore
                welcome = 'Welcome to the application' #we display a simple welcome message in the window
                myuser=MyUser(id=user.user_id()) #
                myuser.user=user.email()
                myuser.uniqueAnagramCounter=0
                myuser.wordCounter=0
                myuser.put()

            # section for subanagrams
            if subanagram_action== 'Search':
                subana=self.request.get('input_subanagram_word')
                print(self.substring(subana))
                lex_subana = self.sort(subana.lower())
                key_word_sub=user.user_id() + lex_subana
                word_key_sub= ndb.Key('Words', key_word_sub)
                sub_word=word_key_sub.get()
                if sub_word == None:
                    message= 'Sub Anagram not found'
                else:
                    message=''
                    subanagram = sub_word.wordsList
                    print(subanagram)


            print(subanagram)
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'



        template_values = {
            'url': url ,
            'url_string': url_string ,
            'user': user ,
            'welcome': welcome,
            'message': message,
            'word': Anagram,
            'subanagram': subanagram
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage), ('/add', Add)], debug = True)
# ,('/details', Details)
